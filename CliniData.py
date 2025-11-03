import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime
import json

# ==========================
# Sección 1: Variables globales
# ==========================
pacientes = []
citas = []

#==================================
#Sección 2: Manejo de archivos JSON
#==================================
#Nuevo

def guardar_datos():
    """Guarda pacientes y citas en archivos JSON"""
    with open("pacientes.json", "w") as f:
        json.dump(pacientes, f, indent=4)
    with open("citas.json", "w") as f:
        json.dump(citas, f, indent=4)

def cargar_datos():
    global pacientes, citas
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

#==========================================
#Sección 3: Registro de cambios (Historial)
#==========================================
#Nuevo

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
        # Si me mandan la fecha comparar contra ahora
        if fecha_str:
            fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
            ahora = datetime.now()
            if fecha_obj.date() == ahora.date() and hora_obj.time() <= ahora.time():
                return False, "No se puede agendar una cita en una hora pasada para hoy"
        return True, hora_obj.strftime('%H:%M') 
    except ValueError:
        return False, "Hora inválida. Use formato 24 horas (00:00 - 23:59)"

def validar_texto(texto, campo, min_len=3):
    """Valida texto general"""
    texto = texto.strip()
    
    if not texto:
        return False, f"El {campo} no puede estar vacío"
    
    if len(texto) < min_len:
        return False, f"El {campo} debe tener al menos {min_len} caracteres"
    
    return True, texto

def paciente_existe(cedula):
    """Verifica si un paciente ya está registrado"""
    for paciente in pacientes:
        if paciente['cedula'] == cedula:
            return True
    return False

# ==========================
# Sección 5: Funciones de lógicas
# ==========================
def registrar_paciente(nombre, edad, cedula, telefono):
    """Registra paciente con validaciones"""
    
    if paciente_existe(cedula):
        messagebox.showerror("Error", "Ya existe un paciente con esta cédula")
        return False
    
    paciente = {
        "nombre": nombre, 
        "edad": edad, 
        "cedula": cedula, 
        "telefono": telefono
    }
    pacientes.append(paciente)
    print(f"Paciente registrado: {paciente}")

    guardar_datos()
    registrar_cambio("admin", "Registro de paciente", f"{nombre} ({cedula})")
    
    return True

def registrar_cita(cedula, fecha, hora, motivo, medico):
    """Registra cita con validaciones"""
    
    if not paciente_existe(cedula):
        messagebox.showerror("Error", "No existe un paciente con esta cédula")
        return False
    
    for cita in citas:
        if (cita['cedula'] == cedula and 
            cita['fecha'] == fecha and 
            cita['hora'] == hora):
            messagebox.showerror("Error", "El paciente ya tiene una cita en esta fecha y hora")
            return False
    
    cita = {
        "cedula": cedula, 
        "fecha": fecha, 
        "hora": hora, 
        "motivo": motivo, 
        "medico": medico
    }
    citas.append(cita)
    print(f"Cita registrada: {cita}") 

    guardar_datos()
    registrar_cambio("admin", "Registro de cita", f"{cedula} - {fecha} {hora}")
    return True

# ==========================
# Sección 6: Interfaz gráfica 
# ==========================
def ventana_menu():
    ventana = tk.Tk()
    ventana.title("CliniData - Menú Principal")
    ventana.geometry("300x200")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Bienvenido a CliniData", font=("Arial", 14)).pack(pady=10)
    tk.Button(ventana, text="Registrar Paciente", command=ventana_pacientes, width=20).pack(pady=5)
    tk.Button(ventana, text="Registrar Cita", command=ventana_citas, width=20).pack(pady=5)
    tk.Button(ventana, text="Historial de Cambios", command=ventana_historial, width=20).pack(pady=5)
    tk.Button(ventana, text="Búsqueda Avanzada", command=ventana_busqueda_filtros, width=20).pack(pady=5)
    
    tk.Button(ventana, text="Salir", command=ventana.destroy, width=20).pack(pady=10)

    ventana.mainloop()

