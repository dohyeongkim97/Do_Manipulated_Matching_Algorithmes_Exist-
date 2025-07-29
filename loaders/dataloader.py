from functions import (
    get_random_summoners,
    get_summoner_name_by_puuid,
    get_recent_match_ids,
    get_match_detail,
    extract_match_summary

)
import pandas as pd


def get_sample_match_data(tier='SILVER', division='I', user_count=3, match_count=2):
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

    return result


if __name__ == "__main__":
    tiers_divisions = [
        ('PLATINUM', 'IV'), ('PLATINUM', 'III'), ('PLATINUM', 'II'), ('PLATINUM', 'I'),
        ('EMERALD', 'IV'),   ('EMERALD', 'III'),   ('EMERALD', 'II'),   ('EMERALD', 'I'),
        ('DIAMOND', 'IV'),  ('DIAMOND', 'III'),  ('DIAMOND', 'II'),  ('DIAMOND', 'I'),
    ]

    all_results = []

    for tier, division in tiers_divisions:
        print(f">>> Collecting {tier} {division}...")
        result = get_sample_match_data(tier=tier, division=division, user_count=3, match_count=2)
        all_results.extend(result)

    df = pd.DataFrame(all_results)
    df.to_json("match_summary.json", orient='records', force_ascii=False, indent=2)
    print("match_summary.json saved")