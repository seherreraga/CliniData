Descripción del Proyecto
MediTrack es un sistema de gestión médica desarrollado en Python con interfaz gráfica Tkinter, diseñado para facilitar el registro y administración de pacientes y citas médicas en consultorios y clínicas pequeñas.

Características Principales:


Gestión de Pacientes

-Registro completo de información del paciente

-Validación avanzada de datos personales

-Prevención de registros duplicados

-Almacenamiento en memoria durante la sesión

Gestión de Citas Médicas
-Programación de citas con médicos

-Validación de horarios y fechas

-Control de conflictos de horario

-Asignación de motivo de consulta



Validaciones Implementadas
-Nombres: Solo caracteres alfabéticos y espacios

-Edad: Rango válido (0-120 años)

-Cédula: Formato numérico y longitud específica

-Teléfono: Formato internacional validado

-Fechas: Formato DD/MM/AAAA y validación de fecha futura

-Horas: Formato 24 horas HH:MM


#Guía de Uso#
Menú Principal
-Al iniciar la aplicación, se presenta un menú con tres opciones:
-Registrar Paciente
-Registrar Cita
-Salir


Registro de Pacientes

-Nombre completo: Solo letras y espacios (mínimo 2 caracteres)

-Edad: Número entre 0 y 120

-Cédula: Número de identificación (8-10 dígitos)

-Teléfono: Número de contacto (7-15 dígitos)


Registro de Citas

-Cédula del paciente: Debe corresponder a un paciente registrado

-Fecha: Formato DD/MM/AAAA (no fechas pasadas)

-Hora: Formato HH:MM en 24 horas

-Motivo de consulta: Descripción breve (mínimo 3 caracteres)

-Médico asignado: Nombre del profesional (mínimo 3 caracteres)


Versión: 1.0

Repositorio: https://github.com/seherreraga/MediTrack
