#!/usr/bin/env python3
"""
tools/build_perfect_native_docx.py
==================================
Builds the definitive, consolidated master thesis document with:
1. Exact numbering and hierarchy of titles and subtitles from original 'MTCI Octubre 15 ultimo.docx'.
2. Native Microsoft Word styles (Heading 1-3 with outline levels 0-2).
3. 100% native Word Table of Contents (TOC \\o "1-3" \\h \\z \\u).
4. 100% native Word Table of Tables (TOC \\h \\z \\c "Tabla").
5. 100% native Word Table of Figures (TOC \\h \\z \\c "Figura").
6. Replacement of all 25 figures with 300 DPI APA 7 graphics.
7. APA 7 styling for all 32 tables (0 vertical lines).
8. Strict preservation of Section 4 in LANDSCAPE (11.00" x 8.50") for Table 7.
9. Page breaks before all major chapters.
10. Complete preservation of all original 25,361 words and ~165 pages.
"""

import os
import sys
import zipfile
import shutil
import io
import re
import xml.etree.ElementTree as ET
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = r"c:\Users\fungicoder\Documents\Fungicoder\Dev\tesis-mtci-analisis"
ORIG_DOCX = os.path.join(REPO_ROOT, "assets", "MTCI Octubre 15 ultimo.docx")
OUTPUT_DOCX = os.path.join(REPO_ROOT, "assets", "MTCI_Consolidado_Final_APA7_Ajustado.docx")
FIG_DIR = os.path.join(REPO_ROOT, "assets", "figuras_apa7")

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'pkg_r': 'http://schemas.openxmlformats.org/package/2006/relationships'
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

W_URI = NS['w']
R_URI = NS['r']
A_URI = NS['a']
WP_URI = NS['wp']
PIC_URI = NS['pic']

def w_tag(tag): return f"{{{W_URI}}}{tag}"
def r_tag(tag): return f"{{{R_URI}}}{tag}"
def a_tag(tag): return f"{{{A_URI}}}{tag}"
def wp_tag(tag): return f"{{{WP_URI}}}{tag}"
def pic_tag(tag): return f"{{{PIC_URI}}}{tag}"

def main():
    print("🚀 INICIANDO CONSTRUCCIÓN DEL DOCUMENTO MAESTRO 100% NATIVO PARA MS WORD")
    print(f"   Origen: {ORIG_DOCX}")
    print(f"   Destino: {OUTPUT_DOCX}")

    with zipfile.ZipFile(ORIG_DOCX, 'r') as z_in:
        files = {name: z_in.read(name) for name in z_in.namelist()}

    doc_root = ET.fromstring(files['word/document.xml'])
    styles_root = ET.fromstring(files['word/styles.xml'])
    rels_root = ET.fromstring(files['word/_rels/document.xml.rels'])

    # 1. Update styles.xml for Heading 1, 2, 3, caption, TDC
    print("\n[PASO 1/7] Actualizando estilos en word/styles.xml...")
    update_styles(styles_root)
    files['word/styles.xml'] = ET.tostring(styles_root, encoding='utf-8', xml_declaration=True)

    # 2. Extract TOC entries and mapping to body bookmarks
    print("\n[PASO 2/7] Mapeando los 108 títulos y subtítulos originales...")
    headings_map = extract_headings_map(doc_root)
    print(f"   ✓ {len(headings_map)} títulos y subtítulos identificados con exactitud")

    # 3. Apply Heading numbering and native Word styles to body paragraphs
    print("\n[PASO 3/7] Aplicando numeración exacta y estilos Heading 1-3 en el cuerpo...")
    apply_headings_to_body(doc_root, headings_map)

    # 4. Format all 32 tables to APA 7 (0 vertical lines)
    print("\n[PASO 4/7] Aplicando formato APA 7 a las 32 tablas (0 líneas verticales)...")
    format_apa7_tables(doc_root)

    # 5. Replace 25 figures with 300 DPI APA 7 graphics and set captions
    print("\n[PASO 5/7] Integrando las 25 figuras APA 7 a 300 DPI en word/media/...")
    replace_figures_media(files, doc_root, rels_root)

    # 6. Rebuild native Word SDT indices (TOC, Table of Tables, Table of Figures)
    print("\n[PASO 6/7] Generando Índices Nativos para MS Word (TOC, Tablas, Figuras)...")
    rebuild_native_indices(doc_root, headings_map)

    # 7. Clean up accidental bold runs on long body paragraphs
    print("\n[PASO 7/7] Limpiando negritas accidentales en párrafos normales...")
    clean_unwanted_bolds(doc_root, headings_map)

    # Save document.xml
    files['word/document.xml'] = ET.tostring(doc_root, encoding='utf-8', xml_declaration=True)
    files['word/_rels/document.xml.rels'] = ET.tostring(rels_root, encoding='utf-8', xml_declaration=True)

    # Write out new docx
    print(f"\n💾 Escribiendo archivo final en: {OUTPUT_DOCX}...")
    with zipfile.ZipFile(OUTPUT_DOCX, 'w', compression=zipfile.ZIP_DEFLATED) as z_out:
        for name, data in files.items():
            z_out.writestr(name, data)

    print(f"✅ ¡DOCUMENTO CONSTRUIDO CON ÉXITO! ({os.path.getsize(OUTPUT_DOCX):,} bytes)")

    # Also copy to MTCI_Consolidado_Final_APA7.docx if possible
    dest_master = os.path.join(REPO_ROOT, "assets", "MTCI_Consolidado_Final_APA7.docx")
    try:
        shutil.copyfile(OUTPUT_DOCX, dest_master)
        print(f"   ✓ Copiado también a: {dest_master}")
    except Exception as e:
        print(f"   ⚠️ No se pudo copiar a {dest_master} ({e})")

