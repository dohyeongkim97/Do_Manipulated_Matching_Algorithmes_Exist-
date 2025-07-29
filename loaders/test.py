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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}

#%% 
url = f'https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}&api_key=RGAPI-cd6e17ed-172e-4ddc-aba8-b2bc88b29c04'