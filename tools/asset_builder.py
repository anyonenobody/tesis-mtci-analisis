#!/usr/bin/env python3
"""
Autonomous Manuscript Asset Builder for PRISMA-ScR Reviews.
Generates, synchronizes, and audits all empirical artifacts:
- Tables: PCC Operationalization, Eligibility Matrix, Search Strategies, Study Characteristics (Table 1)
- Diagrams & Figures: PRISMA-ScR SVG Flowchart, Evidence Mapping Visualizations
- Checklists & Preregistration: PRISMA-ScR 22-item Checklist, Standalone OSF Protocol
- Asset State Registry: state/manuscript_assets.json
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List

# Reconfigure stdout/stderr for Unicode/UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure repository root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
PRISMA_SCR_FALLBACK = r"c:\Users\fungicoder\Documents\Fungicoder\Dev\prisma-scr"
if os.path.exists(PRISMA_SCR_FALLBACK) and PRISMA_SCR_FALLBACK not in sys.path:
    sys.path.append(PRISMA_SCR_FALLBACK)

from core.storage import (
    get_connection,
    get_prisma_flow_numbers,
    get_charting_data,
    get_articles,
    get_checklist,
    get_search_logs,
    export_project_snapshot,
    CSV_TABLE1_PATH,
    SNAPSHOT_PATH
)
from core.pcc_data import (
    DEFAULT_PROTOCOL,
    LATAM_COUNTRIES,
    DEFAULT_EXCLUSION_REASONS,
    MTCI_MODALITIES,
    PSYCHOLOGICAL_CONDITIONS,
    PSYCHOTHERAPEUTIC_APPROACHES
)
from core.prisma_diagram import generate_prisma_svg
from tools.export_supplementary_docx import export_supplementary_materials_docx, OUT_DOCX_PATH

ASSETS_DIR = os.path.join(REPO_ROOT, "docs", "assets")
STATE_DIR = os.path.join(REPO_ROOT, "state")
MANUSCRIPT_ASSETS_JSON = os.path.join(STATE_DIR, "manuscript_assets.json")


def compute_file_hash(filepath: str) -> str:
    """Calcula hash SHA256 de un archivo para control de versiones."""
    if not os.path.exists(filepath):
        return ""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()[:12]


def build_pcc_table() -> str:
    """Genera la Tabla de Operacionalización del Marco Conceptual PCC (JBI)."""
    pcc = DEFAULT_PROTOCOL
    pop = pcc["pcc"]["population"]
    con = pcc["pcc"]["concept"]
    ctx = pcc["pcc"]["context"]

    content = f"""# Tabla de Operacionalización del Marco Conceptual PCC (JBI)

| Componente PCC | Definición Conceptual Operativa | Descriptores DeCS / MeSH Principales | Límites e Inclusiones Metodológicas |
| :--- | :--- | :--- | :--- |
| **Población (P)** | {pop} | *Salud mental, psicoterapia, consultantes, estudiantes, profesionales de psicología* | Cualquier grupo etario atendido en salud mental; profesionales o estudiantes cuando evalúan intervenciones MTCI. |
| **Concepto (C)** | {con} | *Medicina tradicional, terapias complementarias, fitoterapia, acupuntura, mindfulness, saberes ancestrales* | Prácticas MTCI (fitoterapia, acupuntura, mindfulness, saberes ancestrales) integradas o co-manejadas en psicología. |
| **Contexto (C)** | {ctx} | *América Latina, Caribe, Nicaragua, Brasil, Colombia, México, Chile, atención primaria, salud comunitaria* | Ámbitos comunitarios, clínicos, hospitalarios o atención primaria en América Latina y el Caribe (2016–2026). |

### Justificación Metodológica:
La formulación sigue estrictamente las directrices del *Joanna Briggs Institute* (JBI; Peters et al., 2020) para revisiones exploratorias (*scoping reviews*). A diferencia del esquema comparativo PICO, el marco PCC permite mapear de manera comprensiva y no excluyente la amplitud de la literatura empírica regional sin forzar comparadores farmacológicos pasivos o restricciones artificiales en la intervención.
"""
    out_path = os.path.join(ASSETS_DIR, "pcc_operationalization_table.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path


def build_eligibility_matrix() -> str:
    """Genera la Matriz Detallada de Criterios de Elegibilidad."""
    content = """# Matriz Metodológica de Criterios de Elegibilidad (PRISMA-ScR Ítem 6)