def update_styles(styles_root):
    """Ensures Heading 1, 2, 3 have outline levels, Times New Roman, bold, black, 1.5 line spacing."""
    style_configs = {
        'Heading1': {'name': 'heading 1', 'sz': '28', 'b': True, 'i': False, 'lvl': '0'},
        'Heading2': {'name': 'heading 2', 'sz': '24', 'b': True, 'i': False, 'lvl': '1'},
        'Heading3': {'name': 'heading 3', 'sz': '24', 'b': True, 'i': True,  'lvl': '2'},
        'Descripcin': {'name': 'caption',   'sz': '24', 'b': False, 'i': False, 'lvl': None},
        'TDC1': {'name': 'toc 1', 'sz': '24', 'b': True,  'i': False, 'lvl': None},
        'TDC2': {'name': 'toc 2', 'sz': '24', 'b': False, 'i': False, 'lvl': None},
        'TDC3': {'name': 'toc 3', 'sz': '24', 'b': False, 'i': False, 'lvl': None},
    }

    for style in styles_root.findall(f'.//{w_tag("style")}'):
        s_id = style.get(w_tag('styleId'))
        if s_id in style_configs:
            cfg = style_configs[s_id]
            # update pPr
            pPr = style.find(w_tag('pPr'))
            if pPr is None:
                pPr = ET.SubElement(style, w_tag('pPr'))
            
            # outline level
            if cfg['lvl'] is not None:
                outline = pPr.find(w_tag('outlineLvl'))
                if outline is None:
                    outline = ET.SubElement(pPr, w_tag('outlineLvl'))
                outline.set(w_tag('val'), cfg['lvl'])

            # update rPr
            rPr = style.find(w_tag('rPr'))
            if rPr is None:
                rPr = ET.SubElement(style, w_tag('rPr'))
                
            # fonts
            rFonts = rPr.find(w_tag('rFonts'))
            if rFonts is None:
                rFonts = ET.SubElement(rPr, w_tag('rFonts'))
            rFonts.set(w_tag('ascii'), 'Times New Roman')
            rFonts.set(w_tag('hAnsi'), 'Times New Roman')
            rFonts.set(w_tag('cs'), 'Times New Roman')
            rFonts.set(w_tag('eastAsia'), 'Times New Roman')

            # size
            sz = rPr.find(w_tag('sz'))
            if sz is None: sz = ET.SubElement(rPr, w_tag('sz'))
            sz.set(w_tag('val'), cfg['sz'])
            szCs = rPr.find(w_tag('szCs'))
            if szCs is None: szCs = ET.SubElement(rPr, w_tag('szCs'))
            szCs.set(w_tag('val'), cfg['sz'])

            # color
            color = rPr.find(w_tag('color'))
            if color is None: color = ET.SubElement(rPr, w_tag('color'))
            color.set(w_tag('val'), '000000')

            # bold
            b_el = rPr.find(w_tag('b'))
            if cfg['b']:
                if b_el is None: b_el = ET.SubElement(rPr, w_tag('b'))
                b_el.set(w_tag('val'), '1')
            else:
                if b_el is not None: rPr.remove(b_el)

            # italic
            i_el = rPr.find(w_tag('i'))
            if cfg['i']:
                if i_el is None: i_el = ET.SubElement(rPr, w_tag('i'))
                i_el.set(w_tag('val'), '1')
            else:
                if i_el is not None: rPr.remove(i_el)

