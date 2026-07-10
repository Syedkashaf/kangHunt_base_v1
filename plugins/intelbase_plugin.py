import httpx
import os
from dotenv import load_dotenv
from models.schemas import PluginResponse
from .base_plugin import BaseOSINTPlugin

load_dotenv()

class IntelBasePlugin(BaseOSINTPlugin):
    """Plugin for querying IntelBase API for email breach and exposure data."""
    
    def __init__(self):
        # Load API key from environment (do not hardcode credentials)
        self.api_key = os.getenv("INTELBASE_API_KEY", "")
        # Base URL from IntelBase API documentation
        self.base_url = "https://api.intelbase.is/lookup/email"

    async def execute(self, target: str) -> PluginResponse:
        """
        Query IntelBase for email exposure data and breach information.
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                # If no API key configured, return mock response
                if not self.api_key:
                    return PluginResponse(
                        source_name="IntelBase",
                        status="success",
                        raw_data={"breaches": [], "total_breaches": 0},
                        message="IntelBase API key not configured. Set INTELBASE_API_KEY in .env"
                    )
                
                # Prepare request headers as specified in IntelBase documentation
                headers = {
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key
                }
                
                # Build the request payload
                payload = {
                    "email": target,
                    "timeout_ms": 10000,
                    "include_data_breaches": False,
                    "exclude_modules": []
                }
                
                # Send POST request to IntelBase API
                response = await client.post(
                    self.base_url, 
                    headers=headers,
                    json=payload
                )
                
                # Parse the API response
                api_data = response.json()
                
                if response.status_code == 200:
                    # Success response from IntelBase
                    return PluginResponse(
                        source_name="IntelBase",
                        status="success",
                        raw_data=api_data, 
                        message="OSINT intelligence successfully gathered."
                    )
                else:
                    # Handle API error responses
                    error_msg = api_data.get("error", f"HTTP {response.status_code}: {response.text}")
                    return PluginResponse(
                        source_name="IntelBase", 
                        status="error", 
                        message=f"Provider Error: {error_msg}"
                    )
                    
            except httpx.RequestError as e:
                # Handle network connectivity errors
                return PluginResponse(
                    source_name="IntelBase", 
                    status="failed", 
                    message=f"Network Error: {str(e)}"
                )
            except Exception as e:
                # Handle unexpected errors
                return PluginResponse(
                    source_name="IntelBase",
                    status="failed",
                    message=f"IntelBase Error: {str(e)}"
                )
