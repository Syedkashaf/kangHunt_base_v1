import httpx
from models.schemas import PluginResponse
from .base_plugin import BaseOSINTPlugin

class GravatarPlugin(BaseOSINTPlugin):
    def __init__(self):
        self.source_name = "Gravatar"
        self.base_url = "https://www.gravatar.com"

    async def execute(self, target: str) -> PluginResponse:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Gravatar MD5 hash-based lookup
                import hashlib
                email_hash = hashlib.md5(target.lower().encode()).hexdigest()
                url = f"https://www.gravatar.com/{email_hash}.json"
                
                response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    return PluginResponse(
                        source_name=self.source_name,
                        status="success",
                        raw_data=data,
                        message="Gravatar profile found"
                    )
                else:
                    return PluginResponse(
                        source_name=self.source_name,
                        status="success",
                        raw_data=None,
                        message="No Gravatar profile found"
                    )
        except Exception as e:
            return PluginResponse(
                source_name=self.source_name,
                status="failed",
                message=f"Gravatar lookup error: {str(e)}"
            )
