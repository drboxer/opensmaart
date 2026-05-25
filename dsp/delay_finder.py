import numpy as np


def estimate_delay(
        reference,
        measurement,
        samplerate=48000
):

    corr = np.correlate(
        measurement,
        reference,
        mode="full"
    )

    shift = (
        np.argmax(
            corr
        )
        -
        len(
            reference
        )
        +
        1
    )

    return (
        shift
        /
        samplerate
        *
        1000
    )