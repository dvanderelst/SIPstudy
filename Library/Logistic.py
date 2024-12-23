import numpy as np


def coef2odds(beta):
    # Change in odds
    change_in_odds = np.exp(beta)
    msg1 = f"Change in Odds: {change_in_odds}"
    # Percentage change in odds
    percentage_change_in_odds = (change_in_odds - 1) * 100
    msg2 = f"Percentage Change in Odds: {percentage_change_in_odds:.2f}%"
    results = {}
    results['change_in_odds'] = change_in_odds
    results['percentage_change_in_odds'] = percentage_change_in_odds
    results['msg1'] = msg1
    results['msg2'] = msg2
    return results
