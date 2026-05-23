import numpy as np


def smooth(signal, amount=8):

    kernel = np.ones(amount)

    kernel /= amount

    return np.convolve(
        signal,
        kernel,
        mode="same"
    )


def compute_fft(
        samples,
        samplerate=48000
):

    if len(samples) == 0:

        return [], []

    samples = samples.flatten()

    samples *= np.hanning(
        len(samples)
    )

    fft = np.fft.rfft(
        samples
    )

    magnitude = np.abs(
        fft
    )

    db = 20 * np.log10(
        np.maximum(
            magnitude,
            1e-10
        )
    )

    db = smooth(
        db,
        amount=10
    )

    freq = np.fft.rfftfreq(
        len(samples),
        1 / samplerate
    )

    keep = (
        (freq >= 20)
        &
        (freq <= 20000)
    )

    return (
        freq[keep],
        db[keep]
    )