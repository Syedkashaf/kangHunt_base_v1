import httpx
from models.schemas import PluginResponse
from .base_plugin import BaseOSINTPlugin

class BreachPlugin(BaseOSINTPlugin):
    def __init__(self):
        self.source_name = "XposedOrNot (Data Breaches)"
        # XposedOrNot is a 100% free open-source OSINT API
        self.base_url = "https://api.xposedornot.com/v1/check-email/"

    async def execute(self, target: str) -> PluginResponse:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(f"{self.base_url}{target}")
                
                if response.status_code == 200:
                    data = response.json()
                    # API returns data in a 'breaches' list inside another list
                    breaches = data.get("breaches", [[]])[0]
                    return PluginResponse(
                        source_name=self.source_name,
                        status="success",
                        raw_data={
                            "total_breaches": len(breaches),
                            "breached_platforms": breaches
                        },
                        message="Dark-web data breach footprint extracted."
                    )
                elif response.status_code == 404:
                    return PluginResponse(
                        source_name=self.source_name,
                        status="success",
                        raw_data={"total_breaches": 0},
                        message="Secure: No known data breaches for this email."
                    )
                else:
                    return PluginResponse(
                        source_name=self.source_name,
                        status="error",
                        message=f"API Error {response.status_code}"
                    )
                    
        except Exception as e:
            return PluginResponse(
                source_name=self.source_name,
                status="failed",
                message=f"Network Error: {str(e)}"
            )
