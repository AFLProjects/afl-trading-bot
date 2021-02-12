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

def RSI(graph, window_size):
	RSI = [50] * len(graph)
	for i in range(window_size, len(graph)):
		avgG = 0
		avgL = 0
		for j in range(window_size):
			curr = graph[i+j-window_size]
			nxt = graph[i+j-window_size+1]
			if nxt - curr > 0:
				avgG += nxt - curr
			else:
				avgL += abs(nxt - curr)
		avgG /= window_size
		avgL /= window_size
		if avgL == 0:
			RSI[i] = 100.0
		else:
			RSI[i] = 100.0 - (100.0 / (1.0 + (avgG / avgL)))
	return RSI