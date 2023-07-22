import plotly.graph_objects as go
import plotly.io as pio

from scipy.signal import find_peaks
from datetime import datetime

import pandas as pd
import yfinance as yf

from datetime import timedelta

from CandleIdentify import *


def analyseLastMonth():
    # This function reads in all the data from stocks in stockslist and evaluates the functions under runScript()
    allStocks = {}
    print('lol')
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)
    # for i in range(0,len(stockList)-1):
    for i in range(0,len(stockList)-450):
        stock = stockList[i]
        print('Processing stock', i,': ', stock)
        allStocks[stock] = runScript(stock, start_date, end_date)
    print('lol')
    return allStocks


def runScript(stock, start_date, end_date):
    # download and format stock data and evaluate candleSizes(), candleIdentifier(), and loop3()
    try:
        df = yf.download(stock, start=start_date, end=end_date)
        print("Data downloaded")
           
        df[['body', 'topTail', 'bottomTail']] = df.apply(
            lambda x: pd.Series(candleSizes(x)), axis=1)
        df['Candle_Type'] = df.apply(
            lambda x: candleIdentifier(candleSizes(x)), axis=1)
        df['star'] = loop3(df)
    except:
        df = 0
        print("Data for stock '", stock, "' could not be found")
    
    return df

def init():
    global stock
    global start_date
    global end_date
    stock = 'MSFT'
    start_date = datetime(2000, 1, 1)
    end_date = datetime.today()

if __name__ == '__main__':
    print('imported file')
# init()
# df = runScript(stock, start_date, end_date)
# # truePositives, trueNegatives, falsePositives, falseNegatives, diff = backtestStar(df)
# allStocks = analyseLastMonth()


# Structure for each stock:
# 1) Download data, identify candles.
# 2) Loop over all possible indicators/patterns:
#   3) Find positions (dates) at which an indicator/pattern occurs. Def findPattern(stock)                                          - df['pattern1'] = findPattern1(stock)
#   4) Determine price at time of pattern occurrence and x days later (e.g. 1, 5, 10, 30 days). Def priceDifference(stock, days)    - df['diffPattern1'] = priceDifference(stock, days)
#   5) Add up the price differences per pattern and number of days (x).                                                             - sumPattern1 = sum(df['diffPatern1'])
#   6) Count the number of times the pattern resulted in a positive move and a negative move                                        - Pattern1Up, Pattern1Down = count(df['diffPattern1'] > 0), count(df['diffPattern1'] < 0)
#   7) Create bar chart showing how often each gain or loss occurred (10 buckets?)                                                  - Barchart(df['diffPattern1'], Nbuckets = 10)