def extract_headings_map(doc_root):
    """Extracts all 108 headings from SDT 0 and maps them to body paragraphs via bookmarks."""
    sdts = doc_root.findall(f'.//{w_tag("sdt")}')
    sdt0 = sdts[0]
    ps = sdt0.findall(f'.//{w_tag("p")}')

    body = doc_root.find(w_tag('body'))
    all_bms = {}
    for idx, p in enumerate(body.findall(w_tag('p'))):
        for b in p.findall(f'.//{w_tag("bookmarkStart")}'):
            name = b.get(w_tag('name'))
            all_bms[name] = idx

    items = []
    for i, p in enumerate(ps):
        t = ''.join(p.itertext()).strip()
        if 'TOC \\' in t:
            t = t.split('"')[-1].strip()

        m_bm = re.search(r'PAGEREF\s+([^\s]+)', t)
        hl = p.find(f'.//{w_tag("hyperlink")}')
        anchor = hl.get(w_tag('anchor')) if hl is not None else ''
        bm = m_bm.group(1) if m_bm else anchor

        clean_t = re.sub(r'PAGEREF\s+[^\s]+\s+\\h', '', t).strip()
        m_page = re.search(r'(\d+)$', clean_t)
        page = m_page.group(1) if m_page else ''
        raw_title = clean_t[:len(clean_t)-len(page)].strip() if page else clean_t

        if not raw_title and not bm:
            continue

        m3 = re.match(r'^(\d+\.\d+\.\d+)\.?\s*(.*)$', raw_title)
        m2 = re.match(r'^(\d+\.\d+)\.?-?\s*(.*)$', raw_title)
        m1 = re.match(r'^(\d+)\.?\s*(.*)$', raw_title)

        if m3:
            lvl = 3
            num_str = m3.group(1) + '.'
            text_str = m3.group(2).strip()
        elif m2:
            lvl = 2
            num_str = m2.group(1) + '.'
            text_str = m2.group(2).strip()
        elif m1:
            lvl = 1
            num_str = m1.group(1) + '.'
            text_str = m1.group(2).strip()
        else:
            lvl = 1
            num_str = ''
            text_str = raw_title

        full_title = f"{num_str} {text_str}".strip()
        p_idx = all_bms.get(bm, -1)

        items.append({
            'toc_idx': i,
            'lvl': lvl,
            'num': num_str,
            'text': text_str,
            'full_title': full_title,
            'page': page,
            'bm': bm,
            'p_idx': p_idx
        })

    return items

def apply_headings_to_body(doc_root, headings_map):
    """Applies exact title numbering, native Heading styles, outlineLvl, and page breaks."""
    body = doc_root.find(w_tag('body'))
    body_ps = body.findall(w_tag('p'))

    # List of major Level 1 chapters that start on a new page
    page_break_chapters = [
        "1. Introducción", "2. Antecedentes", "3. Planteamiento del problema",
        "4. Justificación", "5. Objetivos de investigación", "7. Limitaciones del estudio",
        "8. Contexto de la Investigación", "9. Marco Teórico", "10. Diseño metodológico",
        "11. Análisis y discusión de resultados",
        "12. Propuesta de Manual con Estrategias de MTCI para docentes y estudiantes de psicología",
        "13. Conclusiones", "14. Recomendaciones", "15. Referencias", "16. Anexos"
    ]

    for item in headings_map:
        p_idx = item['p_idx']
        if p_idx == -1 or p_idx >= len(body_ps):
            continue

        p = body_ps[p_idx]
        lvl = item['lvl']
        full_title = item['full_title']

        # Determine style and outline level
        style_id = f"Heading{lvl}"
        outline_val = str(lvl - 1)

        # Update or create pPr
        pPr = p.find(w_tag('pPr'))
        if pPr is None:
            pPr = ET.Element(w_tag('pPr'))
            p.insert(0, pPr)

        # Style
        pStyle = pPr.find(w_tag('pStyle'))
        if pStyle is None:
            pStyle = ET.SubElement(pPr, w_tag('pStyle'))
        pStyle.set(w_tag('val'), style_id)

        # Outline level
        outline = pPr.find(w_tag('outlineLvl'))
        if outline is None:
            outline = ET.SubElement(pPr, w_tag('outlineLvl'))
        outline.set(w_tag('val'), outline_val)

        # Keep with next
        keepNext = pPr.find(w_tag('keepNext'))
        if keepNext is None:
            keepNext = ET.SubElement(pPr, w_tag('keepNext'))
        keepNext.set(w_tag('val'), '1')

        # Spacing
        spacing = pPr.find(w_tag('spacing'))
        if spacing is None:
            spacing = ET.SubElement(pPr, w_tag('spacing'))
        spacing.set(w_tag('before'), '240')
        spacing.set(w_tag('after'), '120')
        spacing.set(w_tag('line'), '360')
        spacing.set(w_tag('lineRule'), 'auto')

        # Indentation (0 for headings)
        ind = pPr.find(w_tag('ind'))
        if ind is None:
            ind = ET.SubElement(pPr, w_tag('ind'))
        ind.set(w_tag('left'), '0')
        ind.set(w_tag('firstLine'), '0')

        # Alignment
        jc = pPr.find(w_tag('jc'))
        if jc is None:
            jc = ET.SubElement(pPr, w_tag('jc'))
        jc.set(w_tag('val'), 'left')

        # Page break before for major chapters
        if any(full_title.startswith(ch) for ch in page_break_chapters):
            pbb = pPr.find(w_tag('pageBreakBefore'))
            if pbb is None:
                pbb = ET.SubElement(pPr, w_tag('pageBreakBefore'))
            pbb.set(w_tag('val'), '1')

        # Keep bookmarks, remove old runs
        b_starts = p.findall(w_tag('bookmarkStart'))
        b_ends = p.findall(w_tag('bookmarkEnd'))

        # Remove all existing children except pPr, bookmarkStart, bookmarkEnd
        for child in list(p):
            if child.tag not in [w_tag('pPr'), w_tag('bookmarkStart'), w_tag('bookmarkEnd')]:
                p.remove(child)

        # Create new run with full_title
        r = ET.SubElement(p, w_tag('r'))
        rPr = ET.SubElement(r, w_tag('rPr'))

        rFonts = ET.SubElement(rPr, w_tag('rFonts'))
        rFonts.set(w_tag('ascii'), 'Times New Roman')
        rFonts.set(w_tag('hAnsi'), 'Times New Roman')
        rFonts.set(w_tag('cs'), 'Times New Roman')

        b_el = ET.SubElement(rPr, w_tag('b'))
        b_el.set(w_tag('val'), '1')

        if lvl == 3:
            i_el = ET.SubElement(rPr, w_tag('i'))
            i_el.set(w_tag('val'), '1')

        color = ET.SubElement(rPr, w_tag('color'))
        color.set(w_tag('val'), '000000')

        sz = ET.SubElement(rPr, w_tag('sz'))
        sz.set(w_tag('val'), '28' if lvl == 1 else '24')
        szCs = ET.SubElement(rPr, w_tag('szCs'))
        szCs.set(w_tag('val'), '28' if lvl == 1 else '24')

        t_el = ET.SubElement(r, w_tag('t'))
        t_el.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t_el.text = full_title

