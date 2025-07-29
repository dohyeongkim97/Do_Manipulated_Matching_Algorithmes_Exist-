import load_func as fn
import time
from dotenv import dotenv_values
from pathlib import Path
import os

# .env 파일 경로 설정 (현재 작업 디렉토리에 있다고 가정)
# 실제 프로젝트 구조에 따라 경로를 조정해야 할 수 있습니다.
env_path = Path(os.getcwd()) / '.env' 

s = time.time()

## 현재 내 riot api (24시간마다 갱신필요)
# .env 파일에서 API 키 로드
config = dotenv_values(env_path)
my_api = config.get("API") # .env 파일에 API_KEY=YOUR_API_KEY 로 저장되어야 합니다.

if not my_api:
    print("Error: RIOT API_KEY not found in .env file. Please set 'API_KEY=YOUR_API_KEY'.")
    exit()

# ## 챌린저 [소환사명, puuid] csv파일 생성 또는 로드
user_list = fn.gen_challenger_userlist(my_api)
e1 = time.time()

## user_list에서 puuid_list 뽑기 (첫 번째 행은 헤더이므로 스킵)
puuid_list = [row[1] for row in user_list[1:] if len(row) > 1 and row[1]] # PUUID가 존재하는 경우만 포함

if not puuid_list:
    print("No PUUIDs found to process. Exiting.")
    exit()

## puuid_list로 matchid_list 받아오기 (최근 100경기)
matchid_list = fn.recent_matchid_by_puuids(100, puuid_list, my_api)
e2 = time.time()

## gamedata table 만들기 (matchid_list의 첫 번째 행은 헤더이므로 스킵)
# 여기서는 예시로 상위 1000개의 매치 ID만 처리하도록 했습니다. 모든 매치 ID를 처리하려면 matchid_list[1:]를 사용하세요.
challenger_gamedata = fn.gen_gamedata(matchid_list[1:1000], my_api) 

e = time.time()

# 시간 측정 결과 출력 (Rate Limit 대기 시간 제외)
print(f'Get challenger PUUID time taken: {(e1-s)//60}m {(e1-s)%60//1}s')
print(f'Get match IDs by PUUID time taken: {(e2-e1)//60}m {(e2-e1)%60//1}s')
print(f'Get game data by match ID time taken: {(e-e2)//60}m {(e-e2)%60//1}s')
print(f'Total time taken: {(e-s)//60}m {(e-s)%60//1}s')