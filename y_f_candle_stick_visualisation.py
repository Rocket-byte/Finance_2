import yfinance as yf
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
import pandas as pd
import psutil
import orca


def getTicker():
    path_tickers_name = os.path.abspath('ticker.csv')
    stockName = pd.read_csv(path_tickers_name)

    return stockName


def getStockData(stockName):
    df = yf.download(stockName, period="1mo", interval="1d")
    df1 = yf.download(stockName, period="1mo", interval="30m")
    # StockName for first column
    df.insert(0, 'StockName', len(df))
    df['StockName'] = stockName
    df['DATE_TIME'] = df.index

    df1.insert(0, 'StockName', len(df1))
    df1['StockName'] = stockName
    df1['DATE_TIME'] = df1.index

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


    fig2 = make_subplots(rows=2, cols=1)


    fig2.add_trace(go.Candlestick(x=df['DATE_TIME'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close']), row=1, col=1)

    fig2.add_shape(type="line",
                    x0='2021-05-19', y0=127, x1='2021-06-18', y1=127,
                    line=dict(
                                color="LightSeaGreen",
                                width=4,
                                dash="dashdot"
                             )
                  )

    fig2.add_shape(type="line",
                   x0='2021-05-19', y0=127, x1='2021-06-18', y1=127,
                   line=dict(
                       color="LightSeaGreen",
                       width=4,
                       dash="dashdot"
                   ),
                   row=2,
                   col=1
                   )


    fig2.add_trace(go.Candlestick(x=df1['DATE_TIME'],
                                         open=df1['Open'], high=df1['High'],
                                         low=df1['Low'], close=df1['Close'])
                   , row=2, col=1)


    fig2.update_layout(title='The Great Recession', yaxis_title=f'{stockName}', yaxis2_title=f'{stockName}', xaxis_rangeslider_visible=False, xaxis2_rangeslider_visible=False, showlegend=False)
    fig2.show()
    #fig2.write_image(r"d:\fig1.png")
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