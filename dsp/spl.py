import numpy as np


class SPLMeter:

    def __init__(self):

        self.offset = 94.0

    def calibrate(
            self,
            measured,
            target
    ):

        self.offset += (
            target
            -
            measured
        )

    def compute(
            self,
            samples
    ):

        rms = np.sqrt(
            np.mean(
                samples ** 2
            )
        )

        rms = max(
            rms,
            1e-9
        )

        dbfs = (
            20
            *
            np.log10(
                rms
            )
        )

        return (
            dbfs
            +
            self.offset
        )