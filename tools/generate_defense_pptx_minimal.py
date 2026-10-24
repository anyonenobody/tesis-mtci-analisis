#!/usr/bin/env python3
"""
tools/generate_defense_pptx_minimal.py
================================================================================
Generador de Presentación de Defensa de Tesis MTCI · UNAN-Managua CUR-Estelí
ESTILO: Ultra-Moderno, Creativo, Minimalista y Libre de Cajas (No-Card Layout)
- Animaciones: Transiciones nativas OpenXML de desvanecimiento suave (p:transition p:fade)
- Cero "cajas" / rectángulos con bordes: Contenido flotante con espacio negativo editorial
- Jerarquía tipográfica refinada: Cambria (Serif editorial) + Calibri / Aptos (Sans limpio)
- Métricas escultóricas en gran formato (36–48pt)
- Separadores lineales de 0.5pt y acentos de color intencionales (Teal, Gold, Navy)
================================================================================
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml import parse_xml

# ==============================================================================
# PALETA DE COLOR MINIMALISTA & EDITORIAL
# ==============================================================================
COLOR_DARK_CANVAS  = RGBColor(8, 14, 26)       # #080E1A Obsidian Midnight (Portada y Cierre)
COLOR_LIGHT_CANVAS = RGBColor(253, 254, 255)   # #FDFEFF Blanco Editorial Luminoso (Láms. 2 a 15)

COLOR_NAVY_TITLE   = RGBColor(15, 23, 42)      # #0F172A Slate 900
COLOR_TEAL_ACCENT  = RGBColor(13, 148, 136)    # #0D9488 Botanical Teal 600
COLOR_GOLD_ACCENT  = RGBColor(217, 119, 6)     # #D97706 Warm Amber 600
COLOR_ALERT_CRIMSON= RGBColor(220, 38, 38)     # #DC2626 Warning Red 600
COLOR_BLUE_ROYAL   = RGBColor(37, 99, 235)     # #2563EB Royal Blue 600

COLOR_TEXT_PRIMARY = RGBColor(30, 41, 59)      # #1E293B Charcoal Slate
COLOR_TEXT_MUTED   = RGBColor(100, 116, 139)   # #64748B Secondary Slate
COLOR_HAIRLINE     = RGBColor(226, 232, 240)   # #E2E8F0 Subtle Hairline Separator
COLOR_WHITE        = RGBColor(255, 255, 255)

FONT_SERIF = "Cambria"
FONT_SANS  = "Calibri"

LOGO_CLEAN_PATH   = "assets/extracted/unan_logo_clean.png"
SHIELD_PATH       = "assets/extracted/unan_shield_only.png"
MANUAL_COVER_PATH = "assets/extracted/portada_manual.jpg"
FIG_03_PATH       = "assets/figuras_apa7/figura_03_demografia_estudiantes.png"
FIG_07_PATH       = "assets/figuras_apa7/figura_07_frecuencia_uso_estudiantes.png"

def add_native_transition(slide):
    """Inyecta transición nativa de desvanecimiento suave (Smooth Fade) en el OpenXML de la diapositiva."""
    trans_xml = (
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
        'spd="med" advClick="1"><p:fade/></p:transition>'
    )
    slide._element.append(parse_xml(trans_xml))

def create_presentation():
    prs = Presentation()
    prs.slide_width  = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout     = prs.slide_layouts[6]

    def set_slide_bg(slide, color):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_minimal_header(slide, category_text, title_text):
        """Header minimalista sin líneas de acento bajo el título, con espaciado generoso."""
        eb_box = slide.shapes.add_textbox(Inches(0.85), Inches(0.48), Inches(10.5), Inches(0.3))
        tf_eb = eb_box.text_frame
        tf_eb.word_wrap = True
        tf_eb.margin_left = tf_eb.margin_right = tf_eb.margin_top = tf_eb.margin_bottom = 0
        p_eb = tf_eb.paragraphs[0]
        p_eb.text = category_text.upper()
        p_eb.font.name = FONT_SANS
        p_eb.font.size = Pt(10)
        p_eb.font.bold = True
        p_eb.font.color.rgb = COLOR_TEAL_ACCENT

        t_box = slide.shapes.add_textbox(Inches(0.85), Inches(0.78), Inches(10.8), Inches(0.75))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = FONT_SERIF
        p_t.font.size = Pt(28)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY_TITLE

        if os.path.exists(SHIELD_PATH):
            slide.shapes.add_picture(SHIELD_PATH, Inches(12.0), Inches(0.45), height=Inches(0.85))

    def add_minimal_footer(slide, current_num, total_slides=16):
        """Pie de página minimalista flotante sin bordes pesados."""
        f_box = slide.shapes.add_textbox(Inches(0.85), Inches(7.08), Inches(10.5), Inches(0.25))
        tf = f_box.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "UNAN-Managua • CUR-Estelí | Carrera de Psicología • Segundo Semestre 2026"
        p.font.name = FONT_SANS
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MUTED

        n_box = slide.shapes.add_textbox(Inches(11.8), Inches(7.08), Inches(0.7), Inches(0.25))
        tf_n = n_box.text_frame
        tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
        pn = tf_n.paragraphs[0]
        pn.alignment = PP_ALIGN.RIGHT
        pn.text = f"{current_num} / {total_slides}"
        pn.font.name = FONT_SANS
        pn.font.size = Pt(9)
        pn.font.bold = True
        pn.font.color.rgb = COLOR_TEXT_MUTED

    def add_hairline_h(slide, left, top, width, color=COLOR_HAIRLINE):
        """Añade una línea divisoria ultra-fina (0.75pt)."""
        line = slide.shapes.add_shape(1, left, top, width, Pt(1))
        line.fill.background()
        line.line.color.rgb = color
        line.line.width = Pt(0.75)
        return line

    def add_hairline_v(slide, left, top, height, color=COLOR_HAIRLINE):
        """Añade una línea vertical ultra-fina (0.75pt)."""
        line = slide.shapes.add_shape(1, left, top, Pt(1), height)
        line.fill.background()
        line.line.color.rgb = color
        line.line.width = Pt(0.75)
        return line

    # ==========================================================================
    # SLIDE 1: PORTADA INSTITUCIONAL (Dark Minimalist Executive)
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, COLOR_DARK_CANVAS)
    add_native_transition(s1)

    if os.path.exists(LOGO_CLEAN_PATH):
        s1.shapes.add_picture(LOGO_CLEAN_PATH, Inches(0.9), Inches(0.8), height=Inches(1.05))

    univ_box = s1.shapes.add_textbox(Inches(3.1), Inches(0.85), Inches(9.3), Inches(0.95))
    tf_u = univ_box.text_frame
    tf_u.word_wrap = True
    tf_u.margin_left = tf_u.margin_right = tf_u.margin_top = tf_u.margin_bottom = 0
    pu1 = tf_u.paragraphs[0]
    pu1.text = "UNIVERSIDAD NACIONAL AUTÓNOMA DE NICARAGUA, MANAGUA"
    pu1.font.name = FONT_SANS
    pu1.font.size = Pt(14)
    pu1.font.bold = True
    pu1.font.color.rgb = COLOR_WHITE
    pu2 = tf_u.add_paragraph()
    pu2.text = "CENTRO UNIVERSITARIO REGIONAL DE ESTELÍ • RECINTO LEONEL RUGAMA RUGAMA"
    pu2.font.name = FONT_SANS
    pu2.font.size = Pt(10.5)
    pu2.font.bold = True
    pu2.font.color.rgb = RGBColor(245, 158, 11)  # Warm Gold
    pu3 = tf_u.add_paragraph()
    pu3.text = "Departamento de Educación y Humanidades | Carrera de Psicología"
    pu3.font.name = FONT_SANS
    pu3.font.size = Pt(9.5)
    pu3.font.color.rgb = RGBColor(148, 163, 184)

    # Hairline divider
    add_hairline_h(s1, Inches(0.9), Inches(2.15), Inches(11.5), RGBColor(30, 41, 59))

    # Eyebrow & Title
    t_box1 = s1.shapes.add_textbox(Inches(0.9), Inches(2.45), Inches(11.5), Inches(2.4))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
    p_sub = tf1.paragraphs[0]
    p_sub.text = "TRABAJO DE INVESTIGACIÓN PARA OPTAR AL GRADO DE LICENCIADOS EN PSICOLOGÍA"
    p_sub.font.name = FONT_SANS
    p_sub.font.size = Pt(11)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(20, 184, 166)  # Ethereal Teal
    p_sub.space_after = Pt(12)

    p_t = tf1.add_paragraph()
    p_t.text = "La Medicina Tradicional, Complementaria e Integrativa\n(MTCI) como Complemento en la Atención Psicológica"
    p_t.font.name = FONT_SERIF
    p_t.font.size = Pt(32)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE
    p_t.space_after = Pt(14)

    p_baj = tf1.add_paragraph()
    p_baj.text = "Estudio Mixto con Estudiantes y Docentes del CUR-Estelí y Facilitadores Locales del Municipio de Estelí"
    p_baj.font.name = FONT_SANS
    p_baj.font.size = Pt(13.5)
    p_baj.font.color.rgb = RGBColor(226, 232, 240)

    # Hairline divider
    add_hairline_h(s1, Inches(0.9), Inches(5.1), Inches(11.5), RGBColor(30, 41, 59))

    # Floating metadata (NO BOXES, separated by subtle vertical hairlines)
    col_w = Inches(3.6)
    c1_box = s1.shapes.add_textbox(Inches(0.9), Inches(5.35), col_w, Inches(1.6))
    tf_c1 = c1_box.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = tf_c1.margin_bottom = 0
    p1 = tf_c1.paragraphs[0]
    p1.text = "AUTORES / SUSTENTANTES"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(245, 158, 11)
    p1.space_after = Pt(6)
    for name in ["• Dina Fabiola García Torres", "• Tatiana Paola López Ramos", "• Engel Enoc Zamora Velásquez"]:
        pn = tf_c1.add_paragraph()
        pn.text = name
        pn.font.name = FONT_SANS
        pn.font.size = Pt(11)
        pn.font.color.rgb = COLOR_WHITE
        pn.space_after = Pt(3)

    add_hairline_v(s1, Inches(4.75), Inches(5.35), Inches(1.5), RGBColor(30, 41, 59))

    c2_box = s1.shapes.add_textbox(Inches(5.05), Inches(5.35), col_w, Inches(1.6))
    tf_c2 = c2_box.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = tf_c2.margin_bottom = 0
    p2 = tf_c2.paragraphs[0]
    p2.text = "TUTORÍA ACADÉMICA"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(20, 184, 166)
    p2.space_after = Pt(6)
    p_tut = tf_c2.add_paragraph()
    p_tut.text = "• Dra. Tania Libertad Pérez Guevara"
    p_tut.font.name = FONT_SANS
    p_tut.font.size = Pt(11)
    p_tut.font.bold = True
    p_tut.font.color.rgb = COLOR_WHITE
    p_tut_r = tf_c2.add_paragraph()
    p_tut_r.text = "Docente Investigadora • Asesoría Temática y Metodológica\nCUR-Estelí, UNAN-Managua"
    p_tut_r.font.name = FONT_SANS
    p_tut_r.font.size = Pt(10)
    p_tut_r.font.color.rgb = RGBColor(148, 163, 184)

    add_hairline_v(s1, Inches(8.9), Inches(5.35), Inches(1.5), RGBColor(30, 41, 59))

    c3_box = s1.shapes.add_textbox(Inches(9.2), Inches(5.35), col_w, Inches(1.6))
    tf_c3 = c3_box.text_frame
    tf_c3.word_wrap = True
    tf_c3.margin_left = tf_c3.margin_right = tf_c3.margin_top = tf_c3.margin_bottom = 0
    p3 = tf_c3.paragraphs[0]
    p3.text = "DEFENSA DE GRADO"
    p3.font.name = FONT_SANS
    p3.font.size = Pt(9.5)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(226, 232, 240)
    p3.space_after = Pt(6)
    p_deg = tf_c3.add_paragraph()
    p_deg.text = "Licenciatura en Psicología"
    p_deg.font.name = FONT_SANS
    p_deg.font.size = Pt(11)
    p_deg.font.color.rgb = COLOR_WHITE
    p_lin = tf_c3.add_paragraph()
    p_lin.text = "Línea SAL-3 (Salud e Interculturalidad)\nEstelí, Nicaragua • Octubre, 2026"
    p_lin.font.name = FONT_SANS
    p_lin.font.size = Pt(10)
    p_lin.font.color.rgb = RGBColor(148, 163, 184)

    # ==========================================================================
    # SLIDE 2: PLANTEAMIENTO Y JUSTIFICACIÓN (Minimalist Editorial, No Boxes)
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, COLOR_LIGHT_CANVAS)
    add_minimal_header(s2, "Capítulo I • Planteamiento del Problema", "Encrucijada Asistencial, Vacío Formativo y Pertinencia Social")
    add_minimal_footer(s2, 2)
    add_native_transition(s2)

    # Column 1 (Left): Problema
    col_w2 = Inches(5.5)
    p_box = s2.shapes.add_textbox(Inches(0.85), Inches(1.75), col_w2, Inches(5.0))
    tf_p = p_box.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0

    p_p_title = tf_p.paragraphs[0]
    p_p_title.text = "El Conflicto Estructural en Salud Mental"
    p_p_title.font.name = FONT_SERIF
    p_p_title.font.size = Pt(15)
    p_p_title.font.bold = True
    p_p_title.font.color.rgb = COLOR_NAVY_TITLE
    p_p_title.space_after = Pt(14)

    points_p = [
        ("01", "Asimetría Normativa", "La Ley No. 774 garantiza el derecho y acceso ciudadano a las MTCI, pero la Ley No. 292 prohíbe taxativamente al psicólogo formular cualquier fármaco o sustancia."),
        ("02", "Ocultamiento Terapéutico", "Los consultantes recurren activamente a terapias tradicionales pero las silencian en sesión clínica por temor al reproche, burla o escepticismo del terapeuta."),
        ("03", "Vacío Curricular Crítico", "El estudiantado egresa sin lineamientos bioéticos para entablar un diálogo seguro, identificar interacciones adversas o realizar derivaciones oportunas.")
    ]
    for num, heading, body in points_p:
        p_n = tf_p.add_paragraph()
        r_num = p_n.add_run()
        r_num.text = f"{num}  "
        r_num.font.name = FONT_SERIF
        r_num.font.bold = True
        r_num.font.size = Pt(13)
        r_num.font.color.rgb = COLOR_TEAL_ACCENT

        r_h = p_n.add_run()
        r_h.text = f"{heading}: "
        r_h.font.name = FONT_SANS
        r_h.font.bold = True
        r_h.font.size = Pt(12)
        r_h.font.color.rgb = COLOR_NAVY_TITLE

        r_b = p_n.add_run()
        r_b.text = body
        r_b.font.name = FONT_SANS
        r_b.font.size = Pt(11.5)
        r_b.font.color.rgb = COLOR_TEXT_PRIMARY
        p_n.space_after = Pt(12)

    # Pregunta de Investigación al pie de Col 1
    p_q = tf_p.add_paragraph()
    r_ql = p_q.add_run()
    r_ql.text = "✦ Pregunta Central: "
    r_ql.font.bold = True
    r_ql.font.color.rgb = COLOR_GOLD_ACCENT
    r_qt = p_q.add_run()
    r_qt.text = "¿Cómo fundamenta el diagnóstico de MTCI en Estelí el diseño de un manual ético y pedagógico para Psicología?"
    r_qt.font.italic = True
    r_qt.font.color.rgb = COLOR_NAVY_TITLE

    # Subtle vertical hairline between columns
    add_hairline_v(s2, Inches(6.75), Inches(1.85), Inches(4.7), COLOR_HAIRLINE)

    # Column 2 (Right): Justificación
    j_box = s2.shapes.add_textbox(Inches(7.15), Inches(1.75), col_w2, Inches(5.0))
    tf_j = j_box.text_frame
    tf_j.word_wrap = True
    tf_j.margin_left = tf_j.margin_right = tf_j.margin_top = tf_j.margin_bottom = 0

    p_j_title = tf_j.paragraphs[0]
    p_j_title.text = "Justificación y Relevancia Social"
    p_j_title.font.name = FONT_SERIF
    p_j_title.font.size = Pt(15)
    p_j_title.font.bold = True
    p_j_title.font.color.rgb = COLOR_NAVY_TITLE
    p_j_title.space_after = Pt(14)

    points_j = [
        ("✦", "Ética y No Maleficencia", "Explorar el uso de hierbas y remedios tradicionales previene intoxicaciones o interacciones fitofarmacológicas con psicofármacos prescritos."),
        ("✦", "Salud Mental Comunitaria", "Reconoce y articula la memoria etnobotánica viva del norte segoviano y dignifica la labor de los facilitadores tradicionales de Estelí."),
        ("✦", "Impacto Formativo Directo", "Dota a los estudiantes de 4.º y 5.º año de criterios de discernimiento para su práctica en la Clínica Psicosocial del CUR-Estelí."),
        ("✦", "Aporte Propositivo Concreto", "Entrega formalmente un Manual de Estrategias MTCI de 18 páginas (Anexo 16.2) validado como herramienta bioética y pedagógica institucional.")
    ]
    for bullet, heading, body in points_j:
        pj = tf_j.add_paragraph()
        rb = pj.add_run()
        rb.text = f"{bullet} "
        rb.font.bold = True
        rb.font.color.rgb = COLOR_TEAL_ACCENT
        rb.font.size = Pt(12)

        rh = pj.add_run()
        rh.text = f"{heading}: "
        rh.font.name = FONT_SANS
        rh.font.bold = True
        rh.font.size = Pt(12)
        rh.font.color.rgb = COLOR_NAVY_TITLE

        rt = pj.add_run()
        rt.text = body
        rt.font.name = FONT_SANS
        rt.font.size = Pt(11.5)
        rt.font.color.rgb = COLOR_TEXT_PRIMARY
        pj.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 3: ANTECEDENTES (Timeline Horizontal Minimalista, No Boxes)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, COLOR_LIGHT_CANVAS)
    add_minimal_header(s3, "Capítulo I • Estado del Arte", "Trayectoria de la Evidencia Internacional, Regional y Local")
    add_minimal_footer(s3, 3)
    add_native_transition(s3)

    # Horizontal connecting hairline
    add_hairline_h(s3, Inches(0.85), Inches(2.2), Inches(11.6), COLOR_TEAL_ACCENT)

    antecedentes = [
        ("2014 – 2019", "ÁMBITO GLOBAL", "OMS y Salud Integrativa", [
            ("Estrategia OMS sobre MTCI", "Marco global que insta a los sistemas de salud a integrar medicinas tradicionales con base en evidencia."),
            ("Metanálisis de Acupuntura y Fitoterapia", "Furlan et al. (2012) y Guo et al. (2024) comprueban eficacia en dolor crónico, fibromialgia y estrés somático."),
            ("Salud Mental Global", "Sotiropoulos et al. (2025) validan técnicas mente-cuerpo en comorbilidades afectivas.")
        ]),
        ("2020 – 2023", "ÁMBITO REGIONAL", "Iberoamérica y la Paradoja", [
            ("Estudios en Educación Superior", "Investigaciones en Argentina (Papalini, 2022) y Chile evidencian uso masivo de MTCI en universitarios."),
            ("Paradoja Formativa Identificada", "Más del 80% del alumnado en carreras de salud recurre a MTCI pero reporta cero instrucción universitaria."),
            ("Falta de Protocolos", "Ausencia de guías clínicas de derivación entre psicólogos y terapeutas complementarios.")
        ]),
        ("2024 – 2026", "ÁMBITO LOCAL", "Nicaragua y Vacío Curricular", [
            ("Marco Jurídico de Vanguardia", "Leyes 774 y 759 establecen el Instituto de Medicina Natural, pionero en Centroamérica."),
            ("Vacío en Facultades de Psicología", "Cero asignaturas electivas o transversales sobre diálogo intercultural en salud mental."),
            ("Estudio CUR-Estelí (2026)", "Primera investigación empírica mixta que articula estudiantes, claustro docente y facilitadores territoriales.")
        ])
    ]

    col_w3 = Inches(3.65)
    for i, (period, scope, subtitle, items) in enumerate(antecedentes):
        left_pos = Inches(0.85 + i * 4.0)

        # Milestone dot & year
        dot_box = s3.shapes.add_textbox(left_pos, Inches(1.75), col_w3, Inches(0.8))
        tf_d = dot_box.text_frame
        tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
        pd = tf_d.paragraphs[0]
        pd.text = f"●  {period}"
        pd.font.name = FONT_SERIF
        pd.font.bold = True
        pd.font.size = Pt(13)
        pd.font.color.rgb = COLOR_TEAL_ACCENT

        pd_sc = tf_d.add_paragraph()
        pd_sc.text = f"{scope} • {subtitle}"
        pd_sc.font.name = FONT_SANS
        pd_sc.font.bold = True
        pd_sc.font.size = Pt(11)
        pd_sc.font.color.rgb = COLOR_NAVY_TITLE

        # Content column
        c_box = s3.shapes.add_textbox(left_pos, Inches(2.65), col_w3, Inches(4.2))
        tf_c = c_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

        for title, desc in items:
            p_it = tf_c.add_paragraph() if tf_c.paragraphs[0].text else tf_c.paragraphs[0]
            rt = p_it.add_run()
            rt.text = f"• {title}: "
            rt.font.name = FONT_SANS
            rt.font.bold = True
            rt.font.size = Pt(11.5)
            rt.font.color.rgb = COLOR_NAVY_TITLE

            rd = p_it.add_run()
            rd.text = desc
            rd.font.name = FONT_SANS
            rd.font.size = Pt(11)
            rd.font.color.rgb = COLOR_TEXT_PRIMARY
            p_it.space_after = Pt(10)

    # ==========================================================================
    # SLIDE 4: CONTEXTO DEL ESTUDIO (Territorio e Institución)
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, COLOR_LIGHT_CANVAS)
    add_minimal_header(s4, "Capítulo I • Contextualización Situacional", "El Escenario de Investigación: CUR-Estelí y el Territorio Segoviano")
    add_minimal_footer(s4, 4)
    add_native_transition(s4)

    # Col 1: Contexto Territorial y Comunitario
    ctx_w = Inches(5.6)
    box_s4_1 = s4.shapes.add_textbox(Inches(0.85), Inches(1.8), ctx_w, Inches(5.0))
    tf_s4_1 = box_s4_1.text_frame
    tf_s4_1.word_wrap = True
    tf_s4_1.margin_left = tf_s4_1.margin_right = tf_s4_1.margin_top = tf_s4_1.margin_bottom = 0

    p_t1 = tf_s4_1.paragraphs[0]
    p_t1.text = "Municipio de Estelí: Matriz Sociocultural y Saberes Vivos"
    p_t1.font.name = FONT_SERIF
    p_t1.font.bold = True
    p_t1.font.size = Pt(15)
    p_t1.font.color.rgb = COLOR_NAVY_TITLE
    p_t1.space_after = Pt(12)

    pts_ctx1 = [
        ("Memoria Etnobotánica del Norte", "Estelí y la región de Las Segovias conservan una arraigada tradición de uso de plantas medicinales, sobandería y medicina popular transmitida intergeneracionalmente."),
        ("Red Comunitaria de Facilitadores", "Sobadores, naturópatas y curanderos tradicionales constituyen el primer escalón asistencial para dolencias músculo-esqueléticas y malestares emocionales (nervios, aflicción)."),
        ("Barreras de Articulación Sanitaria", "Persiste una desarticulación burocrática y asistencial entre los terapeutas comunitarios y los centros de salud formales, generando estigma y derivaciones tardías.")
    ]
    for h, d in pts_ctx1:
        p = tf_s4_1.add_paragraph()
        rh = p.add_run()
        rh.text = f"✦ {h}\n"
        rh.font.name = FONT_SANS
        rh.font.bold = True
        rh.font.size = Pt(12)
        rh.font.color.rgb = COLOR_TEAL_ACCENT
        rd = p.add_run()
        rd.text = d
        rd.font.name = FONT_SANS
        rd.font.size = Pt(11.5)
        rd.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(12)

    add_hairline_v(s4, Inches(6.75), Inches(1.9), Inches(4.7), COLOR_HAIRLINE)

    # Col 2: Contexto Académico UNAN-Managua CUR-Estelí
    box_s4_2 = s4.shapes.add_textbox(Inches(7.15), Inches(1.8), ctx_w, Inches(5.0))
    tf_s4_2 = box_s4_2.text_frame
    tf_s4_2.word_wrap = True
    tf_s4_2.margin_left = tf_s4_2.margin_right = tf_s4_2.margin_top = tf_s4_2.margin_bottom = 0

    p_t2 = tf_s4_2.paragraphs[0]
    p_t2.text = "UNAN-Managua CUR-Estelí: Clínica y Formación"
    p_t2.font.name = FONT_SERIF
    p_t2.font.bold = True
    p_t2.font.size = Pt(15)
    p_t2.font.color.rgb = COLOR_NAVY_TITLE
    p_t2.space_after = Pt(12)

    pts_ctx2 = [
        ("Recinto Leonel Rugama Rugama", "Sede de formación universitaria de la Carrera de Psicología, formando profesionales orientados al desarrollo psicosocial y comunitario del norte del país."),
        ("Clínica Psicosocial del CUR-Estelí", "Espacio asistencial y docente donde los estudiantes de 4.º y 5.º año brindan atención supervisada a usuarios con problemas de salud mental y estrés adaptativo."),
        ("Oportunidad de Liderazgo Institucional", "La investigación ofrece al CUR-Estelí la oportunidad pionera de implementar el primer protocolo universitario formal de abordaje ético de las MTCI en psicología.")
    ]
    for h, d in pts_ctx2:
        p = tf_s4_2.add_paragraph()
        rh = p.add_run()
        rh.text = f"✦ {h}\n"
        rh.font.name = FONT_SANS
        rh.font.bold = True
        rh.font.size = Pt(12)
        rh.font.color.rgb = COLOR_GOLD_ACCENT
        rd = p.add_run()
        rd.text = d
        rd.font.name = FONT_SANS
        rd.font.size = Pt(11.5)
        rd.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 5: OBJETIVOS DE LA INVESTIGACIÓN (Esquema Jerárquico Flotante)
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, COLOR_LIGHT_CANVAS)
    add_minimal_header(s5, "Capítulo I • Propósito Investigativo", "Objetivos de la Investigación: Del Diagnóstico a la Propuesta")
    add_minimal_footer(s5, 5)
    add_native_transition(s5)

    # Objetivo General en banda superior minimalista
    og_box = s5.shapes.add_textbox(Inches(0.85), Inches(1.75), Inches(11.6), Inches(1.3))
    tf_og = og_box.text_frame
    tf_og.word_wrap = True
    tf_og.margin_left = tf_og.margin_right = tf_og.margin_top = tf_og.margin_bottom = 0
    p_og_lbl = tf_og.paragraphs[0]
    p_og_lbl.text = "OBJETIVO GENERAL"
    p_og_lbl.font.name = FONT_SANS
    p_og_lbl.font.bold = True
    p_og_lbl.font.size = Pt(11)
    p_og_lbl.font.color.rgb = COLOR_GOLD_ACCENT
    p_og_lbl.space_after = Pt(4)

    p_og = tf_og.add_paragraph()
    p_og.text = "Analizar la integración de la Medicina Tradicional, Complementaria e Integrativa (MTCI) como recurso complementario en la atención psicológica, a partir de las percepciones, conocimientos y prácticas de estudiantes, docentes y facilitadores locales, formulando un manual de estrategias bioéticas y formativas en el CUR-Estelí."
    p_og.font.name = FONT_SERIF
    p_og.font.bold = True
    p_og.font.size = Pt(15.5)
    p_og.font.color.rgb = COLOR_NAVY_TITLE

    add_hairline_h(s5, Inches(0.85), Inches(3.25), Inches(11.6), COLOR_HAIRLINE)

    # 3 Objetivos Específicos en 3 columnas flotantes
    col_w5 = Inches(3.6)
    oes = [
        ("OE1 • DIAGNÓSTICO ESTUDIANTIL", COLOR_TEAL_ACCENT, "Caracterizar la percepción, nivel de conocimiento, frecuencia de uso y barreras autopercibidas en los estudiantes de 4.º y 5.º año de la Carrera de Psicología respecto a las MTCI."),
        ("OE2 • SABERES DE FACILITADORES", COLOR_BLUE_ROYAL, "Explorar las experiencias terapéuticas, prácticas tradicionales y barreras socioculturales que enfrentan los facilitadores locales de medicina tradicional en el municipio de Estelí."),
        ("OE3 • PROPUESTA DEL MANUAL", COLOR_GOLD_ACCENT, "Diseñar un Manual de Estrategias de MTCI para la formación y práctica psicológica, articulando pautas bioéticas, algoritmos de derivación y contenidos curriculares para el CUR-Estelí.")
    ]

    for i, (title, color, desc) in enumerate(oes):
        left_pos = Inches(0.85 + i * 4.05)
        oe_box = s5.shapes.add_textbox(left_pos, Inches(3.55), col_w5, Inches(3.2))
        tf_oe = oe_box.text_frame
        tf_oe.word_wrap = True
        tf_oe.margin_left = tf_oe.margin_right = tf_oe.margin_top = tf_oe.margin_bottom = 0

        p_num = tf_oe.paragraphs[0]
        p_num.text = f"0{i+1}"
        p_num.font.name = FONT_SERIF
        p_num.font.bold = True
        p_num.font.size = Pt(36)
        p_num.font.color.rgb = color
        p_num.space_after = Pt(2)

        p_t = tf_oe.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_SANS
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = COLOR_NAVY_TITLE
        p_t.space_after = Pt(8)

        p_d = tf_oe.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_SANS
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = COLOR_TEXT_PRIMARY

    # ==========================================================================
    # SLIDE 6: MARCO TEÓRICO 1 (Epistemología y Bioética, No Boxes)
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, COLOR_LIGHT_CANVAS)
    add_minimal_header(s6, "Capítulo II • Fundamentos Teóricos (1/2)", "Epistemología Médica, Pluralismo Asistencial y Principios Bioéticos")
    add_minimal_footer(s6, 6)
    add_native_transition(s6)

    col_w6 = Inches(3.65)
    pillars = [
        ("01", "Modelo Biopsicosocial Ampliado", "Engel (1977); Babic et al. (2024)", [
            "Superación del reduccionismo mecanicista biomédico.",
            "Reconocimiento de la mente, cuerpo y entorno cultural como unidad dinámica indisoluble.",
            "Regulación somato-autonómica (teoría polivagal y eje cerebro-intestino) como base del autocuidado."
        ]),
        ("02", "Pluralismo Médico y Coexistencia", "Menéndez (2020); OMS (2025)", [
            "Coexistencia de saberes: Modelo Médico Hegemónico vs Prácticas Tradicionales y de Autoatención.",
            "Desjerarquización de saberes sin pérdida del juicio científico riguroso.",
            "Erradicación del ocultamiento terapéutico mediante la escucha clínica desprejuiciada."
        ]),
        ("03", "Bioética y Delimitación Profesional", "Beauchamp & Childress (2019); Ley 292", [
            "Principio de No Maleficencia: prevención de interacciones adversas por fitoterapia o suplementos.",
            "Principio de Autonomía: respeto irrestricto a los valores y decisiones culturales del consultante.",
            "Límites de Rol: el psicólogo NO prescribe ni sustituye la medicina; dialoga y deriva éticamente."
        ])
    ]

    for i, (num, title, author, items) in enumerate(pillars):
        left_pos = Inches(0.85 + i * 4.05)
        box = s6.shapes.add_textbox(left_pos, Inches(1.85), col_w6, Inches(4.9))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_n = tf.paragraphs[0]
        p_n.text = f"{num} • {title}"
        p_n.font.name = FONT_SERIF
        p_n.font.bold = True
        p_n.font.size = Pt(14)
        p_n.font.color.rgb = COLOR_NAVY_TITLE
        p_n.space_after = Pt(2)

        p_a = tf.add_paragraph()
        p_a.text = author
        p_a.font.name = FONT_SANS
        p_a.font.size = Pt(10)
        p_a.font.bold = True
        p_a.font.color.rgb = COLOR_TEAL_ACCENT
        p_a.space_after = Pt(12)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"•  {it}"
            p_it.font.name = FONT_SANS
            p_it.font.size = Pt(11.5)
            p_it.font.color.rgb = COLOR_TEXT_PRIMARY
            p_it.space_after = Pt(8)

    # ==========================================================================
    # SLIDE 7: MARCO TEÓRICO 2 (Marco Jurídico y Evidencia Clínica)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, COLOR_LIGHT_CANVAS)
    add_minimal_header(s7, "Capítulo II • Fundamentos Teóricos (2/2)", "Marco Jurídico Nicaragüense y Evidencia de Eficacia Clínica")
    add_minimal_footer(s7, 7)
    add_native_transition(s7)

    col_w7 = Inches(5.6)
    # Left: Marco Jurídico
    b_l = s7.shapes.add_textbox(Inches(0.85), Inches(1.8), col_w7, Inches(5.0))
    tf_l = b_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p_lt = tf_l.paragraphs[0]
    p_lt.text = "Marco Normativo Nacional (Nicaragua)"
    p_lt.font.name = FONT_SERIF
    p_lt.font.bold = True
    p_lt.font.size = Pt(15)
    p_lt.font.color.rgb = COLOR_NAVY_TITLE
    p_lt.space_after = Pt(12)

    leyes = [
        ("Ley No. 774 (2012)", "Medicina Natural, Terapias Complementarias y Productos Naturales", "Reconoce el derecho a la MTCI en el sistema de salud, promoviendo su articulación respetuosa."),
        ("Ley No. 292 (1998)", "Ley de Medicamentos y Farmacias de Nicaragua", "Límite legal taxativo: prohíbe formular o despachar psicofármacos o sustancias a quienes no posean título de médico."),
        ("Ley No. 759 (2011)", "Medicina Tradicional Ancestral", "Protege los saberes ancestrales y la propiedad intelectual de pueblos originarios y afrodescendientes.")
    ]
    for ley, sub, desc in leyes:
        p = tf_l.add_paragraph()
        r1 = p.add_run()
        r1.text = f"⚖ {ley} — "
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_TEAL_ACCENT
        r2 = p.add_run()
        r2.text = f"{sub}\n"
        r2.font.name = FONT_SANS
        r2.font.bold = True
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_NAVY_TITLE
        r3 = p.add_run()
        r3.text = desc
        r3.font.name = FONT_SANS
        r3.font.size = Pt(11)
        r3.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(12)

    add_hairline_v(s7, Inches(6.75), Inches(1.9), Inches(4.7), COLOR_HAIRLINE)

    # Right: Evidencia Clínica
    b_r = s7.shapes.add_textbox(Inches(7.15), Inches(1.8), col_w7, Inches(5.0))
    tf_r = b_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    p_rt = tf_r.paragraphs[0]
    p_rt.text = "Evidencia Clínica y Eficacia Empírica"
    p_rt.font.name = FONT_SERIF
    p_rt.font.bold = True
    p_rt.font.size = Pt(15)
    p_rt.font.color.rgb = COLOR_NAVY_TITLE
    p_rt.space_after = Pt(12)

    evidencias = [
        ("Fitoterapia con Respaldo Científico", "Manzanilla (Matricaria chamomilla) y Pasiflora con efecto gabaérgico comprobado en ansiedad leve a moderada."),
        ("Técnicas Mente-Cuerpo y Regulación Vagal", "Respiración diafragmática, mindfulness y yoga inducen activación parasimpática y reducción de cortisol."),
        ("Terapias Manuales y Alivio Psicosomático", "Masoterapia y reflexología desarticulan corazas musculares y contracturas por estrés sostenido.")
    ]
    for t, d in evidencias:
        p = tf_r.add_paragraph()
        r1 = p.add_run()
        r1.text = f"✦ {t}\n"
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_BLUE_ROYAL
        r2 = p.add_run()
        r2.text = d
        r2.font.name = FONT_SANS
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 8: DISEÑO METODOLÓGICO 1 (Enfoque, Paradigma y Fases)
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, COLOR_LIGHT_CANVAS)
    add_minimal_header(s8, "Capítulo III • Diseño Metodológico (1/2)", "Paradigma Pragmático, Enfoque Mixto Secuencial y Fases del Estudio")
    add_minimal_footer(s8, 8)
    add_native_transition(s8)

    # 4 Metodología Dimensiones
    dim_w = Inches(2.7)
    dims = [
        ("PARADIGMA", "Pragmático", "Articula métodos cuantitativos y cualitativos según su utilidad empírica y propositiva para resolver problemas reales."),
        ("ENFOQUE", "Mixto Secuencial", "Diseño DEXPLIS (Derivativo): recolección cuantitativa inicial seguida de exploración cualitativa en profundidad."),
        ("ALCANCE", "Descriptivo-Transversal", "Mide el estado actual de conocimientos, actitudes y prácticas en un momento temporal definido (2026)."),
        ("TÉCNICAS", "Multi-Instrumento", "Encuesta estructurada (Likert), entrevistas semiestructuradas a profundidad y grupos focales.")
    ]
    for i, (tag, val, desc) in enumerate(dims):
        left_pos = Inches(0.85 + i * 2.95)
        d_box = s8.shapes.add_textbox(left_pos, Inches(1.8), dim_w, Inches(2.2))
        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0

        p_tag = tf_d.paragraphs[0]
        p_tag.text = tag
        p_tag.font.name = FONT_SANS
        p_tag.font.bold = True
        p_tag.font.size = Pt(9.5)
        p_tag.font.color.rgb = COLOR_TEAL_ACCENT
        p_tag.space_after = Pt(2)

        p_val = tf_d.add_paragraph()
        p_val.text = val
        p_val.font.name = FONT_SERIF
        p_val.font.bold = True
        p_val.font.size = Pt(14)
        p_val.font.color.rgb = COLOR_NAVY_TITLE
        p_val.space_after = Pt(6)

        p_desc = tf_d.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_SANS
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = COLOR_TEXT_PRIMARY

    add_hairline_h(s8, Inches(0.85), Inches(4.3), Inches(11.6), COLOR_HAIRLINE)

    # Fases del Estudio
    f_box = s8.shapes.add_textbox(Inches(0.85), Inches(4.55), Inches(11.6), Inches(2.3))
    tf_f = f_box.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0

    p_ft = tf_f.paragraphs[0]
    p_ft.text = "Fases Metodológicas de la Investigación"
    p_ft.font.name = FONT_SERIF
    p_ft.font.bold = True
    p_ft.font.size = Pt(14)
    p_ft.font.color.rgb = COLOR_NAVY_TITLE
    p_ft.space_after = Pt(10)

    fases = [
        ("Fase 1 (Cuantitativa)", "Censo y Encuesta", "Aplicación de cuestionario estandarizado a n=68 estudiantes de 4.º y 5.º año de Psicología."),
        ("Fase 2 (Cualitativa)", "Entrevistas en Profundidad", "Inmersión territorial con n=9 facilitadores locales y entrevistas focales a n=9 docentes del CUR-Estelí."),
        ("Fase 3 (Propositiva)", "Construcción del Manual", "Triangulación de hallazgos empíricos y formulación modular del Manual de Estrategias MTCI (Anexo 16.2).")
    ]
    for f_nom, f_sub, f_det in fases:
        p = tf_f.add_paragraph()
        r1 = p.add_run()
        r1.text = f"▶ {f_nom} • {f_sub}: "
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_GOLD_ACCENT
        r2 = p.add_run()
        r2.text = f_det
        r2.font.name = FONT_SANS
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(6)

    # ==========================================================================
    # SLIDE 9: DISEÑO METODOLÓGICO 2 (Población, Muestra y Criterios)
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, COLOR_LIGHT_CANVAS)
    add_minimal_header(s9, "Capítulo III • Diseño Metodológico (2/2)", "Delimitación Muestral Consolidada (N = 86) y Criterios de Selección")
    add_minimal_footer(s9, 9)
    add_native_transition(s9)

    # 3 Grupos Muestrales Flotantes
    col_w9 = Inches(3.65)
    grupos = [
        ("ESTUDIANTES", "n = 68", COLOR_TEAL_ACCENT, [
            ("Muestra Censal", "Totalidad de estudiantes activos en 4.º año (n=53, 77.9%) y 5.º año (n=15, 22.1%)."),
            ("Criterio Inclusión", "Matrícula activa en el II Semestre 2026; cursando o habiendo cursado prácticas clínicas."),
            ("Criterio Exclusión", "Estudiantes de 1.º a 3.er año o con baja académica temporal.")
        ]),
        ("FACILITADORES", "n = 9", COLOR_GOLD_ACCENT, [
            ("Muestreo Intencional", "Diversidad de saberes: sobadores, naturópatas, terapeutas florales y curanderos de Estelí."),
            ("Criterio Inclusión", "Práctica activa continua mayor a 5 años en el casco urbano o rural de Estelí."),
            ("Criterio Exclusión", "Comercializadores ambulantes sin arraigo comunitario reconocido.")
        ]),
        ("DOCENTES", "n = 9", COLOR_BLUE_ROYAL, [
            ("Claustro de Psicología", "Docentes con grado de Licenciatura o Maestría que imparten asignaturas clínicas y metodológicas."),
            ("Criterio Inclusión", "Experiencia docente en la UNAN-Managua CUR-Estelí y supervisión de prácticas."),
            ("Criterio Exclusión", "Docentes de otras carreras no vinculadas al área de salud y humanidades.")
        ])
    ]

    for i, (grupo, n_val, col_num, items) in enumerate(grupos):
        left_pos = Inches(0.85 + i * 4.05)
        g_box = s9.shapes.add_textbox(left_pos, Inches(1.85), col_w9, Inches(4.9))
        tf_g = g_box.text_frame
        tf_g.word_wrap = True
        tf_g.margin_left = tf_g.margin_right = tf_g.margin_top = tf_g.margin_bottom = 0

        p_n = tf_g.paragraphs[0]
        p_n.text = n_val
        p_n.font.name = FONT_SERIF
        p_n.font.bold = True
        p_n.font.size = Pt(36)
        p_n.font.color.rgb = col_num
        p_n.space_after = Pt(2)

        p_g = tf_g.add_paragraph()
        p_g.text = grupo
        p_g.font.name = FONT_SANS
        p_g.font.bold = True
        p_g.font.size = Pt(13)
        p_g.font.color.rgb = COLOR_NAVY_TITLE
        p_g.space_after = Pt(12)

        for tag, desc in items:
            p_it = tf_g.add_paragraph()
            r1 = p_it.add_run()
            r1.text = f"• {tag}: "
            r1.font.name = FONT_SANS
            r1.font.bold = True
            r1.font.size = Pt(11.5)
            r1.font.color.rgb = COLOR_NAVY_TITLE
            r2 = p_it.add_run()
            r2.text = desc
            r2.font.name = FONT_SANS
            r2.font.size = Pt(11)
            r2.font.color.rgb = COLOR_TEXT_PRIMARY
            p_it.space_after = Pt(10)

    # ==========================================================================
    # SLIDE 10: RESULTADOS 1 (Demografía Estudiantes)
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, COLOR_LIGHT_CANVAS)
    add_minimal_header(s10, "Capítulo IV • Resultados Empíricos (1/4)", "Perfil Sociodemográfico y Formativo del Estudiantado (n = 68)")
    add_minimal_footer(s10, 10)
    add_native_transition(s10)

    # Embedding high-res Figura 3
    if os.path.exists(FIG_03_PATH):
        s10.shapes.add_picture(FIG_03_PATH, Inches(0.85), Inches(1.75), width=Inches(11.6))

    # Analytical bottom highlights
    hl_box = s10.shapes.add_textbox(Inches(0.85), Inches(5.8), Inches(11.6), Inches(1.1))
    tf_hl = hl_box.text_frame
    tf_hl.word_wrap = True
    tf_hl.margin_left = tf_hl.margin_right = tf_hl.margin_top = tf_hl.margin_bottom = 0

    p_hl = tf_hl.paragraphs[0]
    p_hl.text = "Interpretación Sociodemográfica y Relevancia Clínica:"
    p_hl.font.name = FONT_SANS
    p_hl.font.bold = True
    p_hl.font.size = Pt(11)
    p_hl.font.color.rgb = COLOR_TEAL_ACCENT
    p_hl.space_after = Pt(4)

    p_hl_txt = tf_hl.add_paragraph()
    p_hl_txt.text = "Predominio femenino significativo (82.4%, n = 56) y concentración etaria entre 21 y 25 años (67.6%, n = 46). El 77.9% cursa 4.º año enfrentando el inicio de la atención en la Clínica Psicosocial. El perfil refleja una cohorte receptiva a enfoques integrativos, pero altamente vulnerable al estrés somático por la sobrecarga lectiva y práctica."
    p_hl_txt.font.name = FONT_SANS
    p_hl_txt.font.size = Pt(11)
    p_hl_txt.font.color.rgb = COLOR_TEXT_PRIMARY

    # ==========================================================================
    # SLIDE 11: RESULTADOS 2 (La Paradoja Formativa - Big Stats Flotantes)
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11, COLOR_LIGHT_CANVAS)
    add_minimal_header(s11, "Capítulo IV • Resultados Empíricos (2/4)", "La Paradoja Formativa: Alta Pertinencia frente al Desamparo Curricular (OE1)")
    add_minimal_footer(s11, 11)
    add_native_transition(s11)

    # Left: Big Stats (Sin Cajas!)
    stats_w = Inches(4.8)
    s_box = s11.shapes.add_textbox(Inches(0.85), Inches(1.75), stats_w, Inches(5.1))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0

    big_stats = [
        ("89.7%", COLOR_TEAL_ACCENT, "Pertinencia Asistencial", "Considera necesario y urgente articular la MTCI en el ejercicio de la psicología clínica."),
        ("88.2%", COLOR_ALERT_CRIMSON, "Desamparo Curricular", "Reconoce no haber recibido preparación formal alguna para orientar o derivar en MTCI."),
        ("86.8%", COLOR_GOLD_ACCENT, "Inseguridad Psicoeducativa", "Autopercibe competencias nulas o insuficientes para dialogar sobre remedios tradicionales.")
    ]
    for val, col, title, desc in big_stats:
        p_val = tf_s.add_paragraph() if tf_s.paragraphs[0].text else tf_s.paragraphs[0]
        p_val.text = val
        p_val.font.name = FONT_SERIF
        p_val.font.bold = True
        p_val.font.size = Pt(38)
        p_val.font.color.rgb = col

        p_t = tf_s.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_SANS
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = COLOR_NAVY_TITLE

        p_d = tf_s.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_SANS
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_TEXT_PRIMARY
        p_d.space_after = Pt(10)

    # Right: Embedded Figura 7
    if os.path.exists(FIG_07_PATH):
        s11.shapes.add_picture(FIG_07_PATH, Inches(6.0), Inches(1.75), width=Inches(6.4))

    # Right Text: Uso Personal y Eficacia Somática
    u_box = s11.shapes.add_textbox(Inches(6.0), Inches(5.45), Inches(6.4), Inches(1.4))
    tf_u = u_box.text_frame
    tf_u.word_wrap = True
    tf_u.margin_left = tf_u.margin_right = tf_u.margin_top = tf_u.margin_bottom = 0

    pu_t = tf_u.paragraphs[0]
    pu_t.text = "Uso Personal y Eficacia Somática Percibida:"
    pu_t.font.name = FONT_SANS
    pu_t.font.bold = True
    pu_t.font.size = Pt(11)
    pu_t.font.color.rgb = COLOR_NAVY_TITLE
    pu_t.space_after = Pt(3)

    pu_d = tf_u.add_paragraph()
    pu_d.text = "• Carácter Reactivo: 52.9% no usa MTCI preventivamente; recurren únicamente ante crisis o sobrecarga.\n• Eficacia Plena: 86.7% de usuarios reales reporta alivio muscular y bienestar; 0.0% efectos adversos."
    pu_d.font.name = FONT_SANS
    pu_d.font.size = Pt(11)
    pu_d.font.color.rgb = COLOR_TEXT_PRIMARY

    # ==========================================================================
    # SLIDE 12: RESULTADOS 3 (Facilitadores Locales y Claustro Docente)
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12, COLOR_LIGHT_CANVAS)
    add_minimal_header(s12, "Capítulo IV • Resultados Empíricos (3/4)", "Perspectiva de Facilitadores Locales de Estelí y Claustro Docente")
    add_minimal_footer(s12, 12)
    add_native_transition(s12)

    col_w12 = Inches(5.6)
    # Col 1: Facilitadores Locales
    f_box = s12.shapes.add_textbox(Inches(0.85), Inches(1.8), col_w12, Inches(5.0))
    tf_f1 = f_box.text_frame
    tf_f1.word_wrap = True
    tf_f1.margin_left = tf_f1.margin_right = tf_f1.margin_top = tf_f1.margin_bottom = 0

    p_f_num = tf_f1.paragraphs[0]
    p_f_num.text = "100%"
    p_f_num.font.name = FONT_SERIF
    p_f_num.font.bold = True
    p_f_num.font.size = Pt(40)
    p_f_num.font.color.rgb = COLOR_TEAL_ACCENT

    p_f_lbl = tf_f1.add_paragraph()
    p_f_lbl.text = "FACILITADORES LOCALES DE ESTELÍ (n = 9)"
    p_f_lbl.font.name = FONT_SANS
    p_f_lbl.font.bold = True
    p_f_lbl.font.size = Pt(12)
    p_f_lbl.font.color.rgb = COLOR_NAVY_TITLE
    p_f_lbl.space_after = Pt(12)

    pts_fac = [
        ("Alivio Somático Directo", "Constatan descompresión miofascial inmediata y mayor apertura afectiva del consultante para el diálogo psicológico posterior."),
        ("Memoria Viva en Estelí", "77.8% mujeres; 44.4% acumula entre 20 y 30 años de experiencia comunitaria continuada."),
        ("Estigma Sociocultural", "El 100% enfrenta prejuicios religiosos y mitos urbanos respecto a las terapias naturales."),
        ("Desafío Económico", "77.8% reporta que la falta de recursos de los usuarios vulnerables interrumpe la continuidad del cuidado.")
    ]
    for h, d in pts_fac:
        p = tf_f1.add_paragraph()
        r1 = p.add_run()
        r1.text = f"✦ {h}: "
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_TEAL_ACCENT
        r2 = p.add_run()
        r2.text = d
        r2.font.name = FONT_SANS
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(8)

    add_hairline_v(s12, Inches(6.75), Inches(1.9), Inches(4.7), COLOR_HAIRLINE)

    # Col 2: Claustro Docente
    d_box = s12.shapes.add_textbox(Inches(7.15), Inches(1.8), col_w12, Inches(5.0))
    tf_d1 = d_box.text_frame
    tf_d1.word_wrap = True
    tf_d1.margin_left = tf_d1.margin_right = tf_d1.margin_top = tf_d1.margin_bottom = 0

    p_d_num = tf_d1.paragraphs[0]
    p_d_num.text = "100%"
    p_d_num.font.name = FONT_SERIF
    p_d_num.font.bold = True
    p_d_num.font.size = Pt(40)
    p_d_num.font.color.rgb = COLOR_BLUE_ROYAL

    p_d_lbl = tf_d1.add_paragraph()
    p_d_lbl.text = "CLAUSTRO DOCENTE-PSICÓLOGOS (n = 9)"
    p_d_lbl.font.name = FONT_SANS
    p_d_lbl.font.bold = True
    p_d_lbl.font.size = Pt(12)
    p_d_lbl.font.color.rgb = COLOR_NAVY_TITLE
    p_d_lbl.space_after = Pt(12)

    pts_doc = [
        ("Respaldo Curricular Pleno", "Apoyo unánime a la incorporación transversal de las MTCI bajo un enfoque crítico y científico."),
        ("Metodologías Activas (88.9%)", "Rechazan la enseñanza memorística; priorizan talleres vivenciales y análisis de casos clínicos."),
        ("Competencias Clave", "Demandan formar en juicio clínico ético, consentimiento informado y límites profesionales de no prescripción."),
        ("Capacitación Propia Urgente", "El profesorado solicita formación continua en neurobiología somática y regulación Bottom-Up.")
    ]
    for h, d in pts_doc:
        p = tf_d1.add_paragraph()
        r1 = p.add_run()
        r1.text = f"✦ {h}: "
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_BLUE_ROYAL
        r2 = p.add_run()
        r2.text = d
        r2.font.name = FONT_SANS
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(8)

    # ==========================================================================
    # SLIDE 13: RESULTADOS 4 / PROPUESTA (Manual de Estrategias MTCI)
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13, COLOR_LIGHT_CANVAS)
    add_minimal_header(s13, "Capítulo V • Propuesta Operativa (OE3)", "Manual de Estrategias de MTCI para la Formación y Práctica Psicológica")
    add_minimal_footer(s13, 13)
    add_native_transition(s13)

    # Left: Portada del Manual y Ficha Técnica
    if os.path.exists(MANUAL_COVER_PATH):
        s13.shapes.add_picture(MANUAL_COVER_PATH, Inches(0.85), Inches(1.8), width=Inches(3.8))

    fc_box = s13.shapes.add_textbox(Inches(0.85), Inches(4.3), Inches(3.8), Inches(2.5))
    tf_fc = fc_box.text_frame
    tf_fc.word_wrap = True
    tf_fc.margin_left = tf_fc.margin_right = tf_fc.margin_top = tf_fc.margin_bottom = 0

    p_fc_t = tf_fc.paragraphs[0]
    p_fc_t.text = "FICHA TÉCNICA DEL PRODUCTO"
    p_fc_t.font.name = FONT_SANS
    p_fc_t.font.bold = True
    p_fc_t.font.size = Pt(10.5)
    p_fc_t.font.color.rgb = COLOR_TEAL_ACCENT
    p_fc_t.space_after = Pt(4)

    fc_items = [
        "Extensión: 18 páginas in extenso (Anexo 16.2).",
        "Destinatarios: Alumnos y docentes de Clínica Psicosocial.",
        "Propósito: Dotar de discernimiento ético para explorar y derivar, sin habilitar como terapeutas alternativos.",
        "Instrumento: Adaptación del cuestionario I-CAM-Q para tamizaje transcultural."
    ]
    for it in fc_items:
        p = tf_fc.add_paragraph()
        p.text = f"• {it}"
        p.font.name = FONT_SANS
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(3)

    add_hairline_v(s13, Inches(4.9), Inches(1.9), Inches(4.7), COLOR_HAIRLINE)

    # Right: 8 Módulos Formativos en 2 columnas flotantes (Sin Cajas!)
    m_box = s13.shapes.add_textbox(Inches(5.2), Inches(1.8), Inches(7.3), Inches(5.0))
    tf_m = m_box.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0

    p_mt = tf_m.paragraphs[0]
    p_mt.text = "Estructura Modular del Manual (8 Módulos Temáticos)"
    p_mt.font.name = FONT_SERIF
    p_mt.font.bold = True
    p_mt.font.size = Pt(15)
    p_mt.font.color.rgb = COLOR_NAVY_TITLE
    p_mt.space_after = Pt(12)

    modulos = [
        ("Módulo 1", "Fundamentos y Marco Legal", "Definición OMS (2025) y articulación de Leyes 774, 759 y 292 de Nicaragua."),
        ("Módulo 2", "Principios Deontológicos", "Consentimiento informado intercultural y complementariedad sin sustitución."),
        ("Módulo 3", "Mapa Clínico de Prácticas", "Clasificación en 4 niveles: uso directo, psicoeducación, precaución y alerta médica."),
        ("Módulo 4", "Algoritmo de Derivación", "Protocolo secuencial de 4 pasos para derivación clínica informada."),
        ("Módulo 5", "Habilidades de Diálogo", "Técnicas de entrevista abierta para erradicar el ocultamiento terapéutico."),
        ("Módulo 6", "Red Intersectorial", "Criterios de referencia bidireccional y trabajo colaborativo con facilitadores."),
        ("Módulo 7", "Ruta Pedagógica", "Secuencia de 3 etapas vivenciales y propuesta de asignatura electiva."),
        ("Módulo 8", "Soporte CUR-Estelí", "Creación del Comité de Bioética y plan de capacitación docente continua.")
    ]
    for mod, nom, desc in modulos:
        p = tf_m.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{mod} • {nom}: "
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_GOLD_ACCENT
        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_SANS
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(6)

    # ==========================================================================
    # SLIDE 14: CONCLUSIONES CENTRALES (Triangulación de Objetivos, No Boxes)
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14, COLOR_LIGHT_CANVAS)
    add_minimal_header(s14, "Capítulo VI • Síntesis Conclusiva", "Conclusiones Centrales de la Investigación (Triangulación de Objetivos)")
    add_minimal_footer(s14, 14)
    add_native_transition(s14)

    concl_box = s14.shapes.add_textbox(Inches(0.85), Inches(1.8), Inches(11.6), Inches(5.0))
    tf_c = concl_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

    conclusiones = [
        ("01", "Cumplimiento del Objetivo General", "Los tres colectivos investigados (N = 86) validan unánimemente a la MTCI como recurso complementario legítimo en salud mental, condicionado a un ejercicio bioético, científico y respetuoso de los límites profesionales."),
        ("02", "Perfil y Paradoja Estudiantil (OE1)", "El estudiantado posee buen dominio conceptual básico (67.6%) y alta satisfacción somática subjetiva (86.7%), pero padece desinformación legal (58.8% desconoce Ley 774; 64.7% desconoce Ley 292) e inseguridad para derivar (88.2%)."),
        ("03", "Oferta y Resiliencia Territorial (OE2)", "Los facilitadores de Estelí constatan 100% de alivio de sobrecarga muscular y mayor receptividad reflexiva (88.9%), enfrentando barreras de estigma sociocultural (100%) y limitaciones económicas de los usuarios (77.8%)."),
        ("04", "Consenso Curricular Docente (OE3)", "El 100% del claustro apoya transversalizar la MTCI bajo metodologías activas y vivenciales (88.9%), demandando formación en regulación neurovegetativa y la creación de comités de bioética."),
        ("05", "Logro Propositivo del Manual de Estrategias", "Se construyó exitosamente el Manual de Estrategias MTCI de 18 páginas (Anexo 16.2), dotando al CUR-Estelí de algoritmos de decisión clínica, pautas contra el ocultamiento y el inventario I-CAM-Q.")
    ]

    for num, heading, body in conclusiones:
        p = tf_c.add_paragraph() if tf_c.paragraphs[0].text else tf_c.paragraphs[0]
        r_num = p.add_run()
        r_num.text = f"{num}  "
        r_num.font.name = FONT_SERIF
        r_num.font.bold = True
        r_num.font.size = Pt(13)
        r_num.font.color.rgb = COLOR_TEAL_ACCENT

        r_h = p.add_run()
        r_h.text = f"{heading}: "
        r_h.font.name = FONT_SANS
        r_h.font.bold = True
        r_h.font.size = Pt(12)
        r_h.font.color.rgb = COLOR_NAVY_TITLE

        r_b = p.add_run()
        r_b.text = body
        r_b.font.name = FONT_SANS
        r_b.font.size = Pt(11.5)
        r_b.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(11)

    # ==========================================================================
    # SLIDE 15: RECOMENDACIONES ESTRATÉGICAS (4 Cuadrantes Flotantes, Sin Cajas)
    # ==========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15, COLOR_LIGHT_CANVAS)
    add_minimal_header(s15, "Capítulo VI • Directrices Prospectivas", "Recomendaciones Estratégicas para Estudiantes, Docentes, Universidad y MINSA")
    add_minimal_footer(s15, 15)
    add_native_transition(s15)

    # Subtle cross-hairlines dividing the 4 quadrants
    add_hairline_h(s15, Inches(0.85), Inches(4.35), Inches(11.6), COLOR_HAIRLINE)
    add_hairline_v(s15, Inches(6.65), Inches(1.85), Inches(4.9), COLOR_HAIRLINE)

    quad_w = Inches(5.5)
    quads = [
        (Inches(0.85), Inches(1.85), "PARA EL ESTAMENTO ESTUDIANTIL", COLOR_TEAL_ACCENT, [
            ("Límites Legales", "Respetar estrictamente las Leyes 774 y 292 (prohibición terminante de prescribir fármacos)."),
            ("Algoritmo Clínico", "Aplicar el árbol de decisión del manual en las prácticas de la Clínica Psicosocial."),
            ("Diálogo Abierto", "Explorar empáticamente el uso de MTCI en consulta para erradicar el ocultamiento."),
            ("Autocuidado Personal", "Vivenciar la regulación somática (respiración diafragmática) ante la sobrecarga.")
        ]),
        (Inches(7.0), Inches(1.85), "PARA EL CLAUSTRO DOCENTE", COLOR_BLUE_ROYAL, [
            ("Transversalidad Curricular", "Integrar contenidos de MTCI en Psicología Clínica, Comunitaria y Ética."),
            ("Pedagogía Vivencial", "Priorizar análisis de casos clínicos reales y talleres de autorregulación somática."),
            ("Capacitación Continua", "Formarse institucionalmente en neurobiología del estrés y regulación Bottom-Up."),
            ("Derivación Ética", "Instruir en criterios claros de referencia intersectorial hacia facilitadores locales.")
        ]),
        (Inches(0.85), Inches(4.55), "PARA LA GESTIÓN DEL CUR-ESTELÍ", COLOR_GOLD_ACCENT, [
            ("Adopción Oficial", "Formalizar la aprobación institucional del Manual de Estrategias MTCI (Anexo 16.2)."),
            ("Comité de Bioética", "Constituir el Comité de Ética y Delimitación Profesional en el recinto universitario."),
            ("Alianza con MINSA", "Consolidar convenios interinstitucionales para pasantías y ferias de salud comunitaria."),
            ("Asignatura Electiva", "Evaluar a mediano plazo la creación formal del curso electivo 'Psicología Integrativa'.")
        ]),
        (Inches(7.0), Inches(4.55), "PARA EL SISTEMA DE SALUD Y FACILITADORES", COLOR_NAVY_TITLE, [
            ("Registro Oficial", "Difundir mecanismos de acreditación para facilitadores contemplados en la Ley No. 774."),
            ("Red de Interconsulta", "Habilitar canales de referencia bidireccional entre psicólogos y terapeutas locales."),
            ("Atención Primaria", "Fomentar la exploración desestigmatizada de saberes herbolarios en centros de salud."),
            ("Principio Bioético", "Mantener el compromiso de complementariedad sin pretender sustituir tratamientos médicos.")
        ])
    ]

    for left, top, title, col, bullets in quads:
        q_box = s15.shapes.add_textbox(left, top, quad_w, Inches(2.4))
        tf_q = q_box.text_frame
        tf_q.word_wrap = True
        tf_q.margin_left = tf_q.margin_right = tf_q.margin_top = tf_q.margin_bottom = 0

        p_t = tf_q.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_SANS
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = col
        p_t.space_after = Pt(6)

        for tag, desc in bullets:
            p_b = tf_q.add_paragraph()
            r1 = p_b.add_run()
            r1.text = f"✓ {tag}: "
            r1.font.name = FONT_SANS
            r1.font.bold = True
            r1.font.size = Pt(10.5)
            r1.font.color.rgb = COLOR_NAVY_TITLE
            r2 = p_b.add_run()
            r2.text = desc
            r2.font.name = FONT_SANS
            r2.font.size = Pt(10)
            r2.font.color.rgb = COLOR_TEXT_PRIMARY
            p_b.space_after = Pt(2)

    # ==========================================================================
    # SLIDE 16: CIERRE INSTITUCIONAL (Dark Minimalist Executive)
    # ==========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16, COLOR_DARK_CANVAS)
    add_native_transition(s16)

    if os.path.exists(SHIELD_PATH):
        s16.shapes.add_picture(SHIELD_PATH, Inches(5.85), Inches(0.85), height=Inches(1.5))

    cierre_box = s16.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(11.3), Inches(2.4))
    tf_cie = cierre_box.text_frame
    tf_cie.word_wrap = True
    tf_cie.margin_left = tf_cie.margin_right = tf_cie.margin_top = tf_cie.margin_bottom = 0

    p_lema = tf_cie.paragraphs[0]
    p_lema.alignment = PP_ALIGN.CENTER
    p_lema.text = "«¡A la libertad por la Universidad!»"
    p_lema.font.name = FONT_SERIF
    p_lema.font.size = Pt(18)
    p_lema.font.bold = True
    p_lema.font.italic = True
    p_lema.font.color.rgb = RGBColor(245, 158, 11)  # Warm Gold
    p_lema.space_after = Pt(10)

    p_gracias = tf_cie.add_paragraph()
    p_gracias.alignment = PP_ALIGN.CENTER
    p_gracias.text = "Muchas Gracias por su Atención"
    p_gracias.font.name = FONT_SERIF
    p_gracias.font.size = Pt(36)
    p_gracias.font.bold = True
    p_gracias.font.color.rgb = COLOR_WHITE
    p_gracias.space_after = Pt(10)

    p_deb = tf_cie.add_paragraph()
    p_deb.alignment = PP_ALIGN.CENTER
    p_deb.text = "Espacio Abierto para Preguntas, Comentarios y Defensa Oral ante el Honorable Tribunal Examinador"
    p_deb.font.name = FONT_SANS
    p_deb.font.size = Pt(13)
    p_deb.font.color.rgb = RGBColor(148, 163, 184)

    # Hairline divider
    add_hairline_h(s16, Inches(1.5), Inches(5.1), Inches(10.3), RGBColor(30, 41, 59))

    # Bottom team metadata
    f_box16 = s16.shapes.add_textbox(Inches(1.5), Inches(5.35), Inches(10.3), Inches(1.5))
    tf_f16 = f_box16.text_frame
    tf_f16.word_wrap = True
    tf_f16.margin_left = tf_f16.margin_right = tf_f16.margin_top = tf_f16.margin_bottom = 0

    p_t_cie = tf_f16.paragraphs[0]
    p_t_cie.alignment = PP_ALIGN.CENTER
    p_t_cie.text = "Sustentantes: Dina Fabiola García Torres • Tatiana Paola López Ramos • Engel Enoc Zamora Velásquez"
    p_t_cie.font.name = FONT_SANS
    p_t_cie.font.size = Pt(11)
    p_t_cie.font.bold = True
    p_t_cie.font.color.rgb = COLOR_WHITE
    p_t_cie.space_after = Pt(4)

    p_tut_cie = tf_f16.add_paragraph()
    p_tut_cie.alignment = PP_ALIGN.CENTER
    p_tut_cie.text = "Tutoría Académica: Dra. Tania Libertad Pérez Guevara | Carrera de Psicología • CUR-Estelí"
    p_tut_cie.font.name = FONT_SANS
    p_tut_cie.font.size = Pt(10.5)
    p_tut_cie.font.color.rgb = RGBColor(20, 184, 166)

    # Save presentations
    output_minimal = "Presentacion_Defensa_Tesis_MTCI_UNAN_Minimal.pptx"
    output_main    = "Presentacion_Defensa_Tesis_MTCI_UNAN.pptx"
    prs.save(output_minimal)
    prs.save(output_main)
    print(f"Minimalist presentation saved successfully to: {output_minimal} and {output_main}")

if __name__ == "__main__":
    create_presentation()
