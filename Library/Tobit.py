import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.base.model import GenericLikelihoodModel
import matplotlib.pyplot as plt
import scipy

class TobitModel(GenericLikelihoodModel):
    def __init__(self, endog, exog, left_censor=0, right_censor=np.inf, **kwargs):
        super().__init__(endog, exog, **kwargs)
        self.left_censor = left_censor
        self.right_censor = right_censor

    def nloglikeobs(self, params):
        beta = params[:-1]  # Regression coefficients
        sigma = params[-1]  # Standard deviation, must be positive

        if sigma <= 0:
            return np.inf  # Return infinity for invalid sigma

        xb = np.dot(self.exog, beta)
        z = (self.endog - xb) / sigma

        # Likelihood components for censored and uncensored observations
        uncensored = -0.5 * np.log(2 * np.pi) - np.log(sigma) - 0.5 * z ** 2
        left_censored = np.log(1 - self._norm_cdf((self.left_censor - xb) / sigma))
        right_censored = np.log(self._norm_cdf((self.right_censor - xb) / sigma))

        # Combine likelihoods based on censoring
        loglik = np.where(self.endog <= self.left_censor, left_censored,
                          np.where(self.endog >= self.right_censor, right_censored, uncensored))

        return -np.sum(loglik)  # Negative log-likelihood

    def fit(self, start_params=None, **kwargs):
        if start_params is None:
            start_params = np.append(np.zeros(self.exog.shape[1]), 1.0)
        return super().fit(start_params=start_params, **kwargs)

    def predict(self, params):
        beta = params[:-1]
        return np.dot(self.exog, beta)

    @staticmethod
    def _norm_cdf(z):
        return 0.5 * (1 + scipy.special.erf(z / np.sqrt(2)))


class TobitRegression:
    def __init__(self, dataframe, predictor, dependent, left_censor=0, right_censor=np.inf):
        self.dataframe = dataframe
        self.predictor = [predictor] if isinstance(predictor, str) else predictor
        self.dependent = dependent
        self.left_censor = left_censor
        self.right_censor = right_censor
        self.model = None
        self.results = None

    def fit(self):
        endog = self.dataframe[self.dependent].values
        exog = sm.add_constant(self.dataframe[self.predictor].values)
        self.model = TobitModel(endog, exog, self.left_censor, self.right_censor)
        self.results = self.model.fit()
        return self.results

    def summary(self):
        if self.results is None:
            raise ValueError("The model must be fitted before accessing the summary.")
        return self.results.summary()

    def get_residuals(self):
        if self.results is None:
            raise ValueError("The model must be fitted before calculating residuals.")
        predicted = self.model.predict(self.results.params)
        residuals = self.dataframe[self.dependent].values - predicted
        return residuals

    def plot_fitted_line(self, ax=None, color='red', label='Fitted Line'):
        """
        Plot the fitted line on an existing graph.

        Parameters:
        - ax: Matplotlib axis object. If None, creates a new figure.
        - color: Line color (default: 'red').
        - label: Line label for the legend (default: 'Fitted Line').
        """
        if self.results is None:
            raise ValueError("The model must be fitted before plotting.")

        if ax is None:
            _, ax = plt.subplots()

        # Sort data for a smooth line
        sorted_data = self.dataframe.sort_values(by=self.predictor)
        exog_sorted = sm.add_constant(sorted_data[self.predictor].values)
        predicted = self.model.predict(self.results.params)

        # Plot the fitted line
        ax.plot(sorted_data[self.predictor], predicted, color=color, label=label)
        ax.legend()
        ax.set_xlabel(self.predictor[0])
        ax.set_ylabel(self.dependent)
        return ax


# Example Usage
if __name__ == "__main__":
    # Generate example data
    np.random.seed(42)
    n = 200
    X = np.random.normal(size=n)
    Y = 2 + 3 * X + np.random.normal(size=n)
    Y = np.clip(Y, a_min=0, a_max=5)  # Censor at 0 and 5

    df = pd.DataFrame({'X': X, 'Y': Y})

    # Fit Tobit model
    tobit = TobitRegression(dataframe=df, predictor='X', dependent='Y', left_censor=0, right_censor=5)
    results = tobit.fit()
    print(tobit.summary())

    # Plot data and fitted line
    fig, ax = plt.subplots()
    ax.scatter(df['X'], df['Y'], alpha=0.6, label='Data')
    tobit.plot_fitted_line(ax=ax, color='blue', label='Tobit Fitted Line')
    plt.legend()
    plt.show()
