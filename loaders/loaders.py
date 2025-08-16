#%%
import load_function 
from load_function import RiotAPIClient
import os
from dotenv import  dotenv_values
import pandas as pd
import requests
import random
import time
import pandas as pd
# %%
env_path = os.getcwd()+"\\.env"
config = dotenv_values(env_path)
my_api = config.get("API")

#%%
my_api
#%%
# Create Riot API client
client = RiotAPIClient(my_api)


#%%
# Example usage
tiers = ["GOLD", "PLATINUM", 'EMERALD', "DIAMOND", "MASTER", "GRANDMASTER"]
divisions = ['IV', "III", "II", "I"]

for tier in tiers:
    temp_df = pd.DataFrame()
    for division in divisions:
        df = client.get_summoners_by_division(tier, division)
        temp_df = pd.concat([temp_df, df], axis=0)
    temp_df.to_csv(f"{tier}.csv", index=False)
# %%
pd.read_csv("MASTER.csv")

#%%

# %%
matches = client.get_matchlist(pd.read_csv("MASTER.csv").loc[0, 'puuid'])
#%%

#%%

user = [pd.read_csv("MASTER.csv").loc[0, 'puuid']]*100
pd.DataFrame([user, matches], index = ['user', 'matches']).T
#%%
random.random()
#%%

# %%
for i in os.listdir():
    df_matches = pd.DataFrame()
    user_puuid = []
    if i.endswith('.csv'):
        if ("EMERALD" in i):
            user_df = pd.read_csv(f"./{i}")
            for user in range(len(user_df)):
            # for user in range(5):
                matches = client.get_matchlist(user_df.loc[user, 'puuid'])
                user_puuid = [user_df.loc[user, 'puuid']]*len(matches)
                temp_df = pd.DataFrame([user_puuid, matches], index=['user', 'matches']).T

                df_matches = pd.concat([df_matches, temp_df])

                if random.random() > 0.8:
                    time.sleep(3)

                print(f'{i}: {user}')

            df_matches.to_csv(f"{i[:-4]}_matches2.csv")
# diamond 737까지 완료. HTTPSConnectionPool Max retries exceeded with url. Timeout error.

# %%
df_matches.to_csv("diamond_matches_1.csv")

#%%
df_matches
#%% 
match_detail = client.get_match_detail(pd.read_csv("./EMERALD_matches.csv").loc[190, 'matches'])
# %%
match_detail['info']['participants'][0].keys()
# %%
match_detail['info']['participants']

match_detail['info']['participants'][1]

# participants riotIdGameName riotIdTagline 
# enemyMissingPings 
# enemyVisionPings
# gameDuration, by milisecond
# puuid
# lane
# teamPosition
# win
# kills / assists / deaths / kda
# challenges-gameLength

# lane = what I wanted
# teamPosition = what I did

# if(info.gameMode=='CLASSIC')
#%%
# for i in 

gamelength = []
puuid = []
lane = []
position = []
kills = []
deaths = []
assists = []
kda = []
ping_missing = []
ping_vision = []
wins = []
ping_assist=[]
ping_hold = []
game_id = []
vision_score = []

match_detail['info']['participants'][0]['challenges']['gameLength']

#%%
match_detail['metadata']['participants']

#%%
len(match_detail['info']['participants'])

#%%
if match_detail['info']['gameMode'] == 'CLASSIC':
    for i in range(len(match_detail['info']['participants'])):
        
        gamelength.append(match_detail['info']['participants'][i]['challenges']['gameLength'])
        puuid.append(match_detail['info']['participants'][i]['puuid'])
        lane.append(match_detail['info']['participants'][i]['lane'])
        position.append(match_detail['info']['participants'][i]['teamPosition'])
        kills.append(match_detail['info']['participants'][i]['kills'])
        deaths.append(match_detail['info']['participants'][i]['deaths'])
        assists.append(match_detail['info']['participants'][i]['assists'])
        ping_missing.append(match_detail['info']['participants'][i]['enemyMissingPings'])
        ping_assist.append(match_detail['info']['participants'][i]['assistMePings'])
        ping_vision.append(match_detail['info']['participants'][i]['enemyVisionPings'])
        ping_hold.append(match_detail['info']['participants'][i]['holdPings'])
        vision_score.append(match_detail['info']['participants'][i]['visionScore'])
        wins.append(match_detail['info']['participants'][i]['win'])

