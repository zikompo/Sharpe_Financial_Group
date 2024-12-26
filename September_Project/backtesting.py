import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import datetime
import random
from typing import Optional

def get_all_symbols():
    df = pd.read_csv('stocks.csv')
    symbols = [symbol for symbol in df['Symbol']]
    return symbols
# Acquire Market Data
# Load historical market data into a pandas DataFrame
def load_market_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Create a ramdom portfolio
def create_random_portfolio(number, exchange): #TODO: Add functionality such that you can use different exchanges
    symbols = get_all_symbols()
    stocks = []
    if not exchange: #Defaults to US Stocks
        for i in range(number):
            stock = random.choice(symbols)
            symbols.remove(stock)
            stocks.append(stock)
    return stocks


# Allows you to get data for multiple tickers
def download_data():
    # name of the stock (key) - stock values (2010-date) as the values
    stock_data = {}
    for stock in stocks:
        ticker = yf.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date, end=end_date)['Close']
    return pd.DataFrame(stock_data)


if __name__ == '__main__':
    print(load_market_data('MSFT', "2020-01-01", "2023-01-01"))