# CliniData

CliniData es un sistema de gestión médica desarrollado en Python con interfaz gráfica Tkinter, diseñado para facilitar el registro y administración de pacientes, citas y médicos en consultorios y clínicas pequeñas.

---

## **Características Principales:**

### **Gestión de Pacientes**
- Registro completo de información del paciente.
- Validación avanzada de datos personales.
- Prevención de registros duplicados.
- Almacenamiento en memoria durante la sesión y persistencia en archivos JSON.

### **Gestión de Citas Médicas**
- Programación de citas con asignación de médico.
- Validación avanzada de horarios y fechas (no se permiten citas en fechas u horas pasadas).
- Control de conflictos de horario para evitar duplicación de citas.
- Nuevo: selección de médico por disponibilidad en función de fecha/hora y servicio solicitado. El paciente puede buscar médicos disponibles para la hora y servicio elegidos y seleccionar uno desde una lista desplegable. Mantiene compatibilidad con entrada manual del nombre del médico.

### **Gestión de Médicos (Nuevo)**
- Registro y listado de médicos con su especialidad.
- Persistencia en archivo medicos.json.
- Función para consultar médicos disponibles en una fecha y hora dadas (considerando conflictos de citas existentes).
- Interfaz para agregar médicos desde la aplicación (ventana "Gestión de Médicos").

### **Búsqueda Avanzada por Filtros**
- Búsqueda de citas utilizando uno o varios filtros combinables:
  - Nombre de paciente
  - Cédula
  - Médico asignado
  - Motivo de consulta
  - Fecha

### **Historial de Cambios**
- Registro automático de todas las acciones sobre pacientes, citas y médicos.
- Guarda usuario (modo admin en esta versión), acción, detalle y fecha/hora.
- Consulta directa del historial desde el menú principal.

### **Análisis y Gráficos (Nuevo)**
- Módulo que utiliza bibliotecas externas (opcional) para análisis y visualización:
  - Estadísticas básicas (edad media, mediana, distribución por rangos).
  - Conteo de citas por mes.
  - Top médicos por número de citas.
  - Gráficas: histograma de edades, barras de citas por mes, barras de top médicos.
- Predicción simple del número de citas del próximo mes mediante regresión lineal (numpy.polyfit).
- Ejemplo de obtención de datos públicos con requests (ejemplo: datos globales COVID desde disease.sh) para demostrar integración con APIs externas.

### **IA simple para recomendaciones (Nuevo)**
- Simulación de un módulo de "IA" simple que sugiere:
  - Prioridad ALTA para pacientes de edad >= 65.
  - Seguimiento proactivo si el paciente tiene más de 3 citas en los últimos 365 días.
  - Recomendaciones operativas basadas en la predicción de citas (estimación de médicos necesarios según capacidad por médico).

## **Validaciones Implementadas**
- **Nombres:** Solo caracteres alfabéticos y espacios (mínimo 2 caracteres).
- **Edad:** Rango válido (0-120 años).
- **Cédula:** Formato numérico (8-10 dígitos).
- **Teléfono:** Formato internacional validado (7-15 dígitos).
- **Fechas:** Formato DD/MM/AAAA, solo fechas futuras permitidas.
- **Horas:** Formato 24 horas (HH:MM). Si la cita es para hoy, solo permite horas posteriores a la actual.

---

## **Guía de Uso**

### **Menú Principal**
Al iniciar la aplicación, se presenta un menú con las siguientes opciones (actualizado):
- Registrar Paciente
- Registrar Cita (ahora con búsqueda de médicos disponibles)
- Gestión de Médicos (Nuevo)
- Búsqueda Avanzada de Citas (por filtros)
- Historial de Cambios
- Análisis y Gráficos (Nuevo)
- Salir

---

### **Registro de Pacientes**
- **Nombre completo:** Solo letras y espacios (mínimo 2 caracteres).
- **Edad:** Número entre 0 y 120.
- **Cédula:** Número de identificación nacional (8-10 dígitos).
- **Teléfono:** Número de contacto (7-15 dígitos).

---