# %%
pd.DataFrame([gamelength, puuid, lane, position, kills, deaths, assists, ping_missing, ping_assist, ping_vision, ping_hold, vision_score, wins],
             index = ['gamelength', 'puuid', 'lane', 'position', 'kills', 'deaths', 'assits', 'ping_missing', 'ping_assists', 'ping_vision', 'ping_hold', 'vision_score', 'wins']).T
# %%

for file in os.listdir():
    if file.endswith('matches.csv'):
        df_matches = pd.read_csv(file)

        # for match_num in range(len(df_matches)):
        for match_num in range(3):
            match = df_matches.loc[match_num, 'matches']
            target_user = df_matches.loc[match_num, 'user']
#%%
target_user


#%%
gamelength = []
puuid = []
lane = []
position = []
kills = []
deaths = []
assists = []
kda = []
ping_missing = []
ping_vision = []
wins = []
ping_assist=[]
ping_hold = []
game_id = []
vision_score = []

df_matches
#%%
sample_list = []

#%%
sample_list.append('a')
sample_list

#%%

df_matches
# %%
for file in os.listdir():
    if file.endswith('matches.csv'):
        print(file)
        df_matches = pd.read_csv(file)
        
        user_list = []
        gamelength = []
        puuid = []
        lane = []
        position = []
        kills = []
        deaths = []
        assists = []
        kda = []
        ping_missing = []
        ping_vision = []
        wins = []
        ping_assist=[]
        ping_hold = []
        game_id = []
        gamename = []
        gametag = []
        vision_score = []

        for match_num in range(len(df_matches)):
        # for match_num in range(3):
            match_target = df_matches.loc[match_num, 'matches']
            target_user = df_matches.loc[match_num, 'user']

            match_detail = client.get_match_detail(df_matches.loc[match_num, 'matches'])

            if not match_detail:
                print(f'match_num: {match_num}')

            if match_detail['info']['gameMode'] == 'CLASSIC':
                # for i in range(10):
                    # user_list.append([target_user]*10)
                for i in range(len(match_detail['info']['participants'])):
                    user_list.append(target_user)
                    gamelength.append(match_detail['info']['participants'][i]['challenges']['gameLength'])
                    puuid.append(match_detail['info']['participants'][i]['puuid'])
                    lane.append(match_detail['info']['participants'][i]['lane'])
                    position.append(match_detail['info']['participants'][i]['teamPosition'])
                    kills.append(match_detail['info']['participants'][i]['kills'])
                    deaths.append(match_detail['info']['participants'][i]['deaths'])
                    assists.append(match_detail['info']['participants'][i]['assists'])
                    ping_missing.append(match_detail['info']['participants'][i]['enemyMissingPings'])
                    ping_assist.append(match_detail['info']['participants'][i]['assistMePings'])
                    ping_vision.append(match_detail['info']['participants'][i]['enemyVisionPings'])
                    ping_hold.append(match_detail['info']['participants'][i]['holdPings'])
                    vision_score.append(match_detail['info']['participants'][i]['visionScore'])
                    gamename.append(match_detail['info']['participants'][i]['riotIdGameName'])
                    gametag.append(match_detail['info']['participants'][i]['riotIdTagline'])
                    wins.append(match_detail['info']['participants'][i]['win'])

                    print(f"match_num: {match_num}")


        df_temp = pd.DataFrame([user_list, gamelength, puuid, 
                                lane, position, kills, deaths, 
                                assists, ping_missing, ping_assist, 
                                ping_vision, ping_hold, vision_score, gamename, gametag, wins],
                                index = ['target_user', 'gamelength', 'puuid', 'lane', 'position', 'kills',
                                         'deaths', 'assists', 'ping_missing', 'ping_assists', 'ping_vision', 
                                         'ping_hold', 'vision_score', 'name', 'tag', 'wins']).T
        
        df_temp.to_csv(f"{file[:-4]}_detail.csv")

#%%
df_matches

#%%
match_detail['info']['participants'][0]['riotIdGameName']
# %%
pd.read_csv('EMERALD_matches.csv')