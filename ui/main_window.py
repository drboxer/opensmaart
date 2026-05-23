from PyQt6.QtWidgets import *

import pyqtgraph as pg

from audio.device_manager import list_input_devices
from audio.stream_engine import StreamEngine


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.engine = StreamEngine()

        self.hold = None

        self.resize(
            1500,
            900
        )

        self.setWindowTitle(
            "OpenSmaart v0.5"
        )

        root = QWidget()

        layout = QVBoxLayout(
            root
        )

        controls = QHBoxLayout()

        self.devices = QComboBox()

        for d in list_input_devices():

            self.devices.addItem(
                d["name"],
                d["id"]
            )

        start = QPushButton(
            "Start"
        )

        stop = QPushButton(
            "Freeze"
        )

        reset = QPushButton(
            "Reset Hold"
        )

        start.clicked.connect(
            self.start_stream
        )

        stop.clicked.connect(
            self.engine.stop
        )

        reset.clicked.connect(
            self.reset_hold
        )

        controls.addWidget(
            self.devices
        )

        controls.addWidget(
            start
        )

        controls.addWidget(
            stop
        )

        controls.addWidget(
            reset
        )

        layout.addLayout(
            controls
        )

        self.plot = pg.PlotWidget()

        self.plot.setLogMode(
            x=True,
            y=False
        )

        self.plot.setXRange(
            np.log10(20),
            np.log10(20000)
        )

        self.curve = (
            self.plot.plot()
        )

        self.hold_curve = (
            self.plot.plot()
        )

        layout.addWidget(
            self.plot
        )

        self.meter = (
            QProgressBar()
        )

        layout.addWidget(
            self.meter
        )

        self.engine.fft_ready.connect(
            self.update_fft
        )

        self.engine.peak_ready.connect(
            self.update_peak
        )

        self.setCentralWidget(
            root
        )

    def start_stream(
            self
    ):

        self.engine.start(
            self.devices.currentData()
        )

    def update_fft(
            self,
            data
    ):

        freq, db = data

        self.curve.setData(
            freq,
            db
        )

        if (
            self.hold
            is None
        ):

            self.hold = db

        else:

            self.hold = (
                self.hold * 0.995
            )

            self.hold = (
                np.maximum(
                    self.hold,
                    db
                )
            )

        self.hold_curve.setData(
            freq,
            self.hold
        )

    def update_peak(
            self,
            value
    ):

        self.meter.setValue(
            int(
                value * 100
            )
        )

    def reset_hold(
            self
    ):

        self.hold = None


import numpy as np