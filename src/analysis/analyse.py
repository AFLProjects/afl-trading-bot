from dft.denoise import *
from analysis.analyse import *
from math import *

# Only on constant trends
# Determine market resitance
# If market breaks resistance it is likely to grow
# The resistance line is now likely to be the new support line
# The trend will probably change
# Sometimes => false breakout
def determineHorizontalResistance(graph, threshold):
	if len(graph) < 1:
		return (-1,-1)
	maxValue = max(graph)
	minValue = maxValue
	count = 0
	for i, value in enumerate(graph):
		if value >= maxValue - threshold and value <= maxValue + threshold:
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
	if len(graph) < 1:
		return (-1,-1)
	minValue = min(graph)
	maxValue = minValue
	count = 0
	for i, value in enumerate(graph):
		if value >= minValue - threshold and value <= minValue + threshold:
			count += 1.0
			if value > maxValue:
				maxValue = value
	graph.remove(minValue)
	return (minValue,maxValue) if count > 2 else determineHorizontalSupport(graph, threshold)

"""
Detect trends (cut the graph and check if the highs are increasing or not)
Add non horizontal resistance/support lines on uptrend or downtrend markets
"""
def determineMovingAverage(graph, window_size):
	L = len(graph) - window_size + 1
	return ([0]*(window_size+1)) + ([sum(graph[i : i + window_size]) / window_size for i in range(L)])