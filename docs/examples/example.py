import valorantClientAPI


client = valorantClientAPI.Client(region="na")

async def main():
    await client.authorize("username", "password")

    ### Simple Examples ###
    ## MMR_FetchPlayer
    player_mmr_data = await client.MMR_FetchPlayer()

    ## MMR_FetchLeaderboard
    # You can get season ids from Content_FetchContent
    seasonId = "97b6e739-44cc-ffa7-49ad-398ba502ceb0" # Episode 1 Act 1 Id
    leaderboard_data = await client.MMR_FetchLeaderboard(seasonId)

    ## MMR_FetchCompetitiveUpdates
    competitive_updates_data = await client.MMR_FetchCompetitiveUpdates()

    ### Advanced Examples ###
    ## MMR_FetchCompetitiveUpdates
    adv_competitive_updates_data = await client.MMR_FetchCompetitiveUpdates(puuid="puuid", region="eu")

    ## MMR_FetchLeaderboard
    adv_leaderboard_data = await client.MMR_FetchLeaderboard(seasonId, startIndex=100, size=50) # Gets the 101th to 150th player

