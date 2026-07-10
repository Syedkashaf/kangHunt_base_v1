from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class PluginResponse(BaseModel):
    """Data structure for individual plugin execution results."""
    source_name: str
    status: str
    confidence_score: int = 100
    raw_data: Optional[Any] = None
    message: Optional[str] = None

class ScanReport(BaseModel):
    """Data structure for raw scan report containing all plugin results."""
    target: str
    total_plugins_executed: int
    successful_plugins: int
    results: List[PluginResponse]

# Unified data models for consolidated profile output

class UnifiedProfile(BaseModel):
    """Consolidated user profile data aggregated from multiple OSINT sources."""
    full_name: Optional[str] = "Unknown"
    avatar_url: Optional[str] = None
    gaia_id: Optional[str] = None
    threat_level: str = "Low"
    total_breaches_found: int = 0
    breached_sources: List[str] = []
    registered_platforms: List[str] = []

class NormalizedScanReport(BaseModel):
    """Final API response containing normalized profile and raw data."""
    target: str
    status: str = "success"
    profile: UnifiedProfile
    raw_intel: List[Dict[str, Any]]
