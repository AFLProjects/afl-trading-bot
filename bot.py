# External libraries
import matplotlib.pyplot as plt

# Project Files
from data.dataprovider import *
from data.datahistory import *
from analysis.dft import *
from analysis.analysis import *
import utils.stdout2 as std2
from constants import *
from exceptions import *
from environement import *

# System libraries
from datetime import date, timedelta
import time, csv, os, sys
import urllib.request
import signal, multiprocessing

#setup_downloader()
std2.write('Extracting csv data...\n')
markets = getsymbols_csv('symbols.csv')
std2.write('Downloading symbol data...\n')
Symbols = [None] * len(markets)
for i, symbol in enumerate(markets):
    std2.write_progress_bar(i+1, len(markets), PROGRESS_BAR_SIZE, end=(' ' + symbol))
    with std2.suppress_stdout():
        try:
            Symbols[i] = SymbolData(symbol)
        except:
            Symbols[i] = None
symbols = [SymbolData(symbol) for i,symbol in enumerate(markets)]
e = Environement('simulation', Symbols)
e.simulate_deposit(400)
e.simulate_monthlydeposit(20)
e.environement_output_init()
e.simulate()
pause = input('\nPress a key to exit.')

