from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QMessageBox
try:
    from .. import services
except Exception:
    services = None

class HistorialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Historial de Cambios")
        self.setFixedSize(600, 420)

        v = QVBoxLayout()
        self.setLayout(v)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        v.addWidget(self.text)

        btn_refresh = QPushButton("Refrescar")
        btn_refresh.clicked.connect(self.cargar_historial)
        v.addWidget(btn_refresh)

        self.cargar_historial()

    def cargar_historial(self):
        self.text.clear()
        historial = None
        if services and hasattr(services, "obtener_historial"):
            try:
                historial = services.obtener_historial()
            except Exception as e:
                QMessageBox.warning(self, "Aviso", f"Error al obtener historial via services: {e}")
        if historial is None:
            self.text.setPlainText("No hay historial disponible o services.obtener_historial no implementado.")
            return
        lines = []
        for e in historial:
            lines.append(f"Usuario: {e.get('usuario')}")
            lines.append(f"Acción: {e.get('accion')}")
            lines.append(f"Detalle: {e.get('detalle')}")
            lines.append(f"Fecha y hora: {e.get('fecha_hora')}")
            lines.append("-"*60)
        self.text.setPlainText("\n".join(lines))