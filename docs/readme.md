# Contents
- [Getting Started](#getting-started)
    - [Intalling the Package](#installing-the-package)
    - [Authorizing](#authorizing)
    - [Setting the Region](#setting-the-region)
- [Endpoints](#endpoints)
    - [Endpoint Examples](#endpoint-examples)
- [Other](#other)
    - [Updating the Package](#updating-the-package)
    - [Requirements](#requirements)
    - [Other Resources/Projects](#useful-resourcesprojects)
# Getting Started
## Installing the Package
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
[Back to top](#contents)
## Authorizing
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
[Back to top](#contents)
## Setting the Region
If no region is set it defaults to 'na'. Capitalization does not matter.
```python
import valorantClientAPI

client = valorantClientAPI.Client(region='na')
```
Valid regions are: ["na", "eu", "latam", "br", "ap", "kr", "pbe"]

[Back to top](#contents)
# Endpoints
Endpoint names and further docs can be found in [techchrism's valorant-api-docs](https://github.com/techchrism/valorant-api-docs/tree/trunk/docs)
### Endpoint Examples
See more examples in [examples.py](examples/example.py)

Example using the MMR_FetchLeaderboard endpoint
```python
import valorantClientAPI

client = valorantClientAPI.Client(region='na')

async def main():
    await client.authorize("username", "password123")

    leaderboard_data = await client.MMR_FetchLeaderboard(seasonID)
```
Example using the MMR_FetchPlayer endpoint
```python
import valorantClientAPI

client = valorantClientAPI.Client(region='na')

async def main():
    await client.authorize("username", "password123")

    player_data = await client.MMR_FetchPlayer()
```
[Back to top](#contents)
# Other
## Updating the Package
Updating to the most recent version
```
pip install -U valorantClientAPI
```
Updating to a specific version
```
pip install valorantClientAPI==[verison]
```
```
pip install valorantClientAPI==0.0.1
```
[Back to top](#contents)
## Requirements
Requirements should be installed when you install the package, however if they aren't or you want to see the requirements see the [requirements.txt](https://github.com/Jet612/VALORANT-Async-Client-API/blob/main/requirements.txt) file. 

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/valorantclientapi)

[Back to top](#contents)
## Useful Resources/Projects
- [techchrism's valorant-api-docs](https://github.com/techchrism/valorant-api-docs)
- [Soneliem's Useful-ValorantAPI-Info](https://github.com/Soneliem/Useful-ValorantAPI-Info)

[Back to top](#contents)