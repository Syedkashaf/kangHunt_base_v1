import logging
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Attempt to load environment variables from multiple possible locations
# This handles cases where the script is run from different directories
env_paths = [
    Path(".env"),                    # Current directory
    Path("../.env"),                 # Parent directory
    Path("../../.env"),              # Two levels up
]

for env_file in env_paths:
    if env_file.exists():
        load_dotenv(env_file)
        print(f"[✓] Loaded .env from: {env_file.absolute()}")
        break

# Suppress verbose logging from external HTTP libraries
logging.getLogger("httpx").setLevel(logging.WARNING)

from fastapi import FastAPI, HTTPException, Header, Depends
from typing import List, Dict, Any
from models.schemas import NormalizedScanReport, UnifiedProfile, PluginResponse
from plugins.gravatar_plugin import GravatarPlugin
from plugins.holehe_plugin import HolehePlugin
from plugins.breach_plugin import BreachPlugin
from plugins.ghunt_plugin import GHuntPlugin
from plugins.social_plugin import SocialMediaPlugin
from plugins.intelbase_plugin import IntelBasePlugin

app = FastAPI(title="Precision OSINT Core Engine")

# Retrieve API key from environment for authentication
API_KEY = os.getenv("CORE_API_KEY")

if not API_KEY:
    print("\n⚠️  WARNING: CORE_API_KEY not set in environment!")
    print("   The server will reject all API requests.")
    print("   Make sure .env file exists with CORE_API_KEY=your_key\n")

# Simple authentication middleware that verifies incoming API key
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    return x_api_key

# Collection of OSINT plugins that will run in parallel during scans
plugins = [
    GravatarPlugin(), 
    HolehePlugin(), 
    BreachPlugin(), 
    GHuntPlugin(),
    SocialMediaPlugin(),
    IntelBasePlugin()
]

