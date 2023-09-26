import pandas as pd
import requests

league_id = '60261358'
espn_cookies = {
    "swid": "{98A29BD7-C472-40E5-83BA-2EB349C3A05B}",
    "espn_s2": "AECTWdVGMsw89WGvGIbpbiOENUKF19pHZtKfBL3%2FkuZosKP6m83MNawQr1T1Sf5zs2oZSsftX4AvRGfBCoUGAMoiHILGHXnT%2BU%2F6cVruVIXczFie09hVdClV9ZzwYl4nMFo2Gs9GmhGlFZeuOKEdjbzHBIMKaB4Hgmr2862TBDLCAh5JkFI2Xjeo17Qa9cLVFBvTtbZ9HZgfeRP0HqAZ73ijZB%2Buvw1fczKdHeM1hdyHQOhB8MyNsiebrn105j1yn3qHw0gUwJ2DpVFD2Olp8rbVmC5Ny6EN64sI2KWSbXYLy8Sc%2FnrbqlM1p2K5c1qbnOU%3D"
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
    team_mapping = {
        7: 'North Maryland Fat Nuts',
        1: 'Daniel Jones',
        11: 'no scam plz',
        12: 'Juju Videos',
        5: 'DooDoo Sh1t Poopster',
        2: 'North Arlington Chaps',
        6: 'Saigon Noodles n Grill',
        4: 'Northfield Nutjobs',
        10: 'GO! BIRDS!',
        3: 'Antonio\'s Cajones',
        14: 'Team Christiansen',
        13: 'Kang Gang'
    }
    
    merged_df['teamId'] = merged_df['teamId'].replace(team_mapping)
    merged_df['defaultPositionId'] = merged_df['defaultPositionId'].replace(position_mapping)
    
    return merged_df[['overallPickNumber', 'fullName', 'defaultPositionId', 'team name', 'teamId']].sort_values(by='overallPickNumber')

def get2022():
    data_path = "\\Users\\leofa\\Documents\\VSCode\\2022rank.csv"
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


twentydf = make_final_df("2022")
season_rankings_df = get2022()

comparison_df = compare_draft_vs_season_end_by_position(twentydf, season_rankings_df)

# Display settings and print dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', None)

print(comparison_df)

# Display settings and print dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', None)



