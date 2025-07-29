#%%
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
import random

#%%
env_path = os.getcwd() + '\\.env'
s = time.time()

## 현재 내 riot api (24시간마다 갱신필요)
config = dotenv_values(env_path)
my_api = config.get("API")
headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": my_api
            }


def get_random_summoners(tier='SILVER', division='I', count=5, queue='RANKED_SOLO_5x5'):
    url = f'https://kr.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}?page=1'
    res = requests.get(url, headers=headers)
    time.sleep(0.85)
    players = res.json()
    return random.sample(players, min(count, len(players)))


def get_summoner_name_by_puuid(puuid):
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    res = requests.get(url, headers=headers)
    time.sleep(0.85)
    if res.status_code == 200:
        return res.json().get("name")
    return None


def get_recent_match_ids(puuid, count=5):
    url = f'https://kr.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}'
    res = requests.get(url, headers=headers)
    time.sleep(0.85)
    return res.json() if res.status_code == 200 else []


def get_match_detail(match_id):
    url = f'https://kr.api.riotgames.com/lol/match/v5/matches/{match_id}'
    res = requests.get(url, headers=headers)
    time.sleep(0.85)
    return res.json() if res.status_code == 200 else None


def extract_match_summary(match_data, target_puuid):
    participants = match_data.get('info', {}).get('participants', [])
    
    player = next((p for p in participants if p['puuid'] == target_puuid), None)
    if not player:
        return None

    team_id = player['teamId']
    win = player['win']
    summoner_name = player.get('summonerName') or "(unknown)"

    def safe_name(p):
        return p.get('summonerName') or "(unknown)"

    team_members = [safe_name(p) for p in participants if p['teamId'] == team_id]
    enemy_members = [safe_name(p) for p in participants if p['teamId'] != team_id]

    return {
        'player_name': summoner_name,
        'win': win,
        'team_members': team_members,
        'enemy_members': enemy_members
    }