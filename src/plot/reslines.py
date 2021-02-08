from dft.dft import *
from dft.denoise import *
from math import *

# Only on constant trends
# Determine market resitance
# If market breaks resistance it is likely to grow
# The resistance line is now likely to be the new support line
# The trend will probably change
# Sometimes => false breakout
def determineHorizontalResistance(graph, threshold):
	maxValue = max(graph)
	minValue = maxValue
	count = 0
	for i, value in enumerate(graph):
		if value >= maxValue * (1 - threshold) and value <= maxValue * (1 + threshold):
			count += 1.0
			if value <= minValue:
				minValue = value
	graph.remove(maxValue)
	return (minValue,maxValue) if count > 2 else determineHorizontalResistance(graph, threshold)
		
# Only on constant trends
# Determine market support
# If market breaks support it is likely to decrease
# The support line is now likely to be the new resistance line
# The trend will probably change
# Sometimes => false breakout
def determineHorizontalSupport(graph, threshold):
	minValue = min(graph)
	maxValue = minValue
	count = 0
	for i, value in enumerate(graph):
		if value >= minValue * (1 - threshold) and value <= minValue * (1 + threshold):
			count += 1.0
			if value > maxValue:
				maxValue = value
	graph.remove(minValue)
	return (minValue,maxValue) if count > 2 else determineHorizontalSupport(graph, threshold)

"""
Add non horizontal resistance/support lines on uptrend or downtrend markets
"""

def determineMovingAverage(graph, window_size):
	L = len(graph) - window_size + 1
	return [sum(graph[i : i + window_size]) / window_size for i in range(L)]