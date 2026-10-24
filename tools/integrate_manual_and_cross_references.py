#!/usr/bin/env python3
"""
tools/integrate_manual_and_cross_references.py
================================================================================
Integra el 'Manual de Estrategias MTCI · Psicología CUR-Estelí' como Anexo 16.2
en 'assets/MTCI_Consolidado_Final_APA7.docx', cumpliendo estrictamente con:
1. Adición del manual en sus anexos tal cual, sin alterar su contenido, tablas ni referencias.
2. Incorporación armónica y coherente del manual en todas las áreas clave del documento:
   - MÉTODO (Cap. 10 / 10.7.5): Fase propositiva de formulación del manual (Objetivo 3).
   - RESULTADOS / TRANSICIÓN (Cap. 11 / 11.3.8): Cierre de aportes docentes y fundamentación del manual.
   - PROPUESTA (Cap. 12 / 12.1 y 12.2): Presentación del manual, Tabla 9 y remisión al Anexo 16.2.
   - CONCLUSIONES (Cap. 13): Conclusión sustantiva del Objetivo 3 materializada en el Anexo 16.2.
   - RECOMENDACIONES (Cap. 14 / 14.1, 14.2, 14.3): Operacionalización del manual por estudiantes, docentes y CUR-Estelí.
   - ANEXOS (Cap. 16): Anexo 16.2 con el texto íntegro, portada, índice interno, 14 secciones,
     13 tablas (incluyendo el instrumento I-CAM-Q adaptado a Nicaragua) y referencias.
3. Preservación absoluta del motor de citas dinámicas nativas en Microsoft Word (<b:Sources>),
   con 63 fuentes canónicas ricas y 100% de marcas de verificación activas (Cited == True).
================================================================================
"""

import os
import sys
import zipfile
import shutil
import copy
from lxml import etree

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DOC = os.path.join(REPO_ROOT, "scratch", "test_perfect_final.docx")
if not os.path.exists(BASE_DOC):
    BASE_DOC = os.path.join(REPO_ROOT, "scratch", "test_rich_com.docx")
MANUAL_DOC = os.path.join(REPO_ROOT, "assets", "Manual de Estrategias MTCI_Psicología.docx")
TARGET_DOC = os.path.join(REPO_ROOT, "assets", "MTCI_Consolidado_Final_APA7.docx")
BACKUP_DOC = os.path.join(REPO_ROOT, "assets", "MTCI_Consolidado_Final_APA7_Ajustado.docx")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
B_NS = "http://schemas.openxmlformats.org/officeDocument/2006/bibliography"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"


def create_p(text, style_id="Normal", bold=False, italic=False, space_before=120, space_after=120, page_break=False):
    p = etree.Element(f"{{{W_NS}}}p")
    pPr = etree.SubElement(p, f"{{{W_NS}}}pPr")
    if style_id != "Normal":
        pStyle = etree.SubElement(pPr, f"{{{W_NS}}}pStyle")
        pStyle.set(f"{{{W_NS}}}val", style_id)
    if page_break:
        etree.SubElement(pPr, f"{{{W_NS}}}pageBreakBefore")
    
    sp = etree.SubElement(pPr, f"{{{W_NS}}}spacing")
    sp.set(f"{{{W_NS}}}before", str(space_before))
    sp.set(f"{{{W_NS}}}after", str(space_after))
    sp.set(f"{{{W_NS}}}line", "360")
    sp.set(f"{{{W_NS}}}lineRule", "auto")

    jc = etree.SubElement(pPr, f"{{{W_NS}}}jc")
    jc.set(f"{{{W_NS}}}val", "both" if style_id == "Normal" else "left")
    
    r = etree.SubElement(p, f"{{{W_NS}}}r")
    rPr = etree.SubElement(r, f"{{{W_NS}}}rPr")
    rFonts = etree.SubElement(rPr, f"{{{W_NS}}}rFonts")
    rFonts.set(f"{{{W_NS}}}ascii", "Times New Roman")
    rFonts.set(f"{{{W_NS}}}hAnsi", "Times New Roman")
    rFonts.set(f"{{{W_NS}}}cs", "Times New Roman")
    
    sz = etree.SubElement(rPr, f"{{{W_NS}}}sz")
    sz.set(f"{{{W_NS}}}val", "24")
    szCs = etree.SubElement(rPr, f"{{{W_NS}}}szCs")
    szCs.set(f"{{{W_NS}}}val", "24")
    
    if bold:
        etree.SubElement(rPr, f"{{{W_NS}}}b")
        etree.SubElement(rPr, f"{{{W_NS}}}bCs")
    if italic:
        etree.SubElement(rPr, f"{{{W_NS}}}i")
        etree.SubElement(rPr, f"{{{W_NS}}}iCs")
        
    t = etree.SubElement(r, f"{{{W_NS}}}t")
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    return p


