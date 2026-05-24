import numpy as np
import sounddevice as sd


class SignalGenerator:

    def __init__(self):

        self.stream = None

        self.phase = 0

    def stop(self):

        if self.stream:

            self.stream.stop()

            self.stream.close()

            self.stream = None

    def start_pink(self):

        self.stop()

        rows = 16

        state = np.zeros(rows)

        def callback(
                outdata,
                frames,
                time,
                status
        ):

            nonlocal state

            white = np.random.randn(
                frames,
                rows
            )

            state = (
                state
                +
                white.mean(
                    axis=0
                )
            )

            noise = np.random.randn(
                frames
            )

            pink = (
                noise
                +
                state.mean()
            )

            pink /= np.max(
                np.abs(
                    pink
                )
            )

            outdata[:, 0] = (
                pink
                *
                0.05
            )

        self.stream = (
            sd.OutputStream(

                channels=1,

                samplerate=48000,

                callback=callback
            )
        )

        self.stream.start()

    def start_sine(
            self,
            freq=1000
    ):

        self.stop()

        def callback(
                outdata,
                frames,
                time,
                status
        ):

            t = (
                np.arange(
                    frames
                )
                +
                self.phase
            )

            wave = np.sin(
                2
                *
                np.pi
                *
                freq
                *
                t
                /
                48000
            )

            self.phase += (
                frames
            )

            outdata[:, 0] = (
                wave
                *
                0.05
            )

        self.stream = (
            sd.OutputStream(

                channels=1,

                samplerate=48000,

                callback=callback
            )
        )

        self.stream.start()