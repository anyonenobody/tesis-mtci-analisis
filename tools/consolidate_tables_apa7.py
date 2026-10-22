#!/usr/bin/env python3
"""
tools/consolidate_tables_apa7.py
================================
Consolidates and standardizes all thesis tables according to strict APA 7th Edition:
- Number above in bold: **Tabla X**
- Title above in italics: *Título descriptivo* (Sentence case)
- Borders: Top line, bottom of header row line, bottom of table line. ZERO vertical lines.
- Note below: *Nota.* ... (10pt regular, 'Nota.' in italics)
- Natural in-text citations: '(véase la Tabla X)' preceding each table.
- Synchronized List of Tables in preliminaries.
- Synchronized Markdown chapters.
"""

import os
import sys
import re
import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX_PATH = os.path.join(REPO_ROOT, "assets", "MTCI_Consolidado_Final_APA7.docx")
CAPITULOS_DIR = os.path.join(REPO_ROOT, "docs", "capitulos")

TABLES_META = {
    1: {
        "title": "Prácticas y terapias de la MTCI según su ámbito de aplicación",
        "note": "Clasificación adaptada de los lineamientos estratégicos de la Organización Mundial de la Salud (OMS, 2023) y la Ley No. 774 de Nicaragua.",
        "cit_anchor": "Como parte de las dimensiones se desglosan también prácticas y terapias que se clasifican según su naturaleza y ámbito de aplicación",
        "cit_text": " (véase la Tabla 1)."
    },
    2: {
        "title": "Tipología y características del diseño metodológico de la investigación",
        "note": "Tipología metodológica delimitada conforme a los criterios de investigación mixta concurrente descritos por Hernández-Sampieri y Mendoza (2023).",
        "cit_anchor": "La investigación adopta un enfoque mixto, entendido como un proceso sistemático",
        "cit_text": " Para abordar las interrogantes de investigación desde múltiples dimensiones, se articuló una tipología metodológica integradora (véase la Tabla 2)."
    },
    3: {
        "title": "Componentes del enfoque mixto concurrente y su articulación metodológica",
        "note": "Desglose operativo de las fases cuantitativa y cualitativa según unidades de análisis, objetivos e instrumentos implementados.",
        "cit_anchor": "La investigación adopta un enfoque mixto, entendido como un proceso sistemático, empírico y crítico",
        "cit_text": " La articulación entre objetivos específicos, participantes e instrumentos de recolección se estructuró de forma concurrente e independiente (véase la Tabla 3)."
    },
    4: {
        "title": "Supuestos del paradigma pragmático y su aplicación en la investigación",
        "note": "Fundamentación ontológica, epistemológica, metodológica y axiológica aplicada a la integración metodológica de saberes.",
        "cit_anchor": "Con los actores locales y docentes, se buscó lo contrario: entender desde su propio lenguaje y experiencia vivida",
        "cit_text": " Esta postura pragmática orientó las decisiones de diseño y análisis de datos en cada fase del estudio (véase la Tabla 4)."
    },
    5: {
        "title": "Caracterización de las unidades de análisis y recolección de información",
        "note": "Delimitación de los tres colectivos participantes conforme al principio de pertinencia informante y complementariedad metodológica.",
        "cit_anchor": "El estudio trabaja con tres unidades de análisis, no una sola, porque cada objetivo específico necesita informantes con una experiencia particular",
        "cit_text": " Dicha delimitación garantiza una perspectiva triangulada entre estudiantes, facilitadores y profesorado (véase la Tabla 5)."
    },
    6: {
        "title": "Composición y tamaño de la muestra participante por unidad de análisis",
        "note": "N = 86 participantes en total (n = 68 estudiantes de Psicología de 4.º y 5.º año, n = 9 facilitadores locales de MTCI y n = 9 docentes del CUR-Estelí).",
        "cit_anchor": "La muestra quedó constituida de la siguiente manera:",
        "cit_text": " La distribución final de participantes por cada unidad de análisis se presenta a continuación (véase la Tabla 6)."
    },
    7: {
        "title": "Matriz de operacionalización de categorías y variables de la investigación",
        "note": "Matriz de consistencia metodológica para la articulación entre preguntas de investigación, objetivos específicos, categorías analíticas e instrumentos.",
        "cit_anchor": "Operacionalización de variables",
        "cit_text": " A continuación se detalla la matriz de consistencia metodológica que guio la recolección y análisis de la información empírica (véase la Tabla 7)."
    },
    8: {
        "title": "Técnicas e instrumentos de recolección de datos primarios aplicados en campo",
        "note": "Instrumentos psicométricos y cualitativos I1, I2 e I3 validados mediante juicio de expertos previo a su aplicación definitiva.",
        "cit_anchor": "Sin embargo, dado que la presente investigación es de tipo descriptivo con alcance exploratorio, no busca comprobar hipótesis estadísticas",
        "cit_text": " En este marco, se diseñaron y administraron tres instrumentos específicos adaptados a cada colectivo participante (véase la Tabla 8)."
    },
    9: {
        "title": "Estructura modular y contenidos temáticos de la propuesta de manual de estrategias de MTCI",
        "note": "Síntesis programática de las orientaciones pedagógicas, éticas y vivenciales diseñadas para docentes y estudiantes de la carrera de Psicología.",
        "cit_anchor": "El manual es el producto del tercer objetivo específico de la investigación: proponer estrategias complementarias",
        "cit_text": " La propuesta pedagógica se organiza en ocho módulos temáticos estructurados secuencialmente (véase la Tabla 9)."
    }
}

