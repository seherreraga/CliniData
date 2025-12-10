import tkinter as tk
from ..storage import cargar_historial

def ventana_historial(parent=None):
    vh = tk.Toplevel(parent) if parent else tk.Tk()
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
