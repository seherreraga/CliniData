from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox
from .pacientes_dialog import PacientesDialog

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CliniData - Menú Principal (PyQt5)")
        self.setFixedSize(360, 300)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        btn_pacientes = QPushButton("Registrar Paciente")
        btn_citas = QPushButton("Registrar Cita")
        btn_medicos = QPushButton("Gestión de Médicos")
        btn_historial = QPushButton("Historial de Cambios")
        btn_analisis = QPushButton("Análisis y Gráficos")
        btn_salir = QPushButton("Salir")

        layout.addWidget(btn_pacientes)
        layout.addWidget(btn_citas)
        layout.addWidget(btn_medicos)
        layout.addWidget(btn_historial)
        layout.addWidget(btn_analisis)
        layout.addWidget(btn_salir)

        btn_pacientes.clicked.connect(self.abrir_pacientes)
        btn_citas.clicked.connect(lambda: QMessageBox.information(self, "Info", "Módulo de citas no implementado aún"))
        btn_medicos.clicked.connect(lambda: QMessageBox.information(self, "Info", "Módulo de médicos no implementado aún"))
        btn_historial.clicked.connect(lambda: QMessageBox.information(self, "Info", "Historial no implementado aún"))
        btn_analisis.clicked.connect(lambda: QMessageBox.information(self, "Info", "Análisis no implementado aún"))
        btn_salir.clicked.connect(self.close)

    def abrir_pacientes(self):
        dlg = PacientesDialog(self)
        dlg.exec_()
