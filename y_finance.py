import csv
#import requests
#from bs4 import BeautifulSoup, SoupStrainer

import yfinance as yf
import datetime
import pandas as pd

#from aapl import write_csv


# Download stock data then export as CSV

#data_df = yf.download("AAPL", start="2019-12-26", end="2020-12-26")

#data_df.to_csv('aapl.csv')



# ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Week', 'Day_of_week']
user1 = pd.read_csv('C:/Users/Rocket/PycharmProjects/Finance/aapl.csv')
#user1.to_csv('aaplTest.csv')
#print(user1)


user1['Week'] = None
user1['Day_of_week'] = None



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

for x in range(253):
    user1['Week'][x] = copyargumentWeek(user1['Date'][x])
    user1['Day_of_week'][x] = copyargumentDay(user1['Date'][x])





user1.to_csv('aaplTest.csv')



#A = ["2020-12-28"]

#buffer = A
#print(buffer[0]

#print(dict(user1))


#for i in range(len(user1)):
#    for j in range(len(user1[i])):
#        print(user1[i][j], end=' ')
#    print()