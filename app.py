import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())