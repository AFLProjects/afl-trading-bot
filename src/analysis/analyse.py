from dft.denoise import *
from analysis.analyse import *
from math import *

def determineMovingAverage(graph, window_size):
	L = len(graph) - window_size + 1
	return [sum(graph[i : i + window_size]) / window_size for i in range(L)]

def determineEMA(graph, window_size, start):
	k = (2.0 / (window_size + 1.0))
	previousEMA = start
	EMA = [None] * len(graph)
	for i in range(len(graph)):
		EMA[i] = graph[i] * k + previousEMA * (1 - k)
		previousEMA = EMA[i]
	return EMA