def normalize_intelligence_payload(target: str, raw_results: List[PluginResponse]) -> UnifiedProfile:
    """
    Consolidates raw data from multiple OSINT plugins into a unified profile.
    Uses recursive extraction to handle deeply nested JSON structures from different sources.
    """
    # Recursively searches through nested dictionaries and lists to find a specific key
    def deep_harvest(target_key: str, data_store: Any) -> Any:
        """Traverse nested JSON to locate a value, returning the first non-empty match."""
        if isinstance(data_store, dict):
            # Check if the key exists at current level and has a non-empty value
            if target_key in data_store and data_store[target_key]:
                return data_store[target_key]
            # Recursively check all nested values
            for key, value in data_store.items():
                result = deep_harvest(target_key, value)
                if result: 
                    return result
        elif isinstance(data_store, list):
            # Check each element in the list
            for item in data_store:
                result = deep_harvest(target_key, item)
                if result: 
                    return result
        return None

    # Initialize profile and tracking lists
    profile = UnifiedProfile()
    active_platforms = []
    breached_sites = []
    total_breaches = 0
    
    # Process results from each plugin
    for result in raw_results:
        # Skip failed or empty responses
        if result.status != "success" or not result.raw_data:
            continue
            
        source = result.source_name
        data = result.raw_data
        
        # Extract profile information from Gravatar service
        if "Gravatar" in source:
            display_name = deep_harvest("displayName", data) or deep_harvest("display_name", data)
            avatar_url = deep_harvest("thumbnailUrl", data) or deep_harvest("avatar_image", data)
            
            if display_name:
                profile.full_name = display_name
                active_platforms.append("gravatar.com")
            if avatar_url:
                profile.avatar_url = avatar_url
                if "gravatar.com" not in active_platforms:
                    active_platforms.append("gravatar.com")
                
        # Extract platform registry information from Holehe service
        elif "Holehe" in source:
            detected_nodes = data.get("accounts_and_numbers") or data.get("successful_platforms") or data.get("platforms") or []
            if isinstance(detected_nodes, list):
                active_platforms.extend(detected_nodes)
            elif isinstance(detected_nodes, dict):
                # Filter to platforms where the account exists
                active_platforms.extend([k for k, v in detected_nodes.items() if v.get("exists")])
                
        # Extract data breach information from XposedOrNot service
        elif "XposedOrNot" in source:
            total_breaches = deep_harvest("total_breaches", data) or deep_harvest("total_breaches_found", data) or 0
            sites = deep_harvest("breached_platforms", data) or deep_harvest("breaches", data) or []
            if isinstance(sites, list):
                breached_sites.extend(sites)
            profile.total_breaches_found = int(total_breaches)
            
        # Extract Google account intelligence from GHunt service
        elif "GHunt" in source:
            # Find the person's name from various possible field names
            extracted_name = deep_harvest("name", data) or deep_harvest("profile_name", data)
            if extracted_name and str(extracted_name).lower() != "unknown":
                profile.full_name = extracted_name
                
            # Collect Google profile picture if available
            profile.avatar_url = deep_harvest("profile_photo", data) or deep_harvest("url", data) or profile.avatar_url
            
            # Locate Google's internal user identifier
            profile.gaia_id = deep_harvest("gaia_id", data) or deep_harvest("personId", data) or deep_harvest("sourceId", data)
            
            # Include Google Maps review links if available
            maps_url = deep_harvest("maps_reviews_url", data)
            if maps_url:
                active_platforms.append(f"Google Maps Reviews ──► {maps_url}")
            elif deep_harvest("maps", data):
                active_platforms.append("Google Maps")
                
            # Include YouTube profile if available
            yt_val = deep_harvest("youtube", data)
            if isinstance(yt_val, str) and "youtube.com" in yt_val:
                active_platforms.append(f"YouTube Channel ──► {yt_val}")
            elif yt_val:
                active_platforms.append("YouTube")
                
            # Check for other Google services
            for service_key in ["calendar", "photos", "play_games", "drive", "meet"]:
                if deep_harvest(service_key, data):
                    active_platforms.append(f"Google {service_key.capitalize()}")
        
        # Add social media accounts from the social plugin
        elif "SocialMedia" in source:
            if isinstance(data, list):
                active_platforms.extend(data)
            elif isinstance(data, dict):
                active_platforms.append(data)
        
        # Extract data breach information from IntelBase service
        elif "IntelBase" in source:
            breaches = deep_harvest("breaches", data) or deep_harvest("exposed_in", data) or []
            if isinstance(breaches, list):
                breached_sites.extend(breaches)
            intelbase_total = deep_harvest("total_breaches", data) or 0
            if intelbase_total > 0:
                # Keep the larger breach count from multiple sources
                profile.total_breaches_found = max(profile.total_breaches_found, int(intelbase_total))

    # Remove duplicate platform entries and clean up
    profile.registered_platforms = list(set([str(p) for p in active_platforms if p]))
    profile.breached_sources = list(set([str(b) for b in breached_sites if b]))
    
    # Calculate threat level based on number of breaches and platform footprint
    threat_score = (profile.total_breaches_found * 12) + (len(profile.registered_platforms) * 5)
    if threat_score > 40:
        profile.threat_level = "Critical"
    elif threat_score > 15:
        profile.threat_level = "Moderate"
    else:
        profile.threat_level = "Low"
        
    return profile

# Main API endpoint that orchestrates the complete OSINT scan
@app.get("/api/v1/scan/{target}", response_model=NormalizedScanReport)
async def run_scan(target: str, token: str = Depends(verify_api_key)):
    """
    Executes all OSINT plugins simultaneously and aggregates results into unified profile.
    """
    # Execute all plugins in parallel for efficiency
    tasks = [plugin.execute(target) for plugin in plugins]
    results = await asyncio.gather(*tasks)
    
    # Consolidate raw data into a structured profile
    normalized_profile = normalize_intelligence_payload(target, results)
    
    # Prepare raw data for response
    raw_intel_dump = [
        {"source_name": r.source_name, "status": r.status, "raw_data": r.raw_data, "message": r.message}
        for r in results
    ]
    
    return NormalizedScanReport(
        target=target,
        status="success",
        profile=normalized_profile,
        raw_intel=raw_intel_dump
    )
