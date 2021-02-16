from __future__ import print_function
import urllib.request
import yfinance as yf 
import math  

import sys
import threading
from time import sleep
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