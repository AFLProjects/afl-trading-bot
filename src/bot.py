import matplotlib.pyplot as plt

from api.connect import *
from api.order import *
from api.tracking import *
from dft.dft import *
from dft.denoise import *
from plot.reslines import *

import time
import csv
"""
_API_ = initAPI()
contract = IBStockContract('AAPL')
order = IBMarketOrder('BUY', 10)
_API_.placeOrder(_API_.nextorderId, contract, order)
"""


graph = []
with open('bot.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for i,row in enumerate(spamreader):
        if i > 0:
            graph.append(float((', '.join(row)).split(',')[1]))

den = denoise(graph, .85)
dft_output = den[0]
graph_cpy = [den[1][i] for i in range(len(den[1]))]
graph_cpy_2 = [den[2][i] for i in range(len(den[2]))]
res = determineHorizontalResistance(graph_cpy, .1)
sup = determineHorizontalSupport(graph_cpy_2, .1)
sma = determineMovingAverage(graph, 20)

plt.subplot(1,2,1)
plt.plot(graph, color='#4285F4')
plt.plot(sma, color='#0F9D58')
plt.axhline(y=res[0], color='gray', linestyle='-')
plt.axhline(y=res[1], color='black', linestyle='-')
plt.axhline(y=sup[1], color='gray', linestyle='-')
plt.axhline(y=sup[0], color='black', linestyle='-')
plt.subplot(1,2,2)
plt.plot(dft_output, color='#4285F4')
plt.plot(sma, color='#0F9D58')
plt.axhline(y=res[0], color='gray', linestyle='-')
plt.axhline(y=res[1], color='black', linestyle='-')
plt.axhline(y=sup[1], color='gray', linestyle='-')
plt.axhline(y=sup[0], color='black', linestyle='-')
"""
money = 1000
moneyOld = 0
q = 0
for i,v in enumerate(dft_output):
    if i != 0 and i != len(dft_output) - 1:
        if dft_output[i].real - dft_output[i-1].real <= 0 and  dft_output[i+1].real - dft_output[i].real >= 0:
            currentPrice = graph[i]
            tmp = money
            q = tmp // currentPrice
            moneyOld = money
            money = tmp % currentPrice
        if dft_output[i].real - dft_output[i-1].real >= 0 and  dft_output[i+1].real - dft_output[i].real <= 0:
            currentPrice = graph[i]
            money += q * currentPrice
            q = 0
            sign = "-"
            if money >= moneyOld:
                sign = "+"
            amount = abs(round((money - moneyOld) / moneyOld * 100))
            out = "Money : {}€ , {}{}%".format(round(money), sign, amount)
            print(out)
"""
plt.show()

