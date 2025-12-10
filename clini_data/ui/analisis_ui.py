import tkinter as tk
from tkinter import messagebox
import json
from .. import analytics
from .. import validators

def ventana_analisis(parent=None):
    vb = tk.Toplevel(parent) if parent else tk.Tk()
    vb.title("Análisis y Gráficos - CliniData")
    vb.geometry("520x520")
    vb.resizable(False, False)
    vb.grab_set()

    tk.Label(vb, text="Módulo de Análisis y Visualización", font=("Arial", 12, "bold")).pack(pady=8)
    text_res = tk.Text(vb, width=62, height=14)
    text_res.pack(padx=8, pady=6)

    def mostrar_resumen():
        text_res.delete("1.0", tk.END)
        resumen = analytics.analizar_datos()
        text_res.insert(tk.END, resumen)

    def boton_predecir():
        pred, texto = analytics.predecir_citas_proximo_mes()
        if pred is None:
            messagebox.showinfo("Predicción", texto)
        else:
            oper = analytics.recomendacion_operativa(pred)
            messagebox.showinfo("Predicción y recomendación", f"{texto}\n\n{oper}")

    def boton_fetch():
        data, msg = analytics.fetch_public_health_example() if hasattr(analytics, 'fetch_public_health_example') else (None, "No disponible")
        messagebox.showinfo("Datos públicos (ejemplo)", f"{msg}\n\n{json.dumps(data, indent=2)}")

    frame_b = tk.Frame(vb)
    frame_b.pack(pady=6)

    tk.Button(frame_b, text="Generar resumen", command=mostrar_resumen, width=18).grid(row=0, column=0, padx=6, pady=6)
    tk.Button(frame_b, text="Histograma de edades", command=analytics.graficar_histograma_edades, width=18).grid(row=0, column=1, padx=6, pady=6)
    tk.Button(frame_b, text="Citas por mes", command=analytics.graficar_citas_por_mes, width=18).grid(row=1, column=0, padx=6, pady=6)
    tk.Button(frame_b, text="Top médicos", command=analytics.graficar_top_medicos, width=18).grid(row=1, column=1, padx=6, pady=6)
    tk.Button(frame_b, text="Predecir próximo mes", command=boton_predecir, width=18).grid(row=2, column=0, padx=6, pady=6)
    tk.Button(frame_b, text="Obtener datos públicos (ej.)", command=boton_fetch, width=18).grid(row=2, column=1, padx=6, pady=6)

    frame_ia = tk.LabelFrame(vb, text="IA: recomendación por paciente", padx=8, pady=8)
    frame_ia.pack(padx=8, pady=8, fill="x")

    tk.Label(frame_ia, text="Cédula paciente:").grid(row=0, column=0, padx=4, pady=4)
    entry_ced = tk.Entry(frame_ia, width=20)
    entry_ced.grid(row=0, column=1, padx=4, pady=4)
    def boton_ia():
        ced = entry_ced.get().strip()
        es_val, res = validators.validar_cedula(ced)
        if not es_val:
            messagebox.showerror("Error", res); return
        texto = analytics.ia_recomendacion_paciente(res) if hasattr(analytics, 'ia_recomendacion_paciente') else "No disponible"
        messagebox.showinfo("Recomendación IA", texto)
    tk.Button(frame_ia, text="Analizar paciente", command=boton_ia, width=16).grid(row=0, column=2, padx=6, pady=4)
