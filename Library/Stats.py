
from matplotlib import pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import numpy as np
import statsmodels.api as sm




def regression(data, column, alpha):
    x = data['days'].values
    y = data[column].values
    x_with_const = sm.add_constant(x)
    # Fit the linear regression model
    model = sm.OLS(y, x_with_const, missing='drop')
    results = model.fit()
    # Extract slope and intercept
    slope = results.params[1]
    intercept = results.params[0]
    residuals = results.resid
    predictions = results.get_prediction(x_with_const).summary_frame(alpha)
    prstd, iv_l, iv_u = wls_prediction_std(results)
    prstd = np.mean(prstd) #take the mean of the prstd
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
        'df': x_with_const,
        'prstd': prstd
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
