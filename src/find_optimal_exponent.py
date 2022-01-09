import read_utils
import numpy as np

from scipy.optimize import minimize

def compute_score(exponent):
    teams_seasons = read_utils.process_games('../data/games.csv')
    score = 0
    for _, team_seasons in teams_seasons.items():
        for _, team_season in team_seasons.seasons.items():
            score += team_season.get_abs_difference(exponent[0])
    return score

if __name__ == '__main__':
    result = minimize(compute_score,
                      np.array([20]),
                      method='nelder-mead',
                      options={'xatol': 1e-8, 'disp': True})
    print(result.x)