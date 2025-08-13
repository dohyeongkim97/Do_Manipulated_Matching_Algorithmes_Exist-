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
#%%
import os
if os.getcwd() != 'C:\\Users\\user\\jupyter\\lol_match\\loaders':
    os.chdir('C:\\Users\\user\\jupyter\\lol_match\\loaders')
import pandas as pd
import functions as fn
import time
from dotenv import dotenv_values
from pathlib import Path
import requests
from pathlib import Path
import time
import datetime
import csv
import os
import sys
import random

#%%
env_path = os.getcwd() + '\\.env'
s = time.time()

config = dotenv_values(env_path)
my_api = config.get("API")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}

#%% 
tier = 'PLATINUM'
division = 'IV'
queue = 'RANKED_SOLO_5x5'


#%%
def get_summoners_by_division(tier, division, queue='RANKED_SOLO_5x5', my_api=my_api):
    url = f'https://kr.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}?page=1&api_key={my_api}'
    res = requests.get(url, headers=headers)
    time.sleep(0.85)
    return res.json() if res.status_code == 200 else []


# %%
def get_matchlist(puuid, count=100, my_api=my_api):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={my_api}'
    res = requests.get(url, headers=headers)
    time.sleep(0.85)
    return res.json() if res.status_code == 200 else []

#%%
def get_match_detail(match_id, my_api=my_api):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={my_api}'
    res = requests.get(url, headers=headers)
    time.sleep(0.85)
    return res.json() if res.status_code == 200 else None

summoners = get_summoners_by_division(tier, division)
#%%
summoners = get_summoners_by_division(tier, division)
df_summon = pd.DataFrame(summoners)

#%%
match_ids = get_matchlist(summoners[0]['puuid'])
#%%
matchdata = get_match_detail(match_ids[0])
#%%
pd.DataFrame(matchdata['metadata'])


#%%
puuid = summoners[4]['puuid']
url_temp = f'https://kr.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}?api_key={my_api}'
res_temp = requests.get(url_temp, headers=headers)
#%%
res_temp.json()

#%%
def summon_info(puuid, my_api=my_api):
    url = f'https://kr.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}?api_key={my_api}'
    res = requests.get(url, headers=headers)
    time.sleep(0.85)

    for i in range(len(res.json())):
        if res.json()[i]['queueType'] != 'RANKED_SOLO_5x5':
            continue
        else:
            res = res.json()[i]
            
            return res
#%%
# review the codes below after.
for i in range(0, 20):
    summ = summoners[i]
    puuid = summ['puuid']
    match_ids = get_matchlist(puuid, count=100)
#%%

#platinum
tier = 'PLATINUM' 
division = ['IV', 'III', 'II', 'I']

#%%
df_meta = pd.DataFrame(matchdata['metadata'])
#%%

df_meta
#%%
target_dict = {}

#%%
matchdata['info']['participants'][7]['win']

target_user = [summoners[0]['puuid']]
game_lists = [match_ids]
#%%
target_users = target_user*10
target_users

len(target_users)
# %%
info = summon_info(summoners[1]['puuid'], my_api=my_api)


target_users
# %%
