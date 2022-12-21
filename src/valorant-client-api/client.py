# Imports
import aiohttp
from . import riot_auth

# Variables
regions = ["na", "eu", "latam", "br", "ap", "kr", "pbe"]

class Client:
    def __init__(self, username: str = None, password: str = None, puuid: str = None, region: str = "na", entitlements_token: str = None, access_token: str = None):
        """If you are using a username and password, you must authorize. If you are using an entitlements token and access token, you do not need to authorize."""
        self.username = username
        self.password = password
        self.puuid = puuid
        self.region = region.lower()
        self.entitlements_token = entitlements_token
        self.access_token = access_token
        self.client_platform = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
        self.riotId = None
        self.name = None
        self.tag = None

        # if a username and password or entitlements token and access token are not provided, raise an error
        if (self.username == None and self.password == None) and (self.entitlements_token == None and self.access_token == None):
            raise ValueError("Either a username and password or entitlements token and access token are needed.")

        if region not in regions:
            raise ValueError("Invalid region.")

    async def authorize(self):
        """Authorizes the client and gets entitlements token and access token."""
        if self.username == None or self.password == None:
            raise ValueError("Username and password are needed to authorize.")

        auth = riot_auth.RiotAuth()
        await auth.authorize(self.username, self.password)
        self.entitlements_token = auth.entitlements_token
        self.access_token = auth.access_token
        self.puuid = auth.user_id