def ventana_pacientes():
    vp = tk.Toplevel()
    vp.title("Registro de Pacientes")
    vp.geometry("350x400")
    vp.resizable(False, False)
    vp.grab_set() 

    tk.Label(vp, text="Registro de Paciente", font=("Arial", 12, "bold")).pack(pady=10)

    # Nombre
    tk.Label(vp, text="Nombre completo *").pack(anchor="w", padx=20)
    entry_nombre = tk.Entry(vp, width=30)
    entry_nombre.pack(pady=(0, 10), padx=20)
    entry_nombre.focus()

    # Edad
    tk.Label(vp, text="Edad *").pack(anchor="w", padx=20)
    entry_edad = tk.Entry(vp, width=30)
    entry_edad.pack(pady=(0, 10), padx=20)

    # Cédula
    tk.Label(vp, text="Cédula *").pack(anchor="w", padx=20)
    entry_cedula = tk.Entry(vp, width=30)
    entry_cedula.pack(pady=(0, 10), padx=20)

    # Teléfono
    tk.Label(vp, text="Teléfono *").pack(anchor="w", padx=20)
    entry_telefono = tk.Entry(vp, width=30)
    entry_telefono.pack(pady=(0, 20), padx=20)

    def guardar_paciente():
        try:
            # Validar todos los campos
            nombre = entry_nombre.get()
            edad = entry_edad.get()
            cedula = entry_cedula.get()
            telefono = entry_telefono.get()

            # Validar nombre
            es_valido, resultado = validar_nombre(nombre)
            if not es_valido:
                messagebox.showerror("Error", resultado)
                entry_nombre.focus()
                return
            nombre_valido = resultado

            # Validar edad
            es_valido, resultado = validar_edad(edad)
            if not es_valido:
                messagebox.showerror("Error", resultado)
                entry_edad.focus()
                return
            edad_valida = resultado

            # Validar cédula
            es_valido, resultado = validar_cedula(cedula)
            if not es_valido:
                messagebox.showerror("Error", resultado)
                entry_cedula.focus()
                return
            cedula_valida = resultado

            # Validar teléfono
            es_valido, resultado = validar_telefono(telefono)
            if not es_valido:
                messagebox.showerror("Error", resultado)
                entry_telefono.focus()
                return
            telefono_valido = resultado

            # Registrar paciente
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
    vc.geometry("350x450")
    vc.resizable(False, False)
    vc.grab_set()

    tk.Label(vc, text="Registro de Cita Médica", font=("Arial", 12, "bold")).pack(pady=10)

    # Cédula del paciente
    tk.Label(vc, text="Cédula del paciente *").pack(anchor="w", padx=20)
    entry_cedula = tk.Entry(vc, width=30)
    entry_cedula.pack(pady=(0, 10), padx=20)
    entry_cedula.focus()

    # Fecha
    tk.Label(vc, text="Fecha (DD/MM/AAAA) *").pack(anchor="w", padx=20)
    entry_fecha = tk.Entry(vc, width=30)
    entry_fecha.pack(pady=(0, 10), padx=20)
    entry_fecha.insert(0, datetime.now().strftime('%d/%m/%Y'))  # Fecha actual por defecto

    # Hora
    tk.Label(vc, text="Hora (HH:MM) *").pack(anchor="w", padx=20)
    entry_hora = tk.Entry(vc, width=30)
    entry_hora.pack(pady=(0, 10), padx=20)
    entry_hora.insert(0, "09:00")  # Hora por defecto

    # Motivo
    tk.Label(vc, text="Motivo de la consulta *").pack(anchor="w", padx=20)
    entry_motivo = tk.Entry(vc, width=30)
    entry_motivo.pack(pady=(0, 10), padx=20)

    # Médico
    tk.Label(vc, text="Médico asignado *").pack(anchor="w", padx=20)
    entry_medico = tk.Entry(vc, width=30)
    entry_medico.pack(pady=(0, 20), padx=20)

    def guardar_cita():
        try:
            # Validar todos los campos
            cedula = entry_cedula.get()
            fecha = entry_fecha.get()
            hora = entry_hora.get()
            motivo = entry_motivo.get()
            medico = entry_medico.get()

            # Validar cédula
            es_valido, resultado = validar_cedula(cedula)
            if not es_valido:
                messagebox.showerror("Error", resultado)
                entry_cedula.focus()
                return
            cedula_valida = resultado

            # Validar fecha
            es_valido, resultado = validar_fecha(fecha)
            if not es_valido:
                messagebox.showerror("Error", resultado)
                entry_fecha.focus()
                return
            fecha_valida = resultado

            # Validar hora
            es_valido, resultado = validar_hora(hora, fecha)
            if not es_valido:
                messagebox.showerror("Error", resultado)
                entry_hora.focus()
                return
            hora_valida = resultado

            # Validar motivo
            es_valido, resultado = validar_texto(motivo, "motivo de consulta")
            if not es_valido:
                messagebox.showerror("Error", resultado)
                entry_motivo.focus()
                return
            motivo_valido = resultado

            # Validar médico
            es_valido, resultado = validar_texto(medico, "nombre del médico")
            if not es_valido:
                messagebox.showerror("Error", resultado)
                entry_medico.focus()
                return
            medico_valido = resultado

            # Registrar cita
            if registrar_cita(cedula_valida, fecha_valida, hora_valida, motivo_valido, medico_valido):
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
        entry_cedula.focus()

    # Frame para botones
    frame_botones = tk.Frame(vc)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Guardar", command=guardar_cita, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botones, text="Limpiar", command=limpiar_campos, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botones, text="Cancelar", command=vc.destroy, width=10).pack(side=tk.LEFT, padx=5)

# ============================
# Sección 7: Búsqueda avanzada con filtros
# ============================
#Nuevo
def ventana_busqueda_filtros():
    vb = tk.Toplevel()
    vb.title("Búsqueda Avanzada por Filtros")
    vb.geometry("500x470")
    vb.resizable(False, False)

    tk.Label(vb, text="Búsqueda avanzada de citas", font=("Arial", 12, "bold")).pack(pady=10)
    # Campos de filtro
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

    # Área de resultados
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
            if (
                (not nombre_filtro or nombre_filtro in nombre_p)
                and (not cedula_filtro or cedula_filtro in c["cedula"])
                and (not medico_filtro or medico_filtro in c["medico"].lower())
                and (not motivo_filtro or motivo_filtro in c["motivo"].lower())
                and (not fecha_filtro or fecha_filtro == c["fecha"])
            ):
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
# Sección 8: Ejecución principal
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
    ventana_menu()

