import sounddevice as sd
import numpy as np

from PyQt6.QtCore import (
    QObject,
    pyqtSignal
)

from dsp.transfer import (
    transfer_analysis
)


class StreamEngine(
    QObject
):

    transfer_ready = (
        pyqtSignal(
            object
        )
    )

    peak_ready = (
        pyqtSignal(
            float
        )
    )

    def __init__(
            self
    ):

        super().__init__()

        self.stream = None

    def start(
            self,
            device,
            ref,
            meas
    ):

        def callback(
                indata,
                frames,
                time,
                status
        ):

            try:

                reference = (
                    indata[
                        :,
                        ref
                    ]
                )

                measurement = (
                    indata[
                        :,
                        meas
                    ]
                )

            except Exception:

                return

            data = (
                transfer_analysis(
                    reference,
                    measurement
                )
            )

            peak = (
                np.max(
                    np.abs(
                        measurement
                    )
                )
            )

            self.transfer_ready.emit(
                data
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