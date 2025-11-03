# Clinidata

CliniData es un sistema de gestión médica desarrollado en Python con interfaz gráfica Tkinter, diseñado para facilitar el registro y administración de pacientes y citas médicas en consultorios y clínicas pequeñas.

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
  
### **Búsqueda Avanzada por Filtros**
- Búsqueda de citas utilizando uno o varios filtros combinables:
  - Nombre de paciente
  - Cédula
  - Médico asignado
  - Motivo de consulta
  - Fecha

### **Historial de Cambios**
- Registro automático de todas las acciones sobre pacientes y citas.
- Guarda usuario (modo admin en esta versión), acción, detalle y fecha/hora.
- Consulta directa del historial desde el menú principal.

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
Al iniciar la aplicación, se presenta un menú con las siguientes opciones:
- Registrar Paciente
- Registrar Cita
- Búsqueda Avanzada de Citas (por filtros)
- Historial de Cambios
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
- **Motivo de consulta:** Descripción breve (mínimo 3 caracteres).
- **Médico asignado:** Nombre del profesional (mínimo 3 caracteres).

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

El sistema almacena los datos en archivos JSON (pacientes.json, citas.json, historial.json) en el mismo directorio donde se ejecuta la aplicación. No requiere base de datos adicional ni instalación de dependencias fuera de la biblioteca estándar de Python.

---

## **Requisitos Técnicos**

- Python 3.7 o superior.
- Librerías de la biblioteca estándar (`tkinter`, `json`, `datetime`, `re`).

---

## **Instalación y Ejecución**

1. Clona o descarga este repositorio.
2. Ejecuta el archivo principal:
   ```sh
   python clinidata.py
   ```
3. Comienza a registrar pacientes y citas desde la interfaz gráfica.

---

## **Notas y Consideraciones**

- Actualmente el sistema está operando en modo administrador ("admin" para historial). La gestión de múltiples usuarios será implementada en versiones futuras.

---


**Versión:** 1.1 

**Repositorio:** https://github.com/seherreraga/CliniData

**Autores:** Susan Galindo, Andres Morales, Juan Juagibioy, Sergio Herrera
