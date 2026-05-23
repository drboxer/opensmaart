import sounddevice as sd
import numpy as np

from PyQt6.QtCore import (
    QObject,
    pyqtSignal
)

from dsp.transfer import (
    transfer_analysis
)


class StreamEngine(QObject):

    transfer_ready = pyqtSignal(object)

    peak_ready = pyqtSignal(float)

    def __init__(self):

        super().__init__()

        self.stream = None

        self.avg_mag = None
        self.avg_phase = None
        self.avg_coh = None

        self.alpha = 0.20

    def smooth(
            self,
            current,
            previous
    ):

        if previous is None:

            return current

        return (
            self.alpha
            *
            current
            +
            (
                1
                -
                self.alpha
            )
            *
            previous
        )

    def start(
            self,
            device,
            ref,
            meas
    ):

        self.stop()

        def callback(
                indata,
                frames,
                time,
                status
        ):

            try:

                reference = (
                    indata[:, ref]
                )

                measurement = (
                    indata[:, meas]
                )

            except Exception:

                return

            (
                freq,
                mag,
                phase,
                coh,
                delay
            ) = transfer_analysis(
                reference,
                measurement
            )

            self.avg_mag = self.smooth(
                mag,
                self.avg_mag
            )

            self.avg_phase = self.smooth(
                phase,
                self.avg_phase
            )

            self.avg_coh = self.smooth(
                coh,
                self.avg_coh
            )

            rms = np.sqrt(
                np.mean(
                    measurement ** 2
                )
            )

            peak_db = (
                20
                *
                np.log10(
                    max(
                        rms,
                        1e-9
                    )
                )
            )

            self.transfer_ready.emit(
                (
                    freq,
                    self.avg_mag,
                    self.avg_phase,
                    self.avg_coh,
                    delay
                )
            )

            self.peak_ready.emit(
                peak_db
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