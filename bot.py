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
from constants import *

# System libraries
from datetime import date, timedelta
import time, csv, os, sys
import urllib.request
import signal, multiprocessing

# Setup user-agent
try:
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', DEFAULT_USER_AGENT)]
    urllib.request.install_opener(opener)
except:
    std2.write_line(MSG_OPENER_FAILED)

# Market data
fecthMarkets = True
markets = []
index = 1

# Fecth trending markets from Finviz
std2.write_line('Finding trending markets from finviz...')
size = 0
while fecthMarkets:
    try:
        url = f'{URL_FINVIZ}{index}'
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
        print(MSG_FETCHING_FAILED)
        break
std2.write_line('\nFinding trending markets from yahoo...')
url = URL_YAHOO
try:
    with urllib.request.urlopen(url) as f:
        htmlParse = f.read().decode('utf-8')
        std2.pause_progress_bar(1)
        while 'data-symbol=\"' in htmlParse:
            htmlParse = htmlParse.split('data-symbol=\"', 1)[1]
            market = htmlParse.split('\"', 1)[0]
            if not market in markets:
                markets.append(market)
    std2.write_line(f'\n[{size} bytes] Found {len(markets)} markets with an uptrend.\n')
except:
    std2.write_line(MSG_FETCHING_FAILED)
    
# History data
marketHistory = {}
dataPoints = 0
size = 0

# Fetch Market History
std2.write_line('Fectching market history...')
errorMsgBuffer = ''
for i, symbol in enumerate(markets):
    std2.write_progress_bar(i+1, len(markets), PROGRESS_BAR_SIZE)
    endDate = date.today().strftime(DATE_FORMAT)
    startDate = (date.today() - timedelta(days=TIME_FRAME_DAYS)).strftime(DATE_FORMAT)
    with std2.suppress_stdout():
        try:
            marketHistory[symbol] = getStockPriceHistory(symbol, '1d', startDate, endDate)
            dataPoints += len(marketHistory[symbol])
            size += sys.getsizeof(marketHistory[symbol])
        except:
            errorMsgBuffer += f'[Exception] Couldn\'t download data for {symbol} !\n'
std2.write_line(f'{errorMsgBuffer}[{size} bytes] Downloaded {dataPoints} data points from {len(markets)} uptrending markets\n')

# Find previously used markets
std2.write_line('Finding previously used markets...')
try:
    with open('logs.txt') as f:
        content = f.readlines()
        logCount = int(content[0])
        if logCount > 0:
            for i in range(1, logCount + 1):
                std2.write_progress_bar(i, logCount, PROGRESS_BAR_SIZE)
                market = content[i].split('|')[0]
                if not market in markets:
                    markets.append(market)
            std2.write_line(f'\nFound {logCount} previously used markets')
        else:
            std2.write_line('\nFound 0 previously used markets')
except IOError:
    f = open(FILE_LOGS, FILE_CREATE)
    f.write("0")
    f.close()
std2.write_line(f'Found a total of {len(markets)} markets to analyse within the next hour !')

# Searching for trades
def print_trade(symbol, price, action):
    time_str = time.strftime(TIME_FORMAT, time.gmtime(time.time()))
    std2.write_autocomplete(time_str, AUTOCOMPLETE_LENGTH)
    std2.write_autocomplete(symbol, AUTOCOMPLETE_LENGTH)
    std2.write_autocomplete(price, AUTOCOMPLETE_LENGTH)
    std2.write_autocomplete(action, AUTOCOMPLETE_LENGTH)
    std2.write('\n')
std2.write_line('\nTime          Symbol        Price         Action')
std2.write_line('------------  ------------  ------------  ------------')

# Analyze data
def print_data(data, EMA2, EMA1, _RSI_):
    plt.subplot(2,1,1)
    plt.plot(data, color=MAIN_CURVE_COLOR)
    plt.plot(EMA1, color=EMA1_COLOR)
    plt.plot(EMA2, color=EMA2_COLOR)
    plt.subplot(2,1,2)
    plt.plot(_RSI_, color=RSI_COLOR)
    plt.axhline(y=MAX_RSI_SELL, color=RSI_MAX_COLOR, linestyle=LINE_STYLE)
    plt.axhline(y=MIN_RSI_BUY, color=RSI_MIN_COLOR, linestyle=LINE_STYLE)
    plt.show()
wins = 0
amount = 0
money = 0
for i, symbol in enumerate(markets):
    if symbol in marketHistory and len(marketHistory[symbol]) > MIN_DATA_PTS:
        data = marketHistory[symbol]
        EMA1 = EMA(data, DEFAULT_EMA_1)
        EMA2 = EMA(data, DEFAULT_EMA_2)
        _RSI_ = RSI(data, DEFAULT_RSI_1)
        #now = len(_RSI_) - 1
        action = 'None'
        previousBuy = -1
        for now in range(len(data)):
            if _RSI_[now] <= MIN_RSI_BUY and data[now] < EMA1[now] and action != 'BUY':
                print_trade(symbol, str(round(data[now] * DATA_PRECISION) / DATA_PRECISION), 'BUY')
                action = 'BUY'
                previousBuy = data[now]
                #print_data(data, EMA2, EMA1, _RSI_)
            elif _RSI_[now] >= MAX_RSI_SELL and data[now] > EMA1[now] and action != 'SELL':
                print_trade(symbol, str(round(data[now] * DATA_PRECISION) / DATA_PRECISION), 'SELL')
                if  previousBuy != 1 and previousBuy <= data[now]:
                    amount += 1
                    wins += 1
                    money += abs(data[now] - previousBuy)
                elif previousBuy != 1:
                    amount += 1
                    money -= abs(data[now] - previousBuy)
                #print_data(data, EMA2, EMA1, _RSI_)
                action = 'SELL'
std2.write_line(f'The startegy tested has a win rate of {round(wins / amount * 100 * DATA_PRECISION) / DATA_PRECISION}% for {amount} BUY&SELL trades')
std2.write_line(f'Money earned : {money} USD')

# Exit
pause = input('\nPress a key to exit.')