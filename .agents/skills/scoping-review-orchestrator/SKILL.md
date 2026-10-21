---
name: scoping-review-orchestrator
description: End-to-end autonomous orchestrator and methodological auditor for Scoping Reviews based on JBI guidelines and PRISMA-ScR extensions. Discovers local codebase tools, enforces a cross-dependency coherence loop, builds all manuscript assets (tables, PRISMA flowcharts, figures, checklists), audits against OSF standards, and refactors local scripts.
---

# 🌿 Scoping Review Orchestrator & Methodological Auditor (JBI / PRISMA-ScR)

Esta skill convierte al agente en el **orquestador metodológico y técnico autónomo** del proyecto de revisión exploratoria (*Scoping Review*). Integra y hace cumplir con rigor las directrices del **Joanna Briggs Institute (JBI; Peters et al., 2020)**, el marco clásico de **Arksey y O'Malley (2005)** perfeccionado por **Levac et al. (2010)**, y la declaración oficial **PRISMA-ScR de 22 ítems (Tricco et al., 2018)**.

El orquestador unifica el código en Python (Suite Streamlit, almacenamiento SQLite, conectores a APIs, generadores vectoriales SVG) con la redacción científica del manuscrito principal ([`docs/Artículo-Engel.md`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/docs/Artículo-Engel.md)), garantizando consistencia empírica absoluta sin métricas alucinadas.

---

## 🧭 1. Fundamentos Epistémicos y Delimitación Metodológica

A diferencia de una revisión sistemática tradicional de efectividad clínica, una **revisión exploratoria (scoping review)** cumple funciones epistémicas específicas que el agente debe preservar en todo momento:

| Dimensión | Scoping Review (JBI / PRISMA-ScR) | Revisión Sistemática Convencional |
| :--- | :--- | :--- |
| **Propósito Rector** | Mapear la extensión, rango y naturaleza de la literatura; identificar vacíos de conocimiento (*knowledge gaps*). | Responder una pregunta clínica cerrada sobre eficacia o precisión diagnóstica. |
| **Marco Conceptual** | **PCC:** Población, Concepto, Contexto (amplio y multidimensional). | **PICO:** Población, Intervención, Comparador, Resultado (*Outcome*). |
| **Prerregistro** | **Open Science Framework (OSF; https://osf.io)**. *PROSPERO rechaza scoping reviews*. | **PROSPERO** (CRD York). |
| **Evaluación Crítica (RoB)** | **Opcional (Ítem 12 PRISMA-ScR)**. No se usa como criterio de exclusión documental. | **Obligatoria** con herramientas estandarizadas (RoB 2, ROBINS-I) que ponderan la síntesis. |
| **Síntesis de Datos** | **Vaciado descriptivo (Data Charting)**, matrices temáticas, frecuencias y mapas de distribución. *Sin metanálisis ni forest plots*. | **Metanálisis cuantitativo**, modelos de efectos aleatorios, heterogeneidad $I^2$ y tablas GRADE. |
| **Recomendaciones** | **Descriptivas y propositivas** (políticas, docencia, líneas de investigación). *No formula guías clínicas categóricas*. | **Guías de práctica clínica** basadas en fuerza de evidencia ponderada. |

---

## 🏗️ 2. Bootstrap & Codebase Discovery (Inspección Inicial)

Al activarse o recibir una tarea en el proyecto, el agente **no asume rutas ni funciones a ciegas**. Ejecuta la fase de descubrimiento para mapear el estado vivo del repositorio:

```mermaid
graph TD
    A["1. Inspección del Entorno"] --> B["2. Mapeo de Motores Core"]
    B --> C["3. Verificación de CLI Tools"]
    C --> D["4. Verificación de Invariantes (Audit)"]
    D --> E["5. Orquestación Operativa (Modos 1-4)"]
```

### Inventario de Componentes del Proyecto:
1. **Motores Algorítmicos (`core/`):**
   * [`core/storage.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/core/storage.py): Persistencia SQLite (`data/prisma_project.db`), snapshot JSON, sincronización y deduplicación.
   * [`core/api_fetcher.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/core/api_fetcher.py): Conectores concurrentes a PubMed, SciELO/Europe PMC, Crossref (*Polite Pool*) y OpenAlex con triaje algorítmico.
   * [`core/pcc_data.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/core/pcc_data.py): Protocolo base PCC, países de América Latina, motivos de exclusión y taxonomías.
   * [`core/prisma_diagram.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/core/prisma_diagram.py): Motor de renderizado vectorial SVG nativo del Diagrama de Flujo PRISMA 2020.
   * [`core/prisma_items.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/core/prisma_items.py): Catálogo de los 22 ítems oficiales de PRISMA-ScR.
2. **Herramientas de Terminal Autónomas (`tools/`):**
   * [`tools/coherence_audit.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/tools/coherence_audit.py): Auditor de coherencia bidireccional y ecuaciones de conservación.
   * [`tools/asset_builder.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/tools/asset_builder.py): Generador de insumos empíricos (tablas Markdown, diagramas SVG, checklist y protocolo OSF).
   * [`tools/export_snapshot.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/tools/export_snapshot.py): Exportador del snapshot reproducible a Git y matriz CSV.
   * [`tools/db_cli.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/tools/db_cli.py): CLI rápido para inspección de estadísticas y registros de artículos.
3. **Matrices de Estado (`state/`):**
   * [`state/coherence_matrix.json`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/state/coherence_matrix.json): Registro del balance aritmético, consistencia del manuscrito y checklist.
   * [`state/manuscript_assets.json`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/state/manuscript_assets.json): Catálogo de hashes, tipos y rutas de artefactos empíricos.
4. **Skills Reutilizables:**
   * `prisma-iterative-search`: Búsquedas multi-API y auto-refinamiento de ecuaciones booleanas ([`scripts/iterative_search.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/.agents/skills/prisma-iterative-search/scripts/iterative_search.py)).
   * `pandas-pro` / `pandas-data-analysis`: Manipulación tabular y analítica de datos extraídos.

