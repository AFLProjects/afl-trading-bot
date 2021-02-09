# Libraries to download
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Project Files
from api.connect import *
from api.order import *
from api.tracking import *
from dft.dft import *
from dft.denoise import *
from analysis.analyse import *

# System libraries
import urllib.request
from datetime import date, timedelta
import time
import csv
import os
import sys

index = 1
markets = []
print('Fectching trending markets...')
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
while True:
    time.sleep(.5)
    try:
        url = f'https://finviz.com/screener.ashx?v=210&s=ta_p_tlsupport&r={index}'
        print(f'[\'url\' : \'{url}\']')
        fecthMarkets = True
        with urllib.request.urlopen(url) as f:
            html = f.read().decode('utf-8')
            parse = (html.split('<!-- TS')[1]).split('TE -->')[0]
            for i, value in enumerate(parse.splitlines()):
                ticker = value.split('|')[0]
                if ticker in markets:
                    fecthMarkets = False
                    break
                elif ticker:
                    markets.append(ticker)
            if not fecthMarkets:
                break
            index += 12
    except:
        print('No more markets')
        break
print(f"Found {len(markets)} markets with an uptrend.")
print(markets)

print('Fectching market history...')
marketHistory = {}
dataPoints = 0
size = 0
for i, symbol in enumerate(markets):
    endDate = date.today().strftime("%Y-%m-%d")
    startDate = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    marketHistory[symbol] = getStockPriceHistory(symbol, '1m', startDate, endDate)
    dataPoints += len(marketHistory[symbol])
    print(f'[{sys.getsizeof(marketHistory[symbol])} bytes] [{symbol}] Found {len(marketHistory[symbol])} data points from {startDate} to {endDate} at an internval of 1m')
    size += sys.getsizeof(marketHistory[symbol])
print(f'[{size} bytes] Downloaded {dataPoints} data points from 100 uptrending markets')

while True:
    time.sleep(0.1)
