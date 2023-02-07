# Imports
import aiohttp
import requests
import json
from . import riot_auth
from .response.core_game import CoreGameDetails, CoreGameMatchLoadout
from .response.pre_game import PreGameDetails
from .response.mmr import MatchHistory, MatchDetails
from dataclass_wizard import fromdict
from .utils.limiter import Limiter
from dataclass_wizard.errors import ParseError


# Variables
regions = ["na", "eu", "latam", "br", "ap", "kr", "pbe"]

# Custom Exceptions
class Exceptions:
    class NotAuthorized(Exception):
        """You must authorize before using this function."""
    class IndexOutOfRange(Exception):
        """Index out of range."""
    class InvalidQueueID(Exception):
        """Invalid Queue ID"""

async def content_verify(response):
    """
    Helper function to verify response content-type & deal
    with the response appropriately 
    """
    content_type = response.headers.get("Content-Type")
    if content_type == "application/json; charset=utf-8" or content_type == "application/json":
        return await response.json()
    elif content_type == "text/plain; charset=utf-8" or content_type == "text/plain":
        return json.loads(await response.text())

class Client:
    def __init__(self, region: str = "na", client_platform: str = None, entitlements_token: str = None, access_token: str = None):
        """Initializes the client."""
        self.username = None
        self.password = None
        self.puuid = None
        self.region = region.lower()
        self.entitlements_token = entitlements_token
        self.access_token = access_token
        self.client_version = get_client_version()

        if client_platform is None:
            self.client_platform = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
        else:
            self.client_platform = client_platform

        if region not in regions:
            raise ValueError("Invalid region.")
       
    
    async def SetTokens(self, access_token: str, entitlements_token: str):
        """Sets tokens."""
        self.access_token = access_token
        self.entitlements_token = entitlements_token
   
   
    @Limiter()
    async def RSO_GetPlayerInfo(self):
        """Gets player info."""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            async with session.get(f"https://auth.riotgames.com/userinfo", headers=headers) as resp:
                return await content_verify(response=resp)
    
    
    @Limiter()
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
    @Limiter()
    async def Content_FetchContent(self, region: str = None):
        """Fetches content."""
        if region is None:
            region = self.region
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "X-Riot-ClientPlatform": self.client_platform,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://{region}.api.riotgames.com/val/content/v1/contents", headers=headers) as resp:
                contentType = resp.headers.get("Content-Type")
                if contentType == "application/json; charset=utf-8" or contentType == "application/json":
                    return await resp.json()
                elif contentType == "text/plain; charset=utf-8" or contentType == "text/plain":
                    return json.loads(await resp.text())
    
    
    @Limiter()
    async def AccountXP_GetPlayer(self, puuid: str = None, region: str = None):
        """Gets player's account XP."""
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if puuid is None:
            puuid = self.puuid

        if region is None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/account-xp/v1/players/{puuid}", headers=headers) as resp:
                return json.loads(await resp.text())
    
    
    @Limiter()
    async def MMR_FetchPlayer(self, puuid: str = None, region: str = None):
        """Fetches player's MMR."""
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if puuid is None:
            puuid = self.puuid

        if region is None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientPlatform": self.client_platform,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}", headers=headers) as resp:
                return await content_verify(response=resp)
    
    
    @Limiter()
    async def MatchHistory_FetchMatchHistory(self, puuid: str = None, region: str = None, start_index: int =0, end_index: int = 25, queue_id: str="null") -> MatchHistory:
        """Fetches match history.
        Pass in a queue_id to filter by queue. Start & End Index should be chunk of 25.
        Valid queue IDs: queues = [
                                    "competitive",
                                    "custom",
                                    "deathmatch",
                                    "ggteam",
                                    "snowball",
                                    "spikerush",
                                    "unrated",
                                    "onefa",
                                    "null",
                                    ]
        """
        # check if start_index & end_index is difference of 25
        if (end_index - start_index) > 25:
            raise Exceptions.IndexOutOfRange("Start & End Index should be chunk of 25.")
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if puuid is None:
            puuid = self.puuid

        if region is None:
            region = self.region
        
        if queue_id not in ["competitive", "custom", "deathmatch", "ggteam", "snowball", "spikerush", "unrated", "onefa", "null"]:
            raise Exceptions.InvalidQueueID('Invalid queue ID. Valid queue IDs: queues = ["competitive", "custom", "deathmatch", "ggteam", "snowball", "spikerush", "unrated", "onefa", "null"]')

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientPlatform": self.client_platform,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/match-history/v1/history/{puuid}?startIndex={start_index}&endIndex={end_index}"
            + (f"&queue={queue_id}" if queue_id != "null" else ""), headers=headers) as resp:
                return fromdict(MatchHistory, await content_verify(response=resp))
    
    
    @Limiter()
    async def MatchDetails_FetchMatchDetails(self, matchId: str, region: str = None) -> MatchDetails:
        """Fetches match details."""
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region is None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/match-details/v1/matches/{matchId}", headers=headers) as resp:
                try:
                    ret= fromdict(MatchDetails, await content_verify(response=resp))
                    return ret
                except ParseError as err:
                    print("Warning!!! Failed to parse the file. You are returned with a json struct.")
                    print("Either change the modify the MatchDetails class in mmr.py & submit an issue to github")
                    print(err)
                    return await content_verify(response=resp)
    
    
    @Limiter()
    async def MMR_FetchCompetitiveUpdates(self, puuid: str = None, region: str = None):
        """Fetches competitive updates."""
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if puuid is None:
            puuid = self.puuid

        if region is None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientPlatform": self.client_platform
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates", headers=headers) as resp:
                return await content_verify(response=resp)
    
    
    @Limiter()
    async def MMR_FetchLeaderboard(self, seasonId: str, startIndex: int = 0, size: int = 200, region: str = None):
        """Fetches Leaderboard."""
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region is None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token,
                "X-Riot-ClientVersion": self.client_version
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/mmr/v1/leaderboards/affinity/na/queue/competitive/season/{seasonId}?startIndex=0&size={size}", headers=headers) as resp:
                return await content_verify(response=resp)
    
    
    @Limiter()
    async def Restrictions_FetchPlayerRestrictionsV2(self, region: str = None):
        """Fetches player restrictions."""
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region is None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/restrictions/v3/penalties", headers=headers) as resp:
                return await content_verify(response=resp)
    
    
    @Limiter()
    async def ItemProgressionDefinitionsV2_Fetch(self, region: str = None):
        """Fetches item progression definitions."""
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region is None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://pd.{region}.a.pvp.net/contract-definitions/v3/item-upgrades", headers=headers) as resp:
                return await content_verify(response=resp)
   
   
    @Limiter()
    async def Config_FetchConfig(self, region: str = None):
        """Fetch Config."""
        if region is None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://shared.{region}.a.pvp.net/v1/config/{region}") as resp:
                return await content_verify(response=resp)
    
    
    @Limiter()
    async def Pregame_GetPlayer(self, region: str = None) -> dict:
        """Get the ID of a game in the pre-game stage"""
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region is None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://glz-{region}-1.{region}.a.pvp.net/pregame/v1/players/{self.puuid}", headers=headers) as resp:
                return await content_verify(response=resp)
   
   
    @Limiter()
    async def Pregame_GetMatch(self, region: str = None, match_id: str=None) -> PreGameDetails:
        """Get info for a game in the pre-game stage"""
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region is None:
            region = self.region

        if match_id is None:
            res = await self.Pregame_GetPlayer()
            match_id = res.get("MatchID")


        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://glz-{region}-1.{region}.a.pvp.net/pregame/v1/matches/{match_id}", headers=headers) as resp:
                return await content_verify(response=resp)

   
    #Current Game Endpoints
    @Limiter()
    async def CoreGame_GetPlayer(self, region: str = None) -> dict:
        """Get the ID of a game in progress
        this api & PreGame_GetPlayer() api returns the same results.
        So, if the game is already in CoreGame stage. Then use this method
        to get match_id. As each endpoint is only response if the game is on that 
        stage.
        """
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region is None:
            region = self.region

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/players/{self.puuid}", headers=headers) as resp:
                return await content_verify(response=resp)
    
    
    @Limiter()
    async def CoreGame_FetchMatch(self, region: str = None, match_id: str = None) -> CoreGameDetails:
        """Get match details of a game in progress"""
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region is None:
            region = self.region

        if match_id is None:
            res = await self.CoreGame_GetPlayer()
            match_id = res.get("MatchID")

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/matches/{match_id}", headers=headers) as resp:
                return fromdict(CoreGameDetails, await content_verify(response=resp))
    
    
    @Limiter()
    async def CoreGame_FetchMatchLoadouts(self, region: str = None, match_id: str = None) -> CoreGameMatchLoadout:
        """Get player skins and spray for a game in progress.
        It will return a CoreGameMatchLoadout Object.
        """
        if self.entitlements_token is None or self.access_token is None:
            raise Exceptions.NotAuthorized("You must authorize before using this function.")

        if region is None:
            region = self.region
        
        if match_id is None:
            res = await self.CoreGame_GetPlayer()
            match_id = res.get("MatchID")

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
            async with session.get(f"https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/matches/{match_id}/loadouts", headers=headers) as resp:
                return fromdict(CoreGameMatchLoadout, await content_verify(response=resp))



    # Store Endpoints
    @Limiter()
    async def Store_GetOffers(self, region: str = None):
        """Gets store offers."""
        if region is None:
            region = self.region

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://store.{region}.a.pvp.net/store/v2/offers", headers=headers) as resp:
                return await content_verify(response=resp)
   
   
    @Limiter()
    async def Store_GetStorefrontV2(self, region: str = None, puuid: str = None):
        """Gets storefront."""
        if region is None:
            region = self.region

        if puuid is None:
            puuid = self.puuid

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pd.{region}.a.pvp.net/store/v2/storefront/{puuid}", headers=headers) as resp:
                return await content_verify(response=resp)
    
    
    @Limiter()
    async def Store_GetWallet(self, region: str = None, puuid: str = None):
        """Gets wallet."""
        if region is None:
            region = self.region

        if puuid is None:
            puuid = self.puuid

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pd.{region}.a.pvp.net/store/v1/wallet/{puuid}", headers=headers) as resp:
                return await content_verify(response=resp)
    
    
    @Limiter()
    async def Store_GetOrder(self, orderId: str, region: str = None):
        """Get Order."""
        if region is None:
            region = self.region

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pd.{region}.a.pvp.net/store/v1/order/{orderId}", headers=headers) as resp:
                return await content_verify(response=resp)
   
   
    @Limiter()
    async def Store_GetEntitlements(self, itemTypeId: str, region: str = None, puuid: str = None):
        """Get Entitlements."""
        if region is None:
            region = self.region

        if puuid is None:
            puuid = self.puuid

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{itemTypeId}", headers=headers) as resp:
                return await content_verify(response=resp)                

    
    # Other
    @Limiter()
    async def PlayerPref_SavePreferenceV3(self, region: str = None, puuid: str = None):
        """Save Preference."""
        if puuid is None:
            puuid = self.puuid

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://playerpreferences.riotgames.com/playerPref/v3/savePreference", headers=headers) as resp:
                return await content_verify(response=resp)

    @Limiter()
    async def get_username_from_ids(self, region: str = None, puuids: list = []):
        """Gets username from List of PUUIDs"""
        if region is None:
            region = self.region

        if not puuids:
            puuids.append(self.puuid)

        headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Riot-Entitlements-JWT": self.entitlements_token
            }

        async with aiohttp.ClientSession() as session:
            async with session.put(f"https://pd.{region}.a.pvp.net/name-service/v2/players", headers=headers, data=json.dumps(puuids)) as resp:
                return await content_verify(response=resp) 


def get_client_version() -> str:
    resp = requests.get("https://valorant-api.com/v1/version")
    respData = resp.json()
    return respData['data']['riotClientVersion']
