import statsmodels.api as sm
import numpy as np
from matplotlib import pyplot as plt

def regression(data, column, alpha):
    x = data['days'].values
    y = data[column].values
    x_with_const = sm.add_constant(x)
    # Fit the linear regression model
    model = sm.OLS(y, x_with_const)
    results = model.fit()
    # Extract slope and intercept
    slope = results.params[1]
    intercept = results.params[0]
    residuals = results.resid
    predictions = results.get_prediction(x_with_const).summary_frame(alpha)
    # Create a dictionary with the results
    results_dict = {
        'x': x,
        'y': y,
        'slope': slope,
        'intercept': intercept,
        'r_squared': results.rsquared,
        'p_value': results.pvalues[1],
        'standard_error': results.bse[1],
        'residuals': residuals,
        'model': model,
        'results': results,
        'predictions': predictions,
        'df': x_with_const
    }

    return results_dict


def plot_line(results, color):
    x = results['x']
    linestyle = '--'
    # Plot the regression line
    x_values = np.linspace(min(x), max(x), 100)
    y_values = results['slope'] * x_values + results['intercept']
    plt.plot(x_values, y_values, color=color, linestyle=linestyle)
    predictions = results['predictions']
    df = results['df']
    plt.fill_between(df[:,1], predictions['obs_ci_lower'], predictions['obs_ci_upper'], alpha=.1, color=color)

def predict(results, day):
    slope = results['slope']
    intercept = results['intercept']
    y_pred = slope * day + intercept
    return y_pred
