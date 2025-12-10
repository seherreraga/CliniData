import tkinter as tk
from . import pacientes_ui, citas_ui, medicos_ui, analisis_ui, historial_ui
from .. import storage
from ..analytics import EXTERNAL_LIBS_AVAILABLE

def ventana_menu():
    ventana = tk.Tk()
    ventana.title("CliniData - Menú Principal")
    ventana.geometry("360x300")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Bienvenido a CliniData", font=("Arial", 14)).pack(pady=10)
    tk.Button(ventana, text="Registrar Paciente", command=lambda: pacientes_ui.ventana_pacientes(ventana), width=28).pack(pady=4)
    tk.Button(ventana, text="Registrar Cita", command=lambda: citas_ui.ventana_citas(ventana), width=28).pack(pady=4)
    tk.Button(ventana, text="Gestión de Médicos", command=lambda: medicos_ui.ventana_medicos(ventana), width=28).pack(pady=4)
    tk.Button(ventana, text="Historial de Cambios", command=lambda: historial_ui.ventana_historial(ventana), width=28).pack(pady=4)
    tk.Button(ventana, text="Búsqueda Avanzada", command=lambda: citas_ui.ventana_busqueda_filtros(ventana), width=28).pack(pady=4)
    tk.Button(ventana, text="Análisis y Gráficos", command=lambda: analisis_ui.ventana_analisis(ventana), width=28).pack(pady=4)
    tk.Button(ventana, text="Salir", command=ventana.destroy, width=28).pack(pady=8)

    if not EXTERNAL_LIBS_AVAILABLE:
        print("Aviso: faltan librerías externas (NumPy/Pandas/Matplotlib/Requests).")
        print("Instale: pip install numpy pandas matplotlib requests para funciones avanzadas.")

    ventana.mainloop()