| Dimensión | Criterios de Inclusión (Aceptación) | Criterios de Exclusión (Descarte) | Justificación Epistémica y Metodológica |
| :--- | :--- | :--- | :--- |
| **Población** | Personas de cualquier franja etaria receptoras de atención psicológica/salud mental, o profesionales/estudiantes en formación clínica. | Modelos animales (*in vivo*), cultivos celulares (*in vitro*) o estudios botánicos sin evaluación clínica en seres humanos. | Preservar el foco conductual, afectivo y relacional de la ciencia psicológica frente al tamizaje fitoquímico somático. |
| **Concepto** | Modalidades de MTCI articuladas, co-administradas o investigadas en conjunción con procesos psicoterapéuticos o de salud mental. | Intervenciones MTCI dirigidas de forma exclusiva a patologías somáticas (e.g. neoplasias, infecciones) sin mediación psicológica. | Evitar el sesgo de agregación somática y circunscribir el alcance a la salud mental integrativa. |
| **Contexto** | Estudios empíricos ejecutados en países de América Latina y el Caribe, o con poblaciones de origen cultural latinoamericano. | Investigaciones conducidas en contextos geográficos y culturales ajenos a América Latina (Asia, Europa, Norteamérica anglosajona). | Responder a la singularidad contextual, legal (Ley 759/774, PNPIC) e intercultural de la región. |
| **Temporalidad** | Artículos científicos publicados en el decenio comprendido entre enero de 2016 y diciembre de 2026. | Publicaciones previas a 2016 o literatura anacrónica desprovista de vigencia técnica. | Capturar la producción científica más reciente y actualizada bajo los marcos regulatorios contemporáneos. |
| **Diseño del Estudio** | Diseños empíricos primarios: ensayos controlados, cuasiexperimentos, estudios observacionales, series de casos y cualitativos. | Editoriales de opinión, cartas al director sin datos primarios, ensayos de divulgación periodística, resúmenes sin informe metodológico. | Asegurar un umbral de rigor metodológico mínimo verificable manteniendo la pluralidad de diseños de la scoping review. |
| **Idioma y Acceso** | Documentos redactados en español, portugués e inglés con informe a texto completo recuperable. | Textos completos no disponibles tras agotar repositorios de acceso abierto y canales de conmutación interbibliotecaria. | Garantizar la trazabilidad y reproducibilidad de la extracción de datos sin barreras de opacidad documental. |
"""
    out_path = os.path.join(ASSETS_DIR, "eligibility_criteria_matrix.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path


def build_search_strategy_table() -> str:
    """Genera la Tabla de Documentación de Estrategias de Búsqueda (PRISMA-ScR Ítems 7 y 8)."""
    search_logs = get_search_logs()
    
    table_rows = []
    total_hits = 0
    for log in search_logs:
        db_name = log.get("database_name", "N/A")
        s_date = log.get("search_date", "N/A")
        count = log.get("results_count", 0)
        total_hits += count
        query_str = log.get("search_string", "").replace("|", "\\|")
        table_rows.append(f"| **{db_name}** | {s_date} | `{query_str}` | Última década (2016–2026); Español, Portugués, Inglés | **{count}** |")

    content = f"""# Documentación de Estrategias de Búsqueda en Fuentes de Evidencia (PRISMA-ScR Ítems 7 y 8)

*Fecha de corte de la búsqueda bibliográfica:* Febrero de 2024 / Actualización continua  
*Total de registros primarios identificados:* **{total_hits}**

| Base de Datos / Fuente | Fecha de Ejecución | Ecuación Booleana y Sintaxis Completa | Límites y Filtros Aplicados | Rendimiento (Registros) |
| :--- | :---: | :--- | :--- | :---: |
""" + "\n".join(table_rows) + f"""
| **TOTAL IDENTIFICADOS** | — | **Ecuaciones combinadas en las 5 fuentes científicas** | — | **{total_hits}** |

