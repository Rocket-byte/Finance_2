import time
import cx_Oracle as ora
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from stockstats import StockDataFrame


def connectToOra():
    dsn = ora.makedsn(host='31.28.168.98', port='6541', service_name='key1uadg.key4.local')
    localConnection = ora.connect(user='XED', password='', dsn=dsn, encoding='UTF-8')
    print("Successfully connected to Oracle Database")
    return localConnection


def getTickersArray(connection):
    # Get Max RN Quantity for future List
    curRN = connection.cursor()
    for row in curRN.execute('SELECT MAX(t.Rn) AS Max_Rn FROM Vw_Ticker_Parts t'):
        partNumbers = row[0]
    print('Loaded partition - ', partNumbers)
    curRN.close()

    # Create partition list
    currentId = 1
    curTickers = connection.cursor()
    res_ticker_array = np.empty(partNumbers, dtype=object)
    for i in range(1, partNumbers + 1):
        ticker_list = []
        for row in curTickers.execute('SELECT t.Ticker AS Max_Rn FROM Vw_Ticker_Parts t where t.Rn=:RN', [i]):
            ticker_list.append(row[0])
        res_ticker_array[i - 1] = ticker_list
        print('Partition №', i, ' - ', ticker_list)
    curTickers.close
    return res_ticker_array


def prepareTickerDataFrame(tickerData, tickerName, tickerInterval):
    # StockName for first column
    # Drop zero columns
    tickerData.dropna(subset=["Open"], inplace=True)
    # Add Columns

    dataLength = len(tickerData)
    print('tickerName - ' + str(dataLength))
    tickerData['DATE_TIME'] = tickerData.index
    tickerData['TICKER'] = tickerName
    tickerData['INTERVAL'] = tickerInterval
    # TA Columns
    tickerData['PREV_OPEN'] = tickerData.Open.shift(1)
    tickerData['PREV_CLOSE'] = tickerData.Close.shift(1)
    tickerData['PREV_HIGH'] = tickerData.High.shift(1)
    tickerData['PREV_LOW'] = tickerData.Low.shift(1)
    tickerData['PREV_VOLUME'] = tickerData.Volume.shift(1)
    tickerData['INTERVAL_NUM'] = tickerData.reset_index().index + 1
    tickerData['CHANGE_OPEN_PRICE'] = tickerData['Open'] - tickerData['PREV_CLOSE']
    tickerData['CHANGE_OPEN_PERCENT'] = (tickerData['CHANGE_OPEN_PRICE'] / tickerData['Close']) * 100
    tickerData['CHANGE_PRICE'] = tickerData['Close'] - tickerData['PREV_CLOSE']
    tickerData['CHANGE_PERCENT'] = (tickerData['CHANGE_PRICE'] / tickerData['PREV_CLOSE']) * 100
    # ATR / RSI
    stocks = StockDataFrame.retype(tickerData[["Open", "Close", "High", "Low", "Volume"]])

    # Add Columns
    tickerData['RSI'] = stocks['rsi_14'].fillna(0)
    tickerData['ATR'] = stocks['atr'].fillna(0)
    # SMA and EMA and check that we have more thea 60 and 200 items
    if dataLength > 60:
        tickerData['EMA_60'] = tickerData.ta.ema(60)
        tickerData['SMA_60'] = tickerData.ta.sma(60)
    else:
        tickerData['EMA_60'] = -1
        tickerData['SMA_60'] = -1
    if dataLength > 200:
        tickerData['EMA_200'] = tickerData.ta.ema(200)
        tickerData['SMA_200'] = tickerData.ta.sma(200)
        tickerData["TI_EMA_GC"] = (tickerData["EMA_60"] > tickerData["EMA_200"]).astype(int)
        tickerData["TI_SMA_GC"] = (tickerData["SMA_60"] > tickerData["SMA_200"]).astype(int)
    else:
        tickerData['EMA_200'] = -1
        tickerData['SMA_200'] = -1
        tickerData["TI_EMA_GC"] = -1
        tickerData["TI_SMA_GC"] = -1
    # Is Last Attr
    tickerData['IS_LAST'] = 0
    tickerData.at[tickerData.index[-1], 'IS_LAST'] = 1
    tickerData = tickerData.round(2)
    # Replace Nan
    tickerData = tickerData.replace(np.nan, 0)
    return tickerData


def deleteTickerFromDataBase(connection, ticker, interval):
    # Delete data for Stock+Interval
    curDelete = connection.cursor()
    curDelete.execute('DELETE FROM Candles t WHERE t.Ticker = :ticker AND t.Interval = :interval', [ticker, interval])
    curDelete.close
    connection.commit()



