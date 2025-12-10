from clini_data.storage import cargar_datos
from clini_data.ui_pyqt.main_window import MainWindow
from clini_data.ui_pyqt import resources
import sys
from PyQt5.QtWidgets import QApplication
import pathlib

if __name__ == "__main__":
    cargar_datos()

    app = QApplication(sys.argv)

    # Cargar QSS (si existe)
    qss_path = pathlib.Path(__file__).parent / "clini_data" / "ui_pyqt" / "styles.qss"
    if qss_path.exists():
        try:
            with open(qss_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print(f"No se pudo cargar styles.qss: {e}")

    # Set app icon si existe
    try:
        icon = resources.app_icon("logo_icon_64.png")
        if not icon.isNull():
            app.setWindowIcon(icon)
    except Exception:
        pass

    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())
