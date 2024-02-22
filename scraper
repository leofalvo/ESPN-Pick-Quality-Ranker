import pandas as pd
import requests

TEAMNAMES = 0
league_id = '#YOUR ID'
espn_cookies = {
    "swid": "{#YOUR SWID}",
    "espn_s2": "#YOUR Espn_S2"
}

def get_draft(season_id):
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season_id}/segments/0/leagues/{league_id}?view=mDraftDetail&view=mSettings&view=mTeam&view=modular&view=mNav"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    r = requests.get(url, headers=headers, cookies=espn_cookies)
    draft_picks = r.json()["draftDetail"]["picks"]
    return pd.DataFrame(draft_picks)[['overallPickNumber', 'playerId', 'teamId']]

def get_players(season_id):
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season_id}/players?scoringPeriodId=0&view=players_wl"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'x-fantasy-filter': '{"filterActive":null}',
        'x-fantasy-platform': 'kona-PROD-1dc40132dc2070ef47881dc95b633e62cebc9913',
        'x-fantasy-source': 'kona'
    }
    player_data = requests.get(url, cookies=espn_cookies, headers=headers).json()
    players_df = pd.DataFrame(player_data)
    return players_df[['defaultPositionId', 'fullName', 'id', 'proTeamId']].rename(columns={'id': 'player_id'})

def get_teams(season_id):
    url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{season_id}?view=proTeamSchedules_wl"
    team_data = requests.get(url, cookies=espn_cookies).json()
    team_names = team_data['settings']['proTeams']
    team_df = pd.DataFrame(team_names)[['id', 'location', 'name']]
    team_df['team name'] = team_df['location'] + " " + team_df["name"]
    return team_df.rename(columns={'id': 'team_ID'})

def make_final_df(season_id):
    draft_df = get_draft(season_id)
    player_df = get_players(season_id)
    team_df = get_teams(season_id)
    
    merged_df = draft_df.merge(player_df, left_on="playerId", right_on="player_id").merge(team_df, left_on="proTeamId", right_on="team_ID")
    
    position_mapping = {
        1: 'QB',
        2: 'RB',
        3: 'WR',
        4: 'TE',
        5: 'K',
        16: 'DST'
    }

# Team names can be added here.
    team_mapping2020 = {
        
    }

    team_mapping2021 = {
       
    }

    team_mapping2022 = {
    
    }

    team_mapping_general = {
        
    }
    if TEAMNAMES == 1:
        merged_df['teamId'] = merged_df['teamId'].replace(locals()[f'team_mapping{season_id}'])
    else:
        merged_df['teamId'] = merged_df['teamId'].replace(team_mapping_general)
    merged_df['defaultPositionId'] = merged_df['defaultPositionId'].replace(position_mapping)
    
    return merged_df[['overallPickNumber', 'fullName', 'defaultPositionId', 'team name', 'teamId']].sort_values(by='overallPickNumber')

def get_ranking(season_id):
    import os
    data_path = os.path.join("C:\\", "Users", "leofa", "Documents", "VSCode", "ESPN", f"{season_id}rank.csv")
    season_rankings_df = pd.read_csv(data_path)
    return season_rankings_df

def compare_draft_vs_season_end_by_position(draft_df, season_rankings_df):
    # Calculate positional draft rank
    draft_df['DraftPosRank'] = draft_df.groupby('defaultPositionId').cumcount() + 1

    # Merge the draft rankings with the end-of-season rankings based on the player's name and position
    combined_df = draft_df.merge(season_rankings_df, left_on=['fullName', 'defaultPositionId'], right_on=['Player', 'FantPos'], how='inner')

    # Calculate the rank difference
    combined_df['RankDifference'] = combined_df['DraftPosRank'] - combined_df['PosRank']

    # Return the combined DataFrame containing draft position rank, end-of-season position rank, and their difference
    return combined_df.sort_values(by='RankDifference')

def make_comparison(season_id):
    twentydf = make_final_df(season_id)
    season_rankings_df = get_ranking(season_id)
    comparison_df = compare_draft_vs_season_end_by_position(twentydf, season_rankings_df)
    return comparison_df

def merge_finals(final0, final1):
    merge_df = pd.concat([final0, final1], ignore_index=True)
    merge_df = merge_df.sort_values(by='RankDifference',ascending=False)
    merge_df.drop('Player', axis=1,inplace=True)
    merge_df.drop('FantPos', axis=1,inplace=True)
    return merge_df


def espn(years):
    #takes a list of years
    final_df = make_comparison(years[0])
    years = years[1:]
    for year in years:
        final_df = merge_finals(make_comparison(year),final_df)
    return final_df

def export_as_csv(filename):
    to_export = espn([2020,2021,2022])
    to_export.to_csv((filename + '.csv'))

# Display settings and print dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', None)

export_as_csv("draft_data2")