---

## ⚖️ 3. Mandatos Metodológicos Invariables (Non-Negotiables)

1. **Conservación Aritmética Estricta del Flujo PRISMA 2020:**
   Toda modificación en búsquedas, deduplicación o cribado debe satisfacer en todo momento la ecuación:
   $$\text{Identificados} - \text{Duplicados} = \text{Cribados Fase 1} - \text{Excluidos Fase 1} = \text{Evaluados Texto Completo} - \text{Excluidos Fase 2} = \text{Incluidos Finales}$$
   $$\sum \text{Motivos de Exclusión en Fase 2} = \text{Excluidos en Fase 2}$$
2. **Cero Métricas Alucinadas:**
   Cada cifra reportada en el texto del manuscrito ([`docs/Artículo-Engel.md`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/docs/Artículo-Engel.md)), en las tablas y en las figuras vectoriales proviene directamente de los registros procesados en SQLite y exportados en el snapshot.
3. **Simetría 1:1 de la Tabla 1 (Estudios Incluidos):**
   Los estudios que figuran en la Tabla 1 del manuscrito son estrictamente aquellos con `screening_status = 'included_phase2'`. Las variables (País, Diseño, Muestra, Modalidad MTCI, Condición, Enfoque y Hallazgos) coinciden literalmente con [`data/tabla_1_extraccion.csv`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/data/tabla_1_extraccion.csv) y [`docs/assets/table_1_characteristics.md`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/docs/assets/table_1_characteristics.md).
4. **Portabilidad y Versionado en Git:**
   Como `data/prisma_project.db` está en `.gitignore`, todo cambio relevante debe respaldarse ejecutando [`tools/export_snapshot.py`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/tools/export_snapshot.py) para actualizar `data/project_snapshot.json`, `data/tabla_1_extraccion.csv` y `assets/prisma_flow_diagram.svg`.
5. **Neutralidad Científica y Perspectiva Intercultural:**
   * Evitar afirmaciones categóricas desmedidas (*"las MTCI curan universalmente"* o *"carecen de valor"*). Usar lenguaje cauteloso y descriptivo (*"la evidencia preliminar sugiere"*, *"se documenta una tendencia positiva"*).
   * Delimitar con precisión el rol del psicólogo (autoaplicación vs derivación vs acompañamiento de integración).
   * Reconocer la legitimidad comunitaria de la medicina tradicional indígena y evitar el extractivismo epistémico (Protocolo de Nagoya).
   * Contextualizar en los marcos legales de Nicaragua (Ley No. 759 y Ley No. 774) y la región (PNPIC de Brasil, lineamientos de México/Colombia).

---

## 🔄 4. The Cross-Dependency Control Loop (Motor de Coherencia)

Antes y después de redactar o modificar cualquier sección, tabla o diagrama, el agente ejecuta este bucle de control bidireccional:

```mermaid
graph LR
    Q["1. Pregunta y Objetivos"] <--> P["2. Marco PCC"]
    P <--> E["3. Criterios y Ecuaciones"]
    E <--> D["4. Charting y Flujo PRISMA"]
    D <--> S["5. Síntesis y Checklist"]
```

