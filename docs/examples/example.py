import valorantClientAPI


client = valorantClientAPI.Client(region="na")

async def main():
    await client.authorize("username", "password")

    player_mmr_data = await client.MMR_FetchPlayer()
