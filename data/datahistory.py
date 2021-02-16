from datetime import *
from exceptions import *

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
			if not math.nan(self.rawData['Close'][i]):
				closeData.append(self.rawData['Close'][i])
				openData.append(self.rawData['Open'][i])
				highData.append(self.rawData['High'][i])
				lowData.append(self.rawData['Low'][i])
				dateIndex.append(keys[i])

	# Get price using formatted date "%Y-%m-%d"
	def getprice_fdate(date):
		if date in dateIndex:
			return self.closeData[self.dateIndex.indexof(date)]
		else:
			raise DataError
			return None

	# Get price using year, month & day
	def getprice_date(day, month, year):
		fdate = datetime(year, month, day).strftime(DATE_FORMAT)
		return getprice_fdate(fdate)

	# Get price using index
	def getprice_index(index):
		if i >= 0 and i < len(self.closeData):
			return self.closeData[i]
		else:
			raise DataError
			return None

	# Get current price
	def getprice():
		return self.closeData[len(self.closeData) - 1]

	# Get End Date
	def get_end_date():
		return self.dateIndex[len(self.dateIndex) - 1]

	# Get Start Date
	def get_start_date():
		return self.dateIndex[0]

	# Convert from index to date
	def convert_from_index_to_date(i):
		if i >= 0 and i < len(self.dateIndex):
			return self.dateIndex[i]
		else:
			raise DataError
			return None

	# Convert from date to index
	def convert_from_date_to_index(i):
		if date in dateIndex:
			return self.dateIndex.indexof(date)
		else:
			raise DataError
			return None

class Symbol:
	def __init__(self, symbol, dataframe):
		self.symbol = symbol
		self.dataframe = dataframe
		self.price = self.dataframe.getprice()
		self.used = False
		self.status = 'None'