def apply_apa7_table_borders(tbl):
    """Applies strict APA 7 borders: top line, header bottom line, table bottom line, zero vertical lines."""
    tblPr = tbl._tbl.tblPr
    for b in tblPr.xpath('w:tblBorders'):
        tblPr.remove(b)
    
    apa7_borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="auto"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="auto"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(apa7_borders)

    # Add bottom border to row 0 (header row)
    if tbl.rows:
        for cell in tbl.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            for b in tcPr.xpath('w:tcBorders'):
                tcPr.remove(b)
            header_bottom = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>\n'
                f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="auto"/>\n'
                f'</w:tcBorders>'
            )
            tcPr.append(header_bottom)

def format_table_cells_typography(tbl):
    """Sets standard 10-11pt Times New Roman, bold headers, and removes internal linebreaks."""
    for r_idx, row in enumerate(tbl.rows):
        is_header = (r_idx == 0)
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(10.5) if not is_header else Pt(11)
                    if is_header:
                        run.bold = True

def consolidate_tables_docx():
    print(f"📖 Cargando documento: {DOCX_PATH}")
    doc = docx.Document(DOCX_PATH)
    print(f"   Tablas encontradas: {len(doc.tables)}, Párrafos: {len(doc.paragraphs)}")

    # 1. Inject in-text citations '(véase la Tabla X)' into preceding narrative paragraphs
    print("\n✍️ Insertando citas en el texto '(véase la Tabla X)' según APA 7...")
    for num, meta in TABLES_META.items():
        anchor = meta["cit_anchor"]
        cit_text = meta["cit_text"]
        matches = [p for p in doc.paragraphs if anchor.lower() in p.text.lower()]
        if matches:
            target_p = matches[0]
            if f"Tabla {num}" not in target_p.text:
                target_p.add_run(cit_text)
                print(f"   ✓ Cita inyectada para Tabla {num} en párrafo con '{anchor[:35]}...'")

    # 2. Format each table from 1 to 9 (reverse order to keep stability)
    print("\n📊 Estandarizando Tablas 1 a 9 con formato APA 7 estricto...")
    for t_id in range(9, 0, -1):
        tbl = doc.tables[t_id]
        meta = TABLES_META[t_id]

        # A. Apply APA 7 borders and typography
        apply_apa7_table_borders(tbl)
        format_table_cells_typography(tbl)

        # B. Clean up old caption paragraph if present immediately before tbl
        prev = tbl._tbl.getprevious()
        while prev is not None and prev.tag.endswith('p'):
            prev_txt = "".join(prev.xpath('.//w:t/text()')).strip()
            if prev_txt.lower().startswith(f"tabla {t_id}") or prev_txt.lower().startswith(f"tabla {t_id}."):
                prev.getparent().remove(prev)
                break
            elif not prev_txt:
                prev.getparent().remove(prev)
                prev = tbl._tbl.getprevious()
            else:
                break

        # C. Insert APA 7 Title paragraphs before tbl
        # Number paragraph
        p_num_elm = parse_xml(f'<w:p {nsdecls("w")}/>')
        tbl._tbl.addprevious(p_num_elm)
        p_num = docx.text.paragraph.Paragraph(p_num_elm, doc)
        p_num.paragraph_format.line_spacing = 1.5
        p_num.paragraph_format.space_before = Pt(14)
        p_num.paragraph_format.space_after = Pt(0)
        r_num = p_num.add_run(f"Tabla {t_id}")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(12)
        r_num.bold = True

        # Title paragraph
        p_title_elm = parse_xml(f'<w:p {nsdecls("w")}/>')
        p_num_elm.addnext(p_title_elm)
        p_title = docx.text.paragraph.Paragraph(p_title_elm, doc)
        p_title.paragraph_format.line_spacing = 1.5
        p_title.paragraph_format.space_before = Pt(0)
        p_title.paragraph_format.space_after = Pt(6)
        r_title = p_title.add_run(meta["title"])
        r_title.font.name = "Times New Roman"
        r_title.font.size = Pt(12)
        r_title.italic = True

        # D. Insert APA 7 Note paragraph immediately after tbl
        p_note_elm = parse_xml(f'<w:p {nsdecls("w")}/>')
        tbl._tbl.addnext(p_note_elm)
        p_note = docx.text.paragraph.Paragraph(p_note_elm, doc)
        p_note.paragraph_format.line_spacing = 1.15
        p_note.paragraph_format.space_before = Pt(4)
        p_note.paragraph_format.space_after = Pt(18)
        r_lbl = p_note.add_run("Nota. ")
        r_lbl.font.name = "Times New Roman"
        r_lbl.font.size = Pt(10)
        r_lbl.italic = True
        r_txt = p_note.add_run(meta["note"])
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(10)

        print(f"   ✓ Tabla {t_id} formateada con éxito (Bordes APA 7, Título doble y Nota)")

    # 3. Clean up borders of Appendix Tables (Tables 10 to 31)
    print("\n📑 Limpiando líneas verticales en matrices de anexos (Tablas 10 a 31)...")
    for t_id in range(10, len(doc.tables)):
        tbl = doc.tables[t_id]
        # Keep clean borders without heavy vertical lines
        apply_apa7_table_borders(tbl)
        format_table_cells_typography(tbl)
    print("   ✓ Matrices de anexos estilizadas con bordes limpios")

    # 4. Update preliminary List of Tables (Índice de tablas)
    print("\n📋 Actualizando Índice de tablas en páginas preliminares...")
    idx_p_list = [p for p in doc.paragraphs if p.text.strip().lower() == "índice de tablas".lower()]
    if idx_p_list:
        pt_idx = idx_p_list[0]
        # Find next section heading (Índice de figuras)
        p_idx = [i for i, p in enumerate(doc.paragraphs) if p._p == pt_idx._p][0]
        next_h = None
        for cand in doc.paragraphs[p_idx + 1:p_idx + 25]:
            if "índice de figuras" in cand.text.strip().lower():
                next_h = cand
                break
        
        anchor_insert = next_h if next_h is not None else doc.paragraphs[p_idx + 1]

        # Remove any old entries between pt_idx and next_h
        for cand in list(doc.paragraphs[p_idx + 1:p_idx + 25]):
            if cand._p == anchor_insert._p:
                break
            txt = cand.text.strip()
            if txt.startswith("Tabla ") or txt.startswith("- Tabla ") or not txt:
                cand._element.getparent().remove(cand._element)

        # Insert 9 clean entries
        for num in range(1, 10):
            meta = TABLES_META[num]
            p_item = anchor_insert.insert_paragraph_before()
            p_item.paragraph_format.line_spacing = 1.5
            p_item.paragraph_format.space_before = Pt(0)
            p_item.paragraph_format.space_after = Pt(2)
            r_num = p_item.add_run(f"Tabla {num}. ")
            r_num.font.name = "Times New Roman"
            r_num.font.size = Pt(12)
            r_num.bold = True
            r_title = p_item.add_run(meta["title"])
            r_title.font.name = "Times New Roman"
            r_title.font.size = Pt(12)

        print("   ✓ 9 entradas añadidas al Índice de tablas con tipografía APA 7")

    # 5. Save document
    print(f"\n💾 Guardando documento actualizado en: {DOCX_PATH}...")
    doc.save(DOCX_PATH)
    print(f"✅ ¡Consolidación de tablas exitosa! Tamaño: {os.path.getsize(DOCX_PATH):,} bytes")

