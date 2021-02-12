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
import signal, multiprocessing

# Setup user-agent
try:
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
except:
    std2.write_line('[Exception] Installing Opener failed => Downloading data migth not work')

# Market data
fecthMarkets = True
markets = []
index = 1

# Fecth trending markets from Finviz
std2.write_line('Finding trending markets from finviz...')
size = 0
while fecthMarkets:
    try:
        url = f'https://finviz.com/screener.ashx?v=210&s=ta_p_tlsupport&r={index}'
        with urllib.request.urlopen(url) as f:
            html = f.read().decode('utf-8')
            std2.pause_progress_bar(1)
            std2.write_line(f'[{sys.getsizeof(html)} bytes] {url}')
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
std2.write_line('\nFinding trending markets from yahoo...')
url = f'https://finance.yahoo.com/trending-tickers/'
with urllib.request.urlopen(url) as f:
    htmlParse = f.read().decode('utf-8')
    std2.pause_progress_bar(1)
    while 'data-symbol=\"' in htmlParse:
        htmlParse = htmlParse.split('data-symbol=\"', 1)[1]
        market = htmlParse.split('\"', 1)[0]
        if not market in markets:
            markets.append(market)
std2.write_line(f'\n[{size} bytes] Found {len(markets)} markets with an uptrend.\n')

# History data
marketHistory = {}
dataPoints = 0
size = 0

# Fetch Market History
std2.write_line('Fectching market history...')
errorMsgBuffer = ''
for i, symbol in enumerate(markets):
    std2.write_progress_bar(i+1, len(markets), 40)
    endDate = date.today().strftime("%Y-%m-%d")
    startDate = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
    with std2.suppress_stdout():
        try:
            marketHistory[symbol] = getStockPriceHistory(symbol, '1d', startDate, endDate)
            dataPoints += len(marketHistory[symbol])
            size += sys.getsizeof(marketHistory[symbol])
        except:
            errorMsgBuffer += f'[Exception] Couldn\'t download data for {symbol} !\n'
std2.write_line(f'{errorMsgBuffer}[{size} bytes] Downloaded {dataPoints} data points from {len(markets)} uptrending markets\n')

# Fetch previously used markets
std2.write_line('Finding previously used markets...')
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
            std2.write_line(f'\nFound {logCount} previously used markets')
        else:
            std2.write_line('\nFound 0 previously used markets')
except IOError:
    f = open("logs.txt", "x")
    f.write("0")
    f.close()
std2.write_line(f'Found a total of {len(markets)} markets to analyse within the next hour !')

# Searching for trades
def print_trade(symbol, price, action):
    time_str = time.strftime("%H:%M:%S", time.gmtime(time.time()))
    std2.write_autocomplete(time_str, 14)
    std2.write_autocomplete(symbol, 14)
    std2.write_autocomplete(price, 14)
    std2.write_autocomplete(action, 14)
    std2.write('\n')
std2.write_line('\nTime          Symbol        Price         Action')
std2.write_line('------------  ------------  ------------  ------------')

# Analyze data
for i, symbol in enumerate(markets):
    if symbol in marketHistory and len(marketHistory[symbol]) > 200:
        data = marketHistory[symbol]
        _EMA_200_ = EMA(data,200)
        _EMA_50_ = EMA(data,50)
        _RSI_ = RSI(data, 10)
        now = len(_RSI_) - 1
        if _RSI_[now] <= 20:
            print_trade(symbol, str(round(data[now]*10000)/10000), 'BUY')
        elif _RSI_[now] >= 80:
            print_trade(symbol, str(round(data[now]*10000)/10000), 'SELL')
        """plt.subplot(2,1,1)
        plt.plot(data, color='black')
        plt.plot(_EMA_200_, color='red')
        plt.plot(_EMA_50_, color='green')
        plt.subplot(2,1,2)
        plt.plot(_RSI_, color='black')
        plt.show()"""

# Exit
pause = input('\nPress a key to exit.')