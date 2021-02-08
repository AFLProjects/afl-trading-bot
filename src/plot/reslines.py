from dft.dft import *
from dft.denoise import *
from math import *

# Determine market resitance
# If market breaks resistance it is likely to grow
# The resistance line is now likely to be the new support line
# Sometimes => false breakout
def determineHorizontalResistance(graph, threshold):
	maxValue = max(graph)
	average = 0.0
	count = 0.0
	for i, value in enumerate(graph):
		if value >= maxValue * (1 - threshold) and value <= maxValue * (1 + threshold):
			count += 1.0
			average += value
	average /= count
	graph = graph.remove(maxValue)
	return average if count >= 2 else determineHorizontalResistance(graph, threshold)
		

# Determine market support
# If market breaks support it is likely to decrease
# The support line is now likely to be the new resistance line
# Sometimes => false breakout
def determineHorizontalSupport(graph, threshold):
	minValue = min(graph)
	average = 0.0
	count = 0.0
	for i, value in enumerate(graph):
		if value >= minValue * (1 - threshold) and value <= minValue * (1 + threshold):
			count += 1.0
			average += value
	average /= count
	graph = graph.remove(minValue)
	return average if count >= 2 else determineHorizontalSupport(graph, threshold)

def determineMovingAverage(graph, window_size):
	L = len(graph) - window_size + 1
	return [sum(graph[i : i + window_size]) / window_size for i in range(L)]