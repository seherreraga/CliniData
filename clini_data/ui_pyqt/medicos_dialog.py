from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from .. import services, validators

class MedicosDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestión de Médicos")
        self.setFixedSize(420, 200)

        form = QFormLayout()
        self.setLayout(form)

        self.entry_nombre = QLineEdit()
        self.entry_especialidad = QLineEdit()
        self.entry_telefono = QLineEdit()

        form.addRow(QLabel("Nombre *"), self.entry_nombre)
        form.addRow(QLabel("Especialidad"), self.entry_especialidad)
        form.addRow(QLabel("Teléfono"), self.entry_telefono)

        botones_layout = QHBoxLayout()
        btn_guardar = QPushButton("Agregar")
        btn_limpiar = QPushButton("Limpiar")
        botones_layout.addWidget(btn_guardar)
        botones_layout.addWidget(btn_limpiar)
        form.addRow(botones_layout)

        btn_guardar.clicked.connect(self.agregar_medico)
        btn_limpiar.clicked.connect(self.limpiar_campos)

    def limpiar_campos(self):
        self.entry_nombre.clear()
        self.entry_especialidad.clear()
        self.entry_telefono.clear()

    def agregar_medico(self):
        nombre = self.entry_nombre.text().strip()
        especialidad = self.entry_especialidad.text().strip()
        telefono = self.entry_telefono.text().strip()

        # Validar nombre si validators está disponible
        if validators and hasattr(validators, "validar_nombre"):
            ok, res = validators.validar_nombre(nombre)
            if not ok:
                QMessageBox.critical(self, "Error", res)
                self.entry_nombre.setFocus()
                return
            nombre = res

        # Validar teléfono opcionalmente
        if telefono and validators and hasattr(validators, "validar_telefono"):
            ok, res = validators.validar_telefono(telefono)
            if not ok:
                QMessageBox.warning(self, "Aviso", f"Teléfono: {res}\nSe intentará guardar de todas formas.")
            else:
                telefono = res

        # Llamada correcta a services.registrar_medico(nombre, especialidad)
        if services and hasattr(services, "registrar_medico"):
            ok, msg = services.registrar_medico(nombre, especialidad)
            if ok:
                QMessageBox.information(self, "Éxito", msg)
                self.accept()
                return
            else:
                QMessageBox.critical(self, "Error", msg)
                return

        # Fallback si services no está disponible
        print("Médico (pendiente guardar):", {"nombre": nombre, "especialidad": especialidad, "telefono": telefono})
        QMessageBox.information(self, "Guardado (simulado)", "Médico mostrado en consola (integración pendiente).")
        self.accept()
