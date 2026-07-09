import httpx
import os
from dotenv import load_dotenv
from models.schemas import PluginResponse
from .base_plugin import BaseOSINTPlugin

load_dotenv()

class IntelBasePlugin(BaseOSINTPlugin):
    def __init__(self):
        # OPSEC REMINDER: Ensure your real key is in the .env file, NOT hardcoded here.
        self.api_key = os.getenv("INTELBASE_API_KEY", "")
        # Updated Base URL from documentation
        self.base_url = "https://api.intelbase.is/lookup/email" 

    async def execute(self, target: str) -> PluginResponse:
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                # If no API key, return mock response
                if not self.api_key:
                    return PluginResponse(
                        source_name="IntelBase",
                        status="success",
                        raw_data={"breaches": [], "total_breaches": 0},
                        message="IntelBase API key not configured. Set INTELBASE_API_KEY in .env"
                    )
                
                # 1. Defining the strict headers exactly as docs requested
                headers = {
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key
                }
                
                # 2. Building the JSON Payload
                payload = {
                    "email": target,
                    "timeout_ms": 10000,
                    "include_data_breaches": False,
                    "exclude_modules": []
                }
                
                # 3. Executing a POST request
                response = await client.post(
                    self.base_url, 
                    headers=headers,
                    json=payload
                )
                
                # API almost always returns JSON, even on errors
                api_data = response.json()
                
                if response.status_code == 200:
                    return PluginResponse(
                        source_name="IntelBase",
                        status="success",
                        raw_data=api_data, 
                        message="OSINT intelligence successfully gathered."
                    )
                else:
                    # 4. Graceful Error Handling
                    error_msg = api_data.get("error", f"HTTP {response.status_code}: {response.text}")
                    return PluginResponse(
                        source_name="IntelBase", 
                        status="error", 
                        message=f"Provider Error: {error_msg}"
                    )
                    
            except httpx.RequestError as e:
                return PluginResponse(
                    source_name="IntelBase", 
                    status="failed", 
                    message=f"Network Error: {str(e)}"
                )
            except Exception as e:
                return PluginResponse(
                    source_name="IntelBase",
                    status="failed",
                    message=f"IntelBase Error: {str(e)}"
                )
