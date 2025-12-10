from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTextEdit, QMessageBox, QWidget, QHBoxLayout
try:
    from .. import analytics
except Exception:
    analytics = None

class AnalisisWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Análisis y Visualización")
        self.setFixedSize(640, 480)

        v = QVBoxLayout()
        self.setLayout(v)

        self.text_res = QTextEdit()
        self.text_res.setReadOnly(True)
        v.addWidget(self.text_res)

        h = QHBoxLayout()
        btn_resumen = QPushButton("Generar resumen")
        btn_predecir = QPushButton("Predecir próximo mes")
        btn_fetch = QPushButton("Obtener datos públicos (ej.)")
        h.addWidget(btn_resumen)
        h.addWidget(btn_predecir)
        h.addWidget(btn_fetch)
        v.addLayout(h)

        btn_resumen.clicked.connect(self.mostrar_resumen)
        btn_predecir.clicked.connect(self.predecir)
        btn_fetch.clicked.connect(self.fetch_public)

    def mostrar_resumen(self):
        if analytics and hasattr(analytics, "analizar_datos"):
            try:
                resumen = analytics.analizar_datos()
            except Exception as e:
                resumen = f"Error al generar análisis: {e}"
        else:
            resumen = "Módulo analytics no disponible."
        self.text_res.setPlainText(resumen)

    def predecir(self):
        if analytics and hasattr(analytics, "predecir_citas_proximo_mes"):
            try:
                pred, texto = analytics.predecir_citas_proximo_mes()
                if pred is None:
                    QMessageBox.information(self, "Predicción", texto)
                else:
                    oper = analytics.recomendacion_operativa(pred) if hasattr(analytics, "recomendacion_operativa") else ""
                    QMessageBox.information(self, "Predicción y recomendación", f"{texto}\n\n{oper}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al predecir: {e}")
        else:
            QMessageBox.information(self, "Info", "Función de predicción no disponible.")

    def fetch_public(self):
        if analytics and hasattr(analytics, "fetch_public_health_example"):
            try:
                data, msg = analytics.fetch_public_health_example()
                QMessageBox.information(self, "Datos públicos", f"{msg}\n\n{data}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo obtener datos: {e}")
        else:
            QMessageBox.information(self, "Info", "Función de fetch no disponible.")
