import requests
from pathlib import Path
import time
import datetime
import csv
import os

# 데이터 저장 경로 설정
data_path = Path(__file__).parent / 'data/'
data_path.mkdir(exist_ok=True) # data 디렉토리가 없으면 생성

## CSV 파일을 리스트로 반환
def csv2list(filename):
    """
    지정된 filename을 포함하는 CSV 파일을 찾아 리스트로 반환합니다.
    """
    for f_name in os.listdir(data_path):
        if filename in f_name:
            full_filename = data_path / f_name
            break
    else:
        print(f"Error: File containing '{filename}' not found in {data_path}")
        return []

    l = []
    with open(full_filename, 'r', encoding='utf-8-sig') as f:
        r = csv.reader(f)
        for row in r:
            l.append(row)
    return l

## 리스트를 CSV 파일로 저장
def list2csv(_list, filename):
    """
    리스트를 지정된 filename으로 CSV 파일에 저장합니다.
    """
    full_path = data_path / (filename + '.csv')
    with open(full_path, 'w', encoding='utf-8-sig', newline='') as f:
        write = csv.writer(f)
        write.writerows(_list)
    print(f"Data saved to {full_path}")
    return filename + '.csv'

## 챌린저 유저의 소환사명, PUUID가 포함된 CSV 파일을 생성 또는 로드
def gen_challenger_userlist(my_api):
    """
    챌린저 리그 유저 목록 (소환사명, PUUID)을 가져오거나 기존 파일을 로드합니다.
    Riot API 업데이트로 인해 summonerId를 사용하여 PUUID를 조회하는 방식으로 변경되었습니다.
    """
    # 기존 파일이 있는지 확인
    for f_name in os.listdir(data_path):
        if '_userlist_' in f_name:
            print(f"Message (gen_challenger_userlist): Loading user list from '{data_path / f_name}'")
            return csv2list(f_name)

    print("Message (gen_challenger_userlist): Requesting to Riot API for challenger list.")
    request_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": my_api
    }

    # 챌린저 리그 정보 요청
    challenger_url = 'https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'
    response = requests.get(challenger_url, headers=request_header)
    response.raise_for_status() # HTTP 오류가 발생하면 예외를 발생시킵니다.
    challenger_data = response.json()

    league_info = [challenger_data['tier'], challenger_data['leagueId'], challenger_data['queue']]
    user_entries = challenger_data['entries']

    name_puuid_list = [['summonerName', 'puuid']] # 헤더 추가

    # 소환사 ID를 통해 PUUID 조회
    cnt = 0
    start_time = time.time()
    for entry in user_entries:
        summoner_name = entry['summonerName']
        encrypted_summoner_id = entry['summonerId']

        if cnt % 100 == 0 and cnt != 0:
            end_time = time.time()
            sleep_time = 120 - (end_time - start_time)
            if sleep_time > 0:
                print(f"Message (gen_challenger_userlist): Sleeping {round(sleep_time, 2)}s due to rate limit.")
                time.sleep(sleep_time)
            start_time = time.time()

        # summonerId로 summoner 정보를 조회하여 puuid 가져오기
        summoner_detail_url = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/{encrypted_summoner_id}'
        summoner_response = requests.get(summoner_detail_url, headers=request_header)
        cnt += 1

        puuid = None
        if summoner_response.status_code == 200:
            puuid = summoner_response.json().get('puuid')
        else:
            print(f"Warning: Could not get PUUID for {summoner_name} (Status Code: {summoner_response.status_code}, Response: {summoner_response.text})")

        name_puuid_list.append([summoner_name, puuid])
        time.sleep(0.05) # 초당 20 요청 제한 준수

    # 파일명에 현재 날짜 포함
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    file_name = f"{league_info[0]}_userlist_{date_str}"
    list2csv(name_puuid_list, file_name)
    return name_puuid_list

