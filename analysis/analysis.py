from math import *

"""
Calculate moving average
graph -> data
window_size -> moving average period
"""
def MA(graph, window_size):
	# Calculate MA Length
	L = len(graph) - window_size + 1

	# Determine MA
	return [sum(graph[i : i + window_size]) / window_size for i in range(L)]

"""
Calculate exponential moving average
graph -> data
window_size -> moving average period
"""
def EMA(graph, window_size):
	# Init EMA
	EMA = [50] * len(graph)

	# Init first EMA with MA
	prevEMA = sum(graph[i] for i in range(window_size)) / window_size
	EMA[0] = prevEMA

	# EMA Multiplier
	k = (2.0 / (window_size + 1.0))

	# Recursively Calculate EMA
	for i in range(1, len(graph)):
		EMA[i] = graph[i] * k + prevEMA * (1 - k)
		prevEMA = EMA[i]
	return EMA

"""
Calculates the average gain
"""
def average_gain(data, offset, window_size):
	avg = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr > 0:
			avg += nxt - curr
	avg /= window_size
	return avg

"""
Calculates the average loss
"""
def average_loss(data, offset, window_size):
	avg = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr < 0:
			avg += abs(nxt - curr)
	avg /= window_size
	return avg

"""
Calculates the gain
"""
def gain(data, offset, window_size):
	gain = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr > 0:
			gain += nxt - curr
	return gain

"""
Calculates the loss
"""
def loss(data, offset, window_size):
	loss = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr > 0:
			loss += abs(nxt - curr)
	return loss

"""
Calculate RSI
"""
def _RSI_(t):
	# Init
	sumGain = 0
	sumLoss = 0

	# Calculate average gain & loss
	for i in range(1, len(t)):
		diff = t[i] - t[i-1]
		if diff > 0:
			sumGain += diff
		else:
			sumLoss -= diff

	# Process special cases
	if sumGain == 0:
		return 0
	if sumLoss == 0:
		return 100

	# Calculate Relative strength
	RS = sumGain / sumLoss

	# Calculate corresponding RSI
	return 100 - (100 / (1 + RS))

"""
Calculate RSI
"""
def RSI(graph, window_size):
	# Init RSI
	RSI = [50] * len(graph)

	# Calculate RSI
	for i in range(window_size, len(graph)):
		RSI[i] = _RSI_(graph[i - window_size:i])
	return RSI