import re
from datetime import datetime

def validar_nombre(nombre):
    nombre = nombre.strip()
    if not nombre:
        return False, "El nombre no puede estar vacío"
    if not re.match(r'^[A-Za-zÁáÉéÍíÓóÚúÑñ\s]+$', nombre):
        return False, "El nombre solo puede contener letras y espacios"
    if len(nombre) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    return True, nombre.title()

def validar_edad(edad_str):
    try:
        edad = int(edad_str)
        if edad < 0 or edad > 120:
            return False, "La edad debe estar entre 0 y 120 años"
        return True, edad
    except ValueError:
        return False, "La edad debe ser un número válido"

def validar_cedula(cedula):
    cedula = cedula.strip()
    if not cedula:
        return False, "La cédula no puede estar vacía"
    cedula_limpia = re.sub(r'[-\s]', '', cedula)
    if not cedula_limpia.isdigit():
        return False, "La cédula debe contener solo números"
    if len(cedula_limpia) < 8 or len(cedula_limpia) > 10:
        return False, "La cédula debe tener entre 8 y 10 dígitos"
    return True, cedula_limpia

def validar_telefono(telefono):
    telefono = telefono.strip()
    if not telefono:
        return False, "El teléfono no puede estar vacío"
    telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
    if not telefono_limpio.isdigit():
        return False, "El teléfono debe contener solo números"
    if len(telefono_limpio) < 7 or len(telefono_limpio) > 15:
        return False, "El teléfono debe tener entre 7 y 15 dígitos"
    if len(telefono_limpio) == 10:
        telefono_formateado = f"({telefono_limpio[:3]}) {telefono_limpio[3:6]}-{telefono_limpio[6:]}"
    else:
        telefono_formateado = telefono_limpio
    return True, telefono_formateado

def validar_fecha(fecha_str):
    fecha = fecha_str.strip()
    if not fecha:
        return False, "La fecha no puede estar vacía"
    if not re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', fecha):
        return False, "Formato de fecha inválido. Use DD/MM/AAAA"
    try:
        fecha_obj = datetime.strptime(fecha, '%d/%m/%Y')
        if fecha_obj.date() < datetime.now().date():
            return False, "No se pueden registrar citas en fechas pasadas"
        return True, fecha_obj.strftime('%d/%m/%Y')
    except ValueError:
        return False, "Fecha inválida. Verifique día, mes y año"

def validar_hora(hora_str, fecha_str=None):
    hora = hora_str.strip()
    if not hora:
        return False, "La hora no puede estar vacía"
    if not re.match(r'^\d{1,2}:\d{2}$', hora):
        return False, "Formato de hora inválido. Use HH:MM"
    try:
        hora_obj = datetime.strptime(hora, '%H:%M')
        if fecha_str:
            fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
            ahora = datetime.now()
            if fecha_obj.date() == ahora.date() and hora_obj.time() <= ahora.time():
                return False, "No se puede agendar una cita en una hora pasada para hoy"
        return True, hora_obj.strftime('%H:%M') 
    except ValueError:
        return False, "Hora inválida. Use formato 24 horas (00:00 - 23:59)"

def validar_texto(texto, campo, min_len=3):
    texto = texto.strip()
    if not texto:
        return False, f"El {campo} no puede estar vacío"
    if len(texto) < min_len:
        return False, f"El {campo} debe tener al menos {min_len} caracteres"
    return True, texto