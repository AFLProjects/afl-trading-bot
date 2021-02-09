""" Simplify and denoise graphs using Discrete Fourier Transform """
from analysis.fourier.dft import *
from math import *

# Find greatest value in an array within a range
def _max_(t, start, end):
    m = max(t[start:end])
    i = start + (t[start:end]).index(m)
    return (m,i)

# Find lowest value in an array within a range
def _min_(t, start, end):
    m = min(t[start:end])
    i = start + (t[start:end]).index(m)
    return (m,i)

# Initialize array
def Array(fill = 0, size = 0):
    return [fill] * size

# Linear interpolation
def linearInterpolation(t, p1, p2):
    for j in range(p1[1], p2[1]):
        dj = (p2[0] - p1[0]) / (p2[1] - p1[1])
        t[j] = p1[0] + (j - p1[1]) * dj

# Simplify graph curve, using Discrete Fourier Transform
def denoise(graph, _threshold_):
    # Create DFT from graph
    dft_complex = dft(graph)
    N = len(dft_complex)

    # Sort data and determine threshold percentile
    dft_graph_sorted  = [abs(dft_complex[i]) for i in range(N)]
    dft_graph_sorted.sort()
    threshold = dft_graph_sorted[int(floor(_threshold_ * float(N)))]

    # Apply filter on DFT
    dft_inverse_filter = [complex(0,0)] * N
    for i,c in enumerate(dft_complex):
        if abs(c) >= threshold:
            dft_inverse_filter[i] = c

    # Restore graph from filtered DFT
    out = dftinv(dft_inverse_filter)
    out = [out[i].real for i in range(N)]

    interpolation = Array(0, N)     # Interpolated spikes
    previousSpike = [graph[0], 0]   # Prevous spike
    spikes = Array(0, 1)            # Spikes on DFT
    newSpikesUp = Array(0, 0)
    newSpikesDown = Array(0, 0)

    # Determine corresponding spikes on the graph and interpolate
    for i, value in enumerate(out):
        if i != 0 and i != N-1:
            if value - out[i-1] < 0 and out[i+1] - value > 0:
                spikes.append(i)
                L = len(spikes)
                if L > 2:
                    point = _max_(graph, spikes[L-3], spikes[L-1])
                    linearInterpolation(interpolation, previousSpike, point)
                    previousSpike = point
                    newSpikesUp.append(previousSpike[0])
            elif value - out[i-1] > 0 and out[i+1] - value < 0:
                spikes.append(i)
                L = len(spikes)
                if L > 2:
                    point = _min_(graph, spikes[L-3], spikes[L-1])
                    linearInterpolation(interpolation, previousSpike, point)
                    previousSpike = point
                    newSpikesDown.append(previousSpike[0])
        if i == N-1:
            point = [out[spikes[len(spikes)-1]], spikes[len(spikes)-1]]
            if out[point[1]] - out[point[1]-1] > 0 and out[point[1]+1] - out[point[1]] < 0:
                point = _max_(graph, previousSpike[1], N-1)
                newSpikesDown.append(previousSpike[0])
            else:
                point = _min_(graph, previousSpike[1], N-1)
                newSpikesUp.append(previousSpike[0])
            spikes.append(point[1])
            linearInterpolation(interpolation, previousSpike, point)
            previousSpike = point
            point = [graph[N-1], N-1]
            for j in range(previousSpike[1], point[1]+1):
                dj = (point[0] - previousSpike[0]) / (point[1] - previousSpike[1])
                interpolation[j] = previousSpike[0] + (j - previousSpike[1]) * dj
    return [interpolation,newSpikesUp,newSpikesDown]

        
    
