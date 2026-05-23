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
        20 *
        np.log10(
            np.maximum(
                np.abs(h),
                EPS
            )
        )
    )

    phase = np.degrees(
        np.unwrap(
            np.angle(h)
        )
    )

    coherence = (
        np.abs(
            ref
            *
            np.conj(meas)
        )
    )

    coherence /= (
        np.maximum(
            np.max(coherence),
            EPS
        )
    )

    corr = np.correlate(
        measurement,
        reference,
        mode="full"
    )

    delay_samples = (
        np.argmax(corr)
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