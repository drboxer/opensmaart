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
            1000
        )

        self.setWindowTitle(
            "OpenSmaart v0.9"
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

        self.ref = QSpinBox()
        self.meas = QSpinBox()

        self.ref.setMinimum(1)
        self.meas.setMinimum(1)

        self.ref.setValue(1)
        self.meas.setValue(2)

        start = QPushButton(
            "Start"
        )

        stop = QPushButton(
            "Stop"
        )

        start.clicked.connect(
            self.start
        )

        stop.clicked.connect(
            self.engine.stop
        )

        controls.addWidget(
            QLabel("Device")
        )

        controls.addWidget(
            self.devices
        )

        controls.addWidget(
            QLabel("Ref")
        )

        controls.addWidget(
            self.ref
        )

        controls.addWidget(
            QLabel("Meas")
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

        self.mag_plot = (
            pg.PlotWidget()
        )

        self.mag_plot.setTitle(
            "Magnitude"
        )

        self.mag_plot.setLogMode(
            x=True
        )

        self.mag_curve = (
            self.mag_plot.plot()
        )

        layout.addWidget(
            self.mag_plot
        )

        self.phase_plot = (
            pg.PlotWidget()
        )

        self.phase_plot.setTitle(
            "Phase"
        )

        self.phase_plot.setLogMode(
            x=True
        )

        self.phase_curve = (
            self.phase_plot.plot()
        )

        layout.addWidget(
            self.phase_plot
        )

        self.meter = (
            QProgressBar()
        )

        layout.addWidget(
            self.meter
        )

        self.engine.transfer_ready.connect(
            self.update_plots
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

    def update_plots(
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

        self.mag_curve.setData(
            freq,
            mag
        )

        self.phase_curve.setData(
            freq,
            phase
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