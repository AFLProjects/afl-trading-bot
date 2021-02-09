import urllib.request
import yfinance as yf 
import math  

def getStockPriceHistory(stock, interval, dateStart, dateEnd):
	data = yf.download(stock, dateStart, dateEnd, interval = interval)['Close']
	graph = []
	for i, value in enumerate(data):
		if not math.isnan(value):
			graph.append(value)
	return graph

def getCurrentPrice(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]