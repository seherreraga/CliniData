import tkinter as tk
from tkinter import messagebox
from .. import services
from .. import validators

def ventana_pacientes(parent=None):
    vp = tk.Toplevel(parent) if parent else tk.Tk()
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
            es_valido, resultado = validators.validar_nombre(nombre)
            if not es_valido:
                messagebox.showerror("Error", resultado); entry_nombre.focus(); return
            nombre_valido = resultado
            es_valido, resultado = validators.validar_edad(edad)
            if not es_valido:
                messagebox.showerror("Error", resultado); entry_edad.focus(); return
            edad_valida = resultado
            es_valido, resultado = validators.validar_cedula(cedula)
            if not es_valido:
                messagebox.showerror("Error", resultado); entry_cedula.focus(); return
            cedula_valida = resultado
            es_valido, resultado = validators.validar_telefono(telefono)
            if not es_valido:
                messagebox.showerror("Error", resultado); entry_telefono.focus(); return
            telefono_valido = resultado
            ok, msg = services.registrar_paciente(nombre_valido, edad_valida, cedula_valida, telefono_valido)
            if ok:
                messagebox.showinfo("Éxito", msg)
                vp.destroy()
            else:
                messagebox.showerror("Error", msg)
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
