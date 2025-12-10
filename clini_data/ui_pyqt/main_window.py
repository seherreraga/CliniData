from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout,
    QApplication, QSizePolicy, QFrame, QSplitter, QScrollArea
)
from PyQt5.QtCore import Qt
from .pacientes_dialog import PacientesDialog
from .citas_dialog import CitasDialog
from .medicos_dialog import MedicosDialog
from .historial_dialog import HistorialDialog
from .analisis_window import AnalisisWindow
from . import resources

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CliniData - Menú Principal (PyQt5)")
        # Permitir redimensionar; establecer tamaño inicial grande y mínimo razonable
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)

        # Set app icon si está disponible
        app = QApplication.instance()
        if app is not None:
            icon = resources.app_icon("logo_icon_64.png")
            if not icon.isNull():
                app.setWindowIcon(icon)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        central.setLayout(main_layout)

        # Header con logo y título (mantener compacto)
        header = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header.setLayout(header_layout)
        logo_label = QLabel()
        pix = resources.get_pixmap("logo_primary.png", width=96, height=96)
        if not pix.isNull():
            logo_label.setPixmap(pix)
            logo_label.setScaledContents(True)
            logo_label.setFixedSize(96, 96)
        title = QLabel("CLINIDATA")
        title.setStyleSheet("font-size:22px; font-weight:700; color: white; margin-left: 12px;")
        header_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        header_layout.addWidget(title, alignment=Qt.AlignVCenter)
        header_layout.addStretch()
        main_layout.addWidget(header)

        # Splitter principal: izquierda (menu) y derecha (contenido)
        splitter = QSplitter(Qt.Horizontal)
        # Panel izquierdo: menú vertical
        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout()
        left_layout.setSpacing(12)
        left_layout.setContentsMargins(8, 8, 8, 8)
        left_panel.setLayout(left_layout)

        # Botones del menú (más grandes)
        btn_style = "padding: 12px; font-size: 14px; border-radius: 6px;"
        btn_pacientes = QPushButton("Registrar Paciente")
        btn_citas = QPushButton("Registrar Cita")
        btn_medicos = QPushButton("Gestión de Médicos")
        btn_historial = QPushButton("Historial de Cambios")
        btn_analisis = QPushButton("Análisis y Gráficos")
        btn_salir = QPushButton("Salir")

        for b in (btn_pacientes, btn_citas, btn_medicos, btn_historial, btn_analisis, btn_salir):
            b.setMinimumHeight(48)
            b.setStyleSheet(btn_style)
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            left_layout.addWidget(b)

        left_layout.addStretch()

        # Panel derecho: área de contenido (ejemplo: panel vacío / placeholder)
        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_panel.setLayout(right_layout)

        placeholder = QLabel("Contenido principal\n(Selecciona una opción del menú izquierdo)")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("font-size:16px; color: white;")
        right_layout.addWidget(placeholder, alignment=Qt.AlignCenter)

        # Añadir los paneles al splitter y darle proporciones iniciales
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 0)  # left panel no crece tanto
        splitter.setStretchFactor(1, 1)  # right panel ocupa el resto
        splitter.setSizes([260, 740])    # anchuras iniciales

        # Hacer que el área derecha sea scrollable si el contenido crece
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(right_panel)

        splitter_widget = QWidget()
        splitter_layout = QHBoxLayout()
        splitter_layout.setContentsMargins(0, 0, 0, 0)
        splitter_widget.setLayout(splitter_layout)
        splitter_layout.addWidget(splitter)
        main_layout.addWidget(splitter_widget)

        # Conexiones de los botones a acciones / diálogos
        btn_pacientes.clicked.connect(self.abrir_pacientes)
        btn_citas.clicked.connect(self.abrir_citas)
        btn_medicos.clicked.connect(self.abrir_medicos)
        btn_historial.clicked.connect(self.abrir_historial)
        btn_analisis.clicked.connect(self.abrir_analisis)
        btn_salir.clicked.connect(self.close)

        # Guardamos el right_panel para poder reemplazar su contenido si queremos
        self.right_panel = right_panel
        self.right_layout = right_layout

    # Funciones para abrir diálogos
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
