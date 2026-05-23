import sounddevice as sd
import numpy as np

from PyQt6.QtCore import QObject, pyqtSignal

from dsp.fft import compute_fft


class StreamEngine(QObject):

    fft_ready = pyqtSignal(object)
    peak_ready = pyqtSignal(float)

    def __init__(self):

        super().__init__()

        self.stream = None

    def start(self, device):

        def callback(indata, frames, time, status):

            samples = np.copy(indata[:, 0])

            freq, db = compute_fft(samples)

            peak = float(np.max(np.abs(samples)))

            self.fft_ready.emit((freq, db))
            self.peak_ready.emit(peak)

        self.stream = sd.InputStream(
            device=device,
            channels=1,
            samplerate=48000,
            blocksize=2048,
            callback=callback
        )

        self.stream.start()

    def stop(self):

        if self.stream:

            self.stream.stop()
            self.stream.close()

            self.stream = None