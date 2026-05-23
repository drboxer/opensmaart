from PyQt6.QtWidgets import *
import pyqtgraph as pg
from audio.device_manager import list_input_devices
from audio.stream_engine import StreamEngine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine=StreamEngine()

        self.setWindowTitle("OpenSmaart v0.3")
        self.resize(1400,850)

        root=QWidget()
        layout=QVBoxLayout(root)

        controls=QHBoxLayout()

        self.device=QComboBox()
        for idx,name,ch in list_input_devices():
            self.device.addItem(f"{idx} | {name} | IN:{ch}", idx)

        self.sr=QComboBox()
        self.sr.addItems(["44100","48000","96000"])

        self.channel=QSpinBox()
        self.channel.setMinimum(1)
        self.channel.setMaximum(32)

        start=QPushButton("Start")
        stop=QPushButton("Stop")
        start.clicked.connect(self.engine.start)
        stop.clicked.connect(self.engine.stop)

        controls.addWidget(QLabel("Input"))
        controls.addWidget(self.device)
        controls.addWidget(QLabel("Sample Rate"))
        controls.addWidget(self.sr)
        controls.addWidget(QLabel("Channel"))
        controls.addWidget(self.channel)
        controls.addWidget(start)
        controls.addWidget(stop)

        layout.addLayout(controls)

        graph=pg.PlotWidget(title="Live FFT / RTA (placeholder)")
        graph.setLabel("left","Level (dB)")
        graph.setLabel("bottom","Frequency")
        graph.plot([20,100,1000,10000,20000],[-70,-20,-15,-30,-60])

        layout.addWidget(graph)

        peak=QProgressBar()
        peak.setValue(0)

        layout.addWidget(QLabel("Peak"))
        layout.addWidget(peak)

        self.setCentralWidget(root)