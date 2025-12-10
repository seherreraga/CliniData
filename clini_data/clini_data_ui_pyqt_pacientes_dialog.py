from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from .. import services, validators

class PacientesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registro de Pacientes")
        self.setFixedSize(360, 260)

        form = QFormLayout()
        self.setLayout(form)

        self.entry_nombre = QLineEdit()
        self.entry_edad = QLineEdit()
        self.entry_cedula = QLineEdit()
        self.entry_telefono = QLineEdit()

        form.addRow(QLabel("Nombre completo *"), self.entry_nombre)
        form.addRow(QLabel("Edad *"), self.entry_edad)
        form.addRow(QLabel("Cédula *"), self.entry_cedula)
        form.addRow(QLabel("Teléfono *"), self.entry_telefono)

        botones_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_limpiar = QPushButton("Limpiar")
        botones_layout.addWidget(btn_guardar)
        botones_layout.addWidget(btn_limpiar)
        form.addRow(botones_layout)

        btn_guardar.clicked.connect(self.guardar_paciente)
        btn_limpiar.clicked.connect(self.limpiar_campos)

    def guardar_paciente(self):
        nombre = self.entry_nombre.text()
        edad = self.entry_edad.text()
        cedula = self.entry_cedula.text()
        telefono = self.entry_telefono.text()

        es_val, res = validators.validar_nombre(nombre)
        if not es_val:
            QMessageBox.critical(self, "Error", res)
            self.entry_nombre.setFocus()
            return
        nombre_val = res

        es_val, res = validators.validar_edad(edad)
        if not es_val:
            QMessageBox.critical(self, "Error", res)
            self.entry_edad.setFocus()
            return
        edad_val = res

        es_val, res = validators.validar_cedula(cedula)
        if not es_val:
            QMessageBox.critical(self, "Error", res)
            self.entry_cedula.setFocus()
            return
        cedula_val = res

        es_val, res = validators.validar_telefono(telefono)
        if not es_val:
            QMessageBox.critical(self, "Error", res)
            self.entry_telefono.setFocus()
            return
        telefono_val = res

        ok, msg = services.registrar_paciente(nombre_val, edad_val, cedula_val, telefono_val)
        if ok:
            QMessageBox.information(self, "Éxito", msg)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", msg)

    def limpiar_campos(self):
        self.entry_nombre.clear()
        self.entry_edad.clear()
        self.entry_cedula.clear()
        self.entry_telefono.clear()
        self.entry_nombre.setFocus()