from cmath import sqrt
import read_utils
import numpy as np

from pprint import pprint
from scipy.optimize import minimize

# Compute RMSE.
def compute_score(exponent):
    teams_seasons = read_utils.process_games("../data/games.csv")
    raw_score = 0
    total_seasons = 0
    for _, team_seasons in teams_seasons.items():
        for _, team_season in team_seasons.seasons.items():
            raw_score += team_season.get_difference_squared(exponent[0])
            total_seasons += 1
    print(total_seasons)
    return sqrt(raw_score / total_seasons).real


if __name__ == "__main__":
    guesses = {}
    for guess in range(2, 30):
        result = minimize(
            compute_score,
            np.array([guess]),
            method="nelder-mead",
            options={"xatol": 1e-8, "disp": True},
        )
        guesses[guess] = result.x
    pprint(guesses)