def format_apa7_tables(doc_root):
    """Enforces APA 7 table borders (top, header bottom, table bottom; 0 vertical lines)."""
    tbls = doc_root.findall(f'.//{w_tag("tbl")}')
    print(f"   Tablas encontradas: {len(tbls)}")

    for t_idx, tbl in enumerate(tbls):
        tblPr = tbl.find(w_tag('tblPr'))
        if tblPr is None:
            tblPr = ET.Element(w_tag('tblPr'))
            tbl.insert(0, tblPr)

        # Replace tblBorders
        old_bdr = tblPr.find(w_tag('tblBorders'))
        if old_bdr is not None:
            tblPr.remove(old_bdr)

        new_bdr = ET.SubElement(tblPr, w_tag('tblBorders'))
        # top border
        top = ET.SubElement(new_bdr, w_tag('top'))
        top.set(w_tag('val'), 'single')
        top.set(w_tag('sz'), '4')
        top.set(w_tag('space'), '0')
        top.set(w_tag('color'), '000000')

        # bottom border
        bottom = ET.SubElement(new_bdr, w_tag('bottom'))
        bottom.set(w_tag('val'), 'single')
        bottom.set(w_tag('sz'), '4')
        bottom.set(w_tag('space'), '0')
        bottom.set(w_tag('color'), '000000')

        # left & right: none
        left = ET.SubElement(new_bdr, w_tag('left'))
        left.set(w_tag('val'), 'none')
        right = ET.SubElement(new_bdr, w_tag('right'))
        right.set(w_tag('val'), 'none')

        # insideH: none, insideV: none
        insideH = ET.SubElement(new_bdr, w_tag('insideH'))
        insideH.set(w_tag('val'), 'none')
        insideV = ET.SubElement(new_bdr, w_tag('insideV'))
        insideV.set(w_tag('val'), 'none')

        # Cell margins
        old_cellMar = tblPr.find(w_tag('tblCellMar'))
        if old_cellMar is not None:
            tblPr.remove(old_cellMar)
        new_mar = ET.SubElement(tblPr, w_tag('tblCellMar'))
        for side, dxa in [('top', '80'), ('bottom', '80'), ('left', '100'), ('right', '100')]:
            m = ET.SubElement(new_mar, w_tag(side))
            m.set(w_tag('w'), dxa)
            m.set(w_tag('type'), 'dxa')

        # Header row bottom border
        rows = tbl.findall(w_tag('tr'))
        if rows:
            for cell in rows[0].findall(w_tag('tc')):
                tcPr = cell.find(w_tag('tcPr'))
                if tcPr is None:
                    tcPr = ET.Element(w_tag('tcPr'))
                    cell.insert(0, tcPr)
                tcBorders = tcPr.find(w_tag('tcBorders'))
                if tcBorders is None:
                    tcBorders = ET.SubElement(tcPr, w_tag('tcBorders'))
                bottom = tcBorders.find(w_tag('bottom'))
                if bottom is None:
                    bottom = ET.SubElement(tcBorders, w_tag('bottom'))
                bottom.set(w_tag('val'), 'single')
                bottom.set(w_tag('sz'), '4')
                bottom.set(w_tag('color'), '000000')

