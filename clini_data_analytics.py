import math
try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import requests
    EXTERNAL_LIBS_AVAILABLE = True
except Exception:
    EXTERNAL_LIBS_AVAILABLE = False

from . import storage
from datetime import datetime

def crear_dataframes():
    if not EXTERNAL_LIBS_AVAILABLE:
        return None, None
    df_p = pd.DataFrame(storage.pacientes)
    df_c = pd.DataFrame(storage.citas)
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