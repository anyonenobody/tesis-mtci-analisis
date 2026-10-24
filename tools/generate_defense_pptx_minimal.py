#!/usr/bin/env python3
"""
tools/generate_defense_pptx_minimal.py
================================================================================
Generador de Presentación Oficial de Defensa de Tesis MTCI · UNAN-Managua CUR-Estelí
ESTÁNDAR: Rigor Académico Estricto APA 7, Sin Sensacionalismo, Gráficas Empíricas
Completas para Estudiantes, Facilitadores y Docentes, y Libre de Cajas (No-Cards).
- 17 láminas con transiciones nativas OpenXML (p:transition p:fade)
- Gráficas empíricas oficiales: Figuras 4, 7, 12, 14, 24, 25 y Portada del Manual
- Cero métricas alucinadas: 100% derivadas de docs/capitulos/ y datos_mtci_anonimizado.csv
- Tipografía editorial académica: Cambria (Serif) + Calibri (Sans)
================================================================================
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml

# ==============================================================================
# PALETA INSTITUCIONAL Y EDITORIAL (Minimalismo Académico)
# ==============================================================================
COLOR_DARK_CANVAS  = RGBColor(8, 14, 26)       # #080E1A Medianoche Institucional (Láms. 1 y 17)
COLOR_LIGHT_CANVAS = RGBColor(253, 254, 255)   # #FDFEFF Blanco Luminoso Editorial (Láms. 2 a 16)

COLOR_NAVY_TITLE   = RGBColor(15, 23, 42)      # #0F172A Slate 900
COLOR_TEAL_ACCENT  = RGBColor(13, 148, 136)    # #0D9488 MTCI / Salud Integrativa
COLOR_GOLD_ACCENT  = RGBColor(217, 119, 6)     # #D97706 Ámbar UNAN / Énfasis
COLOR_ALERT_CRIMSON= RGBColor(220, 38, 38)     # #DC2626 Advertencia / Límite Deontológico
COLOR_BLUE_ROYAL   = RGBColor(37, 99, 235)     # #2563EB Claustro Docente / Academia

COLOR_TEXT_PRIMARY = RGBColor(30, 41, 59)      # #1E293B Texto Principal
COLOR_TEXT_MUTED   = RGBColor(100, 116, 139)   # #64748B Texto Secundario / Metadatos
COLOR_HAIRLINE     = RGBColor(226, 232, 240)   # #E2E8F0 Separador Sutil (0.75 pt)
COLOR_WHITE        = RGBColor(255, 255, 255)

FONT_SERIF = "Cambria"
FONT_SANS  = "Calibri"

# Rutas de Activos Empíricos
LOGO_CLEAN_PATH   = "assets/extracted/unan_logo_clean.png"
SHIELD_PATH       = "assets/extracted/unan_shield_only.png"
MANUAL_COVER_PATH = "assets/extracted/portada_manual.jpg"

FIG_03_PATH = "assets/figuras_apa7/figura_03_demografia_estudiantes.png"
FIG_04_PATH = "assets/figuras_apa7/figura_04_dominio_conceptual_normativo_estudiantes.png"
FIG_07_PATH = "assets/figuras_apa7/figura_07_frecuencia_uso_estudiantes.png"
FIG_12_PATH = "assets/figuras_apa7/figura_12_practicas_actores_locales.png"
FIG_14_PATH = "assets/figuras_apa7/figura_14_apertura_emocional_usuarios_actores.png"
FIG_24_PATH = "assets/figuras_apa7/figura_24_estrategias_academicas_docentes.png"
FIG_25_PATH = "assets/figuras_apa7/figura_25_experiencias_favorables_docentes.png"

def add_native_transition(slide):
    """Inyecta transición nativa de desvanecimiento suave (Smooth Fade) en OpenXML."""
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

    def add_academic_header(slide, category_text, title_text):
        """Encabezado sobrio y estrictamente académico, sin líneas decorativas de IA."""
        eb_box = slide.shapes.add_textbox(Inches(0.85), Inches(0.48), Inches(10.5), Inches(0.28))
        tf_eb = eb_box.text_frame
        tf_eb.word_wrap = True
        tf_eb.margin_left = tf_eb.margin_right = tf_eb.margin_top = tf_eb.margin_bottom = 0
        p_eb = tf_eb.paragraphs[0]
        p_eb.text = category_text.upper()
        p_eb.font.name = FONT_SANS
        p_eb.font.size = Pt(9.5)
        p_eb.font.bold = True
        p_eb.font.color.rgb = COLOR_TEAL_ACCENT

        t_box = slide.shapes.add_textbox(Inches(0.85), Inches(0.76), Inches(10.8), Inches(0.75))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = FONT_SERIF
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY_TITLE

        if os.path.exists(SHIELD_PATH):
            slide.shapes.add_picture(SHIELD_PATH, Inches(12.0), Inches(0.45), height=Inches(0.85))

    def add_academic_footer(slide, current_num, total_slides=17):
        """Pie de página institucional con numeración canónica."""
        f_box = slide.shapes.add_textbox(Inches(0.85), Inches(7.10), Inches(10.5), Inches(0.25))
        tf = f_box.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "UNAN-Managua • CUR-Estelí | Carrera de Psicología • Segundo Semestre 2026"
        p.font.name = FONT_SANS
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_TEXT_MUTED

        n_box = slide.shapes.add_textbox(Inches(11.8), Inches(7.10), Inches(0.7), Inches(0.25))
        tf_n = n_box.text_frame
        tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
        pn = tf_n.paragraphs[0]
        pn.alignment = PP_ALIGN.RIGHT
        pn.text = f"{current_num} / {total_slides}"
        pn.font.name = FONT_SANS
        pn.font.size = Pt(8.5)
        pn.font.bold = True
        pn.font.color.rgb = COLOR_TEXT_MUTED

    def add_hairline_h(slide, left, top, width, color=COLOR_HAIRLINE):
        line = slide.shapes.add_shape(1, left, top, width, Pt(1))
        line.fill.background()
        line.line.color.rgb = color
        line.line.width = Pt(0.75)
        return line

    def add_hairline_v(slide, left, top, height, color=COLOR_HAIRLINE):
        line = slide.shapes.add_shape(1, left, top, Pt(1), height)
        line.fill.background()
        line.line.color.rgb = color
        line.line.width = Pt(0.75)
        return line

    # ==========================================================================
    # SLIDE 1: PORTADA INSTITUCIONAL
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, COLOR_DARK_CANVAS)
    add_native_transition(s1)

    if os.path.exists(LOGO_CLEAN_PATH):
        s1.shapes.add_picture(LOGO_CLEAN_PATH, Inches(0.9), Inches(0.75), height=Inches(1.1))

    univ_box = s1.shapes.add_textbox(Inches(3.1), Inches(0.82), Inches(9.3), Inches(0.95))
    tf_u = univ_box.text_frame
    tf_u.word_wrap = True
    tf_u.margin_left = tf_u.margin_right = tf_u.margin_top = tf_u.margin_bottom = 0
    pu1 = tf_u.paragraphs[0]
    pu1.text = "UNIVERSIDAD NACIONAL AUTÓNOMA DE NICARAGUA, MANAGUA"
    pu1.font.name = FONT_SANS
    pu1.font.size = Pt(13.5)
    pu1.font.bold = True
    pu1.font.color.rgb = COLOR_WHITE
    pu2 = tf_u.add_paragraph()
    pu2.text = "CENTRO UNIVERSITARIO REGIONAL DE ESTELÍ • RECINTO LEONEL RUGAMA RUGAMA"
    pu2.font.name = FONT_SANS
    pu2.font.size = Pt(10)
    pu2.font.bold = True
    pu2.font.color.rgb = RGBColor(245, 158, 11)
    pu3 = tf_u.add_paragraph()
    pu3.text = "Departamento de Educación y Humanidades | Carrera de Licenciatura en Psicología"
    pu3.font.name = FONT_SANS
    pu3.font.size = Pt(9.5)
    pu3.font.color.rgb = RGBColor(148, 163, 184)

    add_hairline_h(s1, Inches(0.9), Inches(2.15), Inches(11.5), RGBColor(30, 41, 59))

    t_box1 = s1.shapes.add_textbox(Inches(0.9), Inches(2.4), Inches(11.5), Inches(2.5))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
    p_sub = tf1.paragraphs[0]
    p_sub.text = "TRABAJO DE INVESTIGACIÓN PARA OPTAR AL GRADO DE LICENCIADOS EN PSICOLOGÍA"
    p_sub.font.name = FONT_SANS
    p_sub.font.size = Pt(10.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(20, 184, 166)
    p_sub.space_after = Pt(10)

    p_t = tf1.add_paragraph()
    p_t.text = "La Medicina Tradicional, Complementaria e Integrativa\n(MTCI) como Complemento en la Atención Psicológica"
    p_t.font.name = FONT_SERIF
    p_t.font.size = Pt(31)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE
    p_t.space_after = Pt(12)

    p_baj = tf1.add_paragraph()
    p_baj.text = "Estudio Mixto con Estudiantes y Docentes del CUR-Estelí y Facilitadores Locales del Municipio de Estelí (Segundo Semestre, 2026)"
    p_baj.font.name = FONT_SANS
    p_baj.font.size = Pt(13)
    p_baj.font.color.rgb = RGBColor(226, 232, 240)

    add_hairline_h(s1, Inches(0.9), Inches(5.1), Inches(11.5), RGBColor(30, 41, 59))

    col_w = Inches(3.6)
    c1_box = s1.shapes.add_textbox(Inches(0.9), Inches(5.35), col_w, Inches(1.5))
    tf_c1 = c1_box.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = tf_c1.margin_bottom = 0
    p1 = tf_c1.paragraphs[0]
    p1.text = "AUTORES / SUSTENTANTES"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(9)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(245, 158, 11)
    p1.space_after = Pt(5)
    for name in ["• Dina Fabiola García Torres", "• Tatiana Paola López Ramos", "• Engel Enoc Zamora Velásquez"]:
        pn = tf_c1.add_paragraph()
        pn.text = name
        pn.font.name = FONT_SANS
        pn.font.size = Pt(10.5)
        pn.font.color.rgb = COLOR_WHITE
        pn.space_after = Pt(2)

    add_hairline_v(s1, Inches(4.75), Inches(5.35), Inches(1.5), RGBColor(30, 41, 59))

    c2_box = s1.shapes.add_textbox(Inches(5.05), Inches(5.35), col_w, Inches(1.5))
    tf_c2 = c2_box.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = tf_c2.margin_bottom = 0
    p2 = tf_c2.paragraphs[0]
    p2.text = "TUTORÍA ACADÉMICA"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(20, 184, 166)
    p2.space_after = Pt(5)
    p_tut = tf_c2.add_paragraph()
    p_tut.text = "• Dra. Tania Libertad Pérez Guevara"
    p_tut.font.name = FONT_SANS
    p_tut.font.size = Pt(10.5)
    p_tut.font.bold = True
    p_tut.font.color.rgb = COLOR_WHITE
    p_tut_r = tf_c2.add_paragraph()
    p_tut_r.text = "Docente Investigadora • Asesoría Temática y Metodológica\nCUR-Estelí, UNAN-Managua"
    p_tut_r.font.name = FONT_SANS
    p_tut_r.font.size = Pt(9.5)
    p_tut_r.font.color.rgb = RGBColor(148, 163, 184)

    add_hairline_v(s1, Inches(8.9), Inches(5.35), Inches(1.5), RGBColor(30, 41, 59))

    c3_box = s1.shapes.add_textbox(Inches(9.2), Inches(5.35), col_w, Inches(1.5))
    tf_c3 = c3_box.text_frame
    tf_c3.word_wrap = True
    tf_c3.margin_left = tf_c3.margin_right = tf_c3.margin_top = tf_c3.margin_bottom = 0
    p3 = tf_c3.paragraphs[0]
    p3.text = "DEFENSA DE GRADO"
    p3.font.name = FONT_SANS
    p3.font.size = Pt(9)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(226, 232, 240)
    p3.space_after = Pt(5)
    p_deg = tf_c3.add_paragraph()
    p_deg.text = "Licenciatura en Psicología"
    p_deg.font.name = FONT_SANS
    p_deg.font.size = Pt(10.5)
    p_deg.font.color.rgb = COLOR_WHITE
    p_lin = tf_c3.add_paragraph()
    p_lin.text = "Línea SAL-3 (Salud e Interculturalidad)\nEstelí, Nicaragua • Octubre, 2026"
    p_lin.font.name = FONT_SANS
    p_lin.font.size = Pt(9.5)
    p_lin.font.color.rgb = RGBColor(148, 163, 184)

    # ==========================================================================
    # SLIDE 2: PLANTEAMIENTO DEL PROBLEMA Y JUSTIFICACIÓN
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, COLOR_LIGHT_CANVAS)
    add_academic_header(s2, "Capítulo I • Introducción", "Planteamiento del Problema y Justificación de la Investigación")
    add_academic_footer(s2, 2)
    add_native_transition(s2)

    col_w2 = Inches(5.5)
    p_box = s2.shapes.add_textbox(Inches(0.85), Inches(1.75), col_w2, Inches(5.0))
    tf_p = p_box.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0

    p_p_title = tf_p.paragraphs[0]
    p_p_title.text = "Problema de Investigación: Tensión Normativa y Formativa"
    p_p_title.font.name = FONT_SERIF
    p_p_title.font.size = Pt(14)
    p_p_title.font.bold = True
    p_p_title.font.color.rgb = COLOR_NAVY_TITLE
    p_p_title.space_after = Pt(12)

    points_p = [
        ("01", "Asimetría Normativa y Vacío Curricular", "La Ley No. 774 reconoce el acceso ciudadano a la MTCI en el sistema de salud, mientras la Ley No. 292 prohíbe taxativamente al psicólogo prescribir fármacos. Los planes de estudio no dotan al alumnado de lineamientos bioéticos claros para dialogar o derivar."),
        ("02", "Ocultamiento Terapéutico en Consulta", "Los usuarios recurren empíricamente a la medicina natural y tradicional para aliviar su angustia, pero silencian estas prácticas en consulta psicológica por temor al rechazo o escepticismo del terapeuta."),
        ("03", "Riesgos Clínicos e Interacciones", "El desconocimiento de fitoterapia y productos naturales impide explorar contraindicaciones con psicofármacos o detectar prácticas que puedan retrasar la atención especializada.")
    ]
    for num, heading, body in points_p:
        p_n = tf_p.add_paragraph()
        r_num = p_n.add_run()
        r_num.text = f"{num}  "
        r_num.font.name = FONT_SERIF
        r_num.font.bold = True
        r_num.font.size = Pt(12)
        r_num.font.color.rgb = COLOR_TEAL_ACCENT

        r_h = p_n.add_run()
        r_h.text = f"{heading}: "
        r_h.font.name = FONT_SANS
        r_h.font.bold = True
        r_h.font.size = Pt(11.5)
        r_h.font.color.rgb = COLOR_NAVY_TITLE

        r_b = p_n.add_run()
        r_b.text = body
        r_b.font.name = FONT_SANS
        r_b.font.size = Pt(11)
        r_b.font.color.rgb = COLOR_TEXT_PRIMARY
        p_n.space_after = Pt(10)

    p_q = tf_p.add_paragraph()
    r_ql = p_q.add_run()
    r_ql.text = "✦ Pregunta Central: "
    r_ql.font.bold = True
    r_ql.font.size = Pt(11)
    r_ql.font.color.rgb = COLOR_GOLD_ACCENT
    r_qt = p_q.add_run()
    r_qt.text = "¿Cómo fundamenta el diagnóstico de MTCI en Estelí el diseño de un manual ético y pedagógico para Psicología?"
    r_qt.font.italic = True
    r_qt.font.size = Pt(11)
    r_qt.font.color.rgb = COLOR_NAVY_TITLE

    add_hairline_v(s2, Inches(6.75), Inches(1.85), Inches(4.7), COLOR_HAIRLINE)

    j_box = s2.shapes.add_textbox(Inches(7.15), Inches(1.75), col_w2, Inches(5.0))
    tf_j = j_box.text_frame
    tf_j.word_wrap = True
    tf_j.margin_left = tf_j.margin_right = tf_j.margin_top = tf_j.margin_bottom = 0

    p_j_title = tf_j.paragraphs[0]
    p_j_title.text = "Justificación y Relevancia de la Investigación"
    p_j_title.font.name = FONT_SERIF
    p_j_title.font.size = Pt(14)
    p_j_title.font.bold = True
    p_j_title.font.color.rgb = COLOR_NAVY_TITLE
    p_j_title.space_after = Pt(12)

    points_j = [
        ("✦", "Ética y No Maleficencia", "Explorar el uso de hierbas y remedios previene interacciones fitofarmacológicas y protege la seguridad clínica del usuario."),
        ("✦", "Salud Mental Comunitaria", "Reconoce la memoria etnobotánica viva y la legitimidad sociocultural de los facilitadores tradicionales en el territorio de Estelí."),
        ("✦", "Pertinencia Formativa en el CUR-Estelí", "Dota a estudiantes de 4.º y 5.º año de discernimiento deontológico para sus prácticas en la Clínica Psicosocial universitaria."),
        ("✦", "Aporte Propositivo Concreto", "Genera el Manual de Estrategias MTCI de 18 páginas (Anexo 16.2), articulando algoritmos clínicos y el inventario I-CAM-Q.")
    ]
    for bullet, heading, body in points_j:
        pj = tf_j.add_paragraph()
        rb = pj.add_run()
        rb.text = f"{bullet} "
        rb.font.bold = True
        rb.font.color.rgb = COLOR_TEAL_ACCENT
        rb.font.size = Pt(11)

        rh = pj.add_run()
        rh.text = f"{heading}: "
        rh.font.name = FONT_SANS
        rh.font.bold = True
        rh.font.size = Pt(11.5)
        rh.font.color.rgb = COLOR_NAVY_TITLE

        rt = pj.add_run()
        rt.text = body
        rt.font.name = FONT_SANS
        rt.font.size = Pt(11)
        rt.font.color.rgb = COLOR_TEXT_PRIMARY
        pj.space_after = Pt(11)

    # ==========================================================================
    # SLIDE 3: ANTECEDENTES DE LA INVESTIGACIÓN
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, COLOR_LIGHT_CANVAS)
    add_academic_header(s3, "Capítulo I • Introducción", "Antecedentes de la Investigación: Ámbitos Internacional, Regional y Local")
    add_academic_footer(s3, 3)
    add_native_transition(s3)

    add_hairline_h(s3, Inches(0.85), Inches(2.2), Inches(11.6), COLOR_TEAL_ACCENT)

    antecedentes = [
        ("2014 – 2019", "ÁMBITO GLOBAL", "Directrices de la OMS y Ensayos Clínicos", [
            ("Estrategia OMS sobre MTCI", "Marco global que insta a los sistemas de salud a incorporar medicinas tradicionales sobre bases de seguridad y evidencia."),
            ("Metanálisis de Acupuntura y Fitoterapia", "Furlan et al. (2012) y Guo et al. (2024) comprueban eficacia en dolor crónico, fibromialgia y estrés somático."),
            ("Salud Mental e Intervenciones Mente-Cuerpo", "Sotiropoulos et al. (2025) validan técnicas de autorregulación somática en cuadros ansioso-depresivos.")
        ]),
        ("2020 – 2023", "ÁMBITO REGIONAL", "Estudios Universitarios en Iberoamérica", [
            ("Estudios en Educación Superior", "Investigaciones en Argentina (Papalini, 2022) y Chile evidencian uso masivo de MTCI en estudiantes de carreras de salud."),
            ("Identificación de la Brecha Formativa", "Más del 80% del alumnado recurre a MTCI como autocuidado pero reporta nula preparación curricular universitaria."),
            ("Ausencia de Protocolos Clínicos", "Carencia de herramientas normalizadas de derivación entre psicólogos y terapeutas tradicionales.")
        ]),
        ("2024 – 2026", "ÁMBITO LOCAL", "Nicaragua, CUR-Estelí y Vacío Curricular", [
            ("Vanguardia Jurídica Sanitaria", "Leyes 774 y 759 establecen el Instituto de Medicina Natural, pionero en el marco normativo centroamericano."),
            ("Vacío en Facultades de Psicología", "Ausencia de asignaturas o módulos sobre diálogo intercultural en salud mental en los planes de estudio vigentes."),
            ("Estudio Mixto CUR-Estelí (2026)", "Primer estudio empírico que triangula las percepciones de estudiantes, docentes universitarios y facilitadores locales.")
        ])
    ]

    col_w3 = Inches(3.65)
    for i, (period, scope, subtitle, items) in enumerate(antecedentes):
        left_pos = Inches(0.85 + i * 4.0)

        dot_box = s3.shapes.add_textbox(left_pos, Inches(1.75), col_w3, Inches(0.8))
        tf_d = dot_box.text_frame
        tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
        pd = tf_d.paragraphs[0]
        pd.text = f"●  {period}"
        pd.font.name = FONT_SERIF
        pd.font.bold = True
        pd.font.size = Pt(12)
        pd.font.color.rgb = COLOR_TEAL_ACCENT

        pd_sc = tf_d.add_paragraph()
        pd_sc.text = f"{scope} • {subtitle}"
        pd_sc.font.name = FONT_SANS
        pd_sc.font.bold = True
        pd_sc.font.size = Pt(10.5)
        pd_sc.font.color.rgb = COLOR_NAVY_TITLE

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
            rt.font.size = Pt(11)
            rt.font.color.rgb = COLOR_NAVY_TITLE

            rd = p_it.add_run()
            rd.text = desc
            rd.font.name = FONT_SANS
            rd.font.size = Pt(10.5)
            rd.font.color.rgb = COLOR_TEXT_PRIMARY
            p_it.space_after = Pt(9)

    # ==========================================================================
    # SLIDE 4: CONTEXTO DEL ESTUDIO
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, COLOR_LIGHT_CANVAS)
    add_academic_header(s4, "Capítulo I • Introducción", "Contexto del Estudio: Territorio de Estelí y UNAN-Managua CUR-Estelí")
    add_academic_footer(s4, 4)
    add_native_transition(s4)

    ctx_w = Inches(5.6)
    box_s4_1 = s4.shapes.add_textbox(Inches(0.85), Inches(1.8), ctx_w, Inches(5.0))
    tf_s4_1 = box_s4_1.text_frame
    tf_s4_1.word_wrap = True
    tf_s4_1.margin_left = tf_s4_1.margin_right = tf_s4_1.margin_top = tf_s4_1.margin_bottom = 0

    p_t1 = tf_s4_1.paragraphs[0]
    p_t1.text = "Municipio de Estelí: Realidad Sociocultural y Prácticas Tradicionales"
    p_t1.font.name = FONT_SERIF
    p_t1.font.bold = True
    p_t1.font.size = Pt(14)
    p_t1.font.color.rgb = COLOR_NAVY_TITLE
    p_t1.space_after = Pt(12)

    pts_ctx1 = [
        ("Tradición Etnobotánica de Las Segovias", "Estelí y el norte de Nicaragua conservan un acervo histórico de uso de plantas medicinales, sobandería y remedios caseros transmitidos de generación en generación."),
        ("Presencia de Terapeutas Comunitarios", "Los facilitadores de medicina natural, masajistas y curanderos atienden de forma cotidiana a personas con dolencias osteomusculares y estados de estrés o aflicción emocional."),
        ("Desarticulación Asistencial y Prejuicios", "Persiste una brecha de comunicación formal entre los terapeutas tradicionales y los centros de salud institucionales, mediada por prejuicios mutuos y falta de vías de derivación.")
    ]
    for h, d in pts_ctx1:
        p = tf_s4_1.add_paragraph()
        rh = p.add_run()
        rh.text = f"✦ {h}\n"
        rh.font.name = FONT_SANS
        rh.font.bold = True
        rh.font.size = Pt(11.5)
        rh.font.color.rgb = COLOR_TEAL_ACCENT
        rd = p.add_run()
        rd.text = d
        rd.font.name = FONT_SANS
        rd.font.size = Pt(11)
        rd.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(11)

    add_hairline_v(s4, Inches(6.75), Inches(1.9), Inches(4.7), COLOR_HAIRLINE)

    box_s4_2 = s4.shapes.add_textbox(Inches(7.15), Inches(1.8), ctx_w, Inches(5.0))
    tf_s4_2 = box_s4_2.text_frame
    tf_s4_2.word_wrap = True
    tf_s4_2.margin_left = tf_s4_2.margin_right = tf_s4_2.margin_top = tf_s4_2.margin_bottom = 0

    p_t2 = tf_s4_2.paragraphs[0]
    p_t2.text = "UNAN-Managua CUR-Estelí: Clínica Psicosocial y Formación"
    p_t2.font.name = FONT_SERIF
    p_t2.font.bold = True
    p_t2.font.size = Pt(14)
    p_t2.font.color.rgb = COLOR_NAVY_TITLE
    p_t2.space_after = Pt(12)

    pts_ctx2 = [
        ("Recinto Universitario Leonel Rugama", "Sede regional que forma a profesionales de la psicología orientados a responder a las demandas del desarrollo humano y comunitario de la región norte."),
        ("Clínica Psicosocial del CUR-Estelí", "Espacio asistencial y docente donde los estudiantes de 4.º y 5.º año brindan atención psicoterapéutica bajo supervisión docente a consultantes con dificultades afectivas y psicosomáticas."),
        ("Demanda de Herramientas Bioéticas", "La investigación responde a la necesidad docente de dotar al estudiantado de pautas estructuradas para explorar el uso de MTCI y establecer límites de práctica claros.")
    ]
    for h, d in pts_ctx2:
        p = tf_s4_2.add_paragraph()
        rh = p.add_run()
        rh.text = f"✦ {h}\n"
        rh.font.name = FONT_SANS
        rh.font.bold = True
        rh.font.size = Pt(11.5)
        rh.font.color.rgb = COLOR_GOLD_ACCENT
        rd = p.add_run()
        rd.text = d
        rd.font.name = FONT_SANS
        rd.font.size = Pt(11)
        rd.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(11)

    # ==========================================================================
    # SLIDE 5: OBJETIVOS DE LA INVESTIGACIÓN
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, COLOR_LIGHT_CANVAS)
    add_academic_header(s5, "Capítulo I • Introducción", "Objetivos de la Investigación: General y Específicos")
    add_academic_footer(s5, 5)
    add_native_transition(s5)

    og_box = s5.shapes.add_textbox(Inches(0.85), Inches(1.75), Inches(11.6), Inches(1.3))
    tf_og = og_box.text_frame
    tf_og.word_wrap = True
    tf_og.margin_left = tf_og.margin_right = tf_og.margin_top = tf_og.margin_bottom = 0
    p_og_lbl = tf_og.paragraphs[0]
    p_og_lbl.text = "OBJETIVO GENERAL"
    p_og_lbl.font.name = FONT_SANS
    p_og_lbl.font.bold = True
    p_og_lbl.font.size = Pt(10.5)
    p_og_lbl.font.color.rgb = COLOR_GOLD_ACCENT
    p_og_lbl.space_after = Pt(4)

    p_og = tf_og.add_paragraph()
    p_og.text = "Analizar la integración de la Medicina Tradicional, Complementaria e Integrativa (MTCI) como recurso complementario en la atención psicológica, a partir de las percepciones, conocimientos y prácticas de estudiantes, docentes y facilitadores locales, formulando un manual de estrategias bioéticas y formativas en el CUR-Estelí."
    p_og.font.name = FONT_SERIF
    p_og.font.bold = True
    p_og.font.size = Pt(15)
    p_og.font.color.rgb = COLOR_NAVY_TITLE

    add_hairline_h(s5, Inches(0.85), Inches(3.25), Inches(11.6), COLOR_HAIRLINE)

    col_w5 = Inches(3.6)
    oes = [
        ("OE1 • MUESTRA ESTUDIANTIL", COLOR_TEAL_ACCENT, "Caracterizar la percepción, nivel de conocimiento, frecuencia de uso y barreras autopercibidas en los estudiantes de 4.º y 5.º año de la Carrera de Psicología respecto a las MTCI."),
        ("OE2 • FACILITADORES LOCALES", COLOR_BLUE_ROYAL, "Explorar las experiencias terapéuticas, prácticas tradicionales y barreras socioculturales que enfrentan los facilitadores locales de medicina tradicional en el municipio de Estelí."),
        ("OE3 • CLAUSTRO Y PROPUESTA", COLOR_GOLD_ACCENT, "Diseñar un Manual de Estrategias de MTCI para la formación y práctica psicológica, fundamentado en los criterios del claustro docente y los hallazgos empíricos del CUR-Estelí.")
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
        p_t.font.size = Pt(10.5)
        p_t.font.color.rgb = COLOR_NAVY_TITLE
        p_t.space_after = Pt(8)

        p_d = tf_oe.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_SANS
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_TEXT_PRIMARY

    # ==========================================================================
    # SLIDE 6: MARCO TEÓRICO 1 (Epistemología y Bioética)
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, COLOR_LIGHT_CANVAS)
    add_academic_header(s6, "Capítulo II • Marco Teórico (1/2)", "Fundamentos Epistemológicos y Principios Bioéticos en Salud Mental")
    add_academic_footer(s6, 6)
    add_native_transition(s6)

    col_w6 = Inches(3.65)
    pillars = [
        ("01", "Modelo Biopsicosocial Ampliado", "Engel (1977); Babic et al. (2024)", [
            "Superación del reduccionismo mecanicista y biomédico en salud mental.",
            "Integración de la dimensión somática, afectiva, cognitiva y sociocultural en un continuo dinámico.",
            "Regulación neurovegetativa y vías Bottom-Up como fundamento fisiológico del autocuidado."
        ]),
        ("02", "Pluralismo Médico y Hermenéutica", "Menéndez (2020); OMS (2025)", [
            "Coexistencia real del Modelo Médico Hegemónico con sistemas tradicionales y de autoatención.",
            "Reconocimiento de los saberes locales y comunitarios sin abandono del rigor metodológico.",
            "Superación del ocultamiento terapéutico mediante una entrevista clínica empática y libre de prejuicios."
        ]),
        ("03", "Bioética y Límites de la Práctica", "Beauchamp & Childress (2019); Ley 292", [
            "Principio de No Maleficencia: prevención de interacciones fitofarmacológicas y riesgos toxicológicos.",
            "Principio de Autonomía: respeto informado a los valores, creencias y decisiones del consultante.",
            "Delimitación Profesional: el psicólogo orienta, psicoeduca y deriva; no prescribe ni formula sustancias."
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
        p_n.font.size = Pt(13.5)
        p_n.font.color.rgb = COLOR_NAVY_TITLE
        p_n.space_after = Pt(2)

        p_a = tf.add_paragraph()
        p_a.text = author
        p_a.font.name = FONT_SANS
        p_a.font.size = Pt(9.5)
        p_a.font.bold = True
        p_a.font.color.rgb = COLOR_TEAL_ACCENT
        p_a.space_after = Pt(12)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"•  {it}"
            p_it.font.name = FONT_SANS
            p_it.font.size = Pt(11)
            p_it.font.color.rgb = COLOR_TEXT_PRIMARY
            p_it.space_after = Pt(8)

    # ==========================================================================
    # SLIDE 7: MARCO TEÓRICO 2 (Marco Jurídico y Evidencia Clínica)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, COLOR_LIGHT_CANVAS)
    add_academic_header(s7, "Capítulo II • Marco Teórico (2/2)", "Marco Normativo Nicaragüense y Evidencia de Eficacia Clínica")
    add_academic_footer(s7, 7)
    add_native_transition(s7)

    col_w7 = Inches(5.6)
    b_l = s7.shapes.add_textbox(Inches(0.85), Inches(1.8), col_w7, Inches(5.0))
    tf_l = b_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p_lt = tf_l.paragraphs[0]
    p_lt.text = "Ordenamiento Jurídico Sanitario Nacional"
    p_lt.font.name = FONT_SERIF
    p_lt.font.bold = True
    p_lt.font.size = Pt(14)
    p_lt.font.color.rgb = COLOR_NAVY_TITLE
    p_lt.space_after = Pt(12)

    leyes = [
        ("Ley No. 774 (2012)", "Medicina Natural, Terapias Complementarias y Productos Naturales", "Institucionaliza la MTCI en el sistema de salud bajo principios de complementariedad, equidad e interculturalidad."),
        ("Ley No. 292 (1998)", "Ley de Medicamentos y Farmacias de Nicaragua", "Límite legal taxativo: inhabilitación expresa para prescribir fármacos o despachar sustancias a quienes no posean título de médico."),
        ("Ley No. 759 (2011)", "Medicina Tradicional Ancestral", "Protege el patrimonio inmaterial y saberes curativos tradicionales de pueblos originarios y comunidades afrodescendientes.")
    ]
    for ley, sub, desc in leyes:
        p = tf_l.add_paragraph()
        r1 = p.add_run()
        r1.text = f"⚖ {ley} — "
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_TEAL_ACCENT
        r2 = p.add_run()
        r2.text = f"{sub}\n"
        r2.font.name = FONT_SANS
        r2.font.bold = True
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_NAVY_TITLE
        r3 = p.add_run()
        r3.text = desc
        r3.font.name = FONT_SANS
        r3.font.size = Pt(10.5)
        r3.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(11)

    add_hairline_v(s7, Inches(6.75), Inches(1.9), Inches(4.7), COLOR_HAIRLINE)

    b_r = s7.shapes.add_textbox(Inches(7.15), Inches(1.8), col_w7, Inches(5.0))
    tf_r = b_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    p_rt = tf_r.paragraphs[0]
    p_rt.text = "Evidencia Clínica y Eficacia Empírica en MTCI"
    p_rt.font.name = FONT_SERIF
    p_rt.font.bold = True
    p_rt.font.size = Pt(14)
    p_rt.font.color.rgb = COLOR_NAVY_TITLE
    p_rt.space_after = Pt(12)

    evidencias = [
        ("Fitoterapia y Respuestas Neuroquímicas", "Ensayos clínicos confirman efectos sedantes y ansiolíticos en fitofármacos como la manzanilla y pasiflora, mediados por modulación gabaérgica."),
        ("Técnicas Mente-Cuerpo y Tono Vagal", "Respiración diafragmática, relajación progresiva y yoga estimulan la activación del nervio vago y la reducción de cortisol sérico."),
        ("Masoterapia y Liberación Miofascial", "La descompresión de contracturas musculares crónicas favorece la reducción del dolor somatomorfo y facilita el procesamiento emocional.")
    ]
    for t, d in evidencias:
        p = tf_r.add_paragraph()
        r1 = p.add_run()
        r1.text = f"✦ {t}\n"
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_BLUE_ROYAL
        r2 = p.add_run()
        r2.text = d
        r2.font.name = FONT_SANS
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(11)

    # ==========================================================================
    # SLIDE 8: DISEÑO METODOLÓGICO 1 (Enfoque, Paradigma y Fases)
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, COLOR_LIGHT_CANVAS)
    add_academic_header(s8, "Capítulo III • Marco Metodológico (1/2)", "Paradigma Pragmático, Enfoque Mixto Secuencial y Fases del Estudio")
    add_academic_footer(s8, 8)
    add_native_transition(s8)

    dim_w = Inches(2.7)
    dims = [
        ("PARADIGMA", "Pragmático", "Articula métodos cuantitativos y cualitativos según su utilidad empírica para fundamentar la propuesta de intervención."),
        ("ENFOQUE", "Mixto Secuencial", "Diseño DEXPLIS (Derivativo): recolección cuantitativa inicial articulada con profundización cualitativa e integración propositiva."),
        ("ALCANCE", "Descriptivo-Transversal", "Caracteriza el estado actual de conocimientos, actitudes y prácticas en un marco temporal definido (segundo semestre 2026)."),
        ("TÉCNICAS", "Multi-Instrumento", "Cuestionarios estructurados con escala Likert (I1, I2, I3), preguntas abiertas y análisis temático de contenido.")
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
        p_tag.font.size = Pt(9)
        p_tag.font.color.rgb = COLOR_TEAL_ACCENT
        p_tag.space_after = Pt(2)

        p_val = tf_d.add_paragraph()
        p_val.text = val
        p_val.font.name = FONT_SERIF
        p_val.font.bold = True
        p_val.font.size = Pt(13.5)
        p_val.font.color.rgb = COLOR_NAVY_TITLE
        p_val.space_after = Pt(5)

        p_desc = tf_d.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_SANS
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = COLOR_TEXT_PRIMARY

    add_hairline_h(s8, Inches(0.85), Inches(4.3), Inches(11.6), COLOR_HAIRLINE)

    f_box = s8.shapes.add_textbox(Inches(0.85), Inches(4.55), Inches(11.6), Inches(2.3))
    tf_f = f_box.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0

    p_ft = tf_f.paragraphs[0]
    p_ft.text = "Fases Metodológicas de la Investigación"
    p_ft.font.name = FONT_SERIF
    p_ft.font.bold = True
    p_ft.font.size = Pt(13.5)
    p_ft.font.color.rgb = COLOR_NAVY_TITLE
    p_ft.space_after = Pt(10)

    fases = [
        ("Fase 1 (Cuantitativa)", "Diagnóstico Estudiantil", "Aplicación de cuestionario estandarizado (I1) a la muestra censal de n = 68 estudiantes de 4.º y 5.º año de Psicología."),
        ("Fase 2 (Cualitativa)", "Inmersión en Actores Clave", "Recolección de percepciones en n = 9 facilitadores locales de Estelí (I2) y n = 9 docentes-psicólogos del CUR-Estelí (I3)."),
        ("Fase 3 (Propositiva)", "Construcción del Manual", "Triangulación metodológica de hallazgos para el diseño modular del Manual de Estrategias MTCI (Anexo 16.2).")
    ]
    for f_nom, f_sub, f_det in fases:
        p = tf_f.add_paragraph()
        r1 = p.add_run()
        r1.text = f"▶ {f_nom} • {f_sub}: "
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_GOLD_ACCENT
        r2 = p.add_run()
        r2.text = f_det
        r2.font.name = FONT_SANS
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(6)

    # ==========================================================================
    # SLIDE 9: DISEÑO METODOLÓGICO 2 (Población, Muestra y Criterios)
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, COLOR_LIGHT_CANVAS)
    add_academic_header(s9, "Capítulo III • Marco Metodológico (2/2)", "Delimitación Muestral Consolidada (N = 86) y Criterios de Selección")
    add_academic_footer(s9, 9)
    add_native_transition(s9)

    col_w9 = Inches(3.65)
    grupos = [
        ("ESTUDIANTES", "n = 68", COLOR_TEAL_ACCENT, [
            ("Muestra Censal", "Totalidad de estudiantes activos de 4.º año (n = 53, 77.9%) y 5.º año (n = 15, 22.1%)."),
            ("Criterio Inclusión", "Matrícula activa en el II Semestre 2026; cursando o habiendo cursado prácticas en la Clínica Psicosocial."),
            ("Criterio Exclusión", "Estudiantes de 1.º a 3.er año o con inactividad académica temporal.")
        ]),
        ("FACILITADORES", "n = 9", COLOR_GOLD_ACCENT, [
            ("Muestreo Intencional", "Diversidad de saberes: masoterapia, fitoterapia, quiropraxia y medicina tradicional en Estelí."),
            ("Criterio Inclusión", "Práctica activa continua mayor a 5 años en el municipio de Estelí con clientela establecida."),
            ("Criterio Exclusión", "Comercializadores ambulantes sin arraigo comunitario reconocido.")
        ]),
        ("DOCENTES", "n = 9", COLOR_BLUE_ROYAL, [
            ("Claustro de Psicología", "Docentes con grado de Licenciatura y Maestría en áreas clínicas, comunitarias y metodológicas."),
            ("Criterio Inclusión", "Docencia activa en el CUR-Estelí y experiencia en supervisión de prácticas formativas."),
            ("Criterio Exclusión", "Docentes de otras disciplinas no vinculadas a la carrera de Psicología.")
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
        p_g.font.size = Pt(12)
        p_g.font.color.rgb = COLOR_NAVY_TITLE
        p_g.space_after = Pt(12)

        for tag, desc in items:
            p_it = tf_g.add_paragraph()
            r1 = p_it.add_run()
            r1.text = f"• {tag}: "
            r1.font.name = FONT_SANS
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = COLOR_NAVY_TITLE
            r2 = p_it.add_run()
            r2.text = desc
            r2.font.name = FONT_SANS
            r2.font.size = Pt(10.5)
            r2.font.color.rgb = COLOR_TEXT_PRIMARY
            p_it.space_after = Pt(9)

    # ==========================================================================
    # SLIDE 10: RESULTADOS ESTUDIANTES 1 (Perfil y Dominio Normativo)
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, COLOR_LIGHT_CANVAS)
    add_academic_header(s10, "Capítulo IV • Resultados en Estudiantes (1/2)", "Perfil Sociodemográfico y Grado de Dominio Conceptual y Normativo")
    add_academic_footer(s10, 10)
    add_native_transition(s10)

    # Left: Embedding Figura 4 (Dominio Conceptual y Normativo)
    if os.path.exists(FIG_04_PATH):
        s10.shapes.add_picture(FIG_04_PATH, Inches(0.85), Inches(1.75), width=Inches(6.2))

    # Right: Interpretación Estadística y Sociodemográfica
    r_box10 = s10.shapes.add_textbox(Inches(7.35), Inches(1.75), Inches(5.1), Inches(5.1))
    tf_r10 = r_box10.text_frame
    tf_r10.word_wrap = True
    tf_r10.margin_left = tf_r10.margin_right = tf_r10.margin_top = tf_r10.margin_bottom = 0

    p_t10 = tf_r10.paragraphs[0]
    p_t10.text = "Hallazgos en la Muestra Estudiantil (n = 68)"
    p_t10.font.name = FONT_SERIF
    p_t10.font.bold = True
    p_t10.font.size = Pt(14)
    p_t10.font.color.rgb = COLOR_NAVY_TITLE
    p_t10.space_after = Pt(12)

    pts_est1 = [
        ("Perfil Demográfico Consolidado", "Marcada feminización (82.4% mujeres, n = 56) y concentración en adultos jóvenes de 20 a 22 años (61.8%). El 77.9% cursa 4.º año enfrentando el inicio de la práctica clínica supervisada."),
        ("Acierto Conceptual Técnico (67.6%)", "La mayoría identifica correctamente la definición de MTCI de la OMS, reconociéndola como saberes de salud integral; no obstante, el 75.0% declara familiaridad práctica baja o nula."),
        ("Brecha Normativa Ley No. 774 (58.8%)", "El 58.8% desconoce el propósito integrador de la ley de medicina natural o sostiene concepciones distorsionadas sobre su alcance en el sistema de salud."),
        ("Vacío Legal Crítico Ley No. 292 (64.7%)", "Apenas el 35.3% reconoce con precisión la inhabilitación taxativa del psicólogo para prescribir fármacos, evidenciando una urgente necesidad de formación deontológica.")
    ]
    for h, d in pts_est1:
        p = tf_r10.add_paragraph()
        r1 = p.add_run()
        r1.text = f"✦ {h}:\n"
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_TEAL_ACCENT
        r2 = p.add_run()
        r2.text = d
        r2.font.name = FONT_SANS
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(8)

    # ==========================================================================
    # SLIDE 11: RESULTADOS ESTUDIANTES 2 (Frecuencia, Bienestar y Paradoja)
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11, COLOR_LIGHT_CANVAS)
    add_academic_header(s11, "Capítulo IV • Resultados en Estudiantes (2/2)", "Frecuencia de Uso, Bienestar Percibido y Brecha Formativa (OE1)")
    add_academic_footer(s11, 11)
    add_native_transition(s11)

    # Left: Big Stats Flotantes
    stats_w = Inches(4.8)
    s_box = s11.shapes.add_textbox(Inches(0.85), Inches(1.75), stats_w, Inches(5.1))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0

    big_stats = [
        ("89.7%", COLOR_TEAL_ACCENT, "Pertinencia Clínica Asistencial", "Considera necesario y conveniente incorporar la MTCI como complemento en el ejercicio de la psicología."),
        ("88.2%", COLOR_ALERT_CRIMSON, "Preparación Insuficiente para Derivación", "Reconoce poseer preparación nula o insuficiente para derivar pacientes hacia facilitadores autorizados."),
        ("86.8%", COLOR_GOLD_ACCENT, "Preparación Insuficiente para Psicoeducación", "Autopercibe competencias nulas o insuficientes para orientar a consultantes sobre el uso de terapias tradicionales.")
    ]
    for val, col, title, desc in big_stats:
        p_val = tf_s.add_paragraph() if tf_s.paragraphs[0].text else tf_s.paragraphs[0]
        p_val.text = val
        p_val.font.name = FONT_SERIF
        p_val.font.bold = True
        p_val.font.size = Pt(36)
        p_val.font.color.rgb = col

        p_t = tf_s.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_SANS
        p_t.font.bold = True
        p_t.font.size = Pt(11.5)
        p_t.font.color.rgb = COLOR_NAVY_TITLE

        p_d = tf_s.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_SANS
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = COLOR_TEXT_PRIMARY
        p_d.space_after = Pt(10)

    # Right: Embedding Figura 7
    if os.path.exists(FIG_07_PATH):
        s11.shapes.add_picture(FIG_07_PATH, Inches(6.0), Inches(1.75), width=Inches(6.4))

    u_box = s11.shapes.add_textbox(Inches(6.0), Inches(5.5), Inches(6.4), Inches(1.4))
    tf_u = u_box.text_frame
    tf_u.word_wrap = True
    tf_u.margin_left = tf_u.margin_right = tf_u.margin_top = tf_u.margin_bottom = 0

    pu_t = tf_u.paragraphs[0]
    pu_t.text = "Uso Personal Reactivo y Efectos en el Bienestar:"
    pu_t.font.name = FONT_SANS
    pu_t.font.bold = True
    pu_t.font.size = Pt(11)
    pu_t.font.color.rgb = COLOR_NAVY_TITLE
    pu_t.space_after = Pt(3)

    pu_d = tf_u.add_paragraph()
    pu_d.text = "• Carácter Reactivo: 52.9% no utiliza MTCI de forma preventiva regular; acuden solo ante sobrecarga académica.\n• Eficacia en Usuarios (n = 30): 86.7% reporta alivio muscular y serenidad; 0.0% reporta efectos adversos."
    pu_d.font.name = FONT_SANS
    pu_d.font.size = Pt(10.5)
    pu_d.font.color.rgb = COLOR_TEXT_PRIMARY

    # ==========================================================================
    # SLIDE 12: RESULTADOS FACILITADORES LOCALES (CON FIGURAS 12 Y 14)
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12, COLOR_LIGHT_CANVAS)
    add_academic_header(s12, "Capítulo IV • Resultados en Facilitadores Locales", "Modalidades Terapéuticas, Eficacia Somática y Barreras en Estelí (OE2)")
    add_academic_footer(s12, 12)
    add_native_transition(s12)

    # Left: Embedding Figura 12 (Modalidades de MTCI)
    if os.path.exists(FIG_12_PATH):
        s12.shapes.add_picture(FIG_12_PATH, Inches(0.85), Inches(1.75), width=Inches(5.8))

    # Right: Embedding Figura 14 (Apertura Emocional) + Datos de Campo
    if os.path.exists(FIG_14_PATH):
        s12.shapes.add_picture(FIG_14_PATH, Inches(7.2), Inches(1.75), width=Inches(3.2))

    fac_desc_box = s12.shapes.add_textbox(Inches(7.0), Inches(4.5), Inches(5.5), Inches(2.3))
    tf_fd = fac_desc_box.text_frame
    tf_fd.word_wrap = True
    tf_fd.margin_left = tf_fd.margin_right = tf_fd.margin_top = tf_fd.margin_bottom = 0

    p_fdt = tf_fd.paragraphs[0]
    p_fdt.text = "Hallazgos Empíricos en Facilitadores de Estelí (n = 9):"
    p_fdt.font.name = FONT_SANS
    p_fdt.font.bold = True
    p_fdt.font.size = Pt(11)
    p_fdt.font.color.rgb = COLOR_NAVY_TITLE
    p_fdt.space_after = Pt(4)

    pts_fac_emp = [
        ("100% Alivio de Estrés Somático", "Constatan descompresión miofascial inmediata y recuperación de calma psicofisiológica en consultantes."),
        ("88.9% Apertura Emocional", "El desbloqueo corporal incrementa la receptividad reflexiva y facilita el diálogo terapéutico posterior."),
        ("Inocuidad Percibida (100%)", "Cero reporte de reacciones adversas o crisis emocionales iatrogénicas en los consultorios."),
        ("Barreras Socioculturales y Económicas", "El 77.8% enfrenta ocasionalmente reservas religiosas y el 77.8% señala que la falta de recursos interrumpe el tratamiento.")
    ]
    for h, d in pts_fac_emp:
        p = tf_fd.add_paragraph()
        r1 = p.add_run()
        r1.text = f"✦ {h}: "
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL_ACCENT
        r2 = p.add_run()
        r2.text = d
        r2.font.name = FONT_SANS
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(3)

    # ==========================================================================
    # SLIDE 13: RESULTADOS CLAUSTRO DOCENTE (CON FIGURAS 24 Y 25)
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13, COLOR_LIGHT_CANVAS)
    add_academic_header(s13, "Capítulo IV • Resultados en el Claustro Docente", "Estrategias Pedagógicas, Didáctica Vivencial y Consenso Ético (OE3)")
    add_academic_footer(s13, 13)
    add_native_transition(s13)

    # Left: Embedding Figura 24 (Estrategias Pedagógicas Priorizadas)
    if os.path.exists(FIG_24_PATH):
        s13.shapes.add_picture(FIG_24_PATH, Inches(0.85), Inches(1.75), width=Inches(5.7))

    # Right: Embedding Figura 25 (Experiencias Formativas Favorables)
    if os.path.exists(FIG_25_PATH):
        s13.shapes.add_picture(FIG_25_PATH, Inches(6.9), Inches(1.75), width=Inches(5.6))

    # Bottom Analysis for Teachers
    doc_an_box = s13.shapes.add_textbox(Inches(0.85), Inches(5.35), Inches(11.6), Inches(1.5))
    tf_da = doc_an_box.text_frame
    tf_da.word_wrap = True
    tf_da.margin_left = tf_da.margin_right = tf_da.margin_top = tf_da.margin_bottom = 0

    p_dat = tf_da.paragraphs[0]
    p_dat.text = "Criterios Rectores del Claustro Docente de Psicología (n = 9):"
    p_dat.font.name = FONT_SANS
    p_dat.font.bold = True
    p_dat.font.size = Pt(11)
    p_dat.font.color.rgb = COLOR_BLUE_ROYAL
    p_dat.space_after = Pt(4)

    pts_doc_emp = [
        "100.0% Respaldo Curricular: Apoyo unánime a la incorporación transversal de la MTCI bajo un enfoque científico y no prescriptivo.",
        "Pedagogía Vivencial (88.9%): Priorizan talleres de autorregulación somática y descartaron la enseñanza puramente teórica o abstracta.",
        "Vinculación Territorial (77.8%): Respaldan intercambios directos con facilitadores tradicionales y visitas a centros MINSA (66.7%).",
        "Demanda Institucional: 77.8% del profesorado solicita capacitación continua en neurobiología somática y la creación de un Comité de Bioética."
    ]
    for it in pts_doc_emp:
        p = tf_da.add_paragraph()
        p.text = f"• {it}"
        p.font.name = FONT_SANS
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(2)

    # ==========================================================================
    # SLIDE 14: PROPUESTA MANUAL DE ESTRATEGIAS MTCI
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14, COLOR_LIGHT_CANVAS)
    add_academic_header(s14, "Capítulo V • Propuesta de Intervención (OE3)", "Manual de Estrategias de MTCI para la Formación y Práctica Psicológica")
    add_academic_footer(s14, 14)
    add_native_transition(s14)

    if os.path.exists(MANUAL_COVER_PATH):
        s14.shapes.add_picture(MANUAL_COVER_PATH, Inches(0.85), Inches(1.8), width=Inches(3.8))

    fc_box = s14.shapes.add_textbox(Inches(0.85), Inches(4.3), Inches(3.8), Inches(2.5))
    tf_fc = fc_box.text_frame
    tf_fc.word_wrap = True
    tf_fc.margin_left = tf_fc.margin_right = tf_fc.margin_top = tf_fc.margin_bottom = 0

    p_fc_t = tf_fc.paragraphs[0]
    p_fc_t.text = "FICHA TÉCNICA DEL MANUAL (ANEXO 16.2)"
    p_fc_t.font.name = FONT_SANS
    p_fc_t.font.bold = True
    p_fc_t.font.size = Pt(10)
    p_fc_t.font.color.rgb = COLOR_TEAL_ACCENT
    p_fc_t.space_after = Pt(4)

    fc_items = [
        "Extensión: 18 páginas in extenso (Capítulo 16, Anexo 16.2).",
        "Destinatarios: Estudiantes y docentes de la Clínica Psicosocial.",
        "Propósito: Dotar de discernimiento bioético para orientar y derivar, sin habilitar como terapeutas alternativos.",
        "Instrumento Anexo: Cuestionario I-CAM-Q adaptado transculturalmente para tamizaje clínico en Nicaragua."
    ]
    for it in fc_items:
        p = tf_fc.add_paragraph()
        p.text = f"• {it}"
        p.font.name = FONT_SANS
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(3)

    add_hairline_v(s14, Inches(4.9), Inches(1.9), Inches(4.7), COLOR_HAIRLINE)

    m_box = s14.shapes.add_textbox(Inches(5.2), Inches(1.8), Inches(7.3), Inches(5.0))
    tf_m = m_box.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0

    p_mt = tf_m.paragraphs[0]
    p_mt.text = "Estructura Modular del Manual (8 Módulos Temáticos)"
    p_mt.font.name = FONT_SERIF
    p_mt.font.bold = True
    p_mt.font.size = Pt(14)
    p_mt.font.color.rgb = COLOR_NAVY_TITLE
    p_mt.space_after = Pt(10)

    modulos = [
        ("Módulo 1", "Fundamentos y Marco Legal", "Definición OMS (2025) y articulación de Leyes 774, 759 y 292 de Nicaragua."),
        ("Módulo 2", "Principios Deontológicos", "Consentimiento informado intercultural y complementariedad sin sustitución médica."),
        ("Módulo 3", "Mapa Clínico de Prácticas", "Clasificación en 4 niveles: uso directo, psicoeducación, precaución y alerta."),
        ("Módulo 4", "Algoritmo de Derivación", "Protocolo secuencial de 4 pasos para derivación clínica informada."),
        ("Módulo 5", "Habilidades de Diálogo", "Técnicas de entrevista abierta para erradicar el ocultamiento terapéutico."),
        ("Módulo 6", "Red Intersectorial", "Criterios de referencia bidireccional y trabajo coordinado con facilitadores."),
        ("Módulo 7", "Ruta Pedagógica", "Secuencia de 3 etapas vivenciales y propuesta de asignatura electiva."),
        ("Módulo 8", "Soporte Institucional", "Creación del Comité de Bioética y plan de capacitación docente continua.")
    ]
    for mod, nom, desc in modulos:
        p = tf_m.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{mod} • {nom}: "
        r1.font.name = FONT_SANS
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_GOLD_ACCENT
        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_SANS
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(5)

    # ==========================================================================
    # SLIDE 15: CONCLUSIONES CENTRALES
    # ==========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15, COLOR_LIGHT_CANVAS)
    add_academic_header(s15, "Capítulo VI • Conclusiones y Recomendaciones", "Conclusiones Centrales de la Investigación (Triangulación de Objetivos)")
    add_academic_footer(s15, 15)
    add_native_transition(s15)

    concl_box = s15.shapes.add_textbox(Inches(0.85), Inches(1.8), Inches(11.6), Inches(5.0))
    tf_c = concl_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

    conclusiones = [
        ("01", "Cumplimiento del Objetivo General", "Los tres colectivos investigados (N = 86) validan unánimemente a la MTCI como recurso complementario legítimo en salud mental, condicionado a un ejercicio bioético, científico y respetuoso de los límites profesionales."),
        ("02", "Brecha Formativa en Estudiantes (OE1)", "El estudiantado posee buen dominio conceptual (67.6%) y alta satisfacción somática personal (86.7%), pero padece desinformación legal (58.8% desconoce Ley 774; 64.7% desconoce Ley 292) e inseguridad para derivar (88.2%)."),
        ("03", "Aporte Somático de Facilitadores (OE2)", "Los terapeutas locales de Estelí constatan 100% de alivio de sobrecarga muscular y mayor apertura reflexiva (88.9%), enfrentando barreras de estigma sociocultural (77.8%) y limitaciones económicas de los usuarios (77.8%)."),
        ("04", "Consenso Curricular Docente (OE3)", "El 100% del claustro apoya transversalizar la MTCI mediante talleres vivenciales (88.9%) e intercambio comunitario, demandando actualización en neurobiología somática y comités de bioética."),
        ("05", "Logro Propositivo del Manual de Estrategias", "Se formuló con éxito el Manual de Estrategias MTCI de 18 páginas (Anexo 16.2), dotando al CUR-Estelí de algoritmos de decisión clínica, pautas contra el ocultamiento y el inventario I-CAM-Q.")
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
        r_h.font.size = Pt(11.5)
        r_h.font.color.rgb = COLOR_NAVY_TITLE

        r_b = p.add_run()
        r_b.text = body
        r_b.font.name = FONT_SANS
        r_b.font.size = Pt(11)
        r_b.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(10)

    # ==========================================================================
    # SLIDE 16: RECOMENDACIONES ESTRATÉGICAS
    # ==========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16, COLOR_LIGHT_CANVAS)
    add_academic_header(s16, "Capítulo VI • Conclusiones y Recomendaciones", "Recomendaciones Estratégicas para la Formación, Práctica e Intersectorialidad")
    add_academic_footer(s16, 16)
    add_native_transition(s16)

    add_hairline_h(s16, Inches(0.85), Inches(4.35), Inches(11.6), COLOR_HAIRLINE)
    add_hairline_v(s16, Inches(6.65), Inches(1.85), Inches(4.9), COLOR_HAIRLINE)

    quad_w = Inches(5.5)
    quads = [
        (Inches(0.85), Inches(1.85), "PARA EL ESTAMENTO ESTUDIANTIL", COLOR_TEAL_ACCENT, [
            ("Límites Legales", "Respetar estrictamente las Leyes 774 y 292 (prohibición terminante de formular fármacos)."),
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
        q_box = s16.shapes.add_textbox(left, top, quad_w, Inches(2.4))
        tf_q = q_box.text_frame
        tf_q.word_wrap = True
        tf_q.margin_left = tf_q.margin_right = tf_q.margin_top = tf_q.margin_bottom = 0

        p_t = tf_q.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_SANS
        p_t.font.bold = True
        p_t.font.size = Pt(10.5)
        p_t.font.color.rgb = col
        p_t.space_after = Pt(5)

        for tag, desc in bullets:
            p_b = tf_q.add_paragraph()
            r1 = p_b.add_run()
            r1.text = f"✓ {tag}: "
            r1.font.name = FONT_SANS
            r1.font.bold = True
            r1.font.size = Pt(10)
            r1.font.color.rgb = COLOR_NAVY_TITLE
            r2 = p_b.add_run()
            r2.text = desc
            r2.font.name = FONT_SANS
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = COLOR_TEXT_PRIMARY
            p_b.space_after = Pt(2)

    # ==========================================================================
    # SLIDE 17: CIERRE INSTITUCIONAL
    # ==========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s17, COLOR_DARK_CANVAS)
    add_native_transition(s17)

    if os.path.exists(SHIELD_PATH):
        s17.shapes.add_picture(SHIELD_PATH, Inches(5.85), Inches(0.85), height=Inches(1.5))

    cierre_box = s17.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(11.3), Inches(2.4))
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
    p_lema.font.color.rgb = RGBColor(245, 158, 11)
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

    add_hairline_h(s17, Inches(1.5), Inches(5.1), Inches(10.3), RGBColor(30, 41, 59))

    f_box17 = s17.shapes.add_textbox(Inches(1.5), Inches(5.35), Inches(10.3), Inches(1.5))
    tf_f17 = f_box17.text_frame
    tf_f17.word_wrap = True
    tf_f17.margin_left = tf_f17.margin_right = tf_f17.margin_top = tf_f17.margin_bottom = 0

    p_t_cie = tf_f17.paragraphs[0]
    p_t_cie.alignment = PP_ALIGN.CENTER
    p_t_cie.text = "Sustentantes: Dina Fabiola García Torres • Tatiana Paola López Ramos • Engel Enoc Zamora Velásquez"
    p_t_cie.font.name = FONT_SANS
    p_t_cie.font.size = Pt(11)
    p_t_cie.font.bold = True
    p_t_cie.font.color.rgb = COLOR_WHITE
    p_t_cie.space_after = Pt(4)

    p_tut_cie = tf_f17.add_paragraph()
    p_tut_cie.alignment = PP_ALIGN.CENTER
    p_tut_cie.text = "Tutoría Académica: Dra. Tania Libertad Pérez Guevara | Carrera de Licenciatura en Psicología • CUR-Estelí"
    p_tut_cie.font.name = FONT_SANS
    p_tut_cie.font.size = Pt(10.5)
    p_tut_cie.font.color.rgb = RGBColor(20, 184, 166)

    output_minimal = "Presentacion_Defensa_Tesis_MTCI_UNAN_Minimal.pptx"
    output_main    = "Presentacion_Defensa_Tesis_MTCI_UNAN.pptx"
    prs.save(output_minimal)
    prs.save(output_main)
    print(f"Presentation saved successfully to: {output_minimal} and {output_main} (17 slides)")

if __name__ == "__main__":
    create_presentation()
