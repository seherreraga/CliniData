import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime
import json
import math

# Librerías externas para análisis y gráficos
try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import requests
    EXTERNAL_LIBS_AVAILABLE = True
except Exception:
    EXTERNAL_LIBS_AVAILABLE = False

# ==========================
# Sección 1: Variables globales
# ==========================
pacientes = []
citas = []
medicos = []  # Nuevo: lista de médicos registrados (cada uno: {"nombre":..., "especialidad":...})

#==================================
#Sección 2: Manejo de archivos JSON
# =================================
# Se agregó manejo adicional de medicos (nuevo)
def guardar_datos():
    """Guarda pacientes, citas y médicos en archivos JSON"""
    with open("pacientes.json", "w") as f:
        json.dump(pacientes, f, indent=4)
    with open("citas.json", "w") as f:
        json.dump(citas, f, indent=4)
    with open("medicos.json", "w") as f:
        json.dump(medicos, f, indent=4)

def cargar_datos():
    global pacientes, citas, medicos
    try:
        with open("pacientes.json", "r") as f:
            pacientes = json.load(f)
    except FileNotFoundError:
        pacientes = []
    try:
        with open("citas.json", "r") as f:
            citas = json.load(f)
    except FileNotFoundError:
        citas = []
    try:
        with open("medicos.json", "r") as f:
            medicos = json.load(f)
    except FileNotFoundError:
        medicos = []

