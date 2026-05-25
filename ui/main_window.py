import csv

from PyQt6.QtWidgets import *

import pyqtgraph as pg

from audio.device_manager import list_input_devices

from audio.stream_engine import StreamEngine

from audio.signal_generator import SignalGenerator

from project.session import (
    save_session,
    load_session
)

from dsp.smoothing import smooth

class MainWindow(
    QMainWindow
):

    def __init__(self):

        super().__init__()

        self.last = None

        self.traces = []

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

        self.smoothing = 1

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

        clear = QPushButton(
            "Clear Traces"
        )

        clear.clicked.connect(
            self.clear_traces
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

        save_btn = QPushButton(
            "Save"
        )

        load_btn = QPushButton(
            "Load"
        )

        delay_btn = QPushButton(
            "Find Delay"
        )

        delay_btn.clicked.connect(
            self.show_delay
        )

        save_btn.clicked.connect(
            self.save_project
        )

        load_btn.clicked.connect(
            self.load_project
        )

        self.smooth_box = QComboBox()

        self.smooth_box.addItems([

            "Off",

            "1/24",

            "1/12",

            "1/6",

            "1/3"

        ])

        self.smooth_box.currentIndexChanged.connect(
            self.change_smoothing
        )

        for w in [

            self.devices,

            self.ref,

            self.meas,

            self.smooth_box,

            start,

            stop,

            pink,

            sine,

            gen_stop,

            snap,

            export,

            cal,

            save_btn,

            load_btn,

            clear,

            delay_btn

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

            smooth(

                mag,

                self.smoothing

            )
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

        if self.last is None:
            return

        (
            freq,
            mag,
            phase,
            coh,
            delay
        ) = self.last

        curve = self.mag.plot()

        curve.setData(
            freq,
            mag
        )

        self.traces.append(
            curve
        )

    def clear_traces(
            self
    ):

        for curve in self.traces:
            self.mag.removeItem(
                curve
            )

        self.traces.clear()

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

    def save_project(
            self
    ):

        file, _ = (
            QFileDialog.getSaveFileName(

                self,

                "Save Session",

                "",

                "*.osm"
            )
        )

        if not file:
            return

        data = {

            "device":
                self.devices.currentIndex(),

            "ref":
                self.ref.value(),

            "meas":
                self.meas.value(),

            "spl_offset":
                self.engine.spl.offset,

            "measurement":
                (
                    None
                    if
                    self.last
                    is None
                    else [

                        x.tolist()

                        if hasattr(
                            x,
                            "tolist"
                        )

                        else x

                        for x
                        in self.last
                    ]
                )
        }

        save_session(
            file,
            data
        )

    def load_project(
            self
    ):

        file, _ = (
            QFileDialog.getOpenFileName(

                self,

                "Load Session",

                "",

                "*.osm"
            )
        )

        if not file:
            return

        data = load_session(
            file
        )

        self.devices.setCurrentIndex(
            data[
                "device"
            ]
        )

        self.ref.setValue(
            data[
                "ref"
            ]
        )

        self.meas.setValue(
            data[
                "meas"
            ]
        )

        self.engine.spl.offset = (
            data[
                "spl_offset"
            ]
        )

        self.last = (
            data[
                "measurement"
            ]
        )

        if self.last:
            freq, mag, _, _, _ = (
                self.last
            )

            curve = (
                self.mag.plot()
            )

            curve.setData(
                freq,
                mag
            )

            self.traces.append(
                curve
            )


        QMessageBox.information(

            self,

            "Loaded",

            "Session restored"
        )

    def show_delay(
            self
    ):

        if self.last is None:
            return

        delay = (
            self.last[
                4
            ]
        )

        QMessageBox.information(

            self,

            "Delay",

            f"{delay:.2f} ms"
        )

    def change_smoothing(
            self,
            index
    ):

        mapping = [

            1,
            3,
            7,
            15,
            31
        ]

        self.smoothing = (
            mapping[
                index
            ]
        )