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
    print(res.status_code)
    time.sleep(0.82)
    return res.json() if res.status_code == 200 else []


# %%
def get_matchlist(puuid, count=100, my_api=my_api):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={my_api}'
    res = requests.get(url, headers=headers)
    time.sleep(0.82)
    if res.status_code == 200:
        return res.json()
    else:
        print(f'error occured: {res.status_code}')
        return []
#%%
def get_match_detail(match_id, my_api=my_api):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={my_api}'
    res = requests.get(url, headers=headers)
    time.sleep(0.82)
    return res.json() if res.status_code == 200 else None

#%%
def summon_info(puuid, my_api=my_api):
    url = f'https://kr.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}?api_key={my_api}'
    res = requests.get(url, headers=headers)
    time.sleep(0.82)

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
tier = 'PLATINUM' 
division = ['IV']
df_temp = pd.DataFrame()

ct = 0
for div in division:
    summoners = get_summoners_by_division(tier, div)   
    for i in range(len(summoners)):
        print('summoner_count:', ct)
        ct += 1
        puuid = summoners[i]['puuid']
        match_ids = get_matchlist(puuid, count=100)
        
        summoner_puuid = [summoners[i]['puuid']]*10
        if tier:
            tiers = [tier]*10
        
        divisions = [div]*10

        if summoners[i]['hotStreak'] == True:
            hotstreaks = [True]*10
        else:
            hotstreaks = [False]*10

        ct_match = 0
        for match in match_ids:
            print(f'match_number_by_each_summoner {ct}:', ct_match)
            ct_match += 1
            matches = [match]*10
            win_or_lose = []
            matchdata = get_match_detail(match)
            if matchdata:
                participants = matchdata['metadata']['participants']
                gameinfo = matchdata['info']
                if gameinfo['participants'][0]['win'] == True:
                    win_or_lose.extend([True]*5)
                    win_or_lose.extend([False]*5)

                else:
                    win_or_lose.extend([True]*5)
                    win_or_lose.extend([False]*5)

            temp = pd.DataFrame([summoner_puuid, tiers, divisions, matches, participants, win_or_lose, hotstreaks]).T
            df_temp = pd.concat([df_temp, temp], ignore_index=True, axis=0)

print('done')

# %%
temp
# %%
temp_match_ids = get_matchlist(summoners[90]['puuid'], count=100)
# %%
temp_match_ids