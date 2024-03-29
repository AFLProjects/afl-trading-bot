from datetime import *
import yfinance as yfinance 
import time, math
import pickle
import os
import data.dataprovider as dp

class DataHistory:
    def __init__(self, data):
        # Init Data
        rawData = data
        self.closeData = []
        self.openData = []
        self.highData = []
        self.lowData = []
        self.dateIndex = []

        # Store Data
        keys = list(rawData['Close'].keys())
        for i in range(len(rawData['Close'])):
            if not math.isnan(rawData['Close'][i]) and rawData['Close'][i] != None and rawData['Close'][i] != 0:
                self.closeData.append(rawData['Close'][i])
                self.openData.append(rawData['Open'][i])
                self.highData.append(rawData['High'][i])
                self.lowData.append(rawData['Low'][i])
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

# Static pack cache
def _pack_cache_(symbol):
    path =  f'{os.path.normpath(os.getcwd())}\\cache\\{symbol}.sbl'
    with open(path, 'wb') as output:
        pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
    file = open(f'{os.path.normpath(os.getcwd())}\\cache\\{self.symbol}.log', 'w+')
    file.seek(0)
    file.write(date.today().strftime("%Y-%m-%d"))
    file.truncate()
    file.close()

# Static unpack cache
def _unpack_cache_(symbol):
    path =  f'{os.path.normpath(os.getcwd())}\\cache\\{symbol}.sbl'
    with open(path, 'rb') as input:
        return pickle.load(input)

# Static cache checking
def _cache_created_(symbol):
        path =  f'{os.path.normpath(os.getcwd())}\\cache\\{symbol}.sbl'
        try:
            f = open(path)
            f.close()
            return True
        except:
            return False

class SymbolData:
    # Init symbol data
    def __init__(self, symbol):
        self.symbol = symbol
        if not self.cache_created():
            endDate = date.today().strftime("%Y-%m-%d")
            startDate = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
            datahistory =  dp.gethistory(self.symbol, startDate, endDate, '1d')
            self.datahistory = DataHistory(datahistory)
            if len(self.datahistory.closeData) > 0:
                self.price = self.datahistory.getprice()
                self.previous_price = -1
                self.quantity = 0
                self.used = False
                self.status = 'None'
                self.stoploss = 0
                self.pack_cache()
        else:
            cached = self.unpack_cache()
            self.datahistory = cached.datahistory
            self.price = cached.price
            self.used = cached.used
            self.status = cached.status
            self.quantity = cached.quantity
            self.previous_price = cached.previous_price
            self.stoploss = cached.stoploss
            endDate = date.today().strftime("%Y-%m-%d")
            startDate = datetime.strptime(self.datahistory.get_end_date(), "%Y-%m-%d")
            startDate = (startDate - timedelta(days=7)).strftime("%Y-%m-%d")
            path =  f'{os.path.normpath(os.getcwd())}\\cache\\{self.symbol}.log'
            lastUpdated = ''
            with open(path) as f:
                    lastUpdated = f.readline()
            if endDate > startDate and endDate != lastUpdated:
                datahistory = dp.gethistory(self.symbol, startDate, endDate, '1d')
                self.datahistory.append(datahistory)
            if len(self.datahistory.closeData) > 0:
                self.price = self.datahistory.getprice()
            else:
                self.price = -1
            self.pack_cache()

    # Pack symbol data into cache folder
    def pack_cache(self):
            path =  f'{os.path.normpath(os.getcwd())}\\cache\\{self.symbol}.sbl'
            with open(path, 'wb') as output:
                    pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
            file = open(f'{os.path.normpath(os.getcwd())}\\cache\\{self.symbol}.log', 'w+')
            file.seek(0)
            file.write(date.today().strftime("%Y-%m-%d"))
            file.truncate()
            file.close()

    # Unpack symbol data into cache folder
    def unpack_cache(self):
            path =  f'{os.path.normpath(os.getcwd())}\\cache\\{self.symbol}.sbl'
            with open(path, 'rb') as input:
                    return pickle.load(input)

    # Check if cache is created
    def cache_created(self):
        path =  f'{os.path.normpath(os.getcwd())}\\cache\\{self.symbol}.sbl'
        try:
            f = open(path)
            f.close()
            return True
        except:
            return False
