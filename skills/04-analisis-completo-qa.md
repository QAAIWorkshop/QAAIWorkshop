# Skill: Análisis Integral QA 360° (Pruebas, Edge Cases y Estimación QA)
 
## Objetivo
Realizar un análisis completo y cohesionado de una Historia de Usuario (o del Sprint activo) combinando en un único flujo:
1. **Edge Cases y Riesgos Técnicos** (`skills/02-edge-cases.md`).
2. **Matriz de Pruebas Funcionales BDD/Gherkin** (`skills/01-plan-pruebas.md`), incorporando los casos borde críticos detectados.
3. **Estimación Ágil de Esfuerzo QA** (`skills/03-estimacion-puntos.md`), calculada en función de la complejidad de los escenarios y riesgos identificados.
4. **Publicación consolidada** en Jira en un solo comentario estructurado.
 
## Instrucciones de Ejecución
1. **Extracción de datos:**
   - Si el usuario indica un ticket específico (ej. `QAAIW-1`), ejecuta `python scripts/jira_client.py get <TICKET_ID>`.
   - Si el usuario pide analizar el sprint completo, ejecuta `python scripts/jira_client.py sprint active`.
2. **Ejecución encadenada con contexto unificado:**
   - **Paso A — Riesgos y Edge Cases:** Identifica primero al menos 6 casos borde críticos (Datos, Concurrencia, Resiliencia y Seguridad) siguiendo la estructura de `skills/02-edge-cases.md`.
   - **Paso B — Matriz de Pruebas (BDD):** Diseña la matriz de pruebas funcionales (Positivos, Negativos y Casos Borde derivados del Paso A) siguiendo la estructura de `skills/01-plan-pruebas.md`.
   - **Paso C — Estimación de Esfuerzo QA:** Calcula los Story Points QA y el desglose de horas de QA (Diseño, Ejecución Manual, Exploratorias/Edge Cases, Automatización y Regresión) basándote en el volumen real de casos y riesgos de los pasos anteriores, siguiendo la estructura de `skills/03-estimacion-puntos.md` e incluyendo su **Disclaimer obligatorio**.
3. **Formato de salida obligatorio (Reporte Consolidado):**
   Presenta el reporte completo ordenado bajo estos tres encabezados exactos:
   - `## 1. Análisis de Edge Cases y Riesgos Técnicos` (Tabla Markdown)
   - `## 2. Matriz de Pruebas Funcionales (BDD)` (Tabla Markdown)
   - `## 3. Estimación de Esfuerzo QA y Desglose de Horas` (Tablas Markdown + Resumen total + Disclaimer QA)
4. **Publicación automática o confirmada en Jira:**
   - Si el usuario pidió *"analizar y publicar"* (o equivalente), guarda el reporte completo en un archivo temporal `tmp_jira.md`, ejecuta `python scripts/jira_client.py comment-file <TICKET_ID> tmp_jira.md` y elimina `tmp_jira.md`.
   - Si solo pidió el análisis, muestra el reporte completo en pantalla y pregúntale si desea publicarlo ahora mismo como un comentario unificado en Jira.