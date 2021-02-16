from datetime import *

class DataFrame:
	def IsDataValid(data):
		return True if not (math.nan(data) or data == 0) else False

	def __init__(self, data):
		# Init Data
		self.rawData = data
		self.closeData = []
		self.openData = []
		self.highData = []
		self.lowData = []
		self.dateIndex = []

		# Store Data
		keys = list(self.rawData.keys())
		for i in range(len(self.rawData)):
			if IsDataValid(self.rawData['Close'][i]):
				closeData.append(self.rawData['Close'][i])
				openData.append(self.rawData['Open'][i])
				highData.append(self.rawData['High'][i])
				lowData.append(self.rawData['Low'][i])
				dateIndex.append(keys[i])

	# Get price using formatted date "%Y-%m-%d"
	def getprice_fdate(date):
		return self.closeData[self.dateIndex.indexof(date)]

	# Get price using year, month & day
	def getprice_date(day, month, year):
		fdate = datetime(year, month, day).strftime(DATE_FORMAT)
		return getprice_fdate(fdate)

	# Get price using index
	def getprice_index(index):
		return self.closeData[i]

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
		return self.dateIndex[i]

	# Convert from date to index
	def convert_from_date_to_index(i):
		return self.dateIndex.indexof(date)

class Symbol:
	def __init__(self, symbol, dataframe):
		self.symbol = symbol
		self.dataframe = dataframe
		self.price = self.dataframe.getprice()
		self.used = False
		self.status = 'None'