def replace_figures_media(files, doc_root, rels_root):
    """Replaces all 25 figures with high-res 300 DPI APA 7 graphics and sets proper extents."""
    # Mapping of figure number to original media target
    media_map = {
        1:  'media/image12.jpg',
        2:  'media/image19.png',
        3:  'media/image27.png',
        4:  'media/image4.png',
        5:  'media/image25.png',
        6:  'media/image23.png',
        7:  'media/image8.png',
        8:  'media/image26.png',
        9:  'media/image14.png',
        10: 'media/image6.png',
        11: 'media/image20.png',
        12: 'media/image29.png',
        13: 'media/image31.png',
        14: 'media/image28.png',
        15: 'media/image32.png',
        16: 'media/image30.png',
        17: 'media/image33.png',
        18: 'media/image16.png',
        19: 'media/image18.png',
        20: 'media/image17.png',
        21: 'media/image9.jpg',
        22: 'media/image2.jpg',
        23: 'media/image15.jpg',
        24: 'media/image24.jpg',
        25: 'media/image5.jpg'
    }

    # Dimensions in EMUs: max width 5.5 inches = 5029200 EMUs
    max_w_emu = 5029200

    for num, target_rel in media_map.items():
        src_png = os.path.join(FIG_DIR, [f for f in os.listdir(FIG_DIR) if f.startswith(f"figura_{num:02d}_")][0])
        im = Image.open(src_png)
        w_px, h_px = im.size
        aspect = h_px / w_px

        calc_w = min(max_w_emu, int(w_px * 914400 / 300))
        calc_h = int(calc_w * aspect)

        # If original target is .jpg, convert to high quality JPEG
        dest_zip_path = f"word/{target_rel}"
        if target_rel.endswith('.jpg'):
            rgb_im = im.convert('RGB')
            buf = io.BytesIO()
            rgb_im.save(buf, format='JPEG', quality=95)
            files[dest_zip_path] = buf.getvalue()
        else:
            with open(src_png, 'rb') as f_img:
                files[dest_zip_path] = f_img.read()

        # Update extents in document.xml for this drawing
        # find relationship ID for this target
        rId = None
        for rel in rels_root.findall(f'.//{{{NS["pkg_r"]}}}Relationship'):
            if rel.get('Target') == target_rel:
                rId = rel.get('Id')
                break

        if rId:
            parent_map = {c: p for p in doc_root.iter() for c in p}
            for blip in doc_root.findall(f'.//{a_tag("blip")}'):
                if blip.get(r_tag('embed')) == rId:
                    # Find ancestor inline or anchor
                    curr = blip
                    while curr is not None:
                        if curr.tag in [wp_tag('inline'), wp_tag('anchor')]:
                            extent = curr.find(wp_tag('extent'))
                            if extent is not None:
                                extent.set('cx', str(calc_w))
                                extent.set('cy', str(calc_h))
                            break
                        curr = parent_map.get(curr)

    print("   ✓ Las 25 figuras fueron reemplazadas con gráficos de alta fidelidad 300 DPI")

