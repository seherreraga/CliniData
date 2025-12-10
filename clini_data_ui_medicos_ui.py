import tkinter as tk
from tkinter import messagebox
from .. import services

def ventana_medicos(parent=None):
    vm = tk.Toplevel(parent) if parent else tk.Tk()
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
        ok, msg = services.registrar_medico(n, e)
        if ok:
            messagebox.showinfo("Éxito", msg)
            entry_nom.delete(0, tk.END); entry_esp.delete(0, tk.END)
            listar_medicos()
        else:
            messagebox.showerror("Error", msg)

    tk.Button(frame_in, text="Guardar médico", command=boton_guardar_medico, width=16).grid(row=2, column=1, pady=6)

    tk.Label(vm, text="Médicos registrados:").pack(pady=(8,0))
    text_med = tk.Text(vm, width=50, height=10)
    text_med.pack(padx=6, pady=6)

    def listar_medicos():
        text_med.delete("1.0", tk.END)
        if services:
            if storage := __import__('..', fromlist=['storage']).storage:
                pass
        if storage := __import__('..', fromlist=['storage']).storage:
            medicos = storage.medicos
        else:
            medicos = []
        if medicos:
            for m in medicos:
                text_med.insert(tk.END, f"{m['nombre']} - {m.get('especialidad','N/A')}\n")
        else:
            text_med.insert(tk.END, "No hay médicos registrados.")

    listar_medicos()