def writeTickerToDataBase(connection, dataFrame):
    curWrite = connection.cursor()
    # dataFrame.dropna(subset=["Open"], inplace=True)
    stocks_to_db = dataFrame[
        ['TICKER', 'INTERVAL', 'INTERVAL_NUM', 'DATE_TIME', 'IS_LAST',
         'CHANGE_OPEN_PRICE', 'CHANGE_OPEN_PERCENT', 'CHANGE_PRICE', 'CHANGE_PERCENT',
         'open', 'high', 'low', 'close', 'volume',
         'PREV_OPEN', 'PREV_CLOSE', 'PREV_HIGH', 'PREV_LOW', 'PREV_VOLUME',
         'ATR', 'RSI',
         'EMA_60', 'EMA_200', 'TI_EMA_GC',
         'SMA_60', 'SMA_200', 'TI_SMA_GC']].reset_index().rename(columns={'index': 'DT'}).round(2)
    #print(stocks_to_db)
    for col in stocks_to_db.columns:
        if col == "DT":
            stocks_to_db.pop('DT')
        if col == 'date':
            stocks_to_db.pop('date')
        if col == 'datetime':
            stocks_to_db.pop('datetime')
    data = list(stocks_to_db.itertuples(index=False, name=None))
    query_add_stocks = """INSERT INTO Candles
                                               (Ticker,
                                                INTERVAL,
                                                Interval_Num,
                                                Interval_Date_Time,
                                                Is_Last,
                                                Change_Open_Price,
                                                Change_Open_Percent,
                                                Change_Price,
                                                Change_Percent,
                                                OPEN,
                                                High,
                                                Low,
                                                CLOSE,
                                                Volume,
                                                Prev_Open,
                                                Prev_High,
                                                Prev_Low,
                                                Prev_Close,
                                                Prev_Volume,
                                                Ti_Atr,
                                                Ti_Rsi,
                                                Ti_Ema_60,
                                                Ti_Ema_200,
                                                Ti_Ema_Gc,
                                                Ti_Sma_60,
                                                Ti_Sma_200,
                                                Ti_Sma_Gc)
                                            VALUES
                                                (:Ticker,
                                                :INTERVAL,
                                                :Interval_Num,
                                                :Interval_Date_Time,
                                                :Is_Last,
                                                :Change_Open_Price,
                                                :Change_Open_Percent,
                                                :Change_Price,
                                                :Change_Percent,
                                                :OPEN,
                                                :High,
                                                :Low,
                                                :CLOSE,
                                                :Volume,
                                                :Prev_Open,
                                                :Prev_High,
                                                :Prev_Low,
                                                :Prev_Close,
                                                :Prev_Volume,
                                                :Ti_Atr,
                                                :Ti_Rsi,
                                                :Ti_Ema_60,
                                                :Ti_Ema_200,
                                                :Ti_Ema_Gc,
                                                :Ti_Sma_60,
                                                :Ti_Sma_200,
                                                :Ti_Sma_Gc)"""
    # inserting the stock rows
    curWrite.executemany(query_add_stocks, data)
    curWrite.close
    connection.commit()


def getTickersData(connection, tickers_list, tickers_period, tickers_interval):
    all_data = yf.download(tickers_list,
                           period=tickers_period,
                           interval=tickers_interval,
                           group_by='ticker',
                           auto_adjust=False,
                           prepost=False,
                           threads=True,
                           proxy=None)
    all_data = all_data.T
    for ticker in tickers_list:
        df = all_data.loc[(ticker,),].T
        df = prepareTickerDataFrame(df, ticker, tickers_interval)
        deleteTickerFromDataBase(connection, ticker, tickers_interval)
        writeTickerToDataBase(connection, df)


def doAllTickers(connection, ticker_array):
    i = 0
    maxlength = len(ticker_array)
    for ticker_list in ticker_array:
        i = i + 1
        #print('Work on ', i, '/', maxlength, ' partition. Start ', '5m', ' timeframe')
        #getTickersData(connection, ticker_list, '30d', '5m')

        #print('Work on ', i, '/', maxlength, ' partition. Start ', '30m', ' timeframe')
        #getTickersData(connection, ticker_list, '30d', '30m')

        #print('Work on ', i, '/', maxlength, ' partition. Start ', '1h', ' timeframe')
        #getTickersData(connection, ticker_list, '90d', '1h')



        print('Work on ', i, '/', maxlength, ' partition. Start ', '1wk', ' timeframe')
        getTickersData(connection, ticker_list, '5y', '1wk')

        print('Work on ', i, '/', maxlength, ' partition. Start ', '1mo', ' timeframe')
        getTickersData(connection, ticker_list, '5y', '1mo')


if __name__ == '__main__':
    startWork = time.time()
    oraConnection = connectToOra()
    all_ticker_array = getTickersArray(oraConnection)
    doAllTickers(oraConnection, all_ticker_array)
    oraConnection.close()
    print('It took', time.time() - startWork, 'seconds.')
