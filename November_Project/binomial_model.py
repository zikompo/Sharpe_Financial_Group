import numpy as np
from Options import Option

class Binomial_Model:
    def __init__(self, option: Option, N: int, preset_u=None, preset_d=None):
        self.u = preset_u # up factor
        self.d = preset_d # down factor
        self.p = None # risk-neutral probability
        self.N = N # number of steps in the binomial model
        self.dt = None # length of each time step
        self.price_tree = None
        # option properties
        self.r = option.r # risk-neutral rate
        self.T = option.T # time to maturity (in years)
        self.sigma = option.sigma # volatility
        self.S0 = option.S0 # initial stock price
        self.option_type = option.option_type # option type (call or put)
        self.K = option.K



    def calculate_binomial_factors(self):
        """Calculate the up, down, and risk-neutral probability factors
        Parameters:
        T: float
            time to maturity (in years)
        N: int
            number of steps in the binomial model
        sigma: float
            volatility

        Returns:
        None
        """
        self.dt = self.T/self.N
        if self.u is None and self.d is None:
            self.u = np.exp(self.sigma*np.sqrt(self.dt))
            self.d = 1/self.u
        self.p = (np.exp(self.r*self.dt) - self.d)/(self.u - self.d)

    def build_price_tree(self):
        """Construct the binomial price tree for the underlying asset
        The price tree is a two-dimensional array where:
            - the rows represent the different states of the underlying asset's price at each time step
            - the columns represent the time steps from 0 to N
        Each node in the tree represents the price of the underlying asset at a specific state and time step
        """
        self.price_tree = np.zeros((self.N+1, self.N+1))

        for i in range(self.N+1): # iterates over time steps
            for j in range(i+1): # iterates over states within the time step
                # Calculate the stock price at each node
                self.price_tree[j, i] = self.S0*(self.u**j)*(self.d**(i-j))

    def calculate_option_price(self):
        """Calculate the option price using the binomial model
        - The option price is calculated by working backwards through the price tree
        Returns:
        float: option price
        """
        # initialize option tree with the same shape as the price tree
        self.option_tree = np.zeros_like(self.price_tree)

        # calculate option value at maturity
        for j in range(self.N + 1):
            if self.option_type == "call":
                self.option_tree[j, self.N] = max(0, self.price_tree[j, self.N] - self.K)
            elif self.option_type == "put":
                self.option_tree[j, self.N] = max(0, self.K - self.price_tree[j, self.N])

        # calculate option value at earlier time steps
        for i in range(self.N-1, -1, -1):
            for j in range(i+1):
                # calculate the value of holding the option at each node
                hold = np.exp(-self.r*self.dt)*(self.p*self.option_tree[j+1, i+1] + # Value after an up move
                        (1-self.p)*self.option_tree[j, i+1]) # Value after a down move
                # calculate the intrinsic value of the option at each node
                if self.option_type == "call":
                    early_exercise = max(0, self.price_tree[j, i] - self.K)
                elif self.option_type == "put":
                    early_exercise = max(0, self.K - self.price_tree[j, i])

                # take value of the option at each node as the maximum of holding and early exercise
                self.option_tree[j, i] = max(hold, early_exercise)

        # value of the root at time 0 is the option price
        return self.option_tree[0, 0]

    def price(self):
        """
        Main method to calculate the option price.

        This method combines all the steps:
        - Calculate binomial model factors
        - Build the price tree for the underlying asset
        - Use backward induction to calculate the option price

        Returns:
        float: The price of the option
        """
        self.calculate_binomial_factors()  # Step 1: Calculate factors
        self.build_price_tree()  # Step 2: Build price tree
        return self.calculate_option_price()  # Step 3: Calculate option price






