import numpy as np


def compute_fft(samples):

    if len(samples) == 0:
        return [], []

    samples = samples.flatten()

    window = np.hanning(len(samples))

    spectrum = np.fft.rfft(samples * window)

    magnitude = np.abs(spectrum)

    db = 20 * np.log10(np.maximum(magnitude, 1e-10))

    freq = np.fft.rfftfreq(
        len(samples),
        1 / 48000
    )

    return freq, db