# Imports
import aiohttp
import requests
import json
from . import riot_auth

# Variables
regions = ["na", "eu", "latam", "br", "ap", "kr", "pbe"]

# Custom Exceptions
class Exceptions:
    class NotAuthorized(Exception):
        """You must authorize before using this function."""


class Client:
    def __init__(self, region: str = "na", client_platform: str = None):
        """Initializes the client."""
        self.username = None
        self.password = None
        self.puuid = None
        self.region = region.lower()
        self.entitlements_token = None
        self.access_token = None
        self.client_version = get_client_version()

        if client_platform == None:
            self.client_platform = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
        else:
            self.client_platform = client_platform

        if region not in regions:
            raise ValueError("Invalid region.")

    async def RSO_GetPlayerInfo(self):
        """Gets player info."""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            async with session.get(f"https://auth.riotgames.com/userinfo", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def authorize(self, username: str, password: str, use_query_response_mode: bool = False, multi_factor_code: str = None) -> None:
        """Authorizes the client and gets entitlements token and access token."""
        self.username = username
        self.password = password

        auth = riot_auth.RiotAuth()
        await auth.authorize(username, password)
        self.entitlements_token = auth.entitlements_token
        self.access_token = auth.access_token
        
        player_info = await self.RSO_GetPlayerInfo()
        self.puuid = player_info["sub"]

    # PVP Endpoints
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
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

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
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/account-xp/v1/players/{puuid}", headers=headers) as resp:
                return json.loads(await resp.text())

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
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientPlatform": self.client_platform,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

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
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientPlatform": self.client_platform,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/match-history/v1/history/{puuid}", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def MatchDetails_FetchMatchDetails(self, matchId: str, region: str = None):
        """Fetches match details."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/match-details/v1/matches/{matchId}", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def MMR_FetchCompetitiveUpdates(self, puuid: str = None, region: str = None):
        """Fetches competitive updates."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if puuid == None:
            puuid = self.puuid

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientPlatform": self.client_platform
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def MMR_FetchLeaderboard(self, seasonId: str, startIndex: int = 0, size: int = 200, region: str = None):
        """Fetches Leaderboard."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/mmr/v1/leaderboards/affinity/na/queue/competitive/season/{seasonId}?startIndex=0&size={size}", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def Restrictions_FetchPlayerRestrictionsV2(self, region: str = None):
        """Fetches player restrictions."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/restrictions/v3/penalties", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def ItemProgressionDefinitionsV2_Fetch(self, region: str = None):
        """Fetches item progression definitions."""
        if self.entitlements_token == None or self.access_token == None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/contract-definitions/v3/item-upgrades", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def Config_FetchConfig(self, region: str = None):
        """Fetch Config."""
        if region == None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://shared.{region}.a.pvp.net/v1/config/{region}") as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    # Store Endpoints
    async def Store_GetOffers(self, region: str = None):
        """Gets store offers."""
        if region == None:
            region = self.region

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://store.{region}.a.pvp.net/store/v2/offers", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def Store_GetStorefrontV2(self, region: str = None, puuid: str = None):
        """Gets storefront."""
        if region == None:
            region = self.region

        if puuid == None:
            puuid = self.puuid

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pd.{region}.a.pvp.net/store/v2/storefront/{puuid}", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def Store_GetWallet(self, region: str = None, puuid: str = None):
        """Gets wallet."""
        if region == None:
            region = self.region

        if puuid == None:
            puuid = self.puuid

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pd.{region}.a.pvp.net/store/v1/wallet/{puuid}", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def Store_GetOrder(self, orderId: str, region: str = None):
        """Get Order."""
        if region == None:
            region = self.region

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pd.{region}.a.pvp.net/store/v1/order/{orderId}", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

    async def Store_GetEntitlements(self, itemTypeId: str, region: str = None, puuid: str = None):
        """Get Entitlements."""
        if region == None:
            region = self.region

        if puuid == None:
            puuid = self.puuid

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{itemTypeId}", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8":
                    return json.loads(await resp.text())

def get_client_version() -> str:
    resp = requests.get("https://valorant-api.com/v1/version")
    respData = resp.json()
    return respData['data']['riotClientBuild']
