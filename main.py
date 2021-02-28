import requests  # for "get" request to API
import pandas as pd  # working with data frames
import datetime as dt  # working with dates
import json
import time
import os

def get_binance_bars(symbol, interval, startTime, endTime):
    url = "https://api.binance.com/api/v3/klines"

    startTime = str(int(startTime.timestamp() * 1000))
    endTime = str(int(endTime.timestamp() * 1000))
    limit = '1000'

    req_params = {"symbol": symbol, 'interval': interval, 'startTime': startTime, 'endTime': endTime, 'limit': limit}

    df = pd.DataFrame(json.loads(requests.get(url, params=req_params).text))

    if (len(df.index) == 0):
        return None

    df = df.iloc[:, 0:6]
    df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']

    df.open = df.open.astype("float")
    df.high = df.high.astype("float")
    df.low = df.low.astype("float")
    df.close = df.close.astype("float")
    df.volume = df.volume.astype("float")

    # df['adj_close'] = df['close']

    df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.datetime]

    return df


# Dosyaya girer ve son timestampe bakar
# Şuan ki timestampe göre aradaki dtayı dosyaya yazar sonra while'a girer
def get_missing_data_since_last_open():
    while True:
        with open('binance_BTCUSDT_1m.txt', 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()
            text = float(last_line.split(',', 1)[0])
            last_date = dt.datetime.fromtimestamp(text)
            print("Last time program was used on " + str(last_date))
            last = last_date
            now = dt.datetime.now()
        if last.month == now.month and last.day == now.day and last.hour == now.hour and last.minute == now.minute - 1:
            break
        else:
            print("Getting the data between " + str(last) + " and " + str(now))
            odata = get_binance_bars('BTCUSDT', '1m',
                                     dt.datetime(last.year, last.month, last.day, last.hour, last.minute + 1),
                                     dt.datetime(now.year, now.month, now.day, now.hour, now.minute - 1))
            for column in odata[['datetime']]:
                odata[column] = odata[column] / 1000
            if odata is not None:
                odata.to_csv(r'binance_BTCUSDT_1m.txt', header=None, index=None, sep=',', mode='a')


get_missing_data_since_last_open()
starttime = time.time()
while True:
    now = dt.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    fd = get_binance_bars('BTCUSDT', '1m', dt.datetime(year, month, day, hour, minute),
                          dt.datetime(year, month, day, hour, minute))
    fd[['datetime']] = fd[['datetime']] / 1000
    print("Getting the data from " + str(now))
    fd.to_csv(r'binance_BTCUSDT_1m.txt', header=None, index=None, sep=',', mode='a')
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
