# Contents
- [Getting Started](#getting-started)
    - [Intalling the Package](#installing-the-package)
    - [Authorizing](#authorizing)
    - [Setting the Region](#setting-the-region)
- [Endpoints](#endpoints)
    - [Endpoint Examples](#endpoint-examples)
# Getting Started
### Installing the Package
```
pip install valorantClientAPI
```
### Authorizing
Using a username and password
```
import valorantClientAPI

client = valorantClientAPI.Client()
await client.authorize("username", "password")
```

Using an already made entitlements token and access token
```
import valorantClientAPI

client = valorantClientAPI.Client(entitlements_token="entitlements-token", access_token="access-token")
```

### Setting the Region
If no region is set it defaults to NA. Capitalization does not matter.
```
import valorantClientAPI

client = valorantClientAPI.Client(region='na')
```
Valid regions are: ["na", "eu", "latam", "br", "ap", "kr", "pbe"]

# Endpoints
Endpoint names and further docs can be found in [techchrism's valorant-api-docs](https://github.com/techchrism/valorant-api-docs/tree/trunk/docs)
### Endpoint Examples
Using the MMR_FetchLeaderboard endpoint
```
import valorantClientAPI

client = valorantClientAPI.Client(region='na')
await client.authorize("username", "password123")

leaderboard_data = await client.MMR_FetchLeaderboard(seasonID)
```
Using the MMR_FetchPlayer endpoint
```
import valorantClientAPI

client = valorantClientAPI.Client(region='na')
await client.authorize("username", "password123")

player_data = await client.MMR_FetchPlayer()
```
