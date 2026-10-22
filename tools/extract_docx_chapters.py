#!/usr/bin/env python3
"""
tools/extract_docx_chapters.py
==============================
Extracts and deconstructs 'assets/MTCI Octubre 15 ultimo.docx' into granular,
high-fidelity Markdown chapter files under 'docs/capitulos/'.

Preserves headings hierarchy (14pt bold -> #, 12pt bold -> ##, subsections -> ###),
formatting runs (bold, italic), markdown tables, lists, and Structured Document Tags (SDT).
"""

import os
import sys
import re
import docx
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.ns import qn

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

DOCX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "MTCI_Consolidado_Final_APA7.docx"))
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "capitulos"))

def format_paragraph(p: Paragraph) -> str:
    text = p.text.strip()
    if not text:
        return ""

    style_name = p.style.name if p.style else "Normal"

    # Identify bold runs and font size
    non_empty_runs = [r for r in p.runs if r.text.strip()]
    all_bold = bool(non_empty_runs and all(r.bold for r in non_empty_runs))
    max_size = max((r.font.size.pt for r in non_empty_runs if r.font and r.font.size), default=12.0)

    # Check list items
    is_list = False
    pPr = p._element.pPr
    if pPr is not None and pPr.find(qn("w:numPr")) is not None:
        is_list = True
    elif "list" in style_name.lower():
        is_list = True

    # Check if this paragraph is a Heading by typography (14pt bold or 12pt bold)
    if all_bold and len(text) < 120 and not is_list:
        if max_size >= 13.5:
            return f"\n# {text}\n"
        elif max_size >= 11.5:
            if re.match(r'^\d+\.\d+\.\d+', text):
                return f"\n### {text}\n"
            elif re.match(r'^\d+\.\d+', text):
                return f"\n## {text}\n"
            return f"\n## {text}\n"
        else:
            return f"\n### {text}\n"

    # Run-level formatting (bold, italic)
    runs_formatted = []
    for r in p.runs:
        r_text = r.text
        if not r_text:
            continue
        if r.bold and r.italic:
            runs_formatted.append(f"***{r_text}***")
        elif r.bold:
            runs_formatted.append(f"**{r_text}**")
        elif r.italic:
            runs_formatted.append(f"*{r_text}*")
        else:
            runs_formatted.append(r_text)

    body = "".join(runs_formatted).strip()
    if not body:
        body = text

    if is_list:
        return f"- {body}"
    elif style_name == "Caption" or (len(body) < 80 and (body.startswith("Tabla") or body.startswith("Figura") or "Figura." in body or "Tabla." in body)):
        return f"\n*{body}*\n"
    elif style_name == "Bibliography":
        return f"- {body}"
    else:
        return body

def format_table(tbl: Table, tbl_idx: int) -> str:
    matrix = []
    for row in tbl.rows:
        row_cells = []
        for cell in row.cells:
            # Preserve cell linebreaks as <br>
            cell_txt = " <br> ".join(p.text.strip() for p in cell.paragraphs if p.text.strip())
            cell_txt = cell_txt.replace("|", "\\|")
            row_cells.append(cell_txt)
        matrix.append(row_cells)

    if not matrix:
        return ""

    lines = [f"\n<!-- [Tabla T{tbl_idx}: {len(matrix)} filas x {len(matrix[0])} columnas] -->"]
    header = matrix[0]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in matrix[1:]:
        clean_row = list(row)
        while len(clean_row) < len(header):
            clean_row.append("")
        lines.append("| " + " | ".join(clean_row[:len(header)]) + " |")
    lines.append("")
    return "\n".join(lines)

def detect_chapter_transition(p: Paragraph) -> str | None:
    txt = p.text.strip()
    if not txt or len(txt) > 120:
        return None
    non_empty = [r for r in p.runs if r.text.strip()]
    if not non_empty:
        return None
    all_bold = all(r.bold for r in non_empty)
    max_size = max((r.font.size.pt for r in non_empty if r.font and r.font.size), default=12.0)
    
    t = txt.upper()
    if all_bold and max_size >= 13.5:
        if t in ('INTRODUCCIÓN', 'INTRODUCCION'):
            return '01_introduccion'
        elif t in ('MARCO TEÓRICO', 'MARCO TEORICO'):
            return '02_marco_teorico'
        elif t in ('DISEÑO METODOLÓGICO', 'DISENO METODOLOGICO'):
            return '03_diseno_metodologico'
        elif t in ('ANÁLISIS Y DISCUSIÓN DE RESULTADOS', 'ANALISIS Y DISCUSION DE RESULTADOS'):
            return '04_analisis_y_discusion_resultados'
        elif t == 'CONCLUSIONES':
            return '06_conclusiones_y_recomendaciones'
        elif t == 'REFERENCIAS':
            return '07_referencias_bibliograficas'
        elif t == 'ANEXOS':
            return '08_anexos'
    if all_bold and 'PROPUESTA DE MANUAL' in t:
        return '05_propuesta_manual'
    return None

