from datetime import *
import yfinance as yfinance 
import time, math
import pickle
import os

class DataHistory:
	def __init__(self, data):
		# Init Data
		self.rawData = data
		self.closeData = []
		self.openData = []
		self.highData = []
		self.lowData = []
		self.dateIndex = []

		# Store Data
		keys = list(self.rawData['Close'].keys())
		for i in range(len(self.rawData['Close'])):
			self.closeData.append(self.rawData['Close'][i])
			self.openData.append(self.rawData['Open'][i])
			self.highData.append(self.rawData['High'][i])
			self.lowData.append(self.rawData['Low'][i])
			self.dateIndex.append(keys[i].strftime("%Y-%m-%d"))

	# Get price using formatted date "%Y-%m-%d"
	def getprice_fdate(self, date):
		if date in self.dateIndex:
			return self.closeData[self.dateIndex.index(date)]
		else:
			raise Exception('Data History Error')
			return None

	# Get price using year, month & day
	def getprice_date(self, day, month, year):
		fdate = datetime(year, month, day).strftime("%Y-%m-%d")
		return self.getprice_fdate(fdate)

	# Get price using index
	def getprice_index(self, index):
		if index >= 0 and index < len(self.closeData):
			return self.closeData[index]
		else:
			raise Exception('Data History Error')
			return None

	# Get current price
	def getprice(self):
		if len(self.closeData) > 0:
			return self.closeData[len(self.closeData) - 1]
		else:
			raise Exception('Data History Error')
			return None

	# Get End Date
	def get_end_date(self):
		if len(self.dateIndex) > 0:
			return self.dateIndex[len(self.dateIndex) - 1]
		else:
			raise Exception('Data History Error')
			return None

	# Get Start Date
	def get_start_date(self):
		if len(self.dateIndex) > 0:
			return self.dateIndex[0]
		else:
			raise Exception('Data History Error')
			return None

	# Convert from index to date
	def convert_from_index_to_date(self, i):
		if i >= 0 and i < len(self.dateIndex):
			return self.dateIndex[i]
		else:
			raise Exception('Data History Error')
			return None

	# Convert from date to index
	def convert_from_date_to_index(self, date):
		if date in self.dateIndex:
			return self.dateIndex.index(date)
		else:
			raise Exception('Data History Error')
			return None

	def append(self, rawData):
		keys = list(rawData['Close'].keys())
		for i in range(len(rawData['Close'])):
			k = keys[i].strftime("%Y-%m-%d")
			if not k in self.dateIndex:
				self.closeData.append(rawData['Close'][i])
				self.openData.append(rawData['Open'][i])
				self.highData.append(rawData['High'][i])
				self.lowData.append(rawData['Low'][i])
				self.dateIndex.append(k)

def _pack_cache_(symbol):
	path =  f'{os.path.normpath(os.getcwd() + os.sep + os.pardir)}\\cache\\{symbol}.sbl'
	with open(path, 'wb') as output:
		pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

def _unpack_cache_(symbol):
	path =  f'{os.path.normpath(os.getcwd() + os.sep + os.pardir)}\\cache\\{symbol}.sbl'
	with open(path, 'rb') as input:
		return pickle.load(input)

class Symbol:
    def __init__(self, symbol):
        self.symbol = symbol
        if not self.cache_created():
        	#datahistory = download
            self.datahistory = DataHistory(datahistory)
            self.price = self.datahistory.getprice()
            self.used = False
            self.status = 'None'
            self.pack_cache()
        else:
            self = self.unpack_cache()
            #calc interval
            #download datahistory
            self.datahistory.append(datahistory)

    def pack_cache(self):
            path =  f'{os.path.normpath(os.getcwd() + os.sep + os.pardir)}\\cache\\{self.symbol}.sbl'
            with open(path, 'wb') as output:
                    pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def unpack_cache(self):
            path =  f'{os.path.normpath(os.getcwd() + os.sep + os.pardir)}\\cache\\{self.symbol}.sbl'
            with open(path, 'rb') as input:
                    return pickle.load(input)

    def cache_created(self):
        path =  f'{os.path.normpath(os.getcwd() + os.sep + os.pardir)}\\cache\\{self.symbol}.sbl'
        try:
        	f = open(path)
        	f.close()
        	return True
        except:
        	return False

data = yfinance.download('AAPL', '2020-02-16', '2021-02-13', interval = '1d', threads = False)
dh = DataHistory(data)
AppleSymbol = Symbol('AAPL', dh)

while True:
	time.sleep(1)
