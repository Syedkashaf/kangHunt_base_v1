import httpx
from models.schemas import PluginResponse
from .base_plugin import BaseOSINTPlugin

class GravatarPlugin(BaseOSINTPlugin):
    """Plugin for querying Gravatar profiles using email-based MD5 hash lookup."""
    
    def __init__(self):
        self.source_name = "Gravatar"
        self.base_url = "https://www.gravatar.com"

    async def execute(self, target: str) -> PluginResponse:
        """Query Gravatar API for profile information associated with an email."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Gravatar uses MD5 hash of email for profile lookup
                import hashlib
                email_hash = hashlib.md5(target.lower().encode()).hexdigest()
                url = f"https://www.gravatar.com/{email_hash}.json"
                
                response = await client.get(url)
                
                if response.status_code == 200:
                    # Profile found, return the data
                    data = response.json()
                    return PluginResponse(
                        source_name=self.source_name,
                        status="success",
                        raw_data=data,
                        message="Gravatar profile found"
                    )
                else:
                    # No profile found for this email
                    return PluginResponse(
                        source_name=self.source_name,
                        status="success",
                        raw_data=None,
                        message="No Gravatar profile found"
                    )
        except Exception as e:
            # Handle any network or parsing errors
            return PluginResponse(
                source_name=self.source_name,
                status="failed",
                message=f"Gravatar lookup error: {str(e)}"
            )
