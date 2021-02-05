""" Simplify and denoise graphs using Discr Fourier Transform """
import dft_lib
import matplotlib.pyplot as plt

# Find greatest value in an array within a range
def _max_(t, start, end):
    _max_index_ = -1
    _max_ = -1
    for j in range(start, end):
        if t[j] >= _max_:
            _max_ = t[j]
            _max_index_ = j
    return [_max_,_max_index_]

# Find lowest value in an array within a range
def _min_(t, start, end):
    _min_index_ = -1
    _min_ = 10e12
    for j in range(start, end):
        if t[j] <= _min_:
            _min_ = t[j]
            _min_index_ = j
    return [_min_, _min_index_]

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

    # Sync sinusoidal spikes with graph spikes
    pts = [0]
    for i, value in enumerate(out):
        if i != 0 and i != N-1:

            # Detect spike on Simplified curve
            if value - out[i-1] < 0 and out[i+1] - value > 0:
                pts.append(i)
                K = len(pts)
                if len(pts) > 2:
                    # Find corresponding spike on graph
                    right = _max_(graph, pts[K - 2], pts[K - 1])
                    left = _max_(graph, pts[K - 3], pts[K - 2])
                    maxv = max2(left, right)

            # Detect spike on Simplified curve
            if value - out[i-1] > 0 and out[i+1] - value < 0:
                pts.append(i)
                K = len(pts)
                if len(pts) > 2:
                    # Find corresponding spike on graph
                    right = _min_(graph, pts[K - 2], pts[K - 1])
                    left = _min_(graph, pts[K - 3], pts[K - 2])
                    minv = min2(left, right)
                        

    return out

        
    
