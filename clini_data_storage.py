import json
from datetime import datetime

# Datos en memoria
pacientes = []
citas = []
medicos = []

def guardar_datos():
    """Guarda pacientes, citas y médicos en archivos JSON"""
    with open("pacientes.json", "w", encoding="utf-8") as f:
        json.dump(pacientes, f, indent=4, ensure_ascii=False)
    with open("citas.json", "w", encoding="utf-8") as f:
        json.dump(citas, f, indent=4, ensure_ascii=False)
    with open("medicos.json", "w", encoding="utf-8") as f:
        json.dump(medicos, f, indent=4, ensure_ascii=False)

def cargar_datos():
    global pacientes, citas, medicos
    try:
        with open("pacientes.json", "r", encoding="utf-8") as f:
            pacientes = json.load(f)
    except FileNotFoundError:
        pacientes = []
    try:
        with open("citas.json", "r", encoding="utf-8") as f:
            citas = json.load(f)
    except FileNotFoundError:
        citas = []
    try:
        with open("medicos.json", "r", encoding="utf-8") as f:
            medicos = json.load(f)
    except FileNotFoundError:
        medicos = []

def registrar_cambio(usuario, accion, detalle):
    """Guarda en historial quién hizo qué cambio y cuándo"""
    log = {
        "usuario": usuario,
        "accion": accion,
        "detalle": detalle,
        "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    try:
        with open("historial.json", "r", encoding='utf-8') as f:
            historial = json.load(f)
    except FileNotFoundError:
        historial = []
    historial.append(log)
    with open("historial.json", "w", encoding='utf-8') as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def cargar_historial():
    try:
        with open("historial.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []