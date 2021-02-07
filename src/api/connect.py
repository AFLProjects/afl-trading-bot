from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time

from api import order

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.contract_details = {} 

	def nextValidId(self, orderId: int):
		super().nextValidId(orderId)
		self.nextorderId = orderId
	
	def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
		print(f'Order {status} ~ #{orderId}')
	
	def openOrder(self, orderId, contract, order, orderState):
		print('Order ~ #{} \n\t Symbol : {} \n\t SecType : {} \n\t Exchange : {} \n\t Action : {} \n\t Order Type : {} \n\t Quantity : {} \n\t Order State : {}'.format(
			orderId, contract.symbol, contract.secType, contract.exchange, order.action, order.orderType, order.totalQuantity, orderState.status))
	
	def execDetails(self, reqId, contract, execution):
		print('Order Executed ~ #{} \n\t Symbol : {} \n\t SecType : {} \n\t Currency : {} \n\t Execution ID : {} \n\t Order ID : {}\n\t Shares : {} \n\t Last Liquidity : {}'.format(
			reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity))

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
	app = IBapi()
	app.connect('127.0.0.1', 7497, 123)
	app.nextorderId = None
	thread_exec = lambda: app.run()
	api_thread = threading.Thread(target=thread_exec, daemon=True)
	api_thread.start()
	while not isinstance(app.nextorderId, int):
		print('Waiting For Connection...')
		time.sleep(1)
	print('Connected !')
	return app


