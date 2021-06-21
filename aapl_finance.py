# getStockData(stockName,dateBegin,dateEnd)
# return Pandas [stockName,Date,Open,High,Low,Close,Adj Close,Volume]
# stockApple = getStockData("AAPL",date.today()-365,date.today())

# yf.download(".....",period = "max", interval = "1d")

import yfinance as yf
import os
from datetime import date
import pandas as pd
import numpy as np
from array import *

def getStockData(stockName, dateBegin, dateEnd):
#   data_df = yf.download("AAPL", start="2020-01-11", end="2021-01-11")
    data_df = yf.download(stockName, start=dateBegin, end=dateEnd)
    data_df.to_csv(str(stockName) + '.csv')
    path = os.path.abspath(str(stockName) + '.csv')
    df = pd.read_csv(path)
#   df['stockName'] = None
    Name = []

   # Name =  [stockName]
    Date = df['Date']
    Open = df['Open']
    High = df['High']
    Low = df['Low']
    Close = df['Close']
    Volume = df['Volume']
 #  Adj_Close = df['Adj_Close']
#    for x in range(len(df['Date'])):
#          Name[x] = str(stockName)

    out = np.array([Name, Date, Open, High, Low, Close, Volume])

    return out

#stockApple = getStockData("AAPL", date.today()-365, date.today())
stockApple = getStockData("AAPL", date.today().replace(year=date.today().year-1), date.today())
print(stockApple[0:])

