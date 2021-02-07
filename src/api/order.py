from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

def IBCurrencyExchange(initialCurrency, finalCurrency):
	contract = Contract()
	contract.symbol = finalCurrency
	contract.secType = 'CASH'
	contract.exchange = 'IDEALPRO'
	contract.currency = initialCurrency
	return contract

def IBStockContract(symbol, secType='STK', exchange='SMART', currency='USD'):
	contract = Contract()
	contract.symbol = symbol
	contract.secType = secType
	contract.exchange = exchange
	contract.currency = currency
	return contract

def IBOrder(order, action, quantity):
	order = Order()
	order.action = action
	order.totalQuantity = quantity
	order.orderType = order
	return order

def IBMarketOrder(action, quantity):
	order = Order()
	order.action = action
	order.totalQuantity = quantity
	order.orderType = 'MKT'
	return order

def IBMarketIfTouchedOrder(action, quantity, limit):
	order = Order()
	order.action = action
	order.totalQuantity = quantity
	order.orderType = 'MIT'
	order.lmtPrice = limit 
	return order

def IBLimitOrder(action, quantity, limit):
	order = Order()
	order.action = action
	order.totalQuantity = quantity
	order.orderType = 'LMT'
	order.lmtPrice = limit 
	return order

def IBLimitIfTouchedOrder(action, quantity, limit):
	order = Order()
	order.action = action
	order.totalQuantity = quantity
	order.orderType = 'LMT'
	order.lmtPrice = limit 
	return order

def IBStopLossOrder(action, quantity, limit):
	order = Order()
	order.action = action
	order.totalQuantity = quantity
	order.orderType = 'STP'
	stop_order.auxPrice = limit
	return order