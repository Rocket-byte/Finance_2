import yfinance as yf
import plotly.graph_objects as go
import os
import pandas as pd


def getTicker():
    path_tickers_name = os.path.abspath('ticker.csv')
    stockName = pd.read_csv(path_tickers_name)

    return stockName


def getStockData(stockName):
    df = yf.download(stockName, period="1mo", interval="1d")
    # StockName for first column
    df.insert(0, 'StockName', len(df))
    df['StockName'] = stockName
    df['DATE_TIME'] = df.index
    print(df)

    fig = go.Figure(data=[go.Candlestick(x=df['DATE_TIME'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])
                          ])

    fig.add_shape(type="line",
                  x0='2021-05-19', y0=127, x1='2021-06-18', y1=127,
                  line=dict(
                      color="LightSeaGreen",
                      width=4,
                      dash="dashdot"
                  )
                 )

    fig.update_layout(title='The Great Recession', yaxis_title=f'{stockName}', xaxis_rangeslider_visible=False)
    fig.show()

    return df


def concatenate_df():
    tickers = getTicker()

    for ticker in range(0, 1):  #len(tickers)
        nameTicker = tickers['tickers'][ticker]
        print(nameTicker)
        df_Current = getStockData('AAPL')

        if ticker == 0:
            print('Done')
            df_Final = df_Current
        else:
            df_Buffer = df_Current
            df_Final = pd.concat([df_Final, df_Buffer])
            df_Final.to_csv('Final.csv')

            print(df_Final)


if __name__ == '__main__':
    concatenate_df()
