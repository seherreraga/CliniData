from PyQt5.QtWidgets import QApplication
from clini_data.ui_pyqt import resources
import pathlib

app = QApplication(sys.argv)

# Cargar QSS
qss_path = pathlib.Path(__file__).parent / "clini_data" / "ui_pyqt" / "styles.qss"
if qss_path.exists():
    with open(qss_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
