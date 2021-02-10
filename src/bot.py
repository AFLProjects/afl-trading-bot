# External libraries
import matplotlib.pyplot as plt

# Project Files
from api.connect import *
from api.order import *
from api.tracking import *
from dft.dft import *
from dft.denoise import *
from analysis.analyse import *
import utils.stdout2 as std2

# System libraries
from datetime import date, timedelta
import time, csv, os, sys
import urllib.request


# Setup user-agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# Market data
fecthMarkets = True
markets = []
index = 1

# Fecth trending markets
print('Fectching trending markets...')
while fecthMarkets:
    time.sleep(1)
    try:
        url = f'https://finviz.com/screener.ashx?v=210&s=ta_p_tlsupport&r={index}'
        print(f'[\'url\' : \'{url}\']')
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
            index += 12
    except:
        print('No more markets')
        break
print(f"Found {len(markets)} markets with an uptrend.")
print(markets)

# History data
marketHistory = {}
dataPoints = 0
size = 0

# Fetch Market History
print('Fectching market history...')
for i, symbol in enumerate(markets):
    std2.write_progress_bar(i+1, len(markets), 40)
    endDate = date.today().strftime("%Y-%m-%d")
    startDate = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    with std2.suppress_stdout():
        marketHistory[symbol] = getStockPriceHistory(symbol, '1m', startDate, endDate)
    dataPoints += len(marketHistory[symbol])
    size += sys.getsizeof(marketHistory[symbol])
print(f'[{size} bytes] Downloaded {dataPoints} data points from {len(markets)} uptrending markets')

# Pause
while True:
    time.sleep(0.1)