### Estrategia de Búsqueda Secuencial en Dos Fases:
1. **Fase 1 (Vocabulario Controlado MeSH / DeCS - Paraguas):**
   * *MTCI Trilingüe:* `"medicina tradicional" OR "terapias complementarias" OR "medicina integrativa" OR "prácticas integrativas y complementarias" OR "traditional medicine" OR "complementary therapies" OR "integrative medicine" OR "práticas integrativas e complementares" OR "PICS"`
   * *Psicología Troncal:* `"psicoterapia" OR "psicología" OR "salud mental" OR "intervención psicológica" OR "psychotherapy" OR "psychology" OR "mental health" OR "saúde mental" OR "atenção psicossocial"`
2. **Fase 2 (Prácticas Específicas Desagregadas & Enfoques Clínicos):**
   * *Clústeres MTCI:* Fitoterapia/herbolaria, Acupuntura/auriculoterapia, Mindfulness/contemplativas/yoga, Saberes ancestrales/indígenas/ayahuasca, Terapias florales/reiki, Arteterapia integrativa/biodanza.
   * *Enfoques Clínicos:* TCC, humanista, sistémico, psicosocial comunitario, psicodinámico.
   * *Condiciones:* Ansiedad, depresión, estrés/burnout, trauma/TEPT, duelo, adicciones, insomnio.
3. **Bloque Contexto Regional (21 Países de América Latina y el Caribe):**
   * `"América Latina" OR "Latinoamérica" OR "Latin America" OR "América do Sul" OR "South America" OR "Central America" OR "Caribe" OR "Argentina" OR "Bolivia" OR "Brasil" OR "Brazil" OR "Chile" OR "Colombia" OR "Costa Rica" OR "Cuba" OR "Ecuador" OR "El Salvador" OR "Guatemala" OR "Haití" OR "Honduras" OR "México" OR "Mexico" OR "Nicaragua" OR "Panamá" OR "Paraguay" OR "Perú" OR "Puerto Rico" OR "República Dominicana" OR "Uruguay" OR "Venezuela"` y sus correspondientes gentilicios.
"""
    out_path = os.path.join(ASSETS_DIR, "search_strategy_table.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path


def build_table_1_characteristics() -> str:
    """Genera la Tabla 1 en formato Markdown directamente desde la base de datos SQLite."""
    charting = get_charting_data()

    rows = []
    for c in charting:
        # Formatear cita de autores (e.g. López-Sánchez et al. (2021))
        authors_raw = c.get("authors", "")
        year = c.get("year", "")
        first_author = authors_raw.split(";")[0].split(",")[0].strip()
        has_et_al = ";" in authors_raw or "," in authors_raw
        cite_label = f"**{first_author} et al. ({year})**" if has_et_al else f"**{first_author} ({year})**"
        
        country = c.get("country", "")
        design = c.get("study_design", "")
        sample = f"{c.get('sample_size', '')} {c.get('population_description', '')}".strip()
        mtci = f"{c.get('mtci_modality', '')}: {c.get('mtci_details', '')}".strip(" :")
        cond = c.get("psych_condition", "")
        appr = c.get("psych_approach", "")
        findings = f"{c.get('outcomes_measured', '')}. {c.get('effectiveness_findings', '')}".strip(". ") + "."
        
        rows.append(f"| {cite_label} | {country} | {design} | {sample} | {mtci} | {cond} | {appr} | {findings} |")

    content = f"""# Tabla 1: Características Generales, Metodológicas y Clínicas de los Estudios Incluidos (n = {len(charting)})

