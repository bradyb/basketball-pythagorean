import csv

from copy import deepcopy
from teams import Team


def process_games(filename):
    teams = get_teams_map("../data/teams.csv")
    with open(filename) as games_file:
        games = csv.DictReader(games_file)
        for game in games:
            teams[game["HOME_TEAM_ID"]].add_game(game)
            teams[game["VISITOR_TEAM_ID"]].add_game(game)
    return teams


def get_teams_map(filename):
    return get_teams_map_by_key(filename, "TEAM_ID")


def get_teams_map_by_abbrev(filename):
    return get_teams_map_by_key(filename, "ABBREVIATION")


def get_teams_map_by_key(filename, key_str):
    assert key_str == "TEAM_ID" or key_str == "ABBREVIATION"
    teams_map = {}
    with open(filename) as teams_file:
        teams = csv.DictReader(teams_file)
        for team in teams:
            teams_map[team[key_str]] = Team(team["TEAM_ID"], team["ABBREVIATION"])
    return teams_map


def fix_538_names(teams):
    teams["PHO"] = deepcopy(teams["PHX"])
    del teams["PHX"]
    teams["CHO"] = deepcopy(teams["CHA"])
    del teams["CHA"]
    teams["BRK"] = deepcopy(teams["BKN"])
    del teams["BKN"]
    return teams


def process_538_csv(filename):
    teams = fix_538_names(get_teams_map_by_abbrev("../data/teams.csv"))
    with open(filename) as games_file:
        games = csv.DictReader(games_file)
        for game in games:
            teams[game["team1"]].add_538_game(game)
            teams[game["team2"]].add_538_game(game)
    return teams


if __name__ == "__main__":
    process_538_csv("../data/nba_elo_latest.csv")
