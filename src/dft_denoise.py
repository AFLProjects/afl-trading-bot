""" Simplify and denoise graphs using Discr Fourier Transform """
import dft_lib
import matplotlib.pyplot as plt

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
    s = [0]
    for i,v in enumerate(out):
        if i != 0 and i != N-1:
            if v-out[i-1] < 0 and out[i+1]-v > 0:
                plt.scatter(i,v,10,color="red")
                s.append(i)
                if(len(s) > 2):
                    _max_ = -1
                    _max_index_ = -1
                    for j in range(s[len(s)-1-1], s[len(s)-1]):
                        if graph[j] >= _max_:
                            _max_ = graph[j]
                            _max_index_ = j
                    for j in range(s[len(s)-2-1], s[len(s)-1-1]):
                        if graph[j] >= _max_:
                            _max_ = graph[j]
                            _max_index_ = j
                    plt.scatter(_max_index_,_max_,10,color="blue") 
            if v-out[i-1] > 0 and out[i+1]-v < 0:
                plt.scatter(i,v,10,color="black")
                s.append(i)
                if(len(s) > 2):
                    _min_ = 10e12
                    _min_index_ = -1
                    for j in range(s[len(s)-1-1], s[len(s)-1]):
                        if graph[j] <= _min_:
                            _min_ = graph[j]
                            _min_index_ = j
                    for j in range(s[len(s)-2-1], s[len(s)-1-1]):
                        if graph[j] <= _min_:
                            _min_ = graph[j]
                            _min_index_ = j
                    plt.scatter(_min_index_,_min_,10,color="blue") 
                        

    return out

        
    
