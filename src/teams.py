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
        return points_for_exponent / (
            points_for_exponent + self.points_against ** exponent
        )

    def get_actual_expected_difference(self, exponent):
        return self.get_winning_percentage() - self.get_expected_percentage(exponent)

    def get_abs_difference(self, exponent):
        return abs(
            self.get_winning_percentage() - self.get_expected_percentage(exponent)
        )


class Team:
    def __init__(self, id, abbrev):
        self.id = id
        self.abbrev = abbrev
        self.seasons = {}

    def get_sorted_difference_list(self, exponent):
        diff_dict = {
            int(season): team_season.get_actual_expected_difference(exponent)
            for season, team_season in self.seasons.items()
        }
        return sorted(diff_dict.items())

    def add_game(self, game_dict):
        season_str = game_dict["SEASON"]
        if season_str not in self.seasons:
            self.seasons[season_str] = TeamSeason(season_str)

        team_season = self.seasons[season_str]
        team_season.total_games += 1

        home_points = convert_points(game_dict["PTS_home"])
        away_points = convert_points(game_dict["PTS_away"])
        home_win = home_points > away_points

        if self.id == game_dict["HOME_TEAM_ID"]:
            team_season.points_for += home_points
            team_season.points_against += away_points
            team_season.wins += 1 if home_win else 0
        else:
            team_season.points_for += away_points
            team_season.points_against += home_points
            team_season.wins += 1 if not home_win else 0

    def add_538_game(self, game_dict):
        if game_dict["score1"] == "":
            return

        season_str = game_dict["season"]
        if season_str not in self.seasons:
            self.seasons[season_str] = TeamSeason(season_str)

        team_season = self.seasons[season_str]
        team_season.total_games += 1

        team1points = convert_points(game_dict["score1"])
        team2points = convert_points(game_dict["score2"])
        team1win = team1points > team2points

        if self.abbrev == game_dict["team1"]:
            team_season.points_for += team1points
            team_season.points_against += team2points
            team_season.wins += 1 if team1win else 0
        else:
            team_season.points_for += team2points
            team_season.points_against += team1points
            team_season.wins += 1 if not team1win else 0


def convert_points(points_str):
    if points_str.endswith(".0"):
        return int(float(points_str))
    else:
        return int(points_str)
