import csv
# import requests
# from bs4 import BeautifulSoup, SoupStrainer

import yfinance as yf
import os
import datetime
import pandas as pd
import numpy as np

# from aapl import write_csv


# Download stock data then export as CSV

# data_df = yf.download("AAPL", start="2019-12-26", end="2020-12-26")

# data_df.to_csv('aapl.csv')


# ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Week', 'Day_of_week']
path = os.path.abspath('aapl.csv')
user1 = pd.read_csv(path)
# user1.to_csv('aaplTest.csv')
# print(user1)


user1['Week'] = None
user1['Day_of_week'] = None
user1['Previous_Close'] = None
user1['Previous_Open'] = None
user1['HA_Open'] = None  # Open = Open pr. + Close pr./2
user1['HA_Close'] = None  # Close = Open + High + Low + Close/4
user1['HA_High'] = None  # HA_High = max(High, HA_Open, HA_Close)
user1['HA_Low'] = None  # min(Low, HA_Open, HA_Close)


def copyargumentWeek(buffer):
    year = buffer[0:4]
    month = buffer[5:7]
    day = buffer[8:10]
    wk = datetime.date(int(year), int(month), int(day)).isocalendar()[1]

    return wk


def copyargumentDay(buffer):
    year = buffer[0:4]
    month = buffer[5:7]
    day = buffer[8:10]
    wk = datetime.date(int(year), int(month), int(day)).isocalendar()[2]

    return wk


def HEIKIN(Open, High, Low, Close, Previous_Open, Previous_Close):
    HA_Close = (Open + High + Low + Close) / 4
    HA_Open = (Previous_Open + Previous_Close) / 2
    elements_max = np.array([High, HA_Open, HA_Close])
    elements_min = np.array([Low, HA_Open, HA_Close])
    HA_High = elements_max.max(0)
    HA_Low = elements_min.min(0)
    out = np.array([HA_Close, HA_Open, HA_High, HA_Low])

    return out


for x in range(253):
    user1['Week'][x] = copyargumentWeek(user1['Date'][x])
    user1['Day_of_week'][x] = copyargumentDay(user1['Date'][x])

    if x == 0:
        user1['Previous_Close'][x] = 0
        user1['Previous_Open'][x] = 0
    else:
        user1['Previous_Close'][x] = user1['Close'][x - 1]
        user1['Previous_Open'][x] = user1['Open'][x - 1]

    temp = HEIKIN(user1['Open'][x], user1['High'][x], user1['Low'][x], user1['Close'][x], user1['Previous_Open'][x], user1['Previous_Close'][x])

    user1['HA_Close'][x] = temp[0]
    user1['HA_Open'][x] = temp[1]
    user1['HA_High'][x] = temp[2]
    user1['HA_Low'][x] = temp[3]

user1.to_csv('aaplTest.csv')

# A = ["2020-12-28"]

# buffer = A
# print(buffer[0]

# print(dict(user1))


# for i in range(len(user1)):
#    for j in range(len(user1[i])):
#        print(user1[i][j], end=' ')
#    print()