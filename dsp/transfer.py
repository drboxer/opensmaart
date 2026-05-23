import numpy as np


EPS = 1e-10


def transfer_analysis(
        reference,
        measurement,
        samplerate=48000
):

    reference = reference.flatten()
    measurement = measurement.flatten()

    ref = np.fft.rfft(reference)
    meas = np.fft.rfft(measurement)

    h = meas / (ref + EPS)

    magnitude = (
        20
        *
        np.log10(
            np.maximum(
                np.abs(h),
                EPS
            )
        )
    )

    phase = np.unwrap(
        np.angle(h)
    )

    phase = np.degrees(
        phase
    )

    coherence = (
        np.abs(
            h
        )
    )

    coherence = (
        coherence
        /
        np.max(
            coherence
        )
    )

    corr = np.correlate(
        measurement,
        reference,
        mode="full"
    )

    delay_samples = (
        np.argmax(
            corr
        )
        -
        (
            len(reference)
            -
            1
        )
    )

    delay_ms = (
        delay_samples
        /
        samplerate
        *
        1000
    )

    freq = np.fft.rfftfreq(
        len(reference),
        1 / samplerate
    )

    keep = (
        (freq >= 20)
        &
        (freq <= 20000)
    )

    return (
        freq[keep],
        magnitude[keep],
        phase[keep],
        coherence[keep],
        delay_ms
    )