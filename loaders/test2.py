#%%
from functions import (
    get_random_summoners,
    get_summoner_name_by_puuid,
    get_recent_match_ids,
    get_match_detail,
    extract_match_summary

)
import pandas as pd

tier = 'PLATINUM'
division = 'IV'
user_count = 3
match_count = 2

result = []
summoners = get_random_summoners(tier, division, user_count)

for summ in summoners:
    puuid = summ['puuid']
    summoner_name = get_summoner_name_by_puuid(puuid) or "Unknown"

    match_ids = get_recent_match_ids(puuid, match_count)
    for match_id in match_ids:
        match_detail = get_match_detail(match_id)
        if match_detail:
            match_summary = extract_match_summary(match_detail, puuid)
            if match_summary:
                result.append({
                    "tier": tier,
                    "division": division,
                    "summonerName": match_summary['player_name'],
                    "puuid": puuid,
                    "matchId": match_id,
                    "win": match_summary['win'],
                    "teamMembers": match_summary['team_members'],
                    "enemyMembers": match_summary['enemy_members']
                })


# %%
pd.DataFrame(match_detail)
# %%
