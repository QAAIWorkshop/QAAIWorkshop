# Skill: Análisis de Edge Cases y Riesgos Técnicos
 
## Objetivo
Identificar escenarios límite, condiciones de carrera, fallos de integración y vulnerabilidades de seguridad que no estén explícitos en los criterios de aceptación de una Historia de Usuario o del Sprint completo.
 
## Instrucciones de Ejecución
1. **Extracción de datos:**
   - Si el usuario indica un ticket específico (ej. `QAAIW-1`), ejecuta `python scripts/jira_client.py get <TICKET_ID>`.
   - Si el usuario pide analizar el sprint completo, ejecuta `python scripts/jira_client.py sprint active`.
2. **Dimensiones de análisis obligatorio:**
   - Identifica al menos **6 casos borde (Edge Cases)** críticos cubriendo:
     - **Datos y límites:** Valores nulos, vacíos, caracteres especiales, longitudes máximas o formatos inválidos.
     - **Concurrencia y estado:** Doble envío (double-submit), condiciones de carrera o cambios de estado simultáneos.
     - **Resiliencia e infraestructura:** Timeouts, caídas de red, respuestas parciales o lentitud en servicios externos.
     - **Seguridad y permisos:** Acceso no autorizado, manipulación de parámetros o exposición indebida de datos.
3. **Formato de salida obligatorio:**
   - Presenta los hallazgos en una **tabla Markdown** con las columnas exactas:
     - `Ticket`
     - `ID Riesgo` (ej. `EC-01`)
     - `Categoría` (`Datos` / `Concurrencia` / `Resiliencia` / `Seguridad`)
     - `Escenario Límite`
     - `Impacto`
     - `Severidad` (`Alta` / `Media` / `Baja`)
     - `Mitigación Recomendada`
4. **Cierre interactivo:**
   - Al finalizar, pregunta al usuario si desea publicar este análisis de riesgos como comentario en el ticket de Jira.