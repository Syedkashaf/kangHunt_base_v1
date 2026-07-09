import logging
import asyncio
from fastapi import FastAPI, HTTPException, Header, Depends
from typing import List, Dict, Any

# =========================================================================
# CONFIGURATION LAYER: SUPPRESSING HTTPX LOGGER CONFLICTS
# =========================================================================
logging.getLogger("httpx").setLevel(logging.WARNING)

from models.schemas import NormalizedScanReport, UnifiedProfile, PluginResponse
from plugins.gravatar_plugin import GravatarPlugin
from plugins.holehe_plugin import HolehePlugin
from plugins.breach_plugin import BreachPlugin
from plugins.ghunt_plugin import GHuntPlugin

app = FastAPI(title="Precision OSINT Core Engine")

# Security Access Key Enforcer
import os
API_KEY = os.getenv("CORE_API_KEY")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    return x_api_key

# Asynchronous Micro-Plugin Task Pool Registry
plugins = [GravatarPlugin(), HolehePlugin(), BreachPlugin(), GHuntPlugin()]

# =========================================================================
# INTEL COMPRESSION LAYER: NORMALIZATION MAPPER ENGINE
# =========================================================================
def normalize_intelligence_payload(target: str, raw_results: List[PluginResponse]) -> UnifiedProfile:
    """
    Hyper-resilient normalization engine equipped with a Recursive Deep Harvester
    to extract keys from highly nested and unpredictable JSON structures.
    """
    # ---------------------------------------------------------
    # INTERNAL RECURSIVE CRAWLER (The Ultimate JSON Bypass)
    # ---------------------------------------------------------
    def deep_harvest(target_key: str, data_store: Any) -> Any:
        """Recursively crawls unknown nested JSON layers to find a specific key."""
        if isinstance(data_store, dict):
            # Check if key exists in current dictionary level and is not empty
            if target_key in data_store and data_store[target_key]:
                return data_store[target_key]
            # Dig deeper into all dictionary values
            for key, value in data_store.items():
                result = deep_harvest(target_key, value)
                if result: 
                    return result
        elif isinstance(data_store, list):
            # Dig into arrays
            for item in data_store:
                result = deep_harvest(target_key, item)
                if result: 
                    return result
        return None
    # ---------------------------------------------------------

    profile = UnifiedProfile()
    active_platforms = []
    breached_sites = []
    total_breaches = 0
    
    for result in raw_results:
        if result.status != "success" or not result.raw_data:
            continue
            
        source = result.source_name
        data = result.raw_data
        
        # 1. Resilient Gravatar Extraction
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
                
        # 2. Resilient Holehe Registry Harvesting
        elif "Holehe" in source:
            detected_nodes = data.get("accounts_and_numbers") or data.get("successful_platforms") or data.get("platforms") or []
            if isinstance(detected_nodes, list):
                active_platforms.extend(detected_nodes)
            elif isinstance(detected_nodes, dict):
                active_platforms.extend([k for k, v in detected_nodes.items() if v.get("exists")])
                
        # 3. Resilient XposedOrNot Dark-Web Extraction
        elif "XposedOrNot" in source:
            total_breaches = deep_harvest("total_breaches", data) or deep_harvest("total_breaches_found", data) or 0
            sites = deep_harvest("breached_platforms", data) or deep_harvest("breaches", data) or []
            if isinstance(sites, list):
                breached_sites.extend(sites)
            profile.total_breaches_found = int(total_breaches)
            
        # 4. CRITICAL UPGRADE: Recursive GHunt Intelligence Extraction
        elif "GHunt" in source:
            # Crawling entire JSON tree for names and avatars
            extracted_name = deep_harvest("name", data) or deep_harvest("profile_name", data)
            if extracted_name and str(extracted_name).lower() != "unknown":
                profile.full_name = extracted_name
                
            profile.avatar_url = deep_harvest("profile_photo", data) or deep_harvest("url", data) or profile.avatar_url
            
            # Hunting for the exact Google ID regardless of JSON architecture
            profile.gaia_id = deep_harvest("gaia_id", data) or deep_harvest("personId", data) or deep_harvest("sourceId", data)
            
            # --------------------------------------------------
            # CRITICAL FIX: FORWARDING EXTENDED URLs TO FRONTEND
            # --------------------------------------------------
            # Google Maps Data Transport
            maps_url = deep_harvest("maps_reviews_url", data)
            if maps_url:
                # Passing the full URL so scanner.py can render it natively
                active_platforms.append(f"Google Maps Reviews ──► {maps_url}")
            elif deep_harvest("maps", data):
                active_platforms.append("Google Maps")
                
            # YouTube Data Transport
            yt_val = deep_harvest("youtube", data)
            if isinstance(yt_val, str) and "youtube.com" in yt_val:
                active_platforms.append(f"YouTube Channel ──► {yt_val}")
            elif yt_val:
                active_platforms.append("YouTube")
                
            # Other Google Services Transport
            for service_key in ["calendar", "photos", "play_games", "drive", "meet"]:
                if deep_harvest(service_key, data):
                    active_platforms.append(f"Google {service_key.capitalize()}")

    # Final Deduplication & Clean Up
    profile.registered_platforms = list(set([str(p) for p in active_platforms if p]))
    profile.breached_sources = list(set([str(b) for b in breached_sites if b]))
    
    # Dynamic Composite Threat Matrix Calculations
    threat_score = (profile.total_breaches_found * 12) + (len(profile.registered_platforms) * 5)
    if threat_score > 40:
        profile.threat_level = "Critical"
    elif threat_score > 15:
        profile.threat_level = "Moderate"
    else:
        profile.threat_level = "Low"
        
    return profile

# =========================================================================
# CONTROL PATHWAY LAYER: PARALLEL EXECUTION ENDPOINT
# =========================================================================
@app.get("/api/v1/scan/{target}", response_model=NormalizedScanReport)
async def run_scan(target: str, token: str = Depends(verify_api_key)):
    """
    Orchestrates execution for multiple data acquisition threads concurrently 
    and pipes results through the harmonization engine.
    """
    # Triggering non-blocking parallel tasks across active pool registry
    tasks = [plugin.execute(target) for plugin in plugins]
    results = await asyncio.gather(*tasks)
    
    # Executing Data Normalization Process Mapping
    normalized_profile = normalize_intelligence_payload(target, results)
    
    # Serialization of complex metadata formats into standard lists
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
