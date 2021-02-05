""" Simplify and denoise graphs using Discrete Fourier Transform """
import dft_lib

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
    dft_output = dft_lib.dftinv(dft_inverse_filter)
    return [dft_output[i].real for i in range(N)]
        
    