## PUUID 목록에서 최근 N개 매치 ID 목록을 반환
def recent_matchid_by_puuids(count, puuid_list, my_api):
    """
    제공된 PUUID 목록에서 각 PUUID의 최근 'count'개 매치 ID를 가져오거나 기존 파일을 로드합니다.
    """
    for f_name in os.listdir(data_path):
        if 'MatchId_' in f_name:
            print(f"Message (recent_matchid_by_puuids): Loading match ID list from '{data_path / f_name}'")
            return csv2list(f_name)

    print("Message (recent_matchid_by_puuids): Requesting to Riot API for recent match IDs.")
    request_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,es;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": my_api
    }

    matchid_list = [['matchid']]
    processed_matchids = set() # 중복 매치 ID 방지를 위해 set 사용

    cnt = 0
    start_time = time.time()
    for puuid in puuid_list:
        if puuid is None: # PUUID가 없는 경우 스킵
            continue

        if cnt % 100 == 0 and cnt != 0:
            end_time = time.time()
            sleep_time = 120 - (end_time - start_time)
            if sleep_time > 0:
                print(f"Message (recent_matchid_by_puuids): Sleeping {round(sleep_time, 2)}s due to rate limit.")
                time.sleep(sleep_time)
            start_time = time.time()

        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
        response = requests.get(url, headers=request_header)
        cnt += 1

        if response.status_code == 200:
            matchids = response.json()
            for matchid in matchids:
                if matchid not in processed_matchids:
                    matchid_list.append([matchid])
                    processed_matchids.add(matchid)
        else:
            print(f"Warning: Could not get match IDs for PUUID {puuid} (Status Code: {response.status_code}, Response: {response.text})")

        time.sleep(0.05) # 초당 20 요청 제한 준수

    date_str = datetime.datetime.now().strftime('%Y%m%d')
    list2csv(matchid_list, 'MatchId_' + date_str)
    return matchid_list

## 매치 ID에서 게임 데이터를 가져와 CSV 파일로 저장
def gen_gamedata(matchid_list, my_api):
    """
    매치 ID 목록에서 게임 데이터를 가져오거나 기존 파일을 로드합니다.
    """
    for f_name in os.listdir(data_path):
        if 'gamedata_' in f_name:
            print(f"Message (gen_gamedata): Loading game data from '{data_path / f_name}'")
            return csv2list(f_name)

    print("Message (gen_gamedata): Requesting to Riot API for game data.")
    request_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": my_api
    }

    gamedata = []
    data_header = [] # 데이터 헤더를 저장할 리스트

    cnt = 0
    start_time = time.time()
    for match_entry in matchid_list:
        matchid = match_entry[0] # matchid_list는 [['matchid']] 형태이므로 첫 번째 요소를 가져옴

        if cnt % 100 == 0 and cnt != 0:
            end_time = time.time()
            sleep_time = 120 - (end_time - start_time)
            if sleep_time > 0:
                print(f"Message (gen_gamedata): Sleeping {round(sleep_time, 2)}s due to rate limit.")
                time.sleep(sleep_time)
            start_time = time.time()

        url = f'https://asia.api.riotgames.com/lol/match/v5/matches/{matchid}'
        response = requests.get(url, headers=request_header)
        cnt += 1

        if response.status_code == 200:
            match_info = response.json().get('info')
            if match_info:
                participants = match_info.get('participants')
                if participants:
                    for participant_info in participants:
                        if not data_header: # 헤더가 아직 설정되지 않았다면 첫 번째 참가자 정보에서 헤더를 추출
                            # 핵심 피처 정의
                            primary_keys = ['summonerName', 'championName', 'win', 'kills', 'deaths', 'assists', 'totalDamageDealtToChampions']
                            
                            # participant_info의 직접적인 키 추가
                            participant_keys = [k for k in participant_info.keys() if k not in primary_keys and k != 'challenges']
                            data_header = primary_keys + sorted(participant_keys) # 정렬하여 일관된 순서 유지

                            # 'challenges' 데이터가 있다면 그 키들을 헤더에 추가
                            if 'challenges' in participant_info and participant_info['challenges'] is not None:
                                challenge_keys = sorted(participant_info['challenges'].keys())
                                data_header.extend(challenge_keys)
                            
                            gamedata.append(data_header)

                        # 실제 데이터 추출
                        user_data_row = []
                        for key in data_header:
                            if key in participant_info:
                                user_data_row.append(participant_info.get(key))
                            elif 'challenges' in participant_info and participant_info['challenges'] is not None and key in participant_info['challenges']:
                                user_data_row.append(participant_info['challenges'].get(key))
                            else:
                                user_data_row.append(None) # 해당 키가 없으면 None으로 채움
                        gamedata.append(user_data_row)
            else:
                print(f"Warning: No 'info' found for match ID {matchid}")
        else:
            print(f"Warning: Could not get game data for match ID {matchid} (Status Code: {response.status_code}, Response: {response.text})")

        time.sleep(0.05) # 초당 20 요청 제한 준수

    date_str = datetime.datetime.now().strftime('%Y%m%d')
    list2csv(gamedata, 'gamedata_' + date_str)
    return gamedata