def extract_all():
    if not os.path.exists(DOCX_PATH):
        raise FileNotFoundError(f"No se encuentra el archivo docx en: {DOCX_PATH}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = docx.Document(DOCX_PATH)

    chapters_info = [
        ('00_preliminares', "Páginas Preliminares (Portada, Dedicatorias, Agradecimientos, Aval, Resumen, Abstract, Índices)"),
        ('01_introduccion', "Capítulo I: Introducción, Antecedentes, Problema y Objetivos"),
        ('02_marco_teorico', "Capítulo II: Marco Teórico y Conceptual"),
        ('03_diseno_metodologico', "Capítulo III: Diseño Metodológico y Matriz de Operacionalización"),
        ('04_analisis_y_discusion_resultados', "Capítulo IV: Análisis y Discusión de Resultados (Estudiantes, Actores y Docentes)"),
        ('05_propuesta_manual', "Capítulo V: Propuesta de Manual con Estrategias de MTCI"),
        ('06_conclusiones_y_recomendaciones', "Capítulo VI: Conclusiones y Recomendaciones"),
        ('07_referencias_bibliograficas', "Capítulo VII: Referencias Bibliográficas (Normativa APA 7)"),
        ('08_anexos', "Capítulo VIII: Anexos y Dossier de Validación de Instrumentos")
    ]

    chapters = {key: {"title": title, "content": []} for key, title in chapters_info}

    current_chapter = '00_preliminares'
    tbl_counter = 0

    def process_paragraph_element(p_elem):
        nonlocal current_chapter
        p = Paragraph(p_elem, doc)
        new_ch = detect_chapter_transition(p)
        if new_ch:
            current_chapter = new_ch

        formatted = format_paragraph(p)
        if formatted:
            chapters[current_chapter]["content"].append(formatted)

    def process_table_element(tbl_elem):
        nonlocal tbl_counter, current_chapter
        tbl = Table(tbl_elem, doc)
        tbl_md = format_table(tbl, tbl_counter)
        tbl_counter += 1
        if tbl_md:
            chapters[current_chapter]["content"].append(tbl_md)

    def process_sdt_element(sdt_elem):
        # SDT tags in this docx are the indices (TOC, tables, figures) in 00_preliminares
        sdt_content = sdt_elem.find(qn("w:sdtContent"))
        if sdt_content is not None:
            for child in sdt_content:
                tag = child.tag.split("}")[-1]
                if tag == "p":
                    p = Paragraph(child, doc)
                    txt = p.text.strip()
                    if txt:
                        chapters["00_preliminares"]["content"].append(f"- {txt}")

    # Walk doc.element.body sequentially
    for child in doc.element.body:
        tag = child.tag.split("}")[-1]
        if tag == "p":
            process_paragraph_element(child)
        elif tag == "tbl":
            process_table_element(child)
        elif tag == "sdt":
            process_sdt_element(child)

    # Write each chapter to its corresponding markdown file
    index_manifest = [
        "# Estructura del Manuscrito en Markdown — Tesis MTCI\n",
        "Este directorio contiene la descomposición por capítulos de la versión final del documento:",
        f"**Documento Fuente:** `assets/{os.path.basename(DOCX_PATH)}`\n",
        "| Archivo | Capítulo / Sección | Bloques de Contenido | Tamaño (KB) |",
        "| :--- | :--- | :--- | :--- |"
    ]

    for key, title in chapters_info:
        fname = f"{key}.md"
        fpath = os.path.join(OUTPUT_DIR, fname)
        data = chapters[key]
        text_content = "\n\n".join(data["content"])

        if not text_content.startswith("#"):
            text_content = f"# {data['title']}\n\n" + text_content

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(text_content)

        blocks_count = len(data["content"])
        size_kb = os.path.getsize(fpath) / 1024
        index_manifest.append(f"| [{fname}](./{fname}) | {title} | {blocks_count} bloques | {size_kb:.1f} KB |")
        print(f"Generado: {fname} ({blocks_count} bloques de contenido, {size_kb:.1f} KB)")

    # Write README.md manifest
    readme_path = os.path.join(OUTPUT_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index_manifest) + "\n")
    print(f"Manifiesto generado en: {readme_path}")

if __name__ == "__main__":
    extract_all()
