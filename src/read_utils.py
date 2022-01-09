import csv
import matplotlib.pylab as plt

from teams import Team

def process_games(filename):
    teams = get_teams_map('../data/teams.csv')
    with open(filename) as games_file:
        games = csv.DictReader(games_file)
        for game in games:
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
    # Plot Chicago Bulls values.
    teams_seasons = process_games('../data/games.csv')
    chi_seasons = teams_seasons['1610612741']
    order_seasons = chi_seasons.get_sorted_difference_list(13.91)
    seasons, values = zip(*order_seasons)
    plt.plot(seasons, values)
    plt.show()

