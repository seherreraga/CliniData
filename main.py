from clini_data.storage import cargar_datos
from clini_data.ui_pyqt.main_window import MainWindow
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    # Carga datos (usa las funciones del módulo storage existente)
    cargar_datos()

    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())