def update_markdown_tables():
    print("\n📝 Sincronizando Tablas en archivos Markdown...")
    # 1. Preliminares
    p_path = os.path.join(CAPITULOS_DIR, "00_preliminares.md")
    with open(p_path, "r", encoding="utf-8") as f:
        text = f.read()

    lines = ["## Índice de tablas\n"]
    for num in range(1, 10):
        lines.append(f"- Tabla {num}. {TABLES_META[num]['title']}")
    new_tbl_index = "\n\n".join(lines)

    text = re.sub(r'## Índice de tablas.*?(?=## Índice de figuras)', new_tbl_index + "\n\n", text, flags=re.DOTALL)
    with open(p_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("   ✓ 00_preliminares.md actualizado con Índice de Tablas")

    # 2. Marco Teórico
    m_path = os.path.join(CAPITULOS_DIR, "02_marco_teorico.md")
    if os.path.exists(m_path):
        with open(m_path, "r", encoding="utf-8") as f:
            t = f.read()
        if "Tabla 1" in t and TABLES_META[1]["title"] not in t:
            t = re.sub(r'\*?Tabla 1[^\n]*\*?', f"\n\n**Tabla 1**  \n*{TABLES_META[1]['title']}*\n\n", t)
        if "(véase la Tabla 1)" not in t:
            tgt = TABLES_META[1]["cit_anchor"]
            if tgt in t:
                t = t.replace(tgt, tgt + TABLES_META[1]["cit_text"])
        with open(m_path, "w", encoding="utf-8") as f:
            f.write(t)
        print("   ✓ 02_marco_teorico.md sincronizado con Tabla 1")

    # 3. Metodología
    met_path = os.path.join(CAPITULOS_DIR, "03_diseno_metodologico.md")
    if os.path.exists(met_path):
        with open(met_path, "r", encoding="utf-8") as f:
            t = f.read()
        for num in range(2, 9):
            meta = TABLES_META[num]
            if f"(véase la Tabla {num})" not in t:
                tgt = meta["cit_anchor"]
                if tgt in t:
                    t = t.replace(tgt, tgt + meta["cit_text"])
        with open(met_path, "w", encoding="utf-8") as f:
            f.write(t)
        print("   ✓ 03_diseno_metodologico.md sincronizado con Tablas 2 a 8")

    # 4. Manual
    man_path = os.path.join(CAPITULOS_DIR, "05_propuesta_manual.md")
    if os.path.exists(man_path):
        with open(man_path, "r", encoding="utf-8") as f:
            t = f.read()
        if "(véase la Tabla 9)" not in t:
            tgt = TABLES_META[9]["cit_anchor"]
            if tgt in t:
                t = t.replace(tgt, tgt + TABLES_META[9]["cit_text"])
        if "**Tabla 9**" not in t:
            t = t.replace("12.2. Estructura y puntos clave", f"12.2. Estructura y puntos clave\n\n**Tabla 9**  \n*{TABLES_META[9]['title']}*\n")
        with open(man_path, "w", encoding="utf-8") as f:
            f.write(t)
        print("   ✓ 05_propuesta_manual.md sincronizado con Tabla 9")

def main():
    consolidate_tables_docx()
    update_markdown_tables()
    print("\n🎉 ¡Estandarización y consolidación de tablas completada con éxito!")

if __name__ == "__main__":
    main()
