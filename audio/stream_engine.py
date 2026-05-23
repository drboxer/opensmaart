import sounddevice as sd
import numpy as np

from PyQt6.QtCore import (
    QObject,
    pyqtSignal
)

from dsp.fft import compute_fft


class StreamEngine(QObject):

    fft_ready = pyqtSignal(object)

    peak_ready = pyqtSignal(float)

    def __init__(self):

        super().__init__()

        self.stream = None

    def start(
            self,
            device,
            reference_ch,
            measurement_ch
    ):

        def callback(
                indata,
                frames,
                time,
                status
        ):

            try:

                ref = np.copy(
                    indata[
                        :,
                        reference_ch
                    ]
                )

                meas = np.copy(
                    indata[
                        :,
                        measurement_ch
                    ]
                )

            except Exception:

                return

            rf, rd = compute_fft(
                ref
            )

            mf, md = compute_fft(
                meas
            )

            peak = max(
                np.max(
                    np.abs(ref)
                ),
                np.max(
                    np.abs(meas)
                )
            )

            self.fft_ready.emit(
                (
                    rf,
                    rd,
                    mf,
                    md
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

                blocksize=2048,

                callback=callback
            )
        )

        self.stream.start()

    def stop(self):

        if self.stream:

            self.stream.stop()

            self.stream.close()

            self.stream = None