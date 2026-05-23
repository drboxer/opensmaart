from PyQt6.QtWidgets import *

import pyqtgraph as pg

from audio.device_manager import list_input_devices
from audio.stream_engine import StreamEngine


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.engine = StreamEngine()

        self.resize(1500, 900)

        self.setWindowTitle("OpenSmaart")

        root = QWidget()

        layout = QVBoxLayout(root)

        controls = QHBoxLayout()

        self.devices = QComboBox()

        for d in list_input_devices():

            self.devices.addItem(
                f'{d["id"]} | {d["name"]}',
                d["id"]
            )

        start = QPushButton("Start")

        stop = QPushButton("Stop")

        start.clicked.connect(self.start_stream)

        stop.clicked.connect(
            self.engine.stop
        )

        controls.addWidget(
            QLabel("Input")
        )

        controls.addWidget(
            self.devices
        )

        controls.addWidget(start)

        controls.addWidget(stop)

        layout.addLayout(
            controls
        )

        self.plot = pg.PlotWidget()

        self.curve = self.plot.plot()

        layout.addWidget(
            self.plot
        )

        self.meter = QProgressBar()

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

    def start_stream(self):

        device = (
            self.devices.currentData()
        )

        self.engine.start(
            device
        )

    def update_fft(self, data):

        x, y = data

        self.curve.setData(
            x,
            y
        )

    def update_peak(self, value):

        self.meter.setValue(
            int(value * 100)
        )