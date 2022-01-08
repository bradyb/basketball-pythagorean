class TeamSeason:
    def __init__(self, season):
        self.season = season
        self.wins = 0
        self.total_games = 0
        self.points_for = 0
        self.points_against = 0

    def get_winning_percentage(self):
        return self.wins / self.total_games

    def get_expected_percentage(self, exponent):
        points_for_exponent = self.points_for ** exponent
        return points_for_exponent / (points_for_exponent + self.points_against ** exponent)

    def get_actual_expected_difference(self, exponent):
        return self.get_winning_percentage - self.get_expected_percentage(exponent)

class Team:
    def __init__(self, id, abbrev):
        self.id = id
        self.abbrev = abbrev
        self.seasons = {}

    def add_game(self, game_dict):
        season_str = game_dict['SEASON']
        if season_str not in self.seasons:
            self.seasons[season_str] = TeamSeason(season_str)

        team_season = self.seasons[season_str]
        team_season.total_games += 1

        home_points = convert_points(game_dict['PTS_home'])
        away_points = convert_points(game_dict['PTS_away'])
        home_win = home_points > away_points

        if self.id == game_dict['HOME_TEAM_ID']:
            team_season.points_for += home_points
            team_season.points_against += away_points
            team_season.wins += 1 if home_win else 0
        else:
            team_season.points_for += away_points
            team_season.points_against += home_points
            team_season.wins += 1 if not home_win else 0
    
def convert_points(points_str):
    if points_str.endswith('.0'):
        return int(float(points_str))
    else:
        return int(points_str)