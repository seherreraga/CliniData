import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from .. import services, validators, storage

def ventana_citas(parent=None):
    vc = tk.Toplevel(parent) if parent else tk.Tk()
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
        es_val, resf = validators.validar_fecha(fecha)
        if not es_val:
            messagebox.showerror("Error", "Fecha inválida para búsqueda de médicos: " + resf); return
        es_val, resh = validators.validar_hora(hora, fecha)
        if not es_val:
            messagebox.showerror("Error", "Hora inválida para búsqueda de médicos: " + resh); return
        esp = motivo
        disponibles = services.lista_medicos_disponibles(resf, resh, especialidad=esp)
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
            es_val, resultado = validators.validar_cedula(cedula)
            if not es_val:
                messagebox.showerror("Error", resultado); entry_cedula.focus(); return
            cedula_valida = resultado
            es_val, resultado = validators.validar_fecha(fecha)
            if not es_val:
                messagebox.showerror("Error", resultado); entry_fecha.focus(); return
            fecha_valida = resultado
            es_val, resultado = validators.validar_hora(hora, fecha)
            if not es_val:
                messagebox.showerror("Error", resultado); entry_hora.focus(); return
            hora_valida = resultado
            es_val, resultado = validators.validar_texto(motivo, "motivo de consulta")
            if not es_val:
                messagebox.showerror("Error", resultado); entry_motivo.focus(); return
            motivo_valido = resultado
            medico_seleccionado = medico if medico else ""
            ok, msg = services.registrar_cita(cedula_valida, fecha_valida, hora_valida, motivo_valido, medico_seleccionado)
            if ok:
                messagebox.showinfo("Éxito", msg)
                vc.destroy()
            else:
                messagebox.showerror("Error", msg)
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

def ventana_busqueda_filtros(parent=None):
    vb = tk.Toplevel(parent) if parent else tk.Tk()
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
        for c in storage.citas:
            paciente = next((p for p in storage.pacientes if p["cedula"] == c["cedula"]), None)
            nombre_p = paciente["nombre"].lower() if paciente else ""
            if ((not nombre_filtro or nombre_filtro in nombre_p)
                and (not cedula_filtro or cedula_filtro in c["cedula"])
                and (not medico_filtro or medico_filtro in (c.get("medico") or "").lower())
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