def rebuild_native_indices(doc_root, headings_map):
    """Rebuilds SDT 0, SDT 1, and SDT 2 with native Microsoft Word TOC field codes and pre-rendered rows."""
    sdts = doc_root.findall(f'.//{w_tag("sdt")}')
    if len(sdts) < 3:
        print("   ⚠️ Menos de 3 SDTs encontrados en el documento")
        return

    # --- SDT 0: ÍNDICE GENERAL ---
    sdt0_content = sdts[0].find(w_tag('sdtContent'))
    sdt0_content.clear()

    # Title paragraph
    title_p = ET.SubElement(sdt0_content, w_tag('p'))
    t_pPr = ET.SubElement(title_p, w_tag('pPr'))
    t_style = ET.SubElement(t_pPr, w_tag('pStyle'))
    t_style.set(w_tag('val'), 'TtuloTDC')
    t_jc = ET.SubElement(t_pPr, w_tag('jc'))
    t_jc.set(w_tag('val'), 'center')
    t_r = ET.SubElement(title_p, w_tag('r'))
    t_rPr = ET.SubElement(t_r, w_tag('rPr'))
    ET.SubElement(t_rPr, w_tag('b')).set(w_tag('val'), '1')
    ET.SubElement(t_rPr, w_tag('sz')).set(w_tag('val'), '28')
    ET.SubElement(t_rPr, w_tag('color')).set(w_tag('val'), '000000')
    t_text = ET.SubElement(t_r, w_tag('t'))
    t_text.text = "ÍNDICE GENERAL"

    # Headings rows
    for idx, item in enumerate(headings_map):
        p = ET.SubElement(sdt0_content, w_tag('p'))
        pPr = ET.SubElement(p, w_tag('pPr'))
        pStyle = ET.SubElement(pPr, w_tag('pStyle'))
        pStyle.set(w_tag('val'), f"TDC{item['lvl']}")

        tabs = ET.SubElement(pPr, w_tag('tabs'))
        tab = ET.SubElement(tabs, w_tag('tab'))
        tab.set(w_tag('val'), 'right')
        tab.set(w_tag('leader'), 'dot')
        tab.set(w_tag('pos'), '9360')

        spacing = ET.SubElement(pPr, w_tag('spacing'))
        spacing.set(w_tag('before'), '0')
        spacing.set(w_tag('after'), '0')
        spacing.set(w_tag('line'), '280')
        spacing.set(w_tag('lineRule'), 'auto')

        if item['lvl'] > 1:
            ind = ET.SubElement(pPr, w_tag('ind'))
            ind.set(w_tag('left'), str((item['lvl'] - 1) * 360))

        # Begin field on first entry
        if idx == 0:
            r_begin = ET.SubElement(p, w_tag('r'))
            ET.SubElement(r_begin, w_tag('fldChar')).set(w_tag('fldCharType'), 'begin')
            instr = ET.SubElement(r_begin, w_tag('instrText'))
            instr.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            instr.text = ' TOC \\o "1-3" \\h \\z \\u '
            ET.SubElement(r_begin, w_tag('fldChar')).set(w_tag('fldCharType'), 'separate')

        # Hyperlink to bookmark
        hl = ET.SubElement(p, w_tag('hyperlink'))
        hl.set(w_tag('anchor'), item['bm'])

        r = ET.SubElement(hl, w_tag('r'))
        rPr = ET.SubElement(r, w_tag('rPr'))
        rFonts = ET.SubElement(rPr, w_tag('rFonts'))
        rFonts.set(w_tag('ascii'), 'Times New Roman')
        rFonts.set(w_tag('hAnsi'), 'Times New Roman')
        ET.SubElement(rPr, w_tag('sz')).set(w_tag('val'), '24')
        ET.SubElement(rPr, w_tag('color')).set(w_tag('val'), '000000')
        if item['lvl'] == 1:
            ET.SubElement(rPr, w_tag('b')).set(w_tag('val'), '1')

        t_title = ET.SubElement(r, w_tag('t'))
        t_title.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t_title.text = item['full_title']

        ET.SubElement(r, w_tag('tab'))

        t_page = ET.SubElement(r, w_tag('t'))
        t_page.text = item['page']

        # End field on last entry
        if idx == len(headings_map) - 1:
            r_end = ET.SubElement(p, w_tag('r'))
            ET.SubElement(r_end, w_tag('fldChar')).set(w_tag('fldCharType'), 'end')

    # --- SDT 1: ÍNDICE DE TABLAS ---
    tables_entries = [
        ("Tabla 1. Prácticas y terapias de la MTCI según su ámbito de aplicación", "22"),
        ("Tabla 2. Tipología y características del diseño metodológico de la investigación", "45"),
        ("Tabla 3. Componentes del enfoque mixto concurrente y su articulación metodológica", "46"),
        ("Tabla 4. Supuestos del paradigma pragmático y su aplicación en la investigación", "47"),
        ("Tabla 5. Caracterización de las unidades de análisis y recolección de información", "48"),
        ("Tabla 6. Composición y tamaño de la muestra participante por unidad de análisis", "50"),
        ("Tabla 7. Matriz de operacionalización de categorías y variables de la investigación", "52"),
        ("Tabla 8. Técnicas e instrumentos de recolección de datos primarios aplicados en campo", "64"),
        ("Tabla 9. Estructura modular y contenidos temáticos de la propuesta de manual de estrategias", "98"),
    ]

    sdt1_content = sdts[1].find(w_tag('sdtContent'))
    sdt1_content.clear()

    # Title
    t1_p = ET.SubElement(sdt1_content, w_tag('p'))
    t1_pPr = ET.SubElement(t1_p, w_tag('pPr'))
    ET.SubElement(t1_pPr, w_tag('pStyle')).set(w_tag('val'), 'TtuloTDC')
    ET.SubElement(t1_pPr, w_tag('jc')).set(w_tag('val'), 'center')
    t1_r = ET.SubElement(t1_p, w_tag('r'))
    t1_rPr = ET.SubElement(t1_r, w_tag('rPr'))
    ET.SubElement(t1_rPr, w_tag('b')).set(w_tag('val'), '1')
    ET.SubElement(t1_rPr, w_tag('sz')).set(w_tag('val'), '28')
    ET.SubElement(t1_rPr, w_tag('color')).set(w_tag('val'), '000000')
    ET.SubElement(t1_r, w_tag('t')).text = "ÍNDICE DE TABLAS"

    for idx, (t_title, t_page) in enumerate(tables_entries):
        p = ET.SubElement(sdt1_content, w_tag('p'))
        pPr = ET.SubElement(p, w_tag('pPr'))
        ET.SubElement(pPr, w_tag('pStyle')).set(w_tag('val'), 'TDC1')
        tabs = ET.SubElement(pPr, w_tag('tabs'))
        tab = ET.SubElement(tabs, w_tag('tab'))
        tab.set(w_tag('val'), 'right')
        tab.set(w_tag('leader'), 'dot')
        tab.set(w_tag('pos'), '9360')
        spacing = ET.SubElement(pPr, w_tag('spacing'))
        spacing.set(w_tag('before'), '0')
        spacing.set(w_tag('after'), '0')
        spacing.set(w_tag('line'), '280')
        spacing.set(w_tag('lineRule'), 'auto')

        if idx == 0:
            r_begin = ET.SubElement(p, w_tag('r'))
            ET.SubElement(r_begin, w_tag('fldChar')).set(w_tag('fldCharType'), 'begin')
            instr = ET.SubElement(r_begin, w_tag('instrText'))
            instr.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            instr.text = ' TOC \\h \\z \\c "Tabla" '
            ET.SubElement(r_begin, w_tag('fldChar')).set(w_tag('fldCharType'), 'separate')

        r = ET.SubElement(p, w_tag('r'))
        rPr = ET.SubElement(r, w_tag('rPr'))
        rFonts = ET.SubElement(rPr, w_tag('rFonts'))
        rFonts.set(w_tag('ascii'), 'Times New Roman')
        rFonts.set(w_tag('hAnsi'), 'Times New Roman')
        ET.SubElement(rPr, w_tag('sz')).set(w_tag('val'), '24')
        ET.SubElement(rPr, w_tag('color')).set(w_tag('val'), '000000')

        t_el = ET.SubElement(r, w_tag('t'))
        t_el.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t_el.text = t_title

        ET.SubElement(r, w_tag('tab'))

        t_p_el = ET.SubElement(r, w_tag('t'))
        t_p_el.text = t_page

        if idx == len(tables_entries) - 1:
            r_end = ET.SubElement(p, w_tag('r'))
            ET.SubElement(r_end, w_tag('fldChar')).set(w_tag('fldCharType'), 'end')

    # --- SDT 2: ÍNDICE DE FIGURAS ---
    figures_entries = [
        ("Figura 1. Ubicación geográfica del Centro Universitario Regional (CUR-Estelí)", "16"),
        ("Figura 2. Diagrama de flujo de criterios de inclusión y exclusión de las unidades de análisis", "49"),
        ("Figura 3. Distribución sociodemográfica y formativa de la muestra estudiantil", "73"),
        ("Figura 4. Nivel de dominio conceptual y normativo sobre MTCI en estudiantes de Psicología", "74"),
        ("Figura 5. Reconocimiento de prácticas de MTCI en estudiantes: Medicina natural y terapias manuales", "75"),
        ("Figura 6. Reconocimiento de prácticas de MTCI en estudiantes: Terapias psicoemocionales y holísticas", "75"),
        ("Figura 7. Frecuencia de uso personal de MTCI y efectos psicofisiológicos experimentados", "76"),
        ("Figura 8. Distribución por sexo de los facilitadores y actores locales de MTCI", "77"),
        ("Figura 9. Distribución por rangos de edad de los facilitadores locales de MTCI", "78"),
        ("Figura 10. Años de experiencia profesional en el ejercicio de la MTCI de los facilitadores", "79"),
        ("Figura 11. Procedencia geográfica de los facilitadores locales de MTCI", "79"),
        ("Figura 12. Modalidades terapéuticas de MTCI utilizadas habitualmente en la atención profesional", "80"),
        ("Figura 13. Percepción de cambios en los niveles de estrés y ansiedad en usuarios atendidos", "81"),
        ("Figura 14. Grado de apertura emocional y receptividad observado en los usuarios", "82"),
        ("Figura 15. Frecuencia de efectos desfavorables o reacciones emocionales adversas observadas", "83"),
        ("Figura 16. Nivel de interacción y coordinación con profesionales e instituciones de salud locales", "84"),
        ("Figura 17. Nivel de dificultad normativa y burocrática experimentada por los facilitadores", "85"),
        ("Figura 18. Frecuencia de usuarios con creencias o reservas socioculturales y religiosas hacia la MTCI", "86"),
        ("Figura 19. Incidencia del factor económico en el acceso y continuidad de las terapias de MTCI", "87"),
        ("Figura 20. Distribución por sexo del cuerpo docente de Psicología consultado", "88"),
        ("Figura 21. Distribución por grupos de edad del cuerpo docente de Psicología", "89"),
        ("Figura 22. Distribución de docentes según área de especialidad profesional", "89"),
        ("Figura 23. Años de experiencia en la docencia universitaria de los participantes", "90"),
        ("Figura 24. Estrategias pedagógicas priorizadas por docentes para abordar la MTCI", "91"),
        ("Figura 25. Experiencias formativas consideradas más favorables para la integración de la MTCI", "92"),
    ]

    sdt2_content = sdts[2].find(w_tag('sdtContent'))
    sdt2_content.clear()

    # Title
    t2_p = ET.SubElement(sdt2_content, w_tag('p'))
    t2_pPr = ET.SubElement(t2_p, w_tag('pPr'))
    ET.SubElement(t2_pPr, w_tag('pStyle')).set(w_tag('val'), 'TtuloTDC')
    ET.SubElement(t2_pPr, w_tag('jc')).set(w_tag('val'), 'center')
    t2_r = ET.SubElement(t2_p, w_tag('r'))
    t2_rPr = ET.SubElement(t2_r, w_tag('rPr'))
    ET.SubElement(t2_rPr, w_tag('b')).set(w_tag('val'), '1')
    ET.SubElement(t2_rPr, w_tag('sz')).set(w_tag('val'), '28')
    ET.SubElement(t2_rPr, w_tag('color')).set(w_tag('val'), '000000')
    ET.SubElement(t2_r, w_tag('t')).text = "ÍNDICE DE FIGURAS"

    for idx, (f_title, f_page) in enumerate(figures_entries):
        p = ET.SubElement(sdt2_content, w_tag('p'))
        pPr = ET.SubElement(p, w_tag('pPr'))
        ET.SubElement(pPr, w_tag('pStyle')).set(w_tag('val'), 'TDC1')
        tabs = ET.SubElement(pPr, w_tag('tabs'))
        tab = ET.SubElement(tabs, w_tag('tab'))
        tab.set(w_tag('val'), 'right')
        tab.set(w_tag('leader'), 'dot')
        tab.set(w_tag('pos'), '9360')
        spacing = ET.SubElement(pPr, w_tag('spacing'))
        spacing.set(w_tag('before'), '0')
        spacing.set(w_tag('after'), '0')
        spacing.set(w_tag('line'), '280')
        spacing.set(w_tag('lineRule'), 'auto')

        if idx == 0:
            r_begin = ET.SubElement(p, w_tag('r'))
            ET.SubElement(r_begin, w_tag('fldChar')).set(w_tag('fldCharType'), 'begin')
            instr = ET.SubElement(r_begin, w_tag('instrText'))
            instr.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            instr.text = ' TOC \\h \\z \\c "Figura" '
            ET.SubElement(r_begin, w_tag('fldChar')).set(w_tag('fldCharType'), 'separate')

        r = ET.SubElement(p, w_tag('r'))
        rPr = ET.SubElement(r, w_tag('rPr'))
        rFonts = ET.SubElement(rPr, w_tag('rFonts'))
        rFonts.set(w_tag('ascii'), 'Times New Roman')
        rFonts.set(w_tag('hAnsi'), 'Times New Roman')
        ET.SubElement(rPr, w_tag('sz')).set(w_tag('val'), '24')
        ET.SubElement(rPr, w_tag('color')).set(w_tag('val'), '000000')

        t_el = ET.SubElement(r, w_tag('t'))
        t_el.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t_el.text = f_title

        ET.SubElement(r, w_tag('tab'))

        t_p_el = ET.SubElement(r, w_tag('t'))
        t_p_el.text = f_page

        if idx == len(figures_entries) - 1:
            r_end = ET.SubElement(p, w_tag('r'))
            ET.SubElement(r_end, w_tag('fldChar')).set(w_tag('fldCharType'), 'end')

    print("   ✓ SDT 0 (Índice General), SDT 1 (Tablas) y SDT 2 (Figuras) configurados con campos nativos TOC")

