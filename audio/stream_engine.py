import sounddevice as sd

import numpy as np

from PyQt6.QtCore import (
    QObject,
    pyqtSignal
)

from dsp.transfer import (
    transfer_function
)


class StreamEngine(
    QObject
):

    tf_ready = pyqtSignal(
        object
    )

    peak_ready = pyqtSignal(
        float
    )

    def __init__(
            self
    ):

        super().__init__()

        self.stream = None

    def start(

            self,

            device,

            ref_ch,

            meas_ch
    ):

        def callback(

                indata,

                frames,

                time,

                status
        ):

            try:

                ref = (
                    indata[
                        :,
                        ref_ch
                    ]
                )

                meas = (
                    indata[
                        :,
                        meas_ch
                    ]
                )

            except Exception:

                return

            freq, mag = (
                transfer_function(
                    ref,
                    meas
                )
            )

            peak = (
                np.max(
                    np.abs(
                        meas
                    )
                )
            )

            self.tf_ready.emit(
                (
                    freq,
                    mag
                )
            )

            self.peak_ready.emit(
                peak
            )

        self.stream = (
            sd.InputStream(

                device=device,

                channels=2,

                samplerate=48000,

                blocksize=4096,

                callback=callback
            )
        )

        self.stream.start()

    def stop(
            self
    ):

        if self.stream:

            self.stream.stop()

            self.stream.close()

            self.stream = None