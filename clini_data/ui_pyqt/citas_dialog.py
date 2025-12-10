from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QDateEdit
from PyQt5.QtCore import QDate

try:
    from .. import services, validators
except Exception:
    services = None
    validators = None

class CitasDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Cita")
        self.setFixedSize(420, 220)

        form = QFormLayout()
        self.setLayout(form)

        self.entry_cedula = QLineEdit()
        self.entry_medico = QLineEdit()
        self.entry_motivo = QLineEdit()
        self.date_fecha = QDateEdit()
        self.date_fecha.setCalendarPopup(True)
        self.date_fecha.setDate(QDate.currentDate())

        form.addRow(QLabel("Cédula paciente *"), self.entry_cedula)
        form.addRow(QLabel("Médico *"), self.entry_medico)
        form.addRow(QLabel("Motivo"), self.entry_motivo)
        form.addRow(QLabel("Fecha *"), self.date_fecha)

        botones_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_limpiar = QPushButton("Limpiar")
        botones_layout.addWidget(btn_guardar)
        botones_layout.addWidget(btn_limpiar)
        form.addRow(botones_layout)

        btn_guardar.clicked.connect(self.guardar_cita)
        btn_limpiar.clicked.connect(self.limpiar_campos)

    def limpiar_campos(self):
        self.entry_cedula.clear()
        self.entry_medico.clear()
        self.entry_motivo.clear()
        self.date_fecha.setDate(QDate.currentDate())

    def guardar_cita(self):
        cedula = self.entry_cedula.text().strip()
        medico = self.entry_medico.text().strip()
        motivo = self.entry_motivo.text().strip()
        fecha = self.date_fecha.date().toString("dd/MM/yyyy")

        # Validaciones básicas si existe validators
        if validators and hasattr(validators, "validar_cedula"):
            ok, res = validators.validar_cedula(cedula)
            if not ok:
                QMessageBox.critical(self, "Error", res); return
            cedula = res

        cita = {"cedula": cedula, "medico": medico, "motivo": motivo, "fecha": fecha}

        if services and hasattr(services, "registrar_cita"):
            try:
                services.registrar_cita(cita)
                QMessageBox.information(self, "OK", "Cita registrada correctamente.")
                self.accept()
                return
            except Exception as e:
                QMessageBox.warning(self, "Aviso", f"Error al guardar via services: {e}\nSe mostrará en consola.")

        print("Cita (pendiente guardar):", cita)
        QMessageBox.information(self, "Guardado (simulado)", "Cita mostrada en consola (integración pendiente).")
        self.accept()