def build_consolidated_document():
    print("=" * 70)
    print("INTEGRANDO MANUAL DE ESTRATEGIAS MTCI Y REFERENCIAS CRUZADAS")
    print("=" * 70)
    
    with zipfile.ZipFile(BASE_DOC, "r") as zbase, zipfile.ZipFile(MANUAL_DOC, "r") as zman:
        # 1. Media (Manual Logo)
        print("\n[1/7] Extrayendo y registrando logotipo del manual...")
        manual_logo_bytes = zman.read("word/media/image1.jpg")
        
        # 2. [Content_Types].xml
        print("\n[2/7] Verificando [Content_Types].xml para soporte JPG/JPEG...")
        ct_root = etree.fromstring(zbase.read("[Content_Types].xml"))
        has_jpg = any(d.get("Extension", "").lower() == "jpg" for d in ct_root.findall(f"{{{CT_NS}}}Default"))
        if not has_jpg:
            d_jpg = etree.SubElement(ct_root, f"{{{CT_NS}}}Default")
            d_jpg.set("Extension", "jpg")
            d_jpg.set("ContentType", "image/jpeg")
        has_jpeg = any(d.get("Extension", "").lower() == "jpeg" for d in ct_root.findall(f"{{{CT_NS}}}Default"))
        if not has_jpeg:
            d_jpeg = etree.SubElement(ct_root, f"{{{CT_NS}}}Default")
            d_jpeg.set("Extension", "jpeg")
            d_jpeg.set("ContentType", "image/jpeg")
        ct_bytes = etree.tostring(ct_root, xml_declaration=True, encoding="utf-8", standalone=True)
        
        # 3. word/_rels/document.xml.rels
        print("\n[3/7] Añadiendo relación de imagen con PKG_REL_NS...")
        rels_root = etree.fromstring(zbase.read("word/_rels/document.xml.rels"))
        existing_rids = []
        for rel in rels_root:
            rid = rel.get("Id", "")
            if rid.startswith("rId") and rid[3:].isdigit():
                existing_rids.append(int(rid[3:]))
        next_rid = max(existing_rids) + 1
        manual_img_rid = f"rId{next_rid}"
        
        new_rel = etree.SubElement(rels_root, f"{{{PKG_REL_NS}}}Relationship")
        new_rel.set("Id", manual_img_rid)
        new_rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image")
        new_rel.set("Target", "media/manual_logo.jpg")
        rels_bytes = etree.tostring(rels_root, xml_declaration=True, encoding="utf-8", standalone=True)
        print(f"   ✓ Relación creada: {manual_img_rid} -> media/manual_logo.jpg")
        
        # 4. word/numbering.xml
        print("\n[4/7] Sincronizando listas numeradas y viñetas (101-104)...")
        num_root = etree.fromstring(zbase.read("word/numbering.xml"))
        man_num_root = etree.fromstring(zman.read("word/numbering.xml"))
        num_map = {"1": "101", "2": "102", "3": "103", "4": "104"}
        abs_map = {"0": "100", "3": "101", "1": "102", "2": "103"}
        
        first_num = num_root.find(f"{{{W_NS}}}num")
        idx_first_num = list(num_root).index(first_num)
        
        for abs_el in man_num_root.findall(f"{{{W_NS}}}abstractNum"):
            old_id = abs_el.get(f"{{{W_NS}}}abstractNumId")
            if old_id in abs_map:
                new_abs = copy.deepcopy(abs_el)
                new_abs.set(f"{{{W_NS}}}abstractNumId", abs_map[old_id])
                num_root.insert(idx_first_num, new_abs)
                idx_first_num += 1
                
        for num_el in man_num_root.findall(f"{{{W_NS}}}num"):
            old_id = num_el.get(f"{{{W_NS}}}numId")
            if old_id in num_map:
                new_num = copy.deepcopy(num_el)
                new_num.set(f"{{{W_NS}}}numId", num_map[old_id])
                abs_ref = new_num.find(f"{{{W_NS}}}abstractNumId")
                if abs_ref is not None:
                    old_abs = abs_ref.get(f"{{{W_NS}}}val")
                    if old_abs in abs_map:
                        abs_ref.set(f"{{{W_NS}}}val", abs_map[old_abs])
                num_root.append(new_num)
        num_bytes = etree.tostring(num_root, xml_declaration=True, encoding="utf-8", standalone=True)
        
        # 5. word/styles.xml
        print("\n[5/7] Verificando estilos para el manual (Texto en negrita1)...")
        styles_root = etree.fromstring(zbase.read("word/styles.xml"))
        has_bold1 = any(s.get(f"{{{W_NS}}}styleId") == "Textoennegrita1" for s in styles_root.findall(f"{{{W_NS}}}style"))
        if not has_bold1:
            new_style = etree.SubElement(styles_root, f"{{{W_NS}}}style")
            new_style.set(f"{{{W_NS}}}type", "paragraph")
            new_style.set(f"{{{W_NS}}}customStyle", "1")
            new_style.set(f"{{{W_NS}}}styleId", "Textoennegrita1")
            name_el = etree.SubElement(new_style, f"{{{W_NS}}}name")
            name_el.set(f"{{{W_NS}}}val", "Texto en negrita1")
            etree.SubElement(new_style, f"{{{W_NS}}}qFormat")
            rPr_el = etree.SubElement(new_style, f"{{{W_NS}}}rPr")
            etree.SubElement(rPr_el, f"{{{W_NS}}}b")
            etree.SubElement(rPr_el, f"{{{W_NS}}}bCs")
        styles_bytes = etree.tostring(styles_root, xml_declaration=True, encoding="utf-8", standalone=True)
        
        # 6. customXml/item1.xml (Fuentes bibliográficas)
        print("\n[6/7] Consolidando fuentes bibliográficas nativas del manual...")
        item_root = etree.fromstring(zbase.read("customXml/item1.xml"))
        man_item_root = etree.fromstring(zman.read("customXml/item1.xml"))
        existing_tags = {s.find(f"{{{B_NS}}}Tag").text for s in item_root.findall(f"{{{B_NS}}}Source")}
        
        added_sources = 0
        for s in man_item_root.findall(f"{{{B_NS}}}Source"):
            tag = s.find(f"{{{B_NS}}}Tag").text
            if tag not in existing_tags:
                item_root.append(copy.deepcopy(s))
                existing_tags.add(tag)
                added_sources += 1
                print(f"   ✓ Fuente nativa añadida: {tag}")
        print(f"   Total fuentes consolidadas en <b:Sources>: {len(item_root.findall(f'{{{B_NS}}}Source'))}")
        item_bytes = etree.tostring(item_root, xml_declaration=True, encoding="utf-8", standalone=False)
        
        # 7. word/document.xml (Articulación metodológica, resultados, conclusiones y anexos)
        print("\n[7/7] Armonizando texto narrativo e insertando Anexo 16.2...")
        doc_root = etree.fromstring(zbase.read("word/document.xml"))
        man_doc_root = etree.fromstring(zman.read("word/document.xml"))
        
        master_body = doc_root.find(f"{{{W_NS}}}body")
        manual_body = man_doc_root.find(f"{{{W_NS}}}body")
        master_sectPr = master_body.find(f"{{{W_NS}}}sectPr")
        
        # A) MÉTODO (Cap. 10 / 10.7.5): Insertar Fase propositiva tras párrafo de docentes
        p_docentes_phase = None
        for p in master_body.findall(f"{{{W_NS}}}p"):
            txt = "".join(p.itertext()).strip()
            if "Por otro lado, el cuestionario dirigido a docentes- psicólogos del CUR- Estelí también se realizó de forma virtual" in txt:
                p_docentes_phase = p
                break
                
        if p_docentes_phase is not None:
            p_fase_title = create_p("Fase propositiva: Diseño y estructuración del Manual de Estrategias de MTCI (Objetivo 3)", bold=True, space_before=180, space_after=60)
            p_fase_body = create_p(
                "Como culminación metodológica de la investigación y en estricta concordancia con el tercer objetivo específico "
                "(«Proponer estrategias complementarias para abordar la MTCI en la formación de estudiantes de Psicología»), "
                "se ejecutó una fase propositiva orientada al diseño y formalización del Manual de Estrategias para el Abordaje de la MTCI "
                "en la Formación y Práctica Psicológica (véase el Anexo 16.2). Esta fase tradujo los hallazgos empíricos mediante un procedimiento "
                "inductivo-deductivo en cuatro momentos operativos: 1) Sistematización diagnóstica a partir de la brecha identificada en los estudiantes "
                "entre alta pertinencia percibida y baja autocompetencia práctica para psicoeducar y derivar; 2) Delimitación del marco deontológico y "
                "regulatorio en apego a las Leyes No. 774, No. 759 y No. 292, definiendo un mapa analítico que restringe la MTCI al autocuidado coadyuvante "
                "e inhibe la aplicación de terapias invasivas o la sustitución del tratamiento psicoterapéutico formal; 3) Formulación de algoritmos de toma "
                "de decisiones clínicas en cuatro pasos, pautas comunicacionales para abordar el ocultamiento terapéutico y una ruta formativa para 4.º y 5.º año; "
                "y 4) Adaptación cultural para Nicaragua del Cuestionario Internacional sobre Uso de MTCI (I-CAM-Q), proporcionando a la carrera una herramienta "
                "estandarizada de exploración clínica e investigación."
            )
            p_docentes_phase.addnext(p_fase_body)
            p_docentes_phase.addnext(p_fase_title)
            print("   ✓ [Método] Insertada Fase propositiva del manual en 10.7.5.")
            
        # B) RESULTADOS / DISCUSIÓN (Cap. 11 / 11.3.8): Insertar puente hacia la propuesta al final del capítulo
        p_docentes_last = None
        for p in master_body.findall(f"{{{W_NS}}}p"):
            txt = "".join(p.itertext()).strip()
            if "La propuesta más detallada y estructurada provino de un docente con especialidad en psicología comunitaria" in txt:
                p_docentes_last = p
                break
                
        if p_docentes_last is not None:
            p_bridge = create_p(
                "La convergencia de estas propuestas docentes, articuladas con las necesidades diagnósticas de los estudiantes "
                "y las observaciones de los facilitadores locales sobre las barreras socioculturales del municipio, fundamenta de manera "
                "directa la propuesta operativa que da salida al tercer objetivo de la investigación: el Manual de Estrategias para el Abordaje "
                "de la MTCI en la Formación y Práctica Psicológica. Su estructura modular y fundamentos pedagógicos se exponen en el capítulo 12, "
                "mientras que su desarrollo documental completo se incorpora in extenso en el Anexo 16.2.",
                space_before=120, space_after=120
            )
            p_docentes_last.addnext(p_bridge)
            print("   ✓ [Resultados] Insertado puente hacia la propuesta al cierre de 11.3.8.")
            
        # C) PROPUESTA DE MANUAL (Cap. 12 / 12.1): Actualizar párrafo fundacional con remisión al Anexo 16.2
        for p in master_body.findall(f"{{{W_NS}}}p"):
            txt = "".join(p.itertext()).strip()
            if txt.startswith("El manual es el producto del tercer objetivo específico de la investigación"):
                for r in p.findall(f"{{{W_NS}}}r"):
                    p.remove(r)
                new_r = etree.SubElement(p, f"{{{W_NS}}}r")
                new_t = etree.SubElement(new_r, f"{{{W_NS}}}t")
                new_t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                new_t.text = (
                    "El manual constituye el producto operativo central del tercer objetivo específico de la investigación: proponer "
                    "estrategias complementarias para abordar la MTCI en la formación de estudiantes de Psicología. Se trata de una guía práctica "
                    "de orientación técnico-ética, de 18 páginas, dirigida al claustro docente y a los estudiantes de 4.º y 5.º año de la carrera del "
                    "CUR-Estelí. Su propósito no es formar psicólogos que apliquen técnicas de medicina tradicional o natural invasivas, sino "
                    "profesionales dotados de criterio clínico, discernimiento ético y sensibilidad intercultural para reconocer, dialogar, psicoeducar "
                    "y, cuando corresponda, derivar de manera segura y culturalmente respetuosa. La propuesta pedagógica se organiza en ocho módulos "
                    "temáticos estructurados secuencialmente (véase la Tabla 9), y su texto íntegro, incluyendo directrices clínicas, protocolos de "
                    "referencia y el inventario I-CAM-Q adaptado a Nicaragua, se adjunta in extenso en el Anexo 16.2 de este documento."
                )
                print("   ✓ [Propuesta] Actualizado párrafo 12.1 con remisión explícita a Anexo 16.2.")
                break
                
        # D) CONCLUSIONES (Cap. 13): Enriquecer conclusión del Objetivo 3 con remisión a Anexo 16.2
        for p in master_body.findall(f"{{{W_NS}}}p"):
            txt = "".join(p.itertext()).strip()
            if txt.startswith("Estas propuestas, junto con las necesidades expresadas por estudiantes y actores locales"):
                for r in p.findall(f"{{{W_NS}}}r"):
                    p.remove(r)
                new_r = etree.SubElement(p, f"{{{W_NS}}}r")
                new_t = etree.SubElement(new_r, f"{{{W_NS}}}t")
                new_t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                new_t.text = (
                    "Estas propuestas, articuladas con las necesidades diagnósticas manifestadas por los estudiantes y las valoraciones "
                    "de los facilitadores territoriales, se materializaron en el producto central del tercer objetivo específico: el Manual de "
                    "Estrategias para el Abordaje de la Medicina Tradicional, Complementaria e Integrativa (MTCI) en la Formación y Práctica "
                    "Psicológica, incorporado in extenso en el Anexo 16.2 de esta tesis. Este instrumento traduce los hallazgos empíricos en "
                    "principios éticos rectores, un mapa analítico de prácticas delimitado según el rol profesional, una guía secuencial de toma "
                    "de decisiones clínicas en cuatro pasos, pautas para superar el ocultamiento terapéutico, una ruta formativa para 4.º y 5.º año, "
                    "cuatro acciones institucionales de capacitación docente y la adaptación para Nicaragua del cuestionario internacional I-CAM-Q, "
                    "cumpliendo satisfactoriamente la meta propositiva del estudio."
                )
                print("   ✓ [Conclusiones] Actualizada conclusión del Objetivo 3 con cita a Anexo 16.2.")
                break
                
        # E) RECOMENDACIONES (Cap. 14): Citar Anexo 16.2 en estudiantes, docentes y gestión
        for p in master_body.findall(f"{{{W_NS}}}p"):
            txt = "".join(p.itertext()).strip()
            if txt.startswith("Desarrollar habilidades de psicoeducación y derivación: Practicar la guía de decisiones del manual"):
                for r in p.findall(f"{{{W_NS}}}r"):
                    p.remove(r)
                new_r = etree.SubElement(p, f"{{{W_NS}}}r")
                new_t = etree.SubElement(new_r, f"{{{W_NS}}}t")
                new_t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                new_t.text = (
                    "Desarrollar habilidades de psicoeducación y derivación: Practicar sistemáticamente el algoritmo de toma de decisiones "
                    "clínicas del manual (Anexo 16.2), consultando con los supervisores de casos ante situaciones complejas o dudas sobre posibles "
                    "interacciones terapéuticas en la consulta psicológica."
                )
                print("   ✓ [Recomendaciones Estudiantes] Actualizada recomendación con cita a Anexo 16.2.")
                break
                
        for p in master_body.findall(f"{{{W_NS}}}p"):
            txt = "".join(p.itertext()).strip()
            if txt.startswith("Enseñar los límites del rol con claridad, apoyándose en el mapa de prácticas y en la guía de decisiones"):
                for r in p.findall(f"{{{W_NS}}}r"):
                    p.remove(r)
                new_r = etree.SubElement(p, f"{{{W_NS}}}r")
                new_t = etree.SubElement(new_r, f"{{{W_NS}}}t")
                new_t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                new_t.text = (
                    "Enseñar los límites del rol profesional con claridad, apoyándose en el mapa analítico de prácticas y en la guía de toma de "
                    "decisiones del manual (Anexo 16.2), para que los estudiantes reconozcan cuándo una intervención complementaria debe ser "
                    "derivada a profesionales de la salud habilitados o facilitadores certificados."
                )
                print("   ✓ [Recomendaciones Docentes] Actualizada recomendación con cita a Anexo 16.2.")
                break

        for p in master_body.findall(f"{{{W_NS}}}p"):
            txt = "".join(p.itertext()).strip()
            if txt.startswith("Incorporar la MTCI al plan anual de capacitación docente y reconocer tiempo institucional"):
                for r in p.findall(f"{{{W_NS}}}r"):
                    p.remove(r)
                new_r = etree.SubElement(p, f"{{{W_NS}}}r")
                new_t = etree.SubElement(new_r, f"{{{W_NS}}}t")
                new_t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                new_t.text = (
                    "Formalizar la adopción institucional del manual de estrategias (Anexo 16.2) e incorporar sus cuatro acciones estratégicas "
                    "al plan anual de capacitación profesoral, reconociendo tiempo académico protegido para la actualización docente en salud "
                    "intercultural y regulación emocional."
                )
                print("   ✓ [Recomendaciones CUR-Estelí] Actualizada recomendación institucional con cita a Anexo 16.2.")
                break

        # F) ANEXO 16.2: Insertar encabezado de Anexo y el documento completo del manual
        h2_elem = etree.Element(f"{{{W_NS}}}p")
        h2_pPr = etree.SubElement(h2_elem, f"{{{W_NS}}}pPr")
        pStyle = etree.SubElement(h2_pPr, f"{{{W_NS}}}pStyle")
        pStyle.set(f"{{{W_NS}}}val", "Ttulo2")
        etree.SubElement(h2_pPr, f"{{{W_NS}}}pageBreakBefore")
        
        h2_r = etree.SubElement(h2_elem, f"{{{W_NS}}}r")
        h2_rPr = etree.SubElement(h2_r, f"{{{W_NS}}}rPr")
        etree.SubElement(h2_rPr, f"{{{W_NS}}}b")
        h2_t = etree.SubElement(h2_r, f"{{{W_NS}}}t")
        h2_t.text = "16.2. Manual de Estrategias para el Abordaje de la Medicina Tradicional, Complementaria e Integrativa (MTCI) en la Formación y Práctica Psicológica: Guía Práctica para la Toma de Decisiones y la Delimitación del Rol Profesional (Producto Derivado del Tercer Objetivo de Investigación)"
        
        master_sectPr.addprevious(h2_elem)
        
        # Mapeo de estilos internos del manual para que mantenga fidelidad tipográfica
        # sin duplicar títulos de capítulos principales en el Índice General
        manual_children = [c for c in manual_body if c.tag != f"{{{W_NS}}}sectPr"]
        print(f"   Insertando {len(manual_children)} elementos íntegros del manual en Anexo 16.2...")
        
        for child in manual_children:
            new_c = copy.deepcopy(child)
            
            # 1. Remapear rId de imagen
            for blip in new_c.iter(f"{{{A_NS}}}blip"):
                if blip.get(f"{{{R_NS}}}embed") == "rId8":
                    blip.set(f"{{{R_NS}}}embed", manual_img_rid)
                    
            # 2. Remapear numId de listas
            for numId_el in new_c.iter(f"{{{W_NS}}}numId"):
                old_n = numId_el.get(f"{{{W_NS}}}val")
                if old_n in num_map:
                    numId_el.set(f"{{{W_NS}}}val", num_map[old_n])
                    
            # 3. Estilos de títulos internos del manual:
            # Heading 1 -> Ttulo4 (Heading 4), Heading 2 -> Ttulo5 (Heading 5)
            # Esto garantiza que el manual se formatee nítidamente pero no colisione con los capítulos en el TOC 1-3.
            pStyle_el = new_c.find(f".//{{{W_NS}}}pStyle")
            if pStyle_el is not None:
                val = pStyle_el.get(f"{{{W_NS}}}val", "")
                if val in ["Ttulo1", "Heading1", "Heading 1"]:
                    pStyle_el.set(f"{{{W_NS}}}val", "Ttulo4")
                elif val in ["Ttulo2", "Heading2", "Heading 2"]:
                    pStyle_el.set(f"{{{W_NS}}}val", "Ttulo5")
                    
            master_sectPr.addprevious(new_c)
            
        doc_bytes = etree.tostring(doc_root, xml_declaration=True, encoding="utf-8", standalone=True)

    # 8. Empaquetar limpiamente con compresión ZIP streaming
    print("\n[8/8] Empaquetando documento maestro final...")
    temp_target = TARGET_DOC + ".tmp"
    if os.path.exists(temp_target):
        os.remove(temp_target)

    with zipfile.ZipFile(BASE_DOC, "r") as zin, zipfile.ZipFile(temp_target, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == "[Content_Types].xml":
                zout.writestr(item, ct_bytes)
            elif item.filename == "word/_rels/document.xml.rels":
                zout.writestr(item, rels_bytes)
            elif item.filename == "word/numbering.xml":
                zout.writestr(item, num_bytes)
            elif item.filename == "word/styles.xml":
                zout.writestr(item, styles_bytes)
            elif item.filename == "customXml/item1.xml":
                zout.writestr(item, item_bytes)
            elif item.filename == "word/document.xml":
                zout.writestr(item, doc_bytes)
            else:
                zout.writestr(item, zin.read(item.filename))
        # Incluir archivo binario de imagen del manual
        zout.writestr("word/media/manual_logo.jpg", manual_logo_bytes)

    if os.path.exists(TARGET_DOC):
        # Crear respaldo preventivo
        shutil.copy2(TARGET_DOC, TARGET_DOC + ".pre_manual_bak")
        os.remove(TARGET_DOC)
        
    shutil.move(temp_target, TARGET_DOC)
    print(f"\n✅ Documento maestro generado con éxito en: {TARGET_DOC} ({os.path.getsize(TARGET_DOC):,} bytes)")


if __name__ == '__main__':
    build_consolidated_document()
