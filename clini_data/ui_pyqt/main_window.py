from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from .pacientes_dialog import PacientesDialog
from .citas_dialog import CitasDialog
from .medicos_dialog import MedicosDialog
from .historial_dialog import HistorialDialog
from .analisis_window import AnalisisWindow

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
        btn_citas.clicked.connect(self.abrir_citas)
        btn_medicos.clicked.connect(self.abrir_medicos)
        btn_historial.clicked.connect(self.abrir_historial)
        btn_analisis.clicked.connect(self.abrir_analisis)
        btn_salir.clicked.connect(self.close)

    def abrir_pacientes(self):
        dlg = PacientesDialog(self)
        dlg.exec_()

    def abrir_citas(self):
        dlg = CitasDialog(self)
        dlg.exec_()

    def abrir_medicos(self):
        dlg = MedicosDialog(self)
        dlg.exec_()

    def abrir_historial(self):
        dlg = HistorialDialog(self)
        dlg.exec_()

    def abrir_analisis(self):
        dlg = AnalisisWindow(self)
        dlg.exec_()
