# Libraries to download
import matplotlib.pyplot as plt
import yfinance as yf   

# Project Files
from api.connect import *
from api.order import *
from api.tracking import *
from dft.dft import *
from dft.denoise import *
from analysis.analyse import *

# System libraries
import time
import csv
import os

"""
_API_ = initAPI()
contract = IBStockContract('BABA')
order = IBMarketOrder('SELL', 10)
_API_.placeOrder(_API_.nextorderId, contract, order)
print(getStockPrice('BABA'))
"""

# Get the data for the stock Apple by specifying the stock ticker, start date, and end date 
data = yf.download('AAPL','2021-02-06','2021-02-09', interval = "1m") 
graph = [(data['Close'][i] if not math.isnan(data['Close'][i]) else data['Close'][i+1]) for i in range(len(data['Close'])-1)]

"""
graph = []
with open('bot.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for i,row in enumerate(spamreader):
        if i > 0:
            graph.append(float((', '.join(row)).split(',')[1]))

"""
den = denoise(graph, .95)
dft_output = den[0]
graph_cpy = [den[1][i] for i in range(len(den[1]))]
graph_cpy_2 = [den[2][i] for i in range(len(den[2]))]
res = determineHorizontalResistance(graph_cpy, (max(graph)-min(graph)) * .1)
sup = determineHorizontalSupport(graph_cpy_2, (max(graph)-min(graph)) * .1)
sma50 = determineMovingAverage(graph, 50)
sma150 = determineMovingAverage(graph, 150)
sma200 = determineMovingAverage(graph, 200)


plt.subplot(1,2,1)
plt.plot(graph, color='#4285F4')
#plt.plot(sma50, color='#0F9D58')
#plt.plot(sma150, color='#F4B400')
#plt.plot(sma200, color='#DB4437')
if res[0] != -1:
    plt.axhline(y=res[0], color='gray', linestyle='-')
    plt.axhline(y=res[1], color='black', linestyle='-')
if sup[0] != -1:
    plt.axhline(y=sup[1], color='gray', linestyle='-')
    plt.axhline(y=sup[0], color='black', linestyle='-')
plt.subplot(1,2,2)
plt.plot(dft_output, color='#4285F4')
#plt.plot(sma50, color='#0F9D58')
#plt.plot(sma150, color='#F4B400')
#plt.plot(sma200, color='#DB4437')
if res[0] != -1:
    plt.axhline(y=res[0], color='gray', linestyle='-')
    plt.axhline(y=res[1], color='black', linestyle='-')
if sup[0] != -1:
    plt.axhline(y=sup[1], color='gray', linestyle='-')
    plt.axhline(y=sup[0], color='black', linestyle='-')

plt.show()


os.system("pause")

