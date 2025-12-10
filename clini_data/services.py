from . import storage
from .validators import validar_nombre
from tkinter import messagebox

def paciente_existe(cedula):
    for p in storage.pacientes:
        if p.get('cedula') == cedula:
            return True
    return False

def paciente_buscar_por_cedula(cedula):
    return next((p for p in storage.pacientes if p.get('cedula') == cedula), None)

def registrar_paciente(nombre, edad, cedula, telefono, usuario="admin"):
    if paciente_existe(cedula):
        # UI-level debe mostrar error, pero devolvemos False para manejo programático
        return False, "Ya existe un paciente con esta cédula"
    paciente = {"nombre": nombre, "edad": edad, "cedula": cedula, "telefono": telefono}
    storage.pacientes.append(paciente)
    storage.guardar_datos()
    storage.registrar_cambio(usuario, "Registro de paciente", f"{nombre} ({cedula})")
    return True, "Paciente registrado"

def registrar_cita(cedula, fecha, hora, motivo, medico, usuario="admin"):
    if not paciente_existe(cedula):
        return False, "No existe un paciente con esta cédula"
    for cita in storage.citas:
        if (cita['cedula'] == cedula and cita['fecha'] == fecha and cita['hora'] == hora):
            return False, "El paciente ya tiene una cita en esta fecha y hora"
        if (medico and cita.get('medico') == medico and cita['fecha'] == fecha and cita['hora'] == hora):
            return False, f"El médico {medico} no está disponible en esa fecha/hora"
    cita = {"cedula": cedula, "fecha": fecha, "hora": hora, "motivo": motivo, "medico": medico}
    storage.citas.append(cita)
    storage.guardar_datos()
    storage.registrar_cambio(usuario, "Registro de cita", f"{cedula} - {fecha} {hora} - {medico}")
    return True, "Cita registrada"

def registrar_medico(nombre, especialidad, usuario="admin"):
    nombre = nombre.strip().title()
    especialidad = especialidad.strip().title()
    if not nombre:
        return False, "Nombre de médico vacío"
    if any(m['nombre'] == nombre for m in storage.medicos):
        return False, "Ya existe un médico con ese nombre"
    storage.medicos.append({"nombre": nombre, "especialidad": especialidad})
    storage.guardar_datos()
    storage.registrar_cambio(usuario, "Registro de médico", f"{nombre} ({especialidad})")
    return True, "Médico registrado"

def lista_medicos_disponibles(fecha, hora, especialidad=None):
    disp = []
    for m in storage.medicos:
        if especialidad and especialidad.strip():
            if especialidad.strip().lower() not in m.get('especialidad', '').lower():
                continue
        ocupado = any(c.get('medico') == m['nombre'] and c['fecha'] == fecha and c['hora'] == hora for c in storage.citas)
        if not ocupado:
            disp.append(m['nombre'])
    return disp
