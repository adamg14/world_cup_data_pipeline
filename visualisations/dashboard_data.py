import pandas as pd

def get_stadium_data():
    stadiums = pd.read_csv("../data/stadiums.csv")
    return stadiums


def get_group_stats():
    group_stats = pd.read_csv("../data/group_stats.csv")
    return group_stats


def get_team_data():
    team_data = pd.read_csv("../data/team_data.csv")
    return team_data


def get_player_data():
    player_data = pd.read_csv("../data/players_list.csv")
    return player_data


def get_goalscorers():
    goalscorers = pd.read_csv("../data/goalscorers.csv")
    return goalscorers