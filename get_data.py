import yfinance as yf
import os
import pandas as pd


def getTicker():
    path_tickers_name = os.path.abspath('ticker.csv')
    stockName = pd.read_csv(path_tickers_name)

    return stockName


def getStockData(stockName):
    df = yf.download(stockName, period="max", interval="1d")
    # StockName for first column
    df.insert(0, 'StockName', len(df))
    df['StockName'] = stockName

    return df


def concatenate_df():
    tickers = getTicker()

    for ticker in range(0, len(tickers)):
        print(tickers['tickers'][ticker])
        df_Current = getStockData(tickers['tickers'][ticker])

        if ticker == 0:
            print('Done')
            df_Final = df_Current
        else:
            df_Buffer = df_Current
            df_Final = pd.concat([df_Final, df_Buffer])
            df_Final.to_csv('Final.csv')


if __name__ == '__main__':
    concatenate_df()
