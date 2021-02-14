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

def quit_function(fn_name):
    sys.stderr.flush()
    thread.interrupt_main()
    raise Exception("Time out")

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

#@exit_after(5)
def getStockPriceHistory(stock, interval, dateStart, dateEnd):
	data = yf.download(stock, dateStart, dateEnd, interval = interval, threads = False)['Close']
	graph = []
	for i, value in enumerate(data):
		if not math.isnan(value):
			graph.append(value)
	return graph

def getCurrentPrice(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]