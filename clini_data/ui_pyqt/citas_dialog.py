from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QDateEdit
from PyQt5.QtCore import QDate
from .. import services, validators

class CitasDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Cita")
        self.setFixedSize(420, 260)

        form = QFormLayout()
        self.setLayout(form)

        self.entry_cedula = QLineEdit()
        self.entry_medico = QLineEdit()
        self.entry_motivo = QLineEdit()
        self.entry_hora = QLineEdit()
        self.entry_hora.setPlaceholderText("HH:MM (24h), ej. 09:30")
        self.date_fecha = QDateEdit()
        self.date_fecha.setCalendarPopup(True)
        self.date_fecha.setDate(QDate.currentDate())

        form.addRow(QLabel("Cédula paciente *"), self.entry_cedula)
        form.addRow(QLabel("Médico *"), self.entry_medico)
        form.addRow(QLabel("Motivo"), self.entry_motivo)
        form.addRow(QLabel("Fecha *"), self.date_fecha)
        form.addRow(QLabel("Hora *"), self.entry_hora)

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
        self.entry_hora.clear()
        self.date_fecha.setDate(QDate.currentDate())

    def guardar_cita(self):
        cedula = self.entry_cedula.text().strip()
        medico = self.entry_medico.text().strip()
        motivo = self.entry_motivo.text().strip()
        fecha = self.date_fecha.date().toString("dd/MM/yyyy")
        hora = self.entry_hora.text().strip()

        # Validaciones básicas si existe validators
        if validators and hasattr(validators, "validar_cedula"):
            ok, res = validators.validar_cedula(cedula)
            if not ok:
                QMessageBox.critical(self, "Error", res)
                self.entry_cedula.setFocus()
                return
            cedula = res

        if validators and hasattr(validators, "validar_hora"):
            ok, res = validators.validar_hora(hora, fecha)
            if not ok:
                QMessageBox.critical(self, "Error", res)
                self.entry_hora.setFocus()
                return
            hora = res

        # Llamada correcta a services.registrar_cita(cedula, fecha, hora, motivo, medico)
        if services and hasattr(services, "registrar_cita"):
            ok, msg = services.registrar_cita(cedula, fecha, hora, motivo, medico)
            if ok:
                QMessageBox.information(self, "Éxito", msg)
                self.accept()
                return
            else:
                QMessageBox.critical(self, "Error", msg)
                return

        # Fallback
        print("Cita (pendiente guardar):", {"cedula": cedula, "medico": medico, "motivo": motivo, "fecha": fecha, "hora": hora})
        QMessageBox.information(self, "Guardado (simulado)", "Cita mostrada en consola (integración pendiente).")
        self.accept()
