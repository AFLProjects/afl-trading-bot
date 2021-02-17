# External libraries
import matplotlib.pyplot as plt

# Project Files
from api.ibapi import *
from api.apihelper import *
from data.dataprovider import *
from data.datahistory import *
from analysis.dft import *
from analysis.analysis import *
import utils.stdout2 as std2
from constants import *
from exceptions import *

# System libraries
from datetime import date, timedelta
import time, csv, os, sys
import urllib.request
import signal, multiprocessing

# Setup User Agent
setup_downloader()

# Download Symbol Names
#markets =  download_symbols()
markets = getsymbols_csv('symbols.csv')
std2.write('Downloading symbol data...\n')

# Download symbol data
Symbols = [None] * len(markets)
for i, symbol in enumerate(markets):
    std2.write_progress_bar(i+1, len(markets), PROGRESS_BAR_SIZE, end=(' ' + symbol))
    with std2.suppress_stdout():
        try:
            Symbols[i] = SymbolData(symbol)
        except:
            Symbols[i] = None

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
        try:
            data = marketHistory[symbol]
            EMA1 = EMA(data, DEFAULT_EMA_1)
            EMA2 = EMA(data, DEFAULT_EMA_2)
            _RSI_ = RSI(data, DEFAULT_RSI_1)
        except:
            raise DataError
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