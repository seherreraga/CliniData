from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QApplication
from PyQt5.QtCore import Qt
from .pacientes_dialog import PacientesDialog
from .citas_dialog import CitasDialog
from .medicos_dialog import MedicosDialog
from .historial_dialog import HistorialDialog
from .analisis_window import AnalisisWindow
from . import resources
import os

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CliniData - Menú Principal (PyQt5)")

        # Set app icon if available
        app = QApplication.instance()
        if app is not None:
            icon = resources.app_icon("logo_icon_64.png")
            if not icon.isNull():
                app.setWindowIcon(icon)

        self.setFixedSize(420, 360)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        # Header con logo y título
        header = QWidget()
        header_layout = QHBoxLayout()
        header.setLayout(header_layout)
        logo_label = QLabel()
        logo_label.setObjectName("logoLabel")
        pix = resources.get_pixmap("logo_primary.png", width=80, height=80)
        if not pix.isNull():
            logo_label.setPixmap(pix)
            logo_label.setScaledContents(True)
        title = QLabel("CLINIDATA")
        title.setProperty("class", "title")
        title.setStyleSheet("font-size:20px; font-weight:700; color: white; margin-left: 8px;")
        header_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        header_layout.addWidget(title, alignment=Qt.AlignVCenter)
        header_layout.addStretch()
        layout.addWidget(header)

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
