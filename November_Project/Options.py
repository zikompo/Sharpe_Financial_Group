import numpy as np

class Option:
    def __init__(self, S0, K, r, T, sigma, option_type):
        self.S0 = S0 # initial stock price
        self.K = K # strike price
        self.r = r # risk-free rate
        self.T = T # time to maturity (in years)
        self.sigma = sigma # volatility
        self.option_type = option_type # option type (call or put)

    