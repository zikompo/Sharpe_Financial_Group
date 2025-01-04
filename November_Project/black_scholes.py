import numpy as np
from Options import Option
from scipy.stats import norm

class Black_Scholes_Model:
    def __init__(self, option: Option):
        self.S0 = option.S0
        self.K = option.K
        self.r = option.r
        self.T = option.T
        self.sigma = option.sigma
        self.option_type = option.option_type

    def d1(self):
        """
        Calculate d1 for the Black-Scholes formula.

        Returns the value of d1.
        """
        S0, K, r, T, sigma = self.S0, self.K, self.r, self.T, self.sigma
        return (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    def d2(self):
        """
        Calculate d2 for the Black-Scholes formula.

        Returns the value of d2.
        """
        return self.d1() - self.sigma * np.sqrt(self.T)
    
    def calculate_price(self):
        """
        Calculate the price of the options using the Black-Scholes formula.

        Returns the option price
        """
        d1, d2 = self.d1(), self.d2()
        S0, K, r, T, option_type = self.S0, self.K, self.r, self.T, self.option_type

        if option_type.lower() == 'call':
            return round(S0 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2), 2)
        elif option_type.lower() == 'put':
            return round(K * np.exp(-r*T) * norm.cdf(-d2) - S0 * norm.cdf(-d1), 2)
        else:
            raise ValueError("Option type must be 'call' or 'put'.")
    