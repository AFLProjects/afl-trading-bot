# External libraries
import matplotlib.pyplot as plt

# Project Files
from api.connect import *
from api.order import *
from api.tracking import *
from dft.dft import *
from dft.denoise import *
from strategy.analysis import *
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
std2.write_line('Fectching trending markets...')
size = 0
while fecthMarkets:
    try:
        url = f'https://finviz.com/screener.ashx?v=210&s=ta_p_tlsupport&r={index}'
        with urllib.request.urlopen(url) as f:
            html = f.read().decode('utf-8')
            std2.pause_progress_bar(1)
            std2.write_line(f'[{sys.getsizeof(html)} bytes] Downloaded market data from {url}')
            parse = (html.split('<!-- TS')[1]).split('TE -->')[0]
            for i, value in enumerate(parse.splitlines()):
                ticker = value.split('|')[0]
                if ticker in markets:
                    fecthMarkets = False
                    break
                elif ticker:
                    markets.append(ticker)
            size += sys.getsizeof(html)
            index += 12
    except:
        print('No more markets')
        break
std2.write_line(f'[{size} bytes] Found {len(markets)} markets with an uptrend.')

# History data
marketHistory = {}
dataPoints = 0
size = 0

# Fetch Market History
std2.write_line('Fectching market history...')
for i, symbol in enumerate(markets):
    std2.write_progress_bar(i+1, len(markets), 40)
    endDate = date.today().strftime("%Y-%m-%d")
    startDate = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
    with std2.suppress_stdout():
        marketHistory[symbol] = getStockPriceHistory(symbol, '1d', startDate, endDate)
    dataPoints += len(marketHistory[symbol])
    size += sys.getsizeof(marketHistory[symbol])
std2.write_line(f'[{size} bytes] Downloaded {dataPoints} data points from {len(markets)} uptrending markets')

# Fetch previously used markets
std2.write_line('Fectching previously used markets...')
try:
    with open('logs.txt') as f:
        content = f.readlines()
        logCount = int(content[0])
        if logCount > 0:
            for i in range(1, logCount + 1):
                std2.write_progress_bar(i, logCount, 40)
                market = content[i].split('|')[0]
                if not market in markets:
                    markets.append(market)
            std2.write_line(f'Found {logCount} previously used markets')
        else:
            std2.write_line('Found 0 previously used markets')
except IOError:
    f = open("logs.txt", "x")
    f.write("0")
    f.close()
std2.write_line(f'Found a total of {len(markets)} markets to analyse within the next hour !')

# Exit
pause = input('Press a key to exit.')