### Reglas de Verificación:
1. **Auditoría Retrospectiva (*Backward Audit / Grounding*):**
   * ¿Cada variable extraída en el charting responde a una sub-pregunta de investigación explícita?
   * ¿Cada estudio incluido cumple simultáneamente los 3 componentes del marco PCC?
2. **Auditoría Prospectiva (*Forward Audit / Propagation*):**
   * Si se añade una búsqueda o se reclasifica un artículo en SQLite, ejecutar inmediatamente `python tools/export_snapshot.py` y actualizar las cifras en la Sección 3.1 del manuscrito.
3. **Filtro Adversario (*JBI Peer Reviewer Gate*):**
   * Evaluar si alguna afirmación desliza inadvertidamente una conclusión de eficacia causal que requeriría un ensayo clínico ciego o un metanálisis.
   * Verificar que los motivos de exclusión a texto completo sean transparentes, específicos e irreductibles.

---

## 🛠️ 5. Modos de Operación y Comandos CLI

El agente cuenta con cuatro modos operativos especializados:

### Modo 1: Sincronización y Refactorización de Herramientas (`/tool-sync`)
Se activa cuando cambian los esquemas de datos, fallan los scripts o se requiere conectar nuevas fuentes.
```powershell
# Verificar sintaxis de todo el código Python
.venv\Scripts\python.exe -m py_compile core/*.py tools/*.py modules/*.py app.py

# Inspeccionar base de datos y registros desde terminal
.venv\Scripts\python.exe tools/db_cli.py stats
.venv\Scripts\python.exe tools/db_cli.py articles --status included_phase2
```

### Modo 2: Constructor de Insumos Empíricos (`/build-assets`)
Regenera de forma programática todas las tablas, figuras vectoriales y materiales suplementarios:
```powershell
.venv\Scripts\python.exe tools/asset_builder.py
```
**Artefactos producidos en `docs/assets/`:**
* `pcc_operationalization_table.md`: Tabla de operacionalización conceptual y descriptores.
* `eligibility_criteria_matrix.md`: Matriz de inclusión/exclusión y justificaciones epistémicas.
* `search_strategy_table.md`: Sintaxis completa por base de datos, fechas y rendimiento (Ítems 7 y 8).
* `table_1_characteristics.md`: Tabla 1 comparativa con autores, diseño, muestra, MTCI y hallazgos.
* `evidence_distribution_chart.svg`: Esquema vectorial de distribución geográfica, modalidades y diseños.
* `prisma_scr_filled_checklist.md`: Lista oficial de 22 ítems con mapeo exacto a secciones y páginas.
* `docs/osf_preregistration_protocol.md`: Protocolo congelado para registro en OSF.

### Modo 3: Redactor y Editor del Manuscrito (`/draft-section`)
Redacta, ajusta o calibra secciones del manuscrito [`docs/Artículo-Engel.md`](file:///c:/Users/fungicoder/Documents/Fungicoder/Dev/prisma-scr/docs/Artículo-Engel.md):
* Adhiere a **normas APA 7.ª edición** y estilo formal académico.
* Vincula explícitamente los llamados a tablas (`Tabla 1`), figuras (`Figura 1`, `Figura 2`) y materiales suplementarios (`Material Suplementario S1 a S5`).
* Mantiene el Resumen bilingüe (Español y English) estructurado según el Ítem 2 de PRISMA-ScR.

### Modo 4: Auditoría Metodológica de Coherencia (`/audit-review`)
Ejecuta la verificación global de las 5 invariantes metodológicas:
```powershell
# Auditoría diagnóstica
.venv\Scripts\python.exe tools/coherence_audit.py

# Auditoría con auto-reparación y sincronización de snapshot
.venv\Scripts\python.exe tools/coherence_audit.py --fix
```

---

## 🚀 6. Protocolo de Inicio Rápido para el Agente

Cuando el usuario pida:  
*"Activa el skill scoping-review-orchestrator. Como primer paso, ejecuta el Bootstrap & Codebase Discovery..."*

El agente debe:
1. Ejecutar `.venv\Scripts\python.exe tools/coherence_audit.py` para constatar el estado del flujo PRISMA y la coherencia del manuscrito.
2. Presentar al usuario el inventario de herramientas operativas (`tools/`), el estado de las invariantes numéricas y el plan de trabajo metodológico.
3. Si detecta desalineaciones, ejecutar `tools/coherence_audit.py --fix` y `tools/asset_builder.py` para asegurar que el repositorio quede al 100% de coherencia.
