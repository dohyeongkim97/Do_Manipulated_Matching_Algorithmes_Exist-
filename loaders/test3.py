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

# headers = {
#     "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
#     "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
#     "X-Riot-Token": my_api,
# }

BASE_HEADERS = {
    "X-Riot-Token": my_api,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}

#%% 
tier = 'PLATINUM'
division = 'IV'
queue = 'RANKED_SOLO_5x5'


# #%%
# def get_summoners_by_division(tier, division, queue='RANKED_SOLO_5x5', my_api=my_api):
#     url = f'https://kr.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}?page=1&api_key={my_api}'
#     res = requests.get(url, headers=headers)
#     print(res.status_code)
#     time.sleep(1)
#     return res.json() if res.status_code == 200 else []


# # %%
# def get_matchlist(puuid, count=100, my_api=my_api):
#     url = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={my_api}'
#     res = requests.get(url, headers=headers)
#     time.sleep(1)
#     if res.status_code == 200:
#         return res.json()
#     else:
#         print(f'error occured: {res.status_code}')
#         return res.status_code
# #%%
# def get_match_detail(match_id, my_api=my_api):
#     url = f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={my_api}'
#     res = requests.get(url, headers=headers)
#     time.sleep(1)
#     return res.json() if res.status_code == 200 else None




# #%%
# def summon_info(puuid, my_api=my_api):
#     url = f'https://kr.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}?api_key={my_api}'
#     res = requests.get(url, headers=headers)
#     time.sleep(1)

#     for i in range(len(res.json())):
#         if res.json()[i]['queueType'] != 'RANKED_SOLO_5x5':
#             continue
#         else:
#             res = res.json()[i]
#             return res

def get_summoners_by_division(tier, division, queue='RANKED_SOLO_5x5'):
    url = f'https://kr.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}'
    params = {"page": 1}
    res = requests.get(url, headers=BASE_HEADERS, params=params, timeout=7)
    print(res.status_code, res.text if res.status_code != 200 else "")
    time.sleep(1.0)
    return res.json() if res.status_code == 200 else res.status_code

def get_matchlist(puuid, count=100):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
    params = {"start": 0, "count": count}
    res = requests.get(url, headers=BASE_HEADERS, params=params, timeout=7)
    time.sleep(1.0)
    return res.json() if res.status_code == 200 else res.status_code

def get_match_detail(match_id):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}'
    res = requests.get(url, headers=BASE_HEADERS, timeout=7)
    time.sleep(1.0)
    return res.json() if res.status_code == 200 else res.status_code

def summon_info(puuid):
    url = f'https://kr.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}'
    res = requests.get(url, headers=BASE_HEADERS, timeout=7)
    time.sleep(1.0)
    if res.status_code != 200:
        return res.status_code
    data = res.json()
    for row in data:
        if row.get('queueType') == 'RANKED_SOLO_5x5':
            return row
    return None

#%%
tier = 'PLATINUM' 
division = ['IV']
df_temp = pd.DataFrame()
res_errors = []
ct = 0
for div in division:
    summoners = get_summoners_by_division(tier, div)   
    summoners = summoners[:100]
    for i in range(len(summoners)):
        print('summoner_count:', ct)
        ct += 1
        puuid = summoners[i]['puuid']
        match_ids = get_matchlist(puuid, count=100)
        
        try:
            match_ids = get_matchlist(puuid, count=100)
            
            # match_ids가 리스트가 아니라 숫자(에러코드 등)일 경우
            if not isinstance(match_ids, list) or len(match_ids) < 4:
                res_errors.append(f'{i}:{match_ids}')
                continue

        except Exception as e:
            res_errors.append(f'{i}: exception - {e}')
            continue

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
summoners
#%%
temp_match_ids = get_matchlist(summoners[90]['puuid'], count=100)
# %%
res.status_code
# %%
df_temp

# %%

tier = 'PLATINUM'
division = 'IV'
url = f'https://kr.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}'

res = requests.get(url, headers = headers,)
# %%
res
# %%
