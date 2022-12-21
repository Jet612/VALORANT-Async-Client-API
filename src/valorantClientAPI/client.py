# Imports
import aiohttp
import requests
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
        self.client_version = get_client_version()

        if region not in regions:
            raise ValueError("Invalid region.")

    async def RSO_GetPlayerInfo(self):
        """Gets player info."""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            async with session.get(f"https://auth.riotgames.com/userinfo", headers=headers) as resp:
                return await resp.json()

    async def authorize(self, username: str, password: str, use_query_response_mode: bool = False, multi_factor_code: str = None):
        """Authorizes the client and gets entitlements token and access token."""
        self.username = username
        self.password = password

        auth = riot_auth.RiotAuth()
        await auth.authorize(username, password)
        self.entitlements_token = auth.entitlements_token
        self.access_token = auth.access_token
        
        player_info = await self.RSO_GetPlayerInfo()
        self.puuid = player_info["sub"]

    async def Content_FetchContent(self, region: str = None):
        """Fetches content."""
        if region == None:
            region = self.region
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "X-Riot-ClientPlatform": self.client_platform,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://{region}.api.riotgames.com/val/content/v1/contents", headers=headers) as resp:
                return await resp.json()

    async def AccountXP_GetPlayer(self, puuid: str = None, region: str = None):
        """Gets player's account XP."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if puuid == None:
            puuid = self.puuid

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.entitlements_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/account-xp/v1/players/{puuid}", headers=headers) as resp:
                return await resp.json()

    async def MMR_FetchPlayer(self, puuid: str = None, region: str = None):
        """Fetches player's MMR."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if puuid == None:
            puuid = self.puuid

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.entitlements_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientPlatform": self.client_platform,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}", headers=headers) as resp:
                return await resp.json()

    async def MatchHistory_FetchMatchHistory(self, puuid: str = None, region: str = None):
        """Fetches match history."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if puuid == None:
            puuid = self.puuid

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.entitlements_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientPlatform": self.client_platform,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/match-history/v1/history/{puuid}", headers=headers) as resp:
                return await resp.json()

    async def MatchDetails_FetchMatchDetails(self, matchId: str, region: str = None):
        """Fetches match details."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.entitlements_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/match-details/v1/matches/{matchId}", headers=headers) as resp:
                return await resp.json()

    async def MMR_FetchCompetitiveUpdates(self, puuid: str = None, startIndex: int = 0, size: int = 200, region: str = None):
        """Fetches competitive updates."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if puuid == None:
            puuid = self.puuid

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.entitlements_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientPlatform": self.client_platform
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates", headers=headers) as resp:
                return await resp.json()

    async def MMR_FetchLeaderboard(self, seasonId: str, startIndex: int = 0, size: int = 200, region: str = None):
        """Fetches Leaderboard."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.entitlements_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/mmr/v1/leaderboards/affinity/na/queue/competitive/season/{seasonId}?startIndex=0&size={size}", headers=headers) as resp:
                return await resp.json()

    async def Restrictions_FetchPlayerRestrictionsV2(self, region: str = None):
        """Fetches player restrictions."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.entitlements_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/restrictions/v3/penalties", headers=headers) as resp:
                return await resp.json()

    async def ItemProgressionDefinitionsV2_Fetch(self, region: str = None):
        """Fetches item progression definitions."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.entitlements_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/contract-definitions/v3/item-upgrades", headers=headers) as resp:
                return await resp.json()

    async def Config_FetchConfig(self, region: str = None):
        """Fetch Config."""
        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://shared.{region}.a.pvp.net/v1/config/{region}") as resp:
                return await resp.json()

def get_client_version() -> str:
    resp = requests.get("https://valorant-api.com/v1/version")
    respData = resp.json()
    return respData['data']['riotClientBuild']
