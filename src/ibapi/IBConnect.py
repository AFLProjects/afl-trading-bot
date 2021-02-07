from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time

import IBOrders

# IB API class
class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.contract_details = {} 

	def nextValidId(self, orderId: int):
		super().nextValidId(orderId)
		self.nextorderId = orderId
		print('The next valid order id is: ', self.nextorderId)
	
	def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
		print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
	
	def openOrder(self, orderId, contract, order, orderState):
		print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)
	
	def execDetails(self, reqId, contract, execution):
		print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)
	
	def contractDetails(self, reqId: int, contractDetails):
		self.contract_details[reqId] = contractDetails
	
	def get_contract_details(self, reqId, contract):
		self.contract_details[reqId] = None
		self.reqContractDetails(reqId, contract)

		for err_check in range(50):
			if not self.contract_details[reqId]:
				time.sleep(0.1)
			else:
				break

		if err_check == 49:
			raise Exception('error getting contract details')

		return app.contract_details[reqId].contract

def initAPI():
	# Init API
	app = IBapi()
	app.connect('127.0.0.1', 7497, 123)
	app.nextorderId = None
	# Init thread
	thread_exec = lambda: app.run()
	api_thread = threading.Thread(target=thread_exec, daemon=True)
	api_thread.start()
	# Wait for connection
	while not isinstance(app.nextorderId, int):
		print('Waiting For Connection...')
		time.sleep(1)
	print('Connected !')
	return app

_API_ = initAPI()
contract = IBOrders.IBCurrencyExchange('USD', 'EUR')
order = IBOrders.IBMarketOrder('BUY', 10)
_API_.placeOrder(_API_.nextorderId, contract, order)

