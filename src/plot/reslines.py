from dft.dft import *
from dft.denoise import *
from math import *

def determineResistance(graph, threshold):
	maxValue = max(graph)
	average = 0.0
	count = 0.0
	for i, value in enumerate(graph):
		if value >= maxValue * (1 - threshold) and value <= maxValue * (1 + threshold):
			count += 1.0
			average += value
	average /= count
	graph.remove(maxValue)
	return average if count >= 2 else determineResistance(graph, threshold)
		

def determineSupport(graph, threshold):
	minValue = min(graph)
	average = 0.0
	count = 0.0
	for i, value in enumerate(graph):
		if value >= minValue * (1 - threshold) and value <= minValue * (1 + threshold):
			count += 1.0
			average += value
	average /= count
	graph.remove(minValue)
	return average if count >= 2 else determineSupport(graph, threshold)

