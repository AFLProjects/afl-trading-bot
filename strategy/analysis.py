from math import *

def MA(graph, window_size):
	L = len(graph) - window_size + 1
	return [sum(graph[i : i + window_size]) / window_size for i in range(L)]

def EMA(graph, window_size):
	k = (2.0 / (window_size + 1.0))
	previousEMA = sum(graph[i] for i in range(window_size)) / window_size
	EMA = [None] * len(graph)
	EMA[0] = previousEMA
	for i in range(1, len(graph)):
		EMA[i] = graph[i] * k + previousEMA * (1 - k)
		previousEMA = EMA[i]
	return EMA

def averageGain(data, offset, window_size):
	avgG = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr > 0:
			avgG += nxt - curr
	avgG /= window_size
	return avgG

def averageLoss(data, offset, window_size):
	avgL = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr < 0:
			avgL += abs(nxt - curr)
	avgL /= window_size
	return avgL

def gain(data, offset, window_size):
	gain = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr > 0:
			gain += nxt - curr
	return gain

def loss(data, offset, window_size):
	loss = 0
	for j in range(window_size):
		curr = data[offset+j-window_size]
		nxt = data[offset+j-window_size+1]
		if nxt - curr > 0:
			loss += abs(nxt - curr)
	return loss

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

def RSI(graph, window_size):
	RSI = [50] * len(graph)
	for i in range(window_size, len(graph)):
		RSI[i] = _RSI_(graph[i - window_size:i])
	return RSI