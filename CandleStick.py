# import plotly.graph_objects as go
# import pandas as pd
#
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
#
# fig = go.Figure(data=[go.Candlestick(x=df['Date'],
#                 open=df['AAPL.Open'], high=df['AAPL.High'],
#                 low=df['AAPL.Low'], close=df['AAPL.Close'])
#                      ])
#
# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()


import plotly.graph_objects as go
import pandas as pd
import yfinance as yf


# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
df = yf.download('AAPL', period="1mo", interval="1d")

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['AAPL.Open'], high=df['AAPL.High'],
                low=df['AAPL.Low'], close=df['AAPL.Close'])
                      ])

fig.update_layout(
    title='The Great Recession',
    yaxis_title='AAPL Stock',
    shapes = [dict(
        x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
        line_width=2)],
    annotations=[dict(
        x='2016-12-09', y=0.05, xref='x', yref='paper',
        showarrow=False, xanchor='left', text='Increase Period Begins')]
)

fig.show()