#==========================================
#Sección 3: Registro de cambios (Historial)
#==========================================
def registrar_cambio(usuario, accion, detalle):
    """Guarda en historial quién hizo qué cambio y cuándo"""
    log = {
        "usuario": usuario,
        "accion": accion,
        "detalle": detalle,
        "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    try:
        with open("historial.json", "r") as f:
            historial = json.load(f)
    except FileNotFoundError:
        historial = []
    historial.append(log)
    with open("historial.json", "w") as f:
        json.dump(historial, f, indent=4)

def cargar_historial():
    try:
        with open("historial.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# ==========================
# Sección 4: Funciones de validación
# ==========================
def validar_nombre(nombre):
    """Valida que el nombre contenga solo letras y espacios"""
    nombre = nombre.strip()
    if not nombre:
        return False, "El nombre no puede estar vacío"
    if not re.match(r'^[A-Za-zÁáÉéÍíÓóÚúÑñ\s]+$', nombre):
        return False, "El nombre solo puede contener letras y espacios"
    if len(nombre) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    return True, nombre.title()

def validar_edad(edad_str):
    """Valida que la edad sea un número entre 0 y 120"""
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
    """Valida formato de fecha (DD/MM/AAAA)"""
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

def paciente_existe(cedula):
    for paciente in pacientes:
        if paciente['cedula'] == cedula:
            return True
    return False

# ==========================
# Sección 5: Funciones de lógicas
# ==========================
def registrar_paciente(nombre, edad, cedula, telefono):
    if paciente_existe(cedula):
        messagebox.showerror("Error", "Ya existe un paciente con esta cédula")
        return False
    paciente = {"nombre": nombre, "edad": edad, "cedula": cedula, "telefono": telefono}
    pacientes.append(paciente)
    guardar_datos()
    registrar_cambio("admin", "Registro de paciente", f"{nombre} ({cedula})")
    return True

def paciente_buscar_por_cedula(cedula):
    return next((p for p in pacientes if p['cedula'] == cedula), None)

def registrar_cita(cedula, fecha, hora, motivo, medico):
    """Registra cita validando disponibilidad básica (no permitir doble turno mismo paciente y evitando conflicto médico)."""
    if not paciente_existe(cedula):
        messagebox.showerror("Error", "No existe un paciente con esta cédula")
        return False
    for cita in citas:
        if (cita['cedula'] == cedula and cita['fecha'] == fecha and cita['hora'] == hora):
            messagebox.showerror("Error", "El paciente ya tiene una cita en esta fecha y hora")
            return False
        # Evitar doble reserva del mismo médico en la misma fecha/hora
        if (medico and cita.get('medico') == medico and cita['fecha'] == fecha and cita['hora'] == hora):
            messagebox.showerror("Error", f"El médico {medico} no está disponible en esa fecha/hora")
            return False
    cita = {"cedula": cedula, "fecha": fecha, "hora": hora, "motivo": motivo, "medico": medico}
    citas.append(cita)
    guardar_datos()
    registrar_cambio("admin", "Registro de cita", f"{cedula} - {fecha} {hora} - {medico}")
    return True

# ==========================
# Sección 6: Gestión de médicos (Nuevo)
# ==========================
def registrar_medico(nombre, especialidad):
    nombre = nombre.strip().title()
    especialidad = especialidad.strip().title()
    if not nombre:
        return False, "Nombre de médico vacío"
    # Evitar duplicados
    if any(m['nombre'] == nombre for m in medicos):
        return False, "Ya existe un médico con ese nombre"
    medicos.append({"nombre": nombre, "especialidad": especialidad})
    guardar_datos()
    registrar_cambio("admin", "Registro de médico", f"{nombre} ({especialidad})")
    return True, "Médico registrado"

def lista_medicos_disponibles(fecha, hora, especialidad=None):
    """
    Retorna lista de nombres de médicos que:
    - Estén registrados
    - No tengan cita en la misma fecha y hora
    - Si se especifica especialidad, filtra por ella (subcadena)
    """
    disp = []
    for m in medicos:
        if especialidad and especialidad.strip():
            if especialidad.strip().lower() not in m.get('especialidad', '').lower():
                continue
        # comprobar conflictos en citas
        ocupado = any(c['medico'] == m['nombre'] and c['fecha'] == fecha and c['hora'] == hora for c in citas)
        if not ocupado:
            disp.append(m['nombre'])
    return disp

def ventana_medicos():
    vm = tk.Toplevel()
    vm.title("Gestión de Médicos")
    vm.geometry("420x360")
    vm.resizable(False, False)
    vm.grab_set()

    tk.Label(vm, text="Registro de Médicos", font=("Arial", 12, "bold")).pack(pady=8)

    frame_in = tk.Frame(vm)
    frame_in.pack(pady=6)
    tk.Label(frame_in, text="Nombre:").grid(row=0, column=0, padx=4, pady=4, sticky="e")
    entry_nom = tk.Entry(frame_in, width=28)
    entry_nom.grid(row=0, column=1, padx=4, pady=4)
    tk.Label(frame_in, text="Especialidad:").grid(row=1, column=0, padx=4, pady=4, sticky="e")
    entry_esp = tk.Entry(frame_in, width=28)
    entry_esp.grid(row=1, column=1, padx=4, pady=4)

    def boton_guardar_medico():
        n = entry_nom.get()
        e = entry_esp.get()
        ok, msg = registrar_medico(n, e)
        if ok:
            messagebox.showinfo("Éxito", msg)
            entry_nom.delete(0, tk.END); entry_esp.delete(0, tk.END)
            listar_medicos()
        else:
            messagebox.showerror("Error", msg)

    tk.Button(frame_in, text="Guardar médico", command=boton_guardar_medico, width=16).grid(row=2, column=1, pady=6)

    # Área de listado
    tk.Label(vm, text="Médicos registrados:").pack(pady=(8,0))
    text_med = tk.Text(vm, width=50, height=10)
    text_med.pack(padx=6, pady=6)

    def listar_medicos():
        text_med.delete("1.0", tk.END)
        if medicos:
            for m in medicos:
                text_med.insert(tk.END, f"{m['nombre']} - {m.get('especialidad','N/A')}\n")
        else:
            text_med.insert(tk.END, "No hay médicos registrados.")

    listar_medicos()

# ==========================
# Sección 7: Interfaz gráfica de citas (modificada para selección de médicos disponibles)
# ==========================
def ventana_menu():
    ventana = tk.Tk()
    ventana.title("CliniData - Menú Principal")
    ventana.geometry("360x300")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Bienvenido a CliniData", font=("Arial", 14)).pack(pady=10)
    tk.Button(ventana, text="Registrar Paciente", command=ventana_pacientes, width=28).pack(pady=4)
    tk.Button(ventana, text="Registrar Cita", command=ventana_citas, width=28).pack(pady=4)
    tk.Button(ventana, text="Gestión de Médicos", command=ventana_medicos, width=28).pack(pady=4)
    tk.Button(ventana, text="Historial de Cambios", command=ventana_historial, width=28).pack(pady=4)
    tk.Button(ventana, text="Búsqueda Avanzada", command=ventana_busqueda_filtros, width=28).pack(pady=4)
    tk.Button(ventana, text="Análisis y Gráficos", command=ventana_analisis, width=28).pack(pady=4)
    tk.Button(ventana, text="Salir", command=ventana.destroy, width=28).pack(pady=8)

    ventana.mainloop()

def ventana_pacientes():
    vp = tk.Toplevel()
    vp.title("Registro de Pacientes")
    vp.geometry("350x420")
    vp.resizable(False, False)
    vp.grab_set()

    tk.Label(vp, text="Registro de Paciente", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(vp, text="Nombre completo *").pack(anchor="w", padx=20)
    entry_nombre = tk.Entry(vp, width=30)
    entry_nombre.pack(pady=(0, 10), padx=20)
    entry_nombre.focus()

    tk.Label(vp, text="Edad *").pack(anchor="w", padx=20)
    entry_edad = tk.Entry(vp, width=30)
    entry_edad.pack(pady=(0, 10), padx=20)

    tk.Label(vp, text="Cédula *").pack(anchor="w", padx=20)
    entry_cedula = tk.Entry(vp, width=30)
    entry_cedula.pack(pady=(0, 10), padx=20)

    tk.Label(vp, text="Teléfono *").pack(anchor="w", padx=20)
    entry_telefono = tk.Entry(vp, width=30)
    entry_telefono.pack(pady=(0, 20), padx=20)

    def guardar_paciente():
        try:
            nombre = entry_nombre.get()
            edad = entry_edad.get()
            cedula = entry_cedula.get()
            telefono = entry_telefono.get()
            es_valido, resultado = validar_nombre(nombre)
            if not es_valido:
                messagebox.showerror("Error", resultado); entry_nombre.focus(); return
            nombre_valido = resultado
            es_valido, resultado = validar_edad(edad)
            if not es_valido:
                messagebox.showerror("Error", resultado); entry_edad.focus(); return
            edad_valida = resultado
            es_valido, resultado = validar_cedula(cedula)
            if not es_valido:
                messagebox.showerror("Error", resultado); entry_cedula.focus(); return
            cedula_valida = resultado
            es_valido, resultado = validar_telefono(telefono)
            if not es_valido:
                messagebox.showerror("Error", resultado); entry_telefono.focus(); return
            telefono_valido = resultado
            if registrar_paciente(nombre_valido, edad_valida, cedula_valida, telefono_valido):
                messagebox.showinfo("Éxito", "Paciente registrado correctamente")
                vp.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def limpiar_campos():
        entry_nombre.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        entry_cedula.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_nombre.focus()

    frame_botones = tk.Frame(vp)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Guardar", command=guardar_paciente, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botones, text="Limpiar", command=limpiar_campos, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botones, text="Cancelar", command=vp.destroy, width=10).pack(side=tk.LEFT, padx=5)

def ventana_citas():
    vc = tk.Toplevel()
    vc.title("Registro de Citas")
    vc.geometry("420x540")
    vc.resizable(False, False)
    vc.grab_set()

    tk.Label(vc, text="Registro de Cita Médica", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(vc, text="Cédula del paciente *").pack(anchor="w", padx=20)
    entry_cedula = tk.Entry(vc, width=30)
    entry_cedula.pack(pady=(0, 10), padx=20)
    entry_cedula.focus()

    tk.Label(vc, text="Fecha (DD/MM/AAAA) *").pack(anchor="w", padx=20)
    entry_fecha = tk.Entry(vc, width=20)
    entry_fecha.pack(pady=(0, 10), padx=20)
    entry_fecha.insert(0, datetime.now().strftime('%d/%m/%Y'))

    tk.Label(vc, text="Hora (HH:MM) *").pack(anchor="w", padx=20)
    entry_hora = tk.Entry(vc, width=20)
    entry_hora.pack(pady=(0, 10), padx=20)
    entry_hora.insert(0, "09:00")

    tk.Label(vc, text="Motivo / Servicio *").pack(anchor="w", padx=20)
    entry_motivo = tk.Entry(vc, width=30)
    entry_motivo.pack(pady=(0, 10), padx=20)

    # Campo de médico: entrada libre + lista de médicos disponibles (para compatibilidad)
    tk.Label(vc, text="Médico (puede seleccionar uno disponible)").pack(anchor="w", padx=20)
    entry_medico = tk.Entry(vc, width=30)
    entry_medico.pack(pady=(0, 6), padx=20)

    frame_disp = tk.Frame(vc)
    frame_disp.pack(padx=20, pady=4, fill="x")
    tk.Label(frame_disp, text="Médicos disponibles:").grid(row=0, column=0, padx=4, sticky="w")
    var_med_disp = tk.StringVar(frame_disp)
    var_med_disp.set("—Seleccione—")
    option_med = tk.OptionMenu(frame_disp, var_med_disp, "—Seleccione—")
    option_med.config(width=25)
    option_med.grid(row=0, column=1, padx=4, pady=2)

    def actualizar_medicos_disponibles():
        fecha = entry_fecha.get().strip()
        hora = entry_hora.get().strip()
        motivo = entry_motivo.get().strip()
        es_val, resf = validar_fecha(fecha)
        if not es_val:
            messagebox.showerror("Error", "Fecha inválida para búsqueda de médicos: " + resf); return
        es_val, resh = validar_hora(hora, fecha)
        if not es_val:
            messagebox.showerror("Error", "Hora inválida para búsqueda de médicos: " + resh); return
        esp = motivo  # usamos motivo como proxy de especialidad si paciente lo escribe
        disponibles = lista_medicos_disponibles(resf, resh, especialidad=esp)
        # Actualizar menú
        menu = option_med["menu"]
        menu.delete(0, "end")
        if disponibles:
            var_med_disp.set(disponibles[0])
            for m in disponibles:
                menu.add_command(label=m, command=lambda value=m: var_med_disp.set(value))
        else:
            var_med_disp.set("No hay médicos disponibles")
            menu.add_command(label="No hay médicos disponibles", command=lambda: var_med_disp.set("No hay médicos disponibles"))

    def seleccionar_medico_desde_lista(*args):
        sel = var_med_disp.get()
        if sel and sel not in ("—Seleccione—", "No hay médicos disponibles"):
            entry_medico.delete(0, tk.END)
            entry_medico.insert(0, sel)

    var_med_disp.trace_add("write", seleccionar_medico_desde_lista)

    tk.Button(vc, text="Buscar médicos disponibles", command=actualizar_medicos_disponibles, width=24).pack(pady=6)

    def guardar_cita_ui():
        try:
            cedula = entry_cedula.get().strip()
            fecha = entry_fecha.get().strip()
            hora = entry_hora.get().strip()
            motivo = entry_motivo.get().strip()
            medico = entry_medico.get().strip()
            es_val, resultado = validar_cedula(cedula)
            if not es_val:
                messagebox.showerror("Error", resultado); entry_cedula.focus(); return
            cedula_valida = resultado
            es_val, resultado = validar_fecha(fecha)
            if not es_val:
                messagebox.showerror("Error", resultado); entry_fecha.focus(); return
            fecha_valida = resultado
            es_val, resultado = validar_hora(hora, fecha)
            if not es_val:
                messagebox.showerror("Error", resultado); entry_hora.focus(); return
            hora_valida = resultado
            es_val, resultado = validar_texto(motivo, "motivo de consulta")
            if not es_val:
                messagebox.showerror("Error", resultado); entry_motivo.focus(); return
            motivo_valido = resultado
            # Si el médico fue escogido por lista, usar el nombre; si está vacío, dejar cadena vacía
            medico_seleccionado = medico if medico else ""
            if registrar_cita(cedula_valida, fecha_valida, hora_valida, motivo_valido, medico_seleccionado):
                messagebox.showinfo("Éxito", "Cita registrada correctamente")
                vc.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def limpiar_campos():
        entry_cedula.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, datetime.now().strftime('%d/%m/%Y'))
        entry_hora.delete(0, tk.END)
        entry_hora.insert(0, "09:00")
        entry_motivo.delete(0, tk.END)
        entry_medico.delete(0, tk.END)
        var_med_disp.set("—Seleccione—")
        entry_cedula.focus()

    frame_botones = tk.Frame(vc)
    frame_botones.pack(pady=10)
    tk.Button(frame_botones, text="Guardar", command=guardar_cita_ui, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botones, text="Limpiar", command=limpiar_campos, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botones, text="Cancelar", command=vc.destroy, width=10).pack(side=tk.LEFT, padx=5)

# ============================
# Sección 8: Búsqueda avanzada con filtros (mantener)
# ============================
def ventana_busqueda_filtros():
    vb = tk.Toplevel()
    vb.title("Búsqueda Avanzada por Filtros")
    vb.geometry("500x470")
    vb.resizable(False, False)

    tk.Label(vb, text="Búsqueda avanzada de citas", font=("Arial", 12, "bold")).pack(pady=10)
    frame_f = tk.Frame(vb)
    frame_f.pack()

    tk.Label(frame_f, text="Nombre de paciente:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
    entry_nombre = tk.Entry(frame_f, width=20)
    entry_nombre.grid(row=0, column=1, padx=5, pady=2)
    tk.Label(frame_f, text="Cédula:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
    entry_cedula = tk.Entry(frame_f, width=20)
    entry_cedula.grid(row=1, column=1, padx=5, pady=2)
    tk.Label(frame_f, text="Médico:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
    entry_medico = tk.Entry(frame_f, width=20)
    entry_medico.grid(row=2, column=1, padx=5, pady=2)
    tk.Label(frame_f, text="Motivo:").grid(row=3, column=0, padx=5, pady=2, sticky="e")
    entry_motivo = tk.Entry(frame_f, width=20)
    entry_motivo.grid(row=3, column=1, padx=5, pady=2)
    tk.Label(frame_f, text="Fecha (DD/MM/AAAA):").grid(row=4, column=0, padx=5, pady=2, sticky="e")
    entry_fecha = tk.Entry(frame_f, width=20)
    entry_fecha.grid(row=4, column=1, padx=5, pady=2)

    text_resultado = tk.Text(vb, width=58, height=15)
    text_resultado.pack(pady=10)

    def ejecutar_busqueda():
        nombre_filtro = entry_nombre.get().strip().lower()
        cedula_filtro = entry_cedula.get().strip()
        medico_filtro = entry_medico.get().strip().lower()
        motivo_filtro = entry_motivo.get().strip().lower()
        fecha_filtro = entry_fecha.get().strip()
        resultados = []
        for c in citas:
            paciente = next((p for p in pacientes if p["cedula"] == c["cedula"]), None)
            nombre_p = paciente["nombre"].lower() if paciente else ""
            if ((not nombre_filtro or nombre_filtro in nombre_p)
                and (not cedula_filtro or cedula_filtro in c["cedula"])
                and (not medico_filtro or medico_filtro in c["medico"].lower())
                and (not motivo_filtro or motivo_filtro in c["motivo"].lower())
                and (not fecha_filtro or fecha_filtro == c["fecha"])):
                resultados.append((c, paciente["nombre"] if paciente else "N/A"))
        text_resultado.delete("1.0", tk.END)
        if resultados:
            for r, nombre_paciente in resultados:
                text_resultado.insert(tk.END,
                    f"Paciente: {nombre_paciente}\n"
                    f"Cédula: {r['cedula']}\n"
                    f"Fecha: {r['fecha']}\n"
                    f"Hora: {r['hora']}\n"
                    f"Médico: {r['medico']}\n"
                    f"Motivo: {r['motivo']}\n"
                    f"{'-'*45}\n"
                )
        else:
            text_resultado.insert(tk.END, "No se encontraron resultados.")

    tk.Button(vb, text="Buscar", command=ejecutar_busqueda, width=16).pack(pady=5)

# ==========================
# Sección 9: Análisis de datos, gráficas y IA simple (Nuevo)
# ==========================
def crear_dataframes():
    if not EXTERNAL_LIBS_AVAILABLE:
        return None, None
    df_p = pd.DataFrame(pacientes)
    df_c = pd.DataFrame(citas)
    if not df_p.empty and 'edad' in df_p.columns:
        df_p['edad'] = pd.to_numeric(df_p['edad'], errors='coerce').fillna(0).astype(int)
    if not df_c.empty and 'fecha' in df_c.columns:
        df_c['fecha_dt'] = pd.to_datetime(df_c['fecha'], format='%d/%m/%Y', errors='coerce')
        df_c = df_c.sort_values('fecha_dt')
    return df_p, df_c

def analizar_datos():
    if not EXTERNAL_LIBS_AVAILABLE:
        return "Las librerías externas (NumPy/Pandas/Matplotlib/Requests) no están disponibles."
    df_p, df_c = crear_dataframes()
    resumen = []
    resumen.append(f"Total de pacientes: {len(df_p) if df_p is not None else 0}")
    resumen.append(f"Total de citas: {len(df_c) if df_c is not None else 0}")
    if df_p is not None and not df_p.empty:
        resumen.append(f"Edad media de pacientes: {df_p['edad'].mean():.1f}")
        resumen.append(f"Edad mediana: {df_p['edad'].median():.1f}")
        bins = [0, 18, 35, 50, 65, 120]
        counts, _ = np.histogram(df_p['edad'], bins=bins)
        rangos = ["0-17","18-34","35-49","50-64","65+"]
        for r, c in zip(rangos, counts):
            resumen.append(f"  {r}: {c}")
    else:
        resumen.append("No hay datos de pacientes para análisis de edad.")
    if df_c is not None and not df_c.empty:
        df_c['mes'] = df_c['fecha_dt'].dt.to_period('M')
        citas_por_mes = df_c.groupby('mes').size().sort_index()
        resumen.append("Citas por mes:")
        for mes, val in citas_por_mes.items():
            resumen.append(f"  {mes}: {val}")
        top_med = df_c['medico'].value_counts().head(5)
        resumen.append("Top 5 médicos por número de citas:")
        for medico, n in top_med.items():
            resumen.append(f"  {medico}: {n}")
    else:
        resumen.append("No hay datos de citas para análisis temporal.")
    return "\n".join(resumen)

def graficar_histograma_edades():
    if not EXTERNAL_LIBS_AVAILABLE:
        messagebox.showerror("Error", "Faltan librerías: instale numpy y pandas y matplotlib.")
        return
    df_p, _ = crear_dataframes()
    if df_p is None or df_p.empty:
        messagebox.showinfo("Info", "No hay datos de pacientes para graficar.")
        return
    plt.figure(figsize=(8,5))
    plt.hist(df_p['edad'], bins=range(0, 101, 5), color='skyblue', edgecolor='black')
    plt.title("Distribución de edades de pacientes")
    plt.xlabel("Edad")
    plt.ylabel("Cantidad de pacientes")
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def graficar_citas_por_mes():
    if not EXTERNAL_LIBS_AVAILABLE:
        messagebox.showerror("Error", "Faltan librerías: instale numpy y pandas y matplotlib.")
        return
    _, df_c = crear_dataframes()
    if df_c is None or df_c.empty:
        messagebox.showinfo("Info", "No hay datos de citas para graficar.")
        return
    df_c['mes'] = df_c['fecha_dt'].dt.to_period('M')
    conteos = df_c.groupby('mes').size().sort_index()
    conteos.index = conteos.index.to_timestamp()
    plt.figure(figsize=(8,4))
    plt.bar(conteos.index.astype(str), conteos.values, color='salmon', edgecolor='black')
    plt.title("Citas por mes")
    plt.xlabel("Mes")
    plt.ylabel("Número de citas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def graficar_top_medicos():
    if not EXTERNAL_LIBS_AVAILABLE:
        messagebox.showerror("Error", "Faltan librerías: instale numpy y pandas y matplotlib.")
        return
    _, df_c = crear_dataframes()
    if df_c is None or df_c.empty:
        messagebox.showinfo("Info", "No hay datos de citas para graficar.")
        return
    top = df_c['medico'].value_counts().head(8)
    plt.figure(figsize=(8,4))
    top.plot(kind='bar', color='mediumseagreen', edgecolor='black')
    plt.title("Top médicos por número de citas")
    plt.xlabel("Médico")
    plt.ylabel("Número de citas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def predecir_citas_proximo_mes(meses_historicos=6):
    if not EXTERNAL_LIBS_AVAILABLE:
        return None, "Faltan librerías externas."
    _, df_c = crear_dataframes()
    if df_c is None or df_c.empty:
        return None, "No hay datos de citas para predecir."
    df_c['mes'] = df_c['fecha_dt'].dt.to_period('M')
    conteos = df_c.groupby('mes').size().sort_index()
    conteos = conteos[-meses_historicos:]
    if len(conteos) == 0:
        return None, "No hay suficientes datos para predecir."
    x = np.arange(len(conteos))
    y = conteos.values.astype(float)
    if len(x) == 1:
        pred = float(y[0])
        return pred, "Predicción basada en el último mes disponible."
    coef = np.polyfit(x, y, 1)
    m, b = coef
    next_x = len(x)
    pred = m * next_x + b
    pred = max(0, round(pred))
    y_pred = m * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0
    texto = f"Predicción: {pred} citas para el siguiente mes (modelo lineal). R²={r2:.2f}"
    return pred, texto

def recomendacion_operativa(predicted_count, capacidad_por_dia=8, dias_por_mes=22):
    if predicted_count is None:
        return "No hay predicción disponible."
    capacidad_total = capacidad_por_dia * dias_por_mes
    medicos_necesarios = math.ceil(predicted_count / capacidad_total) if capacidad_total > 0 else "N/A"
    return (f"Predicción de citas: {predicted_count}. "
            f"Capacidad por mes por médico aprox.: {capacidad_por_dia * dias_por_mes}. "
            f"Médicos recomendados: {medicos_necesarios}.")

def fetch_public_health_example():
    if not EXTERNAL_LIBS_AVAILABLE:
        return None, "Librerías externas no disponibles."
    url = "https://disease.sh/v3/covid-19/all"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            summary = {"updated": data.get("updated"), "cases": data.get("cases"), "deaths": data.get("deaths"), "recovered": data.get("recovered")}
            return summary, "Datos extraídos de disease.sh"
        else:
            raise Exception("Código HTTP " + str(r.status_code))
    except Exception as e:
        simulated = {"updated": None, "cases": 1000000, "deaths": 30000, "recovered": 900000}
        return simulated, f"No se pudo conectar ({str(e)}). Se usan datos simulados."

def ia_recomendacion_paciente(cedula):
    if not EXTERNAL_LIBS_AVAILABLE:
        paciente = next((p for p in pacientes if p['cedula'] == cedula), None)
        if not paciente:
            return "Paciente no encontrado."
        edad = int(paciente.get('edad', 0))
        if edad >= 65:
            return "Prioridad ALTA por edad (>=65). Recomendar revisión frecuente."
        else:
            return "Prioridad normal."
    df_p, df_c = crear_dataframes()
    paciente = df_p[df_p['cedula'] == cedula]
    if paciente.empty:
        return "Paciente no encontrado."
    edad = int(paciente.iloc[0]['edad'])
    hoy = pd.to_datetime(datetime.now())
    if df_c is None or df_c.empty:
        citas_ult_365 = 0
    else:
        citas_ult_365 = df_c[(df_c['cedula'] == cedula) & (df_c['fecha_dt'] >= (hoy - pd.Timedelta(days=365)))].shape[0]
    mensajes = []
    if edad >= 65:
        mensajes.append("Prioridad ALTA por edad (>=65).")
    if citas_ult_365 > 3:
        mensajes.append(f"Tiene {citas_ult_365} citas en el último año. Recomendar seguimiento proactivo.")
    if not mensajes:
        mensajes.append("Prioridad normal. No se detectan factores que requieran intervención automática.")
    return " ".join(mensajes)

def ventana_analisis():
    vb = tk.Toplevel()
    vb.title("Análisis y Gráficos - CliniData")
    vb.geometry("520x520")
    vb.resizable(False, False)
    vb.grab_set()

    tk.Label(vb, text="Módulo de Análisis y Visualización", font=("Arial", 12, "bold")).pack(pady=8)
    text_res = tk.Text(vb, width=62, height=14)
    text_res.pack(padx=8, pady=6)

    def mostrar_resumen():
        text_res.delete("1.0", tk.END)
        resumen = analizar_datos()
        text_res.insert(tk.END, resumen)

    def boton_predecir():
        pred, texto = predecir_citas_proximo_mes()
        if pred is None:
            messagebox.showinfo("Predicción", texto)
        else:
            oper = recomendacion_operativa(pred)
            messagebox.showinfo("Predicción y recomendación", f"{texto}\n\n{oper}")

    def boton_fetch():
        data, msg = fetch_public_health_example()
        messagebox.showinfo("Datos públicos (ejemplo)", f"{msg}\n\n{json.dumps(data, indent=2)}")

    frame_b = tk.Frame(vb)
    frame_b.pack(pady=6)

    tk.Button(frame_b, text="Generar resumen", command=mostrar_resumen, width=18).grid(row=0, column=0, padx=6, pady=6)
    tk.Button(frame_b, text="Histograma de edades", command=graficar_histograma_edades, width=18).grid(row=0, column=1, padx=6, pady=6)
    tk.Button(frame_b, text="Citas por mes", command=graficar_citas_por_mes, width=18).grid(row=1, column=0, padx=6, pady=6)
    tk.Button(frame_b, text="Top médicos", command=graficar_top_medicos, width=18).grid(row=1, column=1, padx=6, pady=6)
    tk.Button(frame_b, text="Predecir próximo mes", command=boton_predecir, width=18).grid(row=2, column=0, padx=6, pady=6)
    tk.Button(frame_b, text="Obtener datos públicos (ej.)", command=boton_fetch, width=18).grid(row=2, column=1, padx=6, pady=6)

    frame_ia = tk.LabelFrame(vb, text="IA: recomendación por paciente", padx=8, pady=8)
    frame_ia.pack(padx=8, pady=8, fill="x")

    tk.Label(frame_ia, text="Cédula paciente:").grid(row=0, column=0, padx=4, pady=4)
    entry_ced = tk.Entry(frame_ia, width=20)
    entry_ced.grid(row=0, column=1, padx=4, pady=4)
    def boton_ia():
        ced = entry_ced.get().strip()
        es_val, res = validar_cedula(ced)
        if not es_val:
            messagebox.showerror("Error", res); return
        texto = ia_recomendacion_paciente(res)
        messagebox.showinfo("Recomendación IA", texto)
    tk.Button(frame_ia, text="Analizar paciente", command=boton_ia, width=16).grid(row=0, column=2, padx=6, pady=4)

# ==========================
# Sección 10: Historial UI
# ==========================
def ventana_historial():
    vh = tk.Toplevel()
    vh.title("Historial de Cambios")
    vh.geometry("540x450")
    vh.resizable(False, False)
    tk.Label(vh, text="Historial de cambios del sistema", font=("Arial", 12, "bold")).pack(pady=10)
    text_hist = tk.Text(vh, width=65, height=22)
    text_hist.pack(padx=10, pady=5)
    historial = cargar_historial()
    if historial:
        for e in historial:
            text_hist.insert(tk.END,
                f"Usuario: {e['usuario']}\n"
                f"Acción: {e['accion']}\n"
                f"Detalle: {e['detalle']}\n"
                f"Fecha y hora: {e['fecha_hora']}\n"
                f"{'-'*60}\n"
            )
    else:
        text_hist.insert(tk.END, "No hay historial registrado.")

#==========================
# Ejecución principal
# =========================
if __name__ == "__main__":
    cargar_datos()
    if not EXTERNAL_LIBS_AVAILABLE:
        print("Aviso: faltan librerías externas (NumPy/Pandas/Matplotlib/Requests).")
        print("Instale: pip install numpy pandas matplotlib requests para funciones avanzadas.")
    ventana_menu()
