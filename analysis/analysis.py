from math import *

# Calculates moving average
def MA(graph, window_size):
	return [sum(graph[i : i + window_size]) / window_size for i in range(len(graph) - window_size + 1)]

# Calculates exponential moving average
def EMA(graph, window_size):
	EMA = [None] * len(graph)
	prevEMA = sum(graph[i] for i in range(window_size)) / window_size
	EMA[0] = prevEMA
	k = (2.0 / (window_size + 1.0))
	for i in range(1, len(graph)):
		EMA[i] = graph[i] * k + prevEMA * (1 - k)
		prevEMA = EMA[i]
	return EMA

def TR(dataframe, i):
	r = max(dataframe.highData[i], dataframe.closeData[i-1])
	r -= min(dataframe.lowData[i], dataframe.closeData[i-1])
	return r

def ATR(dataframe, n):
	ATR = [0] * len(dataframe.closeData)
	ATR[0] = sum(TR(dataframe, i) for i in range(1, n)) / n
	for j in range(1, len(dataframe.closeData)):
		ATR[j] = (ATR[j-1] * (n-1) + TR(dataframe, j)) / n
	return ATR

# Calculates the average gain
def average_gain(data, offset, window_size):
	avg = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr > 0:
			avg += nxt - curr
	avg /= window_size
	return avg

# Calculates the average loss
def average_loss(data, offset, window_size):
	avg = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr < 0:
			avg += abs(nxt - curr)
	avg /= window_size
	return avg

# Calculates the gain
def gain(data, offset, window_size):
	gain = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr > 0:
			gain += nxt - curr
	return gain

# Calculates the loss
def loss(data, offset, window_size):
	loss = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr > 0:
			loss += abs(nxt - curr)
	return loss

# Calculates RSI for a single index
def _RSI_(t):
	sumGain = 0
	sumLoss = 0
	for i in range(1, len(t)):
		diff = t[i] - t[i-1]
		if diff > 0:
			sumGain += diff
		else:
			sumLoss -= diff
	if sumGain == 0:
		return 0
	if sumLoss == 0:
		return 100
	RS = sumGain / sumLoss
	return 100 - (100 / (1 + RS))

# Calculate RSI
def RSI(graph, window_size):
	RSI = [None] * len(graph)
	for i in range(window_size, len(graph)):
		RSI[i] = _RSI_(graph[i - window_size:i])
	return RSI