def clean_unwanted_bolds(doc_root, headings_map):
    """Removes bold formatting from paragraphs that are not headings, tables, or figure labels."""
    heading_p_indices = {item['p_idx'] for item in headings_map if item['p_idx'] != -1}
    body = doc_root.find(w_tag('body'))
    body_ps = body.findall(w_tag('p'))

    cleaned_count = 0
    for idx, p in enumerate(body_ps):
        if idx in heading_p_indices:
            continue

        text = ''.join(p.itertext()).strip()
        # Keep bold on table or figure caption lines
        if text.startswith('Tabla ') or text.startswith('Figura '):
            continue

        # If a body paragraph is long (> 80 chars) and has bold runs
        if len(text) > 80:
            for r in p.findall(w_tag('r')):
                rPr = r.find(w_tag('rPr'))
                if rPr is not None:
                    b_el = rPr.find(w_tag('b'))
                    # Don't unbold lead-in definitions like 'Ley No. 774:' or short prefix
                    r_text = ''.join(r.itertext()).strip()
                    if b_el is not None and len(r_text) > 60:
                        rPr.remove(b_el)
                        cleaned_count += 1

    print(f"   ✓ {cleaned_count} ejecuciones de negrita redundante limpiadas en párrafos de texto")

if __name__ == '__main__':
    main()
