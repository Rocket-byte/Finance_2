import yfinance as yf
import os
import pandas as pd
from datetime import datetime
import time
import plotly.graph_objects as go
import plotly.offline as offline



#1 - Parameter
#2 - TryCatch
#3 -
#4 - Log
def getTicker(fileName):
    path_tickers_name = os.path.abspath(fileName)
    stockName = pd.read_csv(path_tickers_name)

    return stockName

#1 - Comments
def getStockData(stockName):
    df = yf.download(stockName, period="1mo", interval="1d")
    # StockName for first column
    df.insert(0, 'StockName', len(df))
    df.insert(0, 'Num', len(df))
    df['StockName'] = stockName
    print(df)

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['AAPL.Open'],
                                         high=df['AAPL.High'],
                                         low=df['AAPL.Low'],
                                         close=df['AAPL.Close'])])

    fig.show()

    return df


def getAllStocks(fileName):
    tickers = getTicker(fileName)
    for ticker in range(0, len(tickers)):
        #print(tickers['tickers'][ticker])
        df_Current = getStockData(tickers['tickers'][ticker])
        if ticker == 0:
             #print('Done')
             print(df_Current)
             df_Final = df_Current
        else:
             exit(0)
             df_Final = pd.concat([df_Final, df_Current])

    df_Final.to_csv('Final.csv')



if __name__ == '__main__':
    start_time = time.time()
    getAllStocks('ticker.csv')
    print("--- %s seconds ---" % (time.time() - start_time))
#
# 14/01/2021 09:39:14
# 14/01/2021 09:41:28
# 134
#
# 14/01/2021 09:42:01
# 14/01/2021 09:42:41
# 40
#
# 14/01/2021 09:43:14
# 14/01/2021 09:43:59
# 45
#
#
# 14/01/2021 09:46:59
# 14/01/2021 09:47:39
# 40
#

# import plotly.graph_objects as go
# import pandas as pd
#
# df = pd.read_csv('C:\Users\Rocket\PycharmProjects\Finance\Final.csv')
#
# fig = go.Figure(data=[go.Candlestick(x=df['Date'],
#                 open=df['AAPL.Open'], high=df['AAPL.High'],
#                 low=df['AAPL.Low'], close=df['AAPL.Close'])
#                      ])
#
# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()