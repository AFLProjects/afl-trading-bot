""" Simplify and denoise graphs using Discr Fourier Transform """
import dft_lib
import matplotlib.pyplot as plt

# Find greatest value in an array within a range
def _max_(t, start, end):
    m = max(t[start:end])
    i = start + (t[start:end]).index(m)
    return [m,i]

# Find lowest value in an array within a range
def _min_(t, start, end):
    m = min(t[start:end])
    i = start + (t[start:end]).index(m)
    return [m,i]

# Greatest value between two values [value,index]
def max2(x1, x2):
    return x1 if x1[0] >= x2[0] else x2

# Lowest value between two values [value,index]
def min2(x1, x2):
    return x1 if x1[0] <= x2[0] else x2

# Simplify graph curve, using Discrete Fourier Transform
def denoise(graph, _threshold_):
    # Create DFT from graph
    dft_complex = dft_lib.dft(graph)
    N = len(dft_complex)

    # Sort data and determine threshold percentile
    dft_graph_sorted  = [abs(dft_complex[i]) for i in range(N)]
    dft_graph_sorted.sort()
    threshold = dft_graph_sorted[int(round(_threshold_ * float(N)))]

    # Apply filter on DFT
    dft_inverse_filter = [complex(0,0)] * N
    for i,c in enumerate(dft_complex):
        if abs(c) >= threshold:
            dft_inverse_filter[i] = c

    # Restore graph from filtered DFT
    out = dft_lib.dftinv(dft_inverse_filter)
    out = [out[i].real for i in range(N)]

    # Determine spikes on the graph
    pts = [0]
    _out_ = [None] * N
    prevPoint = [graph[0], 0]
    for i, value in enumerate(out):
        if i != 0 and i != N-1:
            if value - out[i-1] < 0 and out[i+1] - value > 0:
                pts.append(i)
                L = len(pts)
                if L > 2:
                    right = _max_(graph, pts[L-2], pts[L-1])
                    left = _max_(graph, pts[L-3], pts[L-2])
                    point = max2(left, right)
                    for j in range(prevPoint[1], point[1]):
                        dj = (point[0] - prevPoint[0]) / (point[1] - prevPoint[1])
                        _out_[j] = prevPoint[0] + (j-prevPoint[1]) * dj
                    prevPoint = point
            elif value - out[i-1] > 0 and out[i+1] - value < 0:
                pts.append(i)
                L = len(pts)
                if L > 2:
                    right = _min_(graph, pts[L-2], pts[L-1])
                    left = _min_(graph, pts[L-3], pts[L-2])
                    point = min2(left, right)
                    for j in range(prevPoint[1], point[1]):
                        dj = (point[0] - prevPoint[0]) / (point[1] - prevPoint[1])
                        _out_[j] = prevPoint[0] + (j-prevPoint[1]) * dj
                    prevPoint = point
    return _out_

        
    
