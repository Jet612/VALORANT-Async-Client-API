# Imports
import aiohttp
from . import riot_auth

# Variables
regions = ["na", "eu", "latam", "br", "ap", "kr", "pbe"]

# Custom Exceptions
class Exceptions:
    class NotAuthorized(Exception):
        """You must authorize before using this function."""


class Client:
    def __init__(self, puuid: str = None, region: str = "na", entitlements_token: str = None, access_token: str = None):
        """If you are using a username and password, you must authorize. If you are using an entitlements token and access token, you do not need to authorize."""
        self.username = None
        self.password = None
        self.puuid = puuid
        self.region = region.lower()
        self.entitlements_token = entitlements_token
        self.access_token = access_token
        self.client_platform = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
        self.riotId = None
        self.name = None
        self.tag = None

        if region not in regions:
            raise ValueError("Invalid region.")

    async def authorize(self, username, password):
        """Authorizes the client and gets entitlements token and access token."""
        self.username = username
        self.password = password

        auth = riot_auth.RiotAuth()
        await auth.authorize(self.username, self.password)
        self.entitlements_token = auth.entitlements_token
        self.access_token = auth.access_token
        self.puuid = auth.user_id

    async def MMR_FetchCompetitiveUpdates(self, startIndex: int = 0, size: int = 200):
        """Fetches competitive updates."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.entitlements_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientPlatform": self.client_platform
            }
            async with session.get(f"https://{self.region}.api.riotgames.com/val/content/v1/contents", headers=headers) as resp:
                return await resp.json()

