# Skill: Estimación Ágil de Esfuerzo QA (Story Points y Horas)
 
## Objetivo
Evaluar la complejidad de pruebas, la incertidumbre y el esfuerzo de aseguramiento de calidad (QA) de una Historia de Usuario individual o de todo el Sprint activo en Jira para proponer una estimación en escala Fibonacci y un desglose de subtareas de QA con estimación en horas.
 
## Instrucciones de Ejecución
1. **Extracción de datos:**
   - Si el usuario indica un ticket específico (ej. `QAAIW-1`), ejecuta `python scripts/jira_client.py get <TICKET_ID>`.
   - Si el usuario pide estimar todo el sprint, ejecuta `python scripts/jira_client.py sprint active`.
2. **Evaluación de esfuerzo de QA:**
   - Analiza cada historia bajo tres criterios enfocados en calidad:
     - **Complejidad de pruebas:** Cantidad de reglas de negocio, validaciones y combinaciones de datos a verificar.
     - **Incertidumbre / Dependencias de QA:** Disponibilidad de ambientes, datos de prueba o servicios externos.
     - **Esfuerzo de ejecución y automatización:** Tiempo requerido para diseño, ejecución manual, pruebas exploratorias y automatización.
3. **Formato de salida obligatorio:**
   - **Resumen de Estimación QA (Tabla Markdown):**
     - `Ticket`
     - `Historia`
     - `Complejidad QA` (`Baja` / `Media` / `Alta`)
     - `Incertidumbre` (`Baja` / `Media` / `Alta`)
     - `Story Points QA (Fibonacci)` (`1, 2, 3, 5, 8, 13`)
     - `Total Horas QA`
     - `Justificación`
   - **Desglose de Subtareas de QA (Tabla Markdown):**
     - `Ticket`
     - `Tipo de Actividad QA` (`Diseño de Casos` / `Ejecución Manual` / `Pruebas Exploratorias & Edge Cases` / `Automatización` / `Regresión`)
     - `Subtarea QA`
     - `Entregable`
     - `Horas Estimadas QA` (rango realista en horas, ej. `3h`)
   - Incluye al final de la tabla la **suma total de horas de QA** por ticket y el gran total del sprint (si aplica).
   - **Disclaimer obligatorio (incluir siempre al final del reporte):**
     > **Nota / Disclaimer:** Esta estimación contempla **únicamente el esfuerzo y las horas correspondientes a las actividades de Aseguramiento de Calidad (QA)** (diseño, ejecución, pruebas exploratorias y automatización). No incluye tiempos de desarrollo (Backend/Frontend), arquitectura, despliegue ni gestión de proyecto.
4. **Cierre interactivo:**
   - Al finalizar, pregunta al usuario si desea publicar esta estimación de QA (incluyendo el disclaimer) como comentario en el ticket de Jira.