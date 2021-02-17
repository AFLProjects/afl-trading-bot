from __future__ import print_function
import urllib.request
import yfinance as yf 
import math, sys, threading, time
from time import sleep
sys.path.append("../")
import utils.stdout2 as std2
from exceptions import *
from constants import *

try:
    import thread
except ImportError:
    import _thread as thread

try:
    range, _print = xrange, print
    def print(*args, **kwargs): 
        flush = kwargs.pop('flush', False)
        _print(*args, **kwargs)
        if flush:
            kwargs.get('file', sys.stdout).flush()            
except NameError:
    pass

# Force quit function
def quit_function(fn_name):
    sys.stderr.flush()
    thread.interrupt_main()
    raise Exception("Time out")

# Decorator exit after s seconds
def exit_after(s):
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer

"""
Get full data history of a stock
"""
@exit_after(5)
def gethistory(stock, dateStart, dateEnd, interval):
    return yf.download(stock, dateStart, dateEnd, interval = interval, threads = False)

"""
Get current close price of a stock
"""
@exit_after(5)
def getprice(symbol):
    return yf.Ticker(symbol).history(period='1d')['Close'][0]

"""
Setup Downloader
"""
def setup_downloader():
    # Setup user-agent
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', DEFAULT_USER_AGENT)]
        urllib.request.install_opener(opener)
    except:
        std2.write_line(MSG_OPENER_FAILED)
        raise UserAgentSetupError

"""
Find uptrending markets from finviz
using urllib request and web scrapping
"""
def getsymbols_finviz():
    # Market data
    markets = []
    # HTML index
    index = 1

    # Find markets
    fetch_markets = True
    while fetch_markets:
        try:
            # URL
            url = f'{URL_FINVIZ}{index}'
            std2.write_line(url)
            std2.pause_progress_bar(1)

            # Download HTML
            with urllib.request.urlopen(url) as f:
                # Parse HTML
                html = f.read().decode('utf-8')
                parse = (html.split('<!-- TS')[1]).split('TE -->')[0]

                # Find market names
                for i, value in enumerate(parse.splitlines()):
                    name = value.split('|')[0]

                    # Chech if already found
                    if name in markets:
                        fetch_markets = False
                        break
                    elif name:
                        markets.append(name)
                index += 12
        except:
            # Error during symbol downloading
            print(MSG_FETCHING_FAILED)
            raise DownloadException
            break
    return markets

"""
Find uptrending markets from yahoo
using urllib request and web scrapping
"""
def getsymbols_yahoo():
    # Market Data
    markets = []
    # Yahoo website url
    url = URL_YAHOO
    std2.write_line(url)
    std2.pause_progress_bar(1)

    # Find symbols
    try:
        # Open url
        with urllib.request.urlopen(url) as f:
            # Download HTML
            parse = f.read().decode('utf-8')

            # Parse HTML
            while 'data-symbol=\"' in parse:
                parse = parse.split('data-symbol=\"', 1)[1]
                name = parse.split('\"', 1)[0]
                markets.append(name)
    except:
        # Error during symbol downloading
        std2.write_line(MSG_FETCHING_FAILED)
        raise DownloadException
    return markets

"""
Download symbols from yahoo and finviz
"""
def download_symbols():
    # Symbol data
    s1 = getsymbols_finviz()
    s2 = getsymbols_yahoo()
    symbols = []

    # Filter data
    for i, symbol in enumerate(s1):
        if not symbol in symbols:
            symbols.append(symbol)
    for i, symbol in enumerate(s2):
        if not symbol in symbols:
            symbols.append(symbol)
    return symbols

"""
Get symbols from csv
"""
def getsymbols_csv(path):
    markets = []
    with open(path) as f:
        for row in f:
            sbl = row.split(',', 1)[0]
            if sbl != 'Symbol':
                markets.append(sbl)
    return markets