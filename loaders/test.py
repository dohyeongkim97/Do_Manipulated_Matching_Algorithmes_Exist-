import os
if os.getcwd() != 'C:\\Users\\user\\jupyter\\lol_match\\loaders':
    os.chdir('C:\\Users\\user\\jupyter\\lol_match\\loaders')
import pandas as pd
import load_func as fn
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

env_path = os.getcwd() + '\\.env'
s = time.time()

## 현재 내 riot api (24시간마다 갱신필요)
config = dotenv_values(env_path)
my_api = config.get("API")

request_header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": my_api
            }
url = 'https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'
requestData = requests.get(url, headers=request_header)

pd.DataFrame(requestData.json()['entries'][:10])

# ## 챌린저 [소환사명, puuid] csv파일 생성
user_list = fn.gen_challenger_userlist(my_api)
e1 = time.time()
# time.sleep(120)

## user_list에서 puuid_list 뽑기
puuid_list = []
for i in user_list[1:]:
    if i[1]:
        puuid_list.append(i[1])

## puuid_list로 matchid_list 받아오기
matchid_list = fn.recent_matchid_by_puuids(100,puuid_list,my_api)
e2 = time.time()
# time.sleep(120)

## gamedata table 만들기
challenger_gamedata = fn.gen_gamedata(matchid_list[1:1000],my_api)
