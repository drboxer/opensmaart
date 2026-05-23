import numpy as np

def compute_fft(samples):
    if len(samples)==0:
        return np.array([])
    w=np.hanning(len(samples))
    y=np.abs(np.fft.rfft(samples*w))
    return 20*np.log10(np.maximum(y,1e-12))