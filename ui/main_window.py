import numpy as np

from PyQt6.QtWidgets import *

import pyqtgraph as pg

from audio.device_manager import (
    list_input_devices
)

from audio.stream_engine import (
    StreamEngine
)


class MainWindow(
    QMainWindow
):

    def __init__(self):

        super().__init__()

        self.engine = (
            StreamEngine()
        )

        self.resize(
            1600,
            900
        )

        self.setWindowTitle(
            "OpenSmaart v0.6"
        )

        root = QWidget()

        layout = (
            QVBoxLayout(
                root
            )
        )

        controls = (
            QHBoxLayout()
        )

        self.devices = (
            QComboBox()
        )

        for d in (
                list_input_devices()
        ):

            self.devices.addItem(
                d["name"],
                d["id"]
            )

        self.ref = (
            QSpinBox()
        )

        self.meas = (
            QSpinBox()
        )

        self.ref.setMinimum(
            1
        )

        self.meas.setMinimum(
            1
        )

        self.ref.setValue(
            1
        )

        self.meas.setValue(
            2
        )

        start = (
            QPushButton(
                "Start"
            )
        )

        stop = (
            QPushButton(
                "Stop"
            )
        )

        start.clicked.connect(
            self.start
        )

        stop.clicked.connect(
            self.engine.stop
        )

        controls.addWidget(
            QLabel(
                "Device"
            )
        )

        controls.addWidget(
            self.devices
        )

        controls.addWidget(
            QLabel(
                "Ref"
            )
        )

        controls.addWidget(
            self.ref
        )

        controls.addWidget(
            QLabel(
                "Meas"
            )
        )

        controls.addWidget(
            self.meas
        )

        controls.addWidget(
            start
        )

        controls.addWidget(
            stop
        )

        layout.addLayout(
            controls
        )

        self.plot = (
            pg.PlotWidget()
        )

        self.plot.setLogMode(
            x=True
        )

        self.transfer_curve = (
            self.plot.plot()
        )

        self.meas_curve = (
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

        self.engine.transfer_ready.connect(
            self.update_plot
        )

        self.engine.peak_ready.connect(
            self.update_peak
        )

        self.setCentralWidget(
            root
        )

    def start(
            self
    ):

        self.engine.start(

            self.devices.currentData(),

            self.ref.value()
            -
            1,

            self.meas.value()
            -
            1
        )

    def update_plot(
            self,
            data
    ):
        (
            freq,
            mag,
            phase,
            coh,
            delay
        ) = data

        self.transfer_curve.setData(
            freq,
            mag
        )

        self.setWindowTitle(
            (
                "OpenSmaart "
                f"| Delay "
                f"{delay:.2f} ms"
            )
        )

    def update_peak(
            self,
            value
    ):

        self.meter.setValue(
            int(
                value
                *
                100
            )
        )