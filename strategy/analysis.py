from dft.denoise import *
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

