""" Simplify and denoise graphs using Discrete Fourier Transform """
import dft_lib
import matplotlib.pyplot as plt

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
    plt.plot(out)

    interpolation = Array(0, N-1)     # Interpolated spikes
    previousSpike = [graph[0], 0]   # Prevous spike
    spikes = Array(0, 1)            # Spikes on DFT

    # Determine corresponding spikes on the graph and interpolate
    for i, value in enumerate(out):
        if i != 0 and i != N-1:
            if value - out[i-1] < 0 and out[i+1] - value > 0:
                spikes.append(i)
                L = len(spikes)
                if L > 2:
                    point = _max_(graph, spikes[L-3], spikes[L-1])
                    for j in range(previousSpike[1], point[1]):
                        dj = (point[0] - previousSpike[0]) / (point[1] - previousSpike[1])
                        interpolation[j] = previousSpike[0] + (j - previousSpike[1]) * dj
                    previousSpike = point
                    plt.scatter(previousSpike[1], previousSpike[0], 10, color="black")
            elif value - out[i-1] > 0 and out[i+1] - value < 0:
                spikes.append(i)
                L = len(spikes)
                if L > 2:
                    point = _min_(graph, spikes[L-3], spikes[L-1])
                    for j in range(previousSpike[1], point[1]):
                        dj = (point[0] - previousSpike[0]) / (point[1] - previousSpike[1])
                        interpolation[j] = previousSpike[0] + (j - previousSpike[1]) * dj
                    previousSpike = point
                    plt.scatter(previousSpike[1], previousSpike[0], 10, color="black")
        if i == N-1:
            point = [out[spikes[len(spikes)-1]], spikes[len(spikes)-1]]
            spikes.append(point[1])
            for j in range(previousSpike[1], point[1]):
                dj = (point[0] - previousSpike[0]) / (point[1] - previousSpike[1])
                interpolation[j] = previousSpike[0] + (j - previousSpike[1]) * dj
            previousSpike = point
            plt.scatter(previousSpike[1], previousSpike[0], 10, color="black")
            point = [graph[N-1], N-1]
            spikes.append(point[1])
            for j in range(previousSpike[1], point[1]):
                dj = (point[0] - previousSpike[0]) / (point[1] - previousSpike[1])
                interpolation[j] = previousSpike[0] + (j - previousSpike[1]) * dj
            previousSpike = point
            plt.scatter(previousSpike[1], previousSpike[0], 10, color="black")
    return interpolation

        
    