| Estudio (Autores, Año) | País | Diseño Metodológico | Muestra ($N$) y Población | Modalidad MTCI e Intervención | Condición de Salud Mental | Enfoque Psicoterapéutico | Instrumentos y Hallazgos Principales |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- | :--- |
""" + "\n".join(rows) + "\n"

    out_path = os.path.join(ASSETS_DIR, "table_1_characteristics.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path


def _categorize_study_design(raw: str) -> str:
    """Clasifica diseños empíricos heterogéneos en las 5 macro-categorías metodológicas del manuscrito."""
    d = (raw or "").lower().strip()
    if "no randomizado" in d:
        return "Cuasiexperimental y Cohortes"
    elif any(k in d for k in ["randomizado", "rct", "ensayo clínico", "ensayo clinico"]):
        return "Ensayos Clínicos (ECA/RCT)"
    elif any(k in d for k in ["cuasiexperimental", "cohorte", "longitudinal"]):
        return "Cuasiexperimental y Cohortes"
    elif any(k in d for k in ["mixto", "incrustado", "cualicuantitativo"]):
        return "Estudios de Métodos Mixtos"
    elif any(k in d for k in ["cualitativo", "etnogr", "fenomenol", "hermen", "participat"]):
        return "Diseños Cualitativos"
    elif any(k in d for k in ["transversal", "epidemiol", "encuesta", "observacional", "natural", "analítico", "analitico"]):
        return "Observacionales y Transversales"
    return "Otros Diseños"


def _categorize_mtci_modality(raw: str) -> str:
    """Clasifica modalidades y técnicas en los 6 clústeres operativos canónicos de MTCI."""
    m = (raw or "").lower().strip()
    if any(k in m for k in ["floral", "reiki", "bach", "bioenerg"]):
        return "Terapias Florales y Bioenergéticas"
    elif any(k in m for k in ["acupuntura", "auriculo"]):
        return "Acupuntura y Auriculoterapia"
    elif any(k in m for k in ["mindfulness", "mente-cuerpo", "medita"]):
        return "Mindfulness y Mente-Cuerpo"
    elif "fitoterapia" in m and "saberes" not in m:
        return "Fitoterapia Clínica"
    elif any(k in m for k in ["saberes", "indígena", "indigena", "ancestral", "ayahuasca", "curand"]):
        return "Saberes Ancestrales y Med. Trad."
    elif any(k in m for k in ["multimodal", "pics", "corporal", "artística", "artistica", "musicoterap"]):
        return "Prácticas Multimodales / PICS"
    return "Otras Prácticas MTCI"


def build_evidence_visualization_svg() -> str:
    """Genera un diagrama vectorial SVG de alta calidad con la distribución empírica de los estudios incluidos."""
    charting = get_charting_data()
    n_total = len(charting)
    
    if not charting:
        empty_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 240" width="100%" height="100%">
  <rect width="900" height="240" fill="#f8fafc" rx="8" stroke="#cbd5e0" stroke-width="1.2"/>
  <text x="450" y="110" font-family="'Arial', sans-serif" font-size="16" font-weight="bold" fill="#64748b" text-anchor="middle">Mapeo de Evidencia: Sin estudios incluidos para graficar (Base de datos reseteada a 0)</text>
  <text x="450" y="145" font-family="'Arial', sans-serif" font-size="13" fill="#94a3b8" text-anchor="middle">Ejecuta las búsquedas en las APIs y completa el cribado para generar los paneles de distribución.</text>
</svg>"""
        out_path = os.path.join(ASSETS_DIR, "evidence_distribution_chart.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(empty_svg)
        return out_path

    # Conteo por país
    country_counts = {}
    for c in charting:
        ct = c.get("country", "Otro")
        country_counts[ct] = country_counts.get(ct, 0) + 1

    # Conteo por modalidad MTCI canónica
    modality_counts = {}
    for c in charting:
        m = _categorize_mtci_modality(c.get("mtci_modality", ""))
        modality_counts[m] = modality_counts.get(m, 0) + 1

    # Conteo por diseño metodológico canónico
    design_counts = {}
    for c in charting:
        d = _categorize_study_design(c.get("study_design", ""))
        design_counts[d] = design_counts.get(d, 0) + 1

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 430" width="100%" height="100%">
  <style>
    .chart-title {{ font-family: 'Arial', sans-serif; font-size: 16px; font-weight: bold; fill: #0f172a; text-anchor: middle; }}
    .chart-subtitle {{ font-family: 'Arial', sans-serif; font-size: 12px; fill: #475569; text-anchor: middle; }}
    .panel-title {{ font-family: 'Arial', sans-serif; font-size: 13px; font-weight: bold; }}
    .bar-label {{ font-family: 'Arial', sans-serif; font-size: 11px; fill: #1e293b; font-weight: 500; }}
    .bar-value {{ font-family: 'Arial', sans-serif; font-size: 11px; font-weight: bold; }}
    .panel-box {{ fill: #ffffff; stroke: #cbd5e1; stroke-width: 1.0; rx: 4; }}
    .panel-footer {{ font-family: 'Arial', sans-serif; font-size: 10px; fill: #64748b; text-anchor: middle; }}
  </style>

  <!-- Background (Pure White for Direct Journal and Document Embedding) -->
  <rect width="900" height="430" fill="#ffffff"/>

  <!-- Title & Subtitle -->
  <text x="450" y="32" class="chart-title">Mapeo de Evidencia: Distribución de Estudios Incluidos (N = {n_total})</text>
  <text x="450" y="52" class="chart-subtitle">Revisión Exploratoria sobre Prácticas de MTCI en Psicología en América Latina</text>

  <!-- Panel 1: Distribución Geográfica (Países) -->
  <rect x="30" y="70" width="260" height="345" class="panel-box"/>
  <rect x="30" y="70" width="260" height="34" fill="#f8fafc" rx="4"/>
  <line x1="30" y1="104" x2="290" y2="104" stroke="#e2e8f0" stroke-width="1.0"/>
  <text x="45" y="92" class="panel-title" fill="#1e3a8a">1. Procedencia Geográfica</text>
"""
    # Render Panel 1 bars
    max_c = max(country_counts.values()) if country_counts else 1
    y = 125
    sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
    for country, qty in sorted_countries:
        pct = round((qty / n_total) * 100, 1)
        bar_w = max(4, int((qty / max_c) * 165))
        svg_content += f"""  <text x="45" y="{y}" class="bar-label">{country} ({qty})</text>
  <rect x="45" y="{y+5}" width="165" height="9" fill="#f1f5f9" rx="2"/>
  <rect x="45" y="{y+5}" width="{bar_w}" height="9" fill="#1e40af" rx="2"/>
  <text x="275" y="{y+13}" class="bar-value" fill="#1e3a8a" text-anchor="end">{pct}%</text>
"""
        y += 38

    svg_content += f"""  <line x1="45" y1="362" x2="275" y2="362" stroke="#e2e8f0" stroke-width="0.8"/>
  <text x="160" y="388" class="panel-footer">Total: {n_total} estudios · {len(sorted_countries)} países</text>

  <!-- Panel 2: Modalidades MTCI -->
  <rect x="320" y="70" width="260" height="345" class="panel-box"/>
  <rect x="320" y="70" width="260" height="34" fill="#f8fafc" rx="4"/>
  <line x1="320" y1="104" x2="580" y2="104" stroke="#e2e8f0" stroke-width="1.0"/>
  <text x="335" y="92" class="panel-title" fill="#065f46">2. Modalidades de MTCI</text>
"""
    max_m = max(modality_counts.values()) if modality_counts else 1
    y = 125
    sorted_modalities = sorted(modality_counts.items(), key=lambda x: x[1], reverse=True)
    for mod, qty in sorted_modalities:
        pct = round((qty / n_total) * 100, 1)
        bar_w = max(4, int((qty / max_m) * 165))
        svg_content += f"""  <text x="335" y="{y}" class="bar-label">{mod} ({qty})</text>
  <rect x="335" y="{y+5}" width="165" height="9" fill="#f1f5f9" rx="2"/>
  <rect x="335" y="{y+5}" width="{bar_w}" height="9" fill="#059669" rx="2"/>
  <text x="565" y="{y+13}" class="bar-value" fill="#065f46" text-anchor="end">{pct}%</text>
"""
        y += 38

    svg_content += f"""  <line x1="335" y1="362" x2="565" y2="362" stroke="#e2e8f0" stroke-width="0.8"/>
  <text x="450" y="388" class="panel-footer">Total: {n_total} estudios · {len(sorted_modalities)} clústeres</text>

  <!-- Panel 3: Diseños Metodológicos -->
  <rect x="610" y="70" width="260" height="345" class="panel-box"/>
  <rect x="610" y="70" width="260" height="34" fill="#f8fafc" rx="4"/>
  <line x1="610" y1="104" x2="870" y2="104" stroke="#e2e8f0" stroke-width="1.0"/>
  <text x="625" y="92" class="panel-title" fill="#9a3412">3. Diseños de Investigación</text>
"""
    max_d = max(design_counts.values()) if design_counts else 1
    y = 125
    sorted_designs = sorted(design_counts.items(), key=lambda x: x[1], reverse=True)
    for design, qty in sorted_designs:
        pct = round((qty / n_total) * 100, 1)
        bar_w = max(4, int((qty / max_d) * 165))
        svg_content += f"""  <text x="625" y="{y}" class="bar-label">{design} ({qty})</text>
  <rect x="625" y="{y+5}" width="165" height="9" fill="#f1f5f9" rx="2"/>
  <rect x="625" y="{y+5}" width="{bar_w}" height="9" fill="#d97706" rx="2"/>
  <text x="855" y="{y+13}" class="bar-value" fill="#9a3412" text-anchor="end">{pct}%</text>
"""
        y += 38

    svg_content += f"""  <line x1="625" y1="362" x2="855" y2="362" stroke="#e2e8f0" stroke-width="0.8"/>
  <text x="740" y="388" class="panel-footer">Total: {n_total} estudios · {len(sorted_designs)} metodologías</text>

</svg>"""
    
    out_path = os.path.join(ASSETS_DIR, "evidence_distribution_chart.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return out_path


def build_prisma_filled_checklist() -> str:
    """Genera la Lista de Comprobación PRISMA-ScR de 22 Ítems Completada (Material Suplementario S1)."""
    checklist = get_checklist()

    rows = []
    for item in checklist:
        num = item["item_num"]
        section = item.get("section", "")
        topic = item.get("topic", "")
        desc = item.get("description", "")
        status = item.get("status", "Pendiente")
        page_sec = item.get("section_or_page", "Por asignar")
        notes = item.get("author_notes", "")

        status_emoji = "✅ Cumplido" if status == "Cumplido" else ("⏳ En progreso" if status == "En progreso" else "❌ Pendiente")
        rows.append(f"| **{num}** | {section} | **{topic}** | {desc} | {page_sec} | {status_emoji} | {notes} |")

    content = f"""# PRISMA-ScR Checklist de 22 Ítems Completada (Material Suplementario S1)

**Referencia Oficial:** Tricco, A. C., Lillie, E., Zarin, W., O'Brien, K. K., Colquhoun, H., Levac, D., ... & Straus, S. E. (2018). PRISMA extension for scoping reviews (PRISMA-ScR): checklist and explanation. *Annals of Internal Medicine*, 169(7), 467-473. https://doi.org/10.7326/M18-0850

| Ítem | Sección | Tema | Criterio de Notificación PRISMA-ScR | Ubicación en el Manuscrito | Estado | Notas del Revisor |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
""" + "\n".join(rows) + "\n"

    out_path = os.path.join(ASSETS_DIR, "prisma_scr_filled_checklist.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path


def build_osf_preregistration_protocol() -> str:
    """Genera el Protocolo de Prerregistro Congelado para Open Science Framework (OSF)."""
    pcc = DEFAULT_PROTOCOL
    now_str = datetime.now().strftime("%Y-%m-%d")
    
    content = f"""# Protocolo de Investigación para Prerregistro en Open Science Framework (OSF)
## Scoping Review Protocol: Traditional, Complementary, and Integrative Medicine in Psychology in Latin America

* **Título del Protocolo:** Revisión exploratoria de la literatura sobre prácticas de la medicina tradicional, complementaria e integrativa en psicología en América Latina (2016–2026).
* **Autores:** Engel Enoc Velásquez Zamora, Luis David Torres-Esquivel.
* **Institución:** Universidad Nacional Autónoma de Nicaragua, Managua (UNAN-Managua), CUR-Estelí.
* **Fecha de Congelamiento del Protocolo:** {now_str}
* **Marco Metodológico:** Directrices del *Joanna Briggs Institute* (JBI; Peters et al., 2020) y declaración PRISMA-ScR (Tricco et al., 2018).
* **Depósito / Plataforma Prevista:** Open Science Framework (OSF Registries; https://osf.io). *Nota: PROSPERO no acepta revisiones exploratorias.*

---

### 1. Pregunta de Investigación y Marco Conceptual PCC
* **Pregunta Rectora Principal:**  
  *¿Cuál es el alcance, las características metodológicas y la evidencia científica disponible en América Latina en la última década sobre la integración y los resultados de las prácticas de Medicina Tradicional, Complementaria e Integrativa (MTCI) en los procesos psicoterapéuticos y de salud mental?*

* **Población (P):** {pcc['pcc']['population']}
* **Concepto (C):** {pcc['pcc']['concept']}
* **Contexto (C):** {pcc['pcc']['context']}

---

### 2. Criterios de Elegibilidad a Priori
* **Criterios de Inclusión:**
  1. Estudios empíricos en seres humanos con evaluación de desenlaces en salud mental o procesos psicoterapéuticos.
  2. Incorporación explícita de modalidades MTCI articuladas a intervenciones psicológicas.
  3. Ejecutados en países de América Latina y el Caribe durante el periodo 2016–2026.
  4. Diseños metodológicos primarios (cuantitativos, cualitativos o mixtos) en revistas arbitradas por pares.
  5. Textos completos disponibles en español, portugués o inglés.

* **Criterios de Exclusión:**
  1. Ensayos fitoquímicos o farmacológicos exclusivamente *in vitro* o en modelos animales sin mediación psicológica.
  2. Estudios dirigidos estrictamente a patologías somáticas sin variables de salud mental.
  3. Estudios fuera de América Latina o sin análisis contextual regional.
  4. Editoriales, cartas, reseñas de divulgación o actas de congresos sin informe completo.

---

### 3. Fuentes de Información y Estrategia de Búsqueda
Búsquedas sistemáticas en PubMed/MEDLINE, Europe PMC, OpenAlex, SciELO, BVS/LILACS, PePSIC/Redalyc y Crossref API (Polite Pool).
Estrategia secuencial en dos fases trilingüe (español, inglés, portugués) con delimitación temporal estricta 2016–2026 y filtro explícito de los 21 países de América Latina y el Caribe:
* **Fase 1 (MeSH/DeCS Paraguas):** Vocabulario controlado institucional de MTCI y PICS cruzado con el bloque troncal de disciplinas y conceptos de salud mental/psicología.
* **Fase 2 (Prácticas Específicas Desagregadas):** Seis clústeres operativos (Fitoterapia, Acupuntura, Terapias mente-cuerpo/mindfulness, Saberes ancestrales/indígenas/ayahuasca, Terapias florales/reiki, Arteterapia integrativa) cruzados finamente con enfoques psicoterapéuticos (TCC, humanista, sistémico, psicosocial comunitario, psicodinámico) y condiciones de salud mental (ansiedad, depresión, estrés, trauma/TEPT, duelo, adicciones).

---

### 4. Proceso de Selección y Extracción de Datos
Tamizaje independiente en dos etapas:
1. Cribado por título y resumen con deduplicación algorítmica (DOI exacto y *RapidFuzz Token Sort Ratio* al 90%).
2. Elegibilidad a texto completo con registro obligatorio de motivos de exclusión unívocos.
Formulario de extracción pre-especificado (Data Charting) en 15 variables metodológicas y clínicas.
"""
    out_path = os.path.join(REPO_ROOT, "docs", "osf_preregistration_protocol.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path


def build_all_assets() -> Dict[str, Any]:
    """Construye y sincroniza todos los insumos empíricos del manuscrito."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    os.makedirs(STATE_DIR, exist_ok=True)

    flow_numbers = get_prisma_flow_numbers()

    # 1. Tablas en docs/assets/
    pcc_path = build_pcc_table()
    elig_path = build_eligibility_matrix()
    search_path = build_search_strategy_table()
    table1_path = build_table_1_characteristics()

    # 2. Checklists y OSF
    checklist_path = build_prisma_filled_checklist()
    osf_path = build_osf_preregistration_protocol()

    # 3. Diagramas vectoriales
    chart_svg_path = build_evidence_visualization_svg()
    prisma_svg_path = os.path.join(REPO_ROOT, "assets", "prisma_flow_diagram.svg")
    try:
        svg_content = generate_prisma_svg(flow_numbers)
        with open(prisma_svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
    except Exception as e:
        print(f"Error generando prisma_flow_diagram.svg: {e}")

    # 4. Generar Material Suplementario Unificado (.docx)
    try:
        docx_path = export_supplementary_materials_docx()
    except Exception as e:
        print(f"Error generando Material_Suplementario_Completo.docx: {e}")
        docx_path = OUT_DOCX_PATH

    # 5. Exportar Snapshot SQLite y CSV
    export_res = export_project_snapshot()

    # 6. Generar state/manuscript_assets.json
    assets_manifest = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prisma_flow": flow_numbers,
        "assets": {
            "table_pcc": {
                "path": os.path.relpath(pcc_path, REPO_ROOT),
                "hash": compute_file_hash(pcc_path),
                "type": "markdown_table"
            },
            "table_eligibility": {
                "path": os.path.relpath(elig_path, REPO_ROOT),
                "hash": compute_file_hash(elig_path),
                "type": "markdown_table"
            },
            "table_search_strategy": {
                "path": os.path.relpath(search_path, REPO_ROOT),
                "hash": compute_file_hash(search_path),
                "type": "markdown_table"
            },
            "table_1_characteristics": {
                "path": os.path.relpath(table1_path, REPO_ROOT),
                "csv_path": os.path.relpath(CSV_TABLE1_PATH, REPO_ROOT),
                "hash": compute_file_hash(table1_path),
                "studies_count": flow_numbers["studies_included"],
                "type": "empirical_table"
            },
            "prisma_flow_diagram": {
                "path": os.path.relpath(prisma_svg_path, REPO_ROOT),
                "hash": compute_file_hash(prisma_svg_path),
                "type": "vector_svg_figure"
            },
            "evidence_distribution_chart": {
                "path": os.path.relpath(chart_svg_path, REPO_ROOT),
                "hash": compute_file_hash(chart_svg_path),
                "type": "vector_svg_figure"
            },
            "prisma_scr_filled_checklist": {
                "path": os.path.relpath(checklist_path, REPO_ROOT),
                "hash": compute_file_hash(checklist_path),
                "items_count": 22,
                "type": "reporting_checklist"
            },
            "osf_preregistration_protocol": {
                "path": os.path.relpath(osf_path, REPO_ROOT),
                "hash": compute_file_hash(osf_path),
                "type": "preregistration_package"
            },
            "supplementary_materials_docx": {
                "path": os.path.relpath(docx_path, REPO_ROOT),
                "hash": compute_file_hash(docx_path),
                "type": "supplementary_docx_package"
            },
            "project_snapshot": {
                "path": os.path.relpath(SNAPSHOT_PATH, REPO_ROOT),
                "hash": compute_file_hash(SNAPSHOT_PATH),
                "type": "json_snapshot"
            }
        }
    }

    with open(MANUSCRIPT_ASSETS_JSON, "w", encoding="utf-8") as f:
        json.dump(assets_manifest, f, ensure_ascii=False, indent=2)

    return assets_manifest


def main():
    print("=" * 70)
    print("🚀 PRISMA-ScR MANUSCRIPT ASSET BUILDER & PIPELINE SYNCHRONIZER")
    print("=" * 70)
    
    manifest = build_all_assets()
    
    print(f"Generated at: {manifest['generated_at']}")
    print(f"PRISMA Flow State: {manifest['prisma_flow']['studies_included']} included studies from {manifest['prisma_flow']['total_identified']} identified.\n")

    print("Assets produced and synchronized in docs/assets/ & assets/:")
    for name, info in manifest["assets"].items():
        print(f"  📦 {name.ljust(30)} -> {info['path']} (hash: {info['hash']})")

    print(f"\nManifest registry saved to: state/manuscript_assets.json")
    print("=" * 70)


if __name__ == "__main__":
    main()
