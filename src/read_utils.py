import csv

from collections import defaultdict
from pprint import pprint
from teams import Team

def process_games(filename):
    teams = get_teams_map('teams.csv')
    with open(filename) as games_file:
        games = csv.DictReader(games_file)
        for game in games:
            
            if game['PTS_home'] == '' or game['PTS_away'] == '':
                print(game['GAME_ID'])

            teams[game['HOME_TEAM_ID']].add_game(game)
            teams[game['VISITOR_TEAM_ID']].add_game(game)
    return teams

def get_teams_map(filename):
    teams_map = {}
    with open(filename) as teams_file:
        teams = csv.DictReader(teams_file)
        for team in teams:
            teams_map[team['TEAM_ID']] = Team(team['TEAM_ID'], team['ABBREVIATION'])
    return teams_map

if __name__ == '__main__':
    teams_seasons = process_games('games.csv')