### **Registro de Citas**
- **Cédula del paciente:** Debe corresponder a un paciente registrado (verificada automáticamente).
- **Fecha:** Formato DD/MM/AAAA (no permite fechas pasadas).
- **Hora:** Formato HH:MM en 24 horas. Si es el día actual, solo permite un horario futuro.
- **Motivo / Servicio:** Descripción breve (mínimo 3 caracteres). Nuevo: puede usarse como proxy para filtrar médicos por especialidad.
- **Médico asignado:** Ahora puede seleccionarse desde una lista de médicos disponibles (según fecha/hora y servicio) o introducirse manualmente si se prefiere.

Flujo recomendado en la UI de citas:
1. Ingresar fecha, hora y motivo/servicio.
2. Pulsar "Buscar médicos disponibles".
3. Seleccionar el médico deseado desde el menú desplegable (si hay disponibles).
4. Confirmar la cita (el sistema valida que el médico no tenga conflicto en esa fecha/hora).

---

### **Búsqueda Avanzada de Citas**
1. Ingresa uno o más filtros en los campos correspondientes.
2. Pulsa "Buscar" para ver los resultados. Si dejas campos en blanco, ese filtro no se aplicará.
3. Se mostrarán las citas coincidentes junto con los datos principales del paciente y la cita.

---

### **Consulta de Historial de Cambios**
- Accede al historial completo (acciones realizadas, usuario, fecha y detalles) desde la opción del menú principal.
- Útil para seguimiento y auditoría del funcionamiento del sistema.

---

## **Persistencia y Archivos**
- El sistema almacena los datos en archivos JSON en el mismo directorio donde se ejecuta la aplicación:
  - pacientes.json
  - citas.json
  - medicos.json (Nuevo)
  - historial.json
- No requiere base de datos adicional; la persistencia se hace sobre archivos JSON.

---

## **Requisitos Técnicos**

- Python 3.7 o superior.
- Librerías de la biblioteca estándar: tkinter, json, datetime, re.
- Dependencias externas (opcional, para análisis y gráficas):
  - numpy
  - pandas
  - matplotlib
  - requests

Instalación de dependencias opcionales:
```sh
pip install numpy pandas matplotlib requests
```

---

## **Instalación y Ejecución**

1. Clona o descarga este repositorio:
   ```sh
   git clone https://github.com/seherreraga/CliniData.git
   ```
2. (Opcional) Instala dependencias para análisis:
   ```sh
   pip install numpy pandas matplotlib requests
   ```
3. Ejecuta el archivo principal:
   ```sh
   python CliniData.py
   ```
4. Usa el menú para registrar pacientes, médicos y programar citas. Para asignar médicos automáticamente al registrar citas, usa la opción "Buscar médicos disponibles" en la ventana de registro de citas.

---

## **Notas y Consideraciones**
- Actualmente el sistema opera en modo administrador ("admin" en el historial). La gestión de múltiples usuarios y permisos será implementada en versiones futuras.
- Recomendaciones y mejoras futuras:
  - Convertir "motivo/servicio" en un catálogo controlado para mapear servicios a especialidades con precisión.
  - Agregar horarios de atención por médico, bloqueos por ausencias y turnos parciales.
  - Control de concurrencia: en entornos multiusuario/servidor, re-verificar disponibilidad al confirmar la reserva o implementar locking/endpoint de reserva atómica en el backend.
  - Mostrar información adicional del médico (foto, breve bio, calificaciones) para pacientes nuevos.
  - Mejorar la IA y modelos de predicción usando scikit-learn u otros modelos más robustos.
- Limitaciones actuales:
  - La búsqueda de médicos disponibles es básica: verifica conflicto por fecha/hora exacta y usa el campo "motivo" como proxy de especialidad cuando aplica.
  - Predicción simple basada en regresión lineal sobre conteos mensuales (modelo ilustrativo).

---

**Versión:** 1.2

**Repositorio:** https://github.com/seherreraga/CliniData

**Autores:** Susan Galindo, Andres Morales, Juan Juagibioy, Sergio Herrera
