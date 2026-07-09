import httpx
import hashlib
from models.schemas import PluginResponse
from .base_plugin import BaseOSINTPlugin

class GravatarPlugin(BaseOSINTPlugin):
    def __init__(self):
        self.source_name = "Gravatar (Profile Footprint)"

    async def execute(self, target: str) -> PluginResponse:
        try:
            # OSINT Logic: Gravatar email ko directly nahi leta, balki MD5 Hash use karta hai
            # Hum pehle email ko lowercase karenge aur phir usay hash karenge
            email_hash = hashlib.md5(target.strip().lower().encode('utf-8')).hexdigest()
            url = f"https://en.gravatar.com/{email_hash}.json"

            async with httpx.AsyncClient(timeout=10.0) as client:
                # User-Agent dena zaroori hai taake server hamen bot samajh kar block na kare
                response = await client.get(url, headers={"User-Agent": "OSINT-Engine/1.0"})

                if response.status_code == 200:
                    data = response.json()
                    # JSON response se user profile extract karna
                    profile = data.get("entry", [])[0]
                    
                    return PluginResponse(
                        source_name=self.source_name,
                        status="success",
                        raw_data={
                            "display_name": profile.get("displayName", "N/A"),
                            "profile_url": profile.get("profileUrl", "N/A"),
                            "avatar_image": profile.get("thumbnailUrl", "N/A"),
                            "location": profile.get("currentLocation", "Not specified")
                        },
                        message="Live Gravatar profile successfully extracted."
                    )
                elif response.status_code == 404:
                    return PluginResponse(
                        source_name=self.source_name,
                        status="success", 
                        raw_data={"total_found": 0},
                        message="No public Gravatar profile linked to this email."
                    )
                else:
                     return PluginResponse(
                        source_name=self.source_name,
                        status="error",
                        message=f"HTTP Error {response.status_code}"
                    )
                    
        except Exception as e:
            return PluginResponse(
                source_name=self.source_name,
                status="failed",
                message=f"Subprocess Error: {str(e)}"
            )
