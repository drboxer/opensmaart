import csv

from PyQt6.QtWidgets import *

import pyqtgraph as pg

from audio.device_manager import list_input_devices

from audio.stream_engine import StreamEngine

from audio.signal_generator import SignalGenerator


class MainWindow(
    QMainWindow
):

    def __init__(self):

        super().__init__()

        self.last = None

        self.engine = (
            StreamEngine()
        )

        self.generator = (
            SignalGenerator()
        )

        self.resize(
            1700,
            1100
        )

        root = QWidget()

        layout = QVBoxLayout(root)

        top = QHBoxLayout()

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

        self.ref.setValue(1)

        self.meas.setValue(2)

        start = QPushButton(
            "Start"
        )

        stop = QPushButton(
            "Stop"
        )

        pink = QPushButton(
            "Pink"
        )

        sine = QPushButton(
            "1 kHz"
        )

        gen_stop = QPushButton(
            "Stop Gen"
        )

        cal = QPushButton(
            "Calibrate"
        )

        cal.clicked.connect(
            self.calibrate
        )

        pink.clicked.connect(
            self.generator.start_pink
        )

        sine.clicked.connect(
            lambda:
            self.generator.start_sine(
                1000
            )
        )

        gen_stop.clicked.connect(
            self.generator.stop
        )

        snap = QPushButton(
            "Snapshot"
        )

        export = QPushButton(
            "Export CSV"
        )

        start.clicked.connect(
            self.start
        )

        stop.clicked.connect(
            self.engine.stop
        )

        snap.clicked.connect(
            self.snapshot
        )

        export.clicked.connect(
            self.export
        )

        for w in [

            self.devices,

            self.ref,

            self.meas,

            start,

            stop,

            pink,

            sine,

            gen_stop,

            snap,

            export,

            cal

        ]:

            top.addWidget(
                w
            )

        layout.addLayout(
            top
        )

        self.mag = (
            pg.PlotWidget()
        )

        self.phase = (
            pg.PlotWidget()
        )

        self.coh = (
            pg.PlotWidget()
        )

        self.mag_curve = (
            self.mag.plot()
        )

        self.phase_curve = (
            self.phase.plot()
        )

        self.coh_curve = (
            self.coh.plot()
        )

        layout.addWidget(
            self.mag
        )

        layout.addWidget(
            self.phase
        )

        layout.addWidget(
            self.coh
        )

        self.meter = (
            QProgressBar()
        )

        self.spl_label = QLabel(
            "0.0 dB SPL"
        )

        layout.addWidget(
            self.spl_label
        )

        layout.addWidget(
            self.meter
        )

        layout.addWidget(
            self.mag
        )

        layout.addWidget(
            self.phase
        )

        layout.addWidget(
            self.coh
        )

        self.engine.transfer_ready.connect(
            self.update
        )

        self.setCentralWidget(
            root
        )

        self.engine.peak_ready.connect(
            self.update_peak
        )

    def start(
            self
    ):

        self.engine.start(

            self.devices.currentData(),

            self.ref.value() - 1,

            self.meas.value() - 1
        )

    def update(
            self,
            data
    ):

        self.last = data

        freq, mag, phase, coh, delay = data

        self.mag_curve.setData(
            freq,
            mag
        )

        self.phase_curve.setData(
            freq,
            phase
        )

        self.coh_curve.setData(
            freq,
            coh
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

        self.spl_label.setText(
            f"{value:.1f} dB SPL"
        )

        normalized = max(
            0,
            min(
                100,
                value
            )
        )

        self.meter.setValue(
            int(
                normalized
            )
        )

    def snapshot(
            self
    ):

        if not self.last:

            return

        freq, mag, _, _, _ = (
            self.last
        )

        self.mag.plot(
            freq,
            mag
        )

    def export(
            self
    ):

        if not self.last:

            return

        file, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Export",
                "",
                "*.csv"
            )
        )

        if not file:

            return

        freq, mag, phase, coh, _ = (
            self.last
        )

        with open(
                file,
                "w",
                newline=""
        ) as f:

            writer = (
                csv.writer(
                    f
                )
            )

            writer.writerow(
                [
                    "Freq",
                    "Mag",
                    "Phase",
                    "Coherence"
                ]
            )

            for r in zip(
                    freq,
                    mag,
                    phase,
                    coh
            ):

                writer.writerow(
                    r
                )

    def calibrate(
            self
    ):

        value, ok = (
            QInputDialog.getDouble(

                self,

                "Calibration",

                "Measured SPL:",

                94.0,

                40,

                140,

                1
            )
        )

        if not ok:
            return

        if (
                getattr(
                    self,
                    "last",
                    None
                )
                is None
        ):
            QMessageBox.warning(

                self,

                "No Data",

                "Run measurement first"

            )

            return

        freq, mag, phase, coh, delay = (
            self.last
        )

        dummy = (
                mag
                /
                100
        )

        self.engine.calibrate_spl(

            value,

            dummy
        )

        QMessageBox.information(

            self,

            "Done",

            f"Calibrated to {value:.1f} dB SPL"
        )