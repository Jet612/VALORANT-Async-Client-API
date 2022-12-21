# Contents
- [Getting Started](#getting-started)
    - [Intalling the Package](#installing-the-package)
    - [Authorizing](#authorizing)
    - [Setting the Region](#setting-the-region)
- [Endpoints](#endpoints)
    - [Endpoint Examples](#endpoint-examples)
# Getting Started
### Installing the Package
Installing newest version
```
pip install valorantClientAPI
```
Installing a specific version
```
pip install valorantClientAPI==[version]
```
```
pip install valorantClientAPI==0.0.1
```
### Authorizing
Using a username and password
```python
import valorantClientAPI

client = valorantClientAPI.Client()

async def main():
    await client.authorize("username", "password")
```
Using a multi-factor code
```python
import valorantClientAPI

client = valorantClientAPI.Client()

async def main():
    await client.authorize("username", "password", multi_factor_code="code")
```

Using an already made entitlements token and access token
```python
import valorantClientAPI

client = valorantClientAPI.Client(entitlements_token="entitlements-token", access_token="access-token")
```

### Setting the Region
If no region is set it defaults to 'na'. Capitalization does not matter.
```python
import valorantClientAPI

client = valorantClientAPI.Client(region='na')
```
Valid regions are: ["na", "eu", "latam", "br", "ap", "kr", "pbe"]

# Endpoints
Endpoint names and further docs can be found in [techchrism's valorant-api-docs](https://github.com/techchrism/valorant-api-docs/tree/trunk/docs)
### Endpoint Examples
See more examples in [examples.py](examples/example.py)

Using the MMR_FetchLeaderboard endpoint
```python
import valorantClientAPI

client = valorantClientAPI.Client(region='na')

async def main():
    await client.authorize("username", "password123")

    leaderboard_data = await client.MMR_FetchLeaderboard(seasonID)
```
Using the MMR_FetchPlayer endpoint
```python
import valorantClientAPI

client = valorantClientAPI.Client(region='na')

async def main():
    await client.authorize("username", "password123")

    player_data = await client.MMR_FetchPlayer()
```
