import numpy as np


def transfer_function(
        reference,
        measurement
):

    eps = 1e-10

    ref_fft = np.fft.rfft(
        reference
    )

    meas_fft = np.fft.rfft(
        measurement
    )

    h = (
        meas_fft
        /
        (
            ref_fft
            +
            eps
        )
    )

    magnitude = (
        20
        *
        np.log10(
            np.maximum(
                np.abs(h),
                eps
            )
        )
    )

    freq = np.fft.rfftfreq(
        len(reference),
        1 / 48000
    )

    keep = (
        (freq >= 20)
        &
        (freq <= 20000)
    )

    return (
        freq[keep],
        magnitude[keep]
    )