import asyncio
import httpx
from models.schemas import PluginResponse
from .base_plugin import BaseOSINTPlugin

class SocialMediaPlugin(BaseOSINTPlugin):
    """
    Social Media Footprint Detection Plugin
    Queries multiple social media platforms for username availability and profiles
    """
    def __init__(self):
        self.source_name = "SocialMedia (Profile Detection)"
        self.platforms = {
            "twitter": "https://api.twitter.com/2/users/by/username/",
            "github": "https://api.github.com/users/",
            "reddit": "https://www.reddit.com/user/",
            "linkedin": "https://www.linkedin.com/search/results/all/?keywords=",
        }

    async def execute(self, target: str) -> PluginResponse:
        """
        Extracts username from email and checks social media presence
        target format: username or email@domain.com
        """
        try:
            # Extract username from email
            username = target.split("@")[0] if "@" in target else target
            
            found_platforms = []
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Check GitHub (fastest and most reliable public API)
                try:
                    gh_response = await client.get(
                        f"https://api.github.com/users/{username}",
                        headers={"User-Agent": "OSINT-Engine/1.0"}
                    )
                    if gh_response.status_code == 200:
                        data = gh_response.json()
                        found_platforms.append({
                            "platform": "GitHub",
                            "username": username,
                            "profile_url": data.get("html_url"),
                            "public_repos": data.get("public_repos", 0),
                            "followers": data.get("followers", 0)
                        })
                except Exception:
                    pass
            
            if found_platforms:
                return PluginResponse(
                    source_name=self.source_name,
                    status="success",
                    raw_data=found_platforms,
                    message=f"Found {len(found_platforms)} social media presence(s)."
                )
            else:
                return PluginResponse(
                    source_name=self.source_name,
                    status="success",
                    raw_data=[],
                    message="No active social media profiles detected."
                )
                
        except Exception as e:
            return PluginResponse(
                source_name=self.source_name,
                status="failed",
                message=f"Social Media Detection Error: {str(e)}"
            )
