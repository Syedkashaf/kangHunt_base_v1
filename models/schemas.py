from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class PluginResponse(BaseModel):
    source_name: str
    status: str
    confidence_score: int = 100
    raw_data: Optional[Any] = None
    message: Optional[str] = None

class ScanReport(BaseModel):
    target: str
    total_plugins_executed: int
    successful_plugins: int
    results: List[PluginResponse]

# ==========================================
# PHASE 10: UNIFIED DATA SCHEMAS INTEGRATION
# ==========================================

class UnifiedProfile(BaseModel):
    full_name: Optional[str] = "Unknown"
    avatar_url: Optional[str] = None
    gaia_id: Optional[str] = None
    threat_level: str = "Low"
    total_breaches_found: int = 0
    breached_sources: List[str] = []
    registered_platforms: List[str] = []

class NormalizedScanReport(BaseModel):
    target: str
    status: str = "success"
    profile: UnifiedProfile
    raw_intel: List[Dict[str, Any]]
