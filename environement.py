from api.ibapi import *
from api.apihelper import *
from data.dataprovider import *
from data.datahistory import *
from analysis.dft import *
from analysis.analysis import *
import utils.stdout2 as std2
from constants import *
from exceptions import *

class Environement:
    def is_symbol_valid(self, Symbol):
        return Symbol is not None and len(Symbol.datahistory.closeData) > 249 and Symbol.datahistory is not None

    def is_data_valid(self, i, d):
        ema = self.ema_dataset[i][d]
        rsi = self.rsi_dataset[i][d]
        atr = self.atr_dataset[i][d]
        price = self.data[i].datahistory.closeData[d]
        return ema != None and rsi != None and atr != None and price != None

    def __init__(self, mode, data):
        # Init values
        self.mode = mode
        self.data = data
        self.cash = 0
        self.netliquidation = 0
        self.tradeCount = 0
        self.wins = 0

        # Calculate EMA, RSI and ATR for all the symbols
        self.ema_dataset = [None] * len(self.data)
        self.rsi_dataset = [None] * len(self.data)
        self.atr_dataset = [None] * len(self.data)
        for i, symbol in enumerate(self.data):
            if self.is_symbol_valid(symbol):
                self.ema_dataset[i] = EMA(symbol.datahistory.closeData, DEFAULT_EMA_1)
                self.rsi_dataset[i] = RSI(symbol.datahistory.closeData, DEFAULT_RSI_1)
                self.atr_dataset[i] = ATR(symbol.datahistory, 14)

    def environement_output_init(self):
        std2.write_line('\nTime          Symbol        Price         Action        Money         Quantity      Net Value     Stoploss      Type')
        std2.write_line('------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------')

    def environement_print_trade(self, symbol, price, action, time, cash, quantity, netvalue, stoploss, cause):
        std2.write_autocomplete(str(time), AUTOCOMPLETE_LENGTH)
        std2.write_autocomplete(str(symbol), AUTOCOMPLETE_LENGTH)
        std2.write_autocomplete(str(price), AUTOCOMPLETE_LENGTH)
        std2.write_autocomplete(str(action), AUTOCOMPLETE_LENGTH)
        std2.write_autocomplete(str(cash), AUTOCOMPLETE_LENGTH)
        std2.write_autocomplete(str(quantity), AUTOCOMPLETE_LENGTH)
        std2.write_autocomplete(str(netvalue), AUTOCOMPLETE_LENGTH)
        std2.write_autocomplete(str(stoploss), AUTOCOMPLETE_LENGTH)
        std2.write_autocomplete(str(cause), AUTOCOMPLETE_LENGTH)
        std2.write('\n')

    def env_format(self, value):
        return str(round(value * DATA_PRECISION) / DATA_PRECISION)


    def evaluate_netliquidation(self, date):
        self.netliquidation = 0
        for i, symbol in enumerate(self.data):
            if self.is_symbol_valid(symbol) and symbol.quantity != 0:
                self.netliquidation += symbol.quantity * symbol.datahistory.closeData[date]
        self.netliquidation += self.cash

    def buying_opportunity(self, symbol, date):
        if self.rsi_dataset[symbol][date] > MIN_RSI_BUY:
            return False
        if self.data[symbol].datahistory.closeData[date] >= self.ema_dataset[symbol][date]:
            return False
        if self.data[symbol].status == 'BUY':
            return False
        if self.data[symbol].datahistory.closeData[date] > .03 * self.cash:
            return False
        return True

    def selling_opportunity(self, symbol, date):
        if self.rsi_dataset[symbol][date] < MAX_RSI_SELL:
            return False
        if self.data[symbol].datahistory.closeData[date] <= self.ema_dataset[symbol][date]:
            return False
        if self.data[symbol].status == 'SELL':
            return False
        if self.data[symbol].status == 'None':
            return False
        return True

    def stoploss_opportunity(self, symbol, date):
        if self.data[symbol].datahistory.closeData[date] > self.data[symbol].stoploss:
            return False
        if self.data[symbol].stoploss == 0:
            return False
        return True

    def simulate_buy(self, symbol_index, date):
        symbol = self.data[symbol_index]
        close_price = self.data[symbol_index].datahistory.closeData
        symbol.status = 'BUY'
        symbol.previous_price = close_price[date]
        symbol.quantity = floor((.03 * self.cash) / close_price[date])
        symbol.stoploss = close_price[date] - self.atr_dataset[symbol_index][date]
        self.cash -= symbol.quantity * close_price[date]
        self.evaluate_netliquidation(date)
        self.environement_print_trade(symbol.symbol, self.env_format(close_price[date]),'BUY',
            symbol.datahistory.convert_from_index_to_date(date), self.env_format(self.cash),
            symbol.quantity, self.env_format(self.netliquidation), self.env_format(symbol.stoploss), 'BUY')

    def simulate_sell(self, symbol_index, date):
        symbol = self.data[symbol_index]
        close_price = self.data[symbol_index].datahistory.closeData
        if symbol.previous_price <= close_price[date]:
            self.tradeCount += 1
            self.wins += 1
        else:
            self.tradeCount += 1
        symbol.status = 'SELL'
        self.cash += symbol.quantity * close_price[date]
        self.evaluate_netliquidation(date)
        self.environement_print_trade(symbol.symbol, self.env_format(close_price[date]),'SELL',
            symbol.datahistory.convert_from_index_to_date(date), self.env_format(self.cash),
            symbol.quantity, self.env_format(self.netliquidation), self.env_format(symbol.stoploss), 'SELL')
        symbol.quantity = 0
        symbol.stoploss = 0

    def simulate_deposit(self, cash):
        self.cash += cash

    def simulate(self):
        for d in range(250):
            for i, symbol in enumerate(self.data):
                if self.is_symbol_valid(symbol) and self.is_data_valid(i, d):
                    if self.buying_opportunity(i, d):
                        self.simulate_buy(i, d)
                    elif self.selling_opportunity(i, d) or self.stoploss_opportunity(i, d):
                        self.simulate_sell(i, d)
        std2.write_line(f'The startegy tested has a win rate of {round(self.wins / self.tradeCount * 100 * DATA_PRECISION) / DATA_PRECISION}% for {self.tradeCount} BUY&SELL trades')

