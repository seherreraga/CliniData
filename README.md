# CliniData

CliniData es un sistema de gestión médica desarrollado en Python con interfaz gráfica (ahora con PyQt5), diseñado para facilitar el registro y administración de pacientes, citas y médicos en consultorios y clínicas pequeñas.

Esta versión incluye nuevas mejoras de interfaz, modularidad y soporte para estilos y logos basados en la imagen de marca (assets + QSS).

---

## Novedades principales (versión 1.2 → posterior)

- Interfaz gráfica migrada / añadida con PyQt5:
  - Nuevo subpaquete `clini_data.ui_pyqt` con ventana principal y diálogos (pacientes, citas, médicos, historial, análisis).
  - Archivo `main.py` actualizado para arrancar la aplicación PyQt5 y cargar estilos (QSS) y recursos (icono/logo).
- Modularidad mejorada:
  - Paquete principal `clini_data` con módulos separados:
    - `storage` (persistencia JSON y registro de historial)
    - `services` (lógica de negocio: registrar pacientes/citas/médicos, validaciones de alto nivel, wrappers)
    - `validators` (validaciones reutilizables)
    - `analytics` (análisis y predicción de citas; opcional según librerías externas)
    - `ui_pyqt` (subpaquete con diálogos y ventana principal para PyQt5)
  - Se añadieron wrappers y funciones de conveniencia (ej.: `services.obtener_historial()`).
- Soporte para branding (logo y colores):
  - Carpeta de assets: `clini_data/assets/logo/` (logo SVG/PNG y variantes).
  - Hoja de estilos QSS: `clini_data/ui_pyqt/styles.qss` con paleta basada en el logo.
  - Módulo `clini_data/ui_pyqt/resources.py` para cargar imágenes/íconos desde el paquete.
- UI/UX:
  - Ventana principal rediseñada con splitter (menú izquierdo + contenido derecho), permitiendo redimensionado.
  - Diálogos actualizados: validaciones de campos, llamadas correctas a `services` y mensajes de usuario.
  - Tamaños y políticas ajustadas para mejor uso en pantallas grandes (resize, minimumSize).
- Correcciones menores:
  - `main.py` corregido (import `sys` incluido).
  - Eliminadas dependencias cruzadas innecesarias (ej.: import de `tkinter.messagebox` desde `services`).
  - Compatibilidad con ejecución sin librerías externas de análisis (analytics detecta ausencia de numpy/pandas/matplotlib/requests).

---

## Características Principales

### Gestión de Pacientes
- Registro completo de información del paciente.
- Validación avanzada de datos personales.
- Prevención de registros duplicados.
- Persistencia en JSON (`pacientes.json`).

### Gestión de Citas Médicas
- Programación de citas con asignación de médico.
- Validación de horarios y fechas (no se permiten citas en fechas u horas pasadas).
- Control de conflictos de horario.
- Ahora soporta búsqueda de médicos disponibles por fecha/hora y servicio/motivo.

### Gestión de Médicos
- Registro y listado de médicos con su especialidad.
- Persistencia en `medicos.json`.
- Consulta de médicos disponibles considerando citas existentes.

### Historial de Cambios
- Registro automático de acciones (usuario/acción/detalle/fecha-hora).
- Consulta desde la UI (Historial de Cambios).
- Función pública: `services.obtener_historial()`.

### Análisis y Visualización (opcional)
- Estadísticas: edad media, mediana, distribución por rangos.
- Conteo de citas por mes y Top médicos.
- Predicción simple del número de citas del siguiente mes (regresión lineal con numpy).
- Integración ejemplo con APIs públicas (requests).

---

## Paleta y Branding (recomendada)
Paleta aproximada extraída del logo:
- Primario oscuro: #1F3C88
- Primario medio: #375FA9
- Accent claro: #6E8FCE
- Fondo claro para formularios: #EAF0FA
- Texto oscuro: #222831
- Texto sobre azul: #FFFFFF

Assets recomendados (ubicación):
- clini_data/assets/logo/logo_primary.svg
- clini_data/assets/logo/logo_primary.png
- clini_data/assets/logo/logo_icon_128.png
- clini_data/assets/logo/logo_icon_64.png
- clini_data/assets/logo/logo_white.svg
- clini_data/assets/logo/bg_gradient.png (opcional)

Stylesheet (QSS):
- clini_data/ui_pyqt/styles.qss — carga automática desde `main.py` si existe.

---

## Requisitos Técnicos

- Python 3.7 o superior.
- Dependencia para UI:
  - PyQt5
- Dependencias opcionales (para analytics):
  - numpy, pandas, matplotlib, requests

Instalación (ejemplo con pip):
```sh
pip install pyqt5
# Opcional para análisis:
pip install numpy pandas matplotlib requests
```

---


## Estructura del proyecto (resumen)

- clini_data/
  - __init__.py
  - storage.py           # carga/guarda JSON, registrar_cambio, cargar_historial
  - services.py          # lógica de negocio (registrar_paciente, registrar_cita, registrar_medico, lista_medicos_disponibles, obtener_historial, ...)
  - validators.py        # funciones de validación reutilizables
  - analytics.py         # análisis / predicción (opcional)
  - ui_pyqt/
    - __init__.py
    - main_window.py     # ventana principal PyQt5 (nuevo)
    - resources.py       # helpers para cargar logos/iconos
    - styles.qss         # hoja de estilos QSS (opcional)
    - pacientes_dialog.py
    - citas_dialog.py
    - medicos_dialog.py
    - historial_dialog.py
    - analisis_window.py
- main.py                # arranque de la aplicación (PyQt5)
- pacientes.json
- citas.json
- medicos.json
- historial.json

---

## Buenas prácticas y notas de desarrollo

- Mantén el paquete `clini_data` modular: la UI llama a `services` y `services` usa `storage`. Evita que la lógica de negocio dependa de widgets o toolkits.
- Guarda assets en `clini_data/assets` y accede vía `clini_data.ui_pyqt.resources` para que la carga funcione correctamente cuando el paquete sea instalado o empaquetado.
- Para persistencia multiusuario/servidor considera migrar a una base de datos en vez de archivos JSON.
- Para producción en Windows/macOS genera `ico`/`icns` y usa `app.setWindowIcon()` con esos recursos.

---


## Ejecución de pruebas y depuración
- Hay validaciones en `validators.py` y cobertura manual a través de la UI.
- Para depurar, revisa la salida en consola y los archivos JSON generados.
- Si la aplicación no encuentra `styles.qss` o los assets, imprimirá warnings y seguirá funcionando con estilos por defecto.

---

**Versión:** 1.2+ (actualización PyQt5 y modularidad)

**Repositorio:** https://github.com/seherreraga/CliniData

**Autores:** Susan Galindo, Andres Morales, Juan Juagibioy, Sergio Herrera
