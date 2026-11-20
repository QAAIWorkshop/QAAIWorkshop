# Skill: Generación de Matriz de Pruebas Funcionales (BDD / Gherkin)
 
## Objetivo
Analizar una Historia de Usuario individual o todas las historias del Sprint activo en Jira para diseñar una matriz de casos de prueba estructurada, trazable y lista para ejecutar.
 
## Instrucciones de Ejecución
1. **Extracción de datos:**
   - Si el usuario indica un ticket específico (ej. `CQA-1`), ejecuta `python scripts/jira_client.py get <TICKET_ID>`.
   - Si el usuario pide analizar el sprint completo, ejecuta `python scripts/jira_client.py sprint active`.
2. **Análisis de cobertura:**
   - Desglosa cada Criterio de Aceptación y asegúrate de incluir escenarios **Positivos** (flujo feliz), **Negativos** (validaciones y errores esperados) y de **Regresión/Integración** si aplica.
3. **Formato de salida obligatorio:**
   - Presenta la matriz en una **tabla Markdown** con las siguientes columnas exactas:
     - `Ticket` (Clave de Jira, ej. `CQA-1`)
     - `ID Caso` (ej. `TC-01`)
     - `Escenario de Prueba`
     - `Tipo` (`Positivo` / `Negativo`)
     - `Precondiciones`
     - `Pasos (Dado / Cuando / Entonces)`
     - `Resultado Esperado`
4. **Cierre interactivo:**
   - Al finalizar la tabla, pregunta explícitamente al usuario si desea publicar esta matriz de pruebas como comentario en el ticket de Jira correspondiente.