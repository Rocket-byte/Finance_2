# getStockData(stockName,dateBegin,dateEnd)
# return Pandas [stockName,Date,Open,High,Low,Close,Adj Close,Volume]
# stockApple = getStockData("AAPL",date.today()-365,date.today())

# yf.download(".....",period = "max", interval = "1d")

import yfinance as yf
import os
import pandas as pd
import numpy as np

def getStockData(stockName):

    data_df = yf.download(stockName, period = "max", interval = "1d")
    data_df.to_csv(str(stockName) + '.csv')
    path = os.path.abspath(str(stockName) + '.csv')
    df = pd.read_csv(path)
    df.insert(0, 'StockName', len(df))

    df['StockName'] = stockName
    Name =  df['StockName']
    Date = df['Date']
    Open = df['Open']
    High = df['High']
    Low = df['Low']
    Close = df['Close']
    Volume = df['Volume']

    df.to_csv(str(stockName) + '.csv')

    out = np.array([Name, Date, Open, High, Low, Close, Volume])

    return path, df


def getTicker():
    stockName = pd.read_csv('ticker.csv')
    return stockName

#stockApple = getStockData("AAPL", date.today()-365, date.today())
#stockApple = getStockData("AAPL", date.today().replace(year=date.today().year-1), date.today())
#stockApple = getStockData("AAPL")
#print(stockApple[0:])
path = []
tickers = []
tickers = getTicker()





for ticker in range(0, len(tickers)):
    print(tickers['tickers'][ticker])
    path, df_Current = getStockData(tickers['tickers'][ticker])

    if ticker == 0:
        print('Done')
        df_Final = None
    else:
        df_Buffer = pd.read_csv(path)
        df_Final = pd.concat([df_Final, df_Buffer])
        df_Final.to_csv('Final.csv')



print(getTicker())