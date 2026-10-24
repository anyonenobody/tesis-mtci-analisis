import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# MODERN EDITORIAL DESIGN SYSTEM (Anthropic PPTX Standards & Academic Rigor)
# ==============================================================================
COLOR_DARK_CANVAS  = RGBColor(10, 25, 47)       # #0A192F Midnight Executive Navy (Slides 1 & 16)
COLOR_DARK_CARD    = RGBColor(17, 34, 64)       # #112240 Contrast Card for Dark Canvas
COLOR_DARK_BORDER  = RGBColor(30, 58, 138)      # #1E3A8A Dark Card Border

COLOR_LIGHT_CANVAS = RGBColor(255, 255, 255)    # #FFFFFF Pristine Light Canvas (Slides 2-15)
COLOR_CARD_LIGHT   = RGBColor(248, 250, 252)    # #F8FAFC Subtle Tinted Card
COLOR_BORDER_LIGHT = RGBColor(226, 232, 240)    # #E2E8F0 Clean Architectural Border

COLOR_NAVY_TITLE   = RGBColor(15, 32, 67)       # #0F2043 High-Authority Navy
COLOR_TEAL_ACCENT  = RGBColor(13, 110, 93)      # #0D6E5D Traditional Medicine / Nature
COLOR_GOLD_ACCENT  = RGBColor(217, 119, 6)      # #D97706 Warm Amber Gold
COLOR_ALERT_RED    = RGBColor(185, 28, 28)      # #B91C1C Deontological Limit / Alert

COLOR_TEXT_PRIMARY = RGBColor(30, 41, 59)       # #1E293B High Contrast Slate Dark
COLOR_TEXT_MUTED   = RGBColor(100, 116, 139)    # #64748B Secondary Slate Text
COLOR_WHITE        = RGBColor(255, 255, 255)

# Soft Tint Fills
COLOR_TINT_BLUE    = RGBColor(239, 246, 255)    # #EFF6FF
COLOR_TINT_TEAL    = RGBColor(240, 253, 250)    # #F0FDF4
COLOR_TINT_GOLD    = RGBColor(254, 243, 199)    # #FEF3C7
COLOR_TINT_ALERT   = RGBColor(254, 242, 242)    # #FEF2F2

# Typography Pairing: Editorial Serif Headers + Clean Sans Body
FONT_SERIF = "Cambria"
FONT_SANS  = "Calibri"

LOGO_CLEAN_PATH   = "assets/extracted/unan_logo_clean.png"
SHIELD_PATH       = "assets/extracted/unan_shield_only.png"
MANUAL_COVER_PATH = "assets/extracted/portada_manual.jpg"

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

    def add_slide_header(slide, category_text, title_text):
        """Adds modern editorial header with generous whitespace, NO AI accent lines."""
        eb_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.52), Inches(10.5), Inches(0.32))
        tf_eb = eb_box.text_frame
        tf_eb.word_wrap = True
        tf_eb.margin_left = tf_eb.margin_right = tf_eb.margin_top = tf_eb.margin_bottom = 0
        p_eb = tf_eb.paragraphs[0]
        p_eb.text = category_text.upper()
        p_eb.font.name = FONT_SANS
        p_eb.font.size = Pt(10)
        p_eb.font.bold = True
        p_eb.font.color.rgb = COLOR_TEAL_ACCENT

        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.82), Inches(10.8), Inches(0.65))
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
            slide.shapes.add_picture(SHIELD_PATH, Inches(12.1), Inches(0.48), height=Inches(0.85))

    def add_slide_footer(slide, current_num, total_slides=16):
        """Minimal clean footer with breathing room."""
        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(10.5), Inches(0.3))
        tf = f_box.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "UNAN-Managua • CUR-Estelí | Carrera de Psicología • Segundo Semestre 2026"
        p.font.name = FONT_SANS
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MUTED

        n_box = slide.shapes.add_textbox(Inches(11.8), Inches(7.05), Inches(0.7), Inches(0.3))
        tf_n = n_box.text_frame
        tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
        pn = tf_n.paragraphs[0]
        pn.alignment = PP_ALIGN.RIGHT
        pn.text = f"{current_num} / {total_slides}"
        pn.font.name = FONT_SANS
        pn.font.size = Pt(9)
        pn.font.bold = True
        pn.font.color.rgb = COLOR_NAVY_TITLE

    # ==========================================================================
    # SLIDE 1: PORTADA INSTITUCIONAL (DARK CANVAS - PRESTIGIO ACADÉMICO)
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, COLOR_DARK_CANVAS)

    if os.path.exists(LOGO_CLEAN_PATH):
        s1.shapes.add_picture(LOGO_CLEAN_PATH, Inches(0.8), Inches(0.6), height=Inches(1.05))

    uni_tb = s1.shapes.add_textbox(Inches(3.3), Inches(0.65), Inches(9.2), Inches(0.95))
    tf_u = uni_tb.text_frame
    tf_u.word_wrap = True
    tf_u.margin_left = tf_u.margin_right = tf_u.margin_top = tf_u.margin_bottom = 0
    p = tf_u.paragraphs[0]
    p.text = "UNIVERSIDAD NACIONAL AUTÓNOMA DE NICARAGUA, MANAGUA"
    p.font.name = FONT_SANS
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    p = tf_u.add_paragraph()
    p.text = "CENTRO UNIVERSITARIO REGIONAL DE ESTELÍ • RECINTO LEONEL RUGAMA RUGAMA"
    p.font.name = FONT_SANS
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_ACCENT

    p = tf_u.add_paragraph()
    p.text = "Departamento de Educación y Humanidades | Carrera de Psicología"
    p.font.name = FONT_SANS
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(148, 163, 184)

    title_tb = s1.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(11.733), Inches(2.3))
    tf_main = title_tb.text_frame
    tf_main.word_wrap = True
    tf_main.margin_left = tf_main.margin_right = tf_main.margin_top = tf_main.margin_bottom = 0

    p = tf_main.paragraphs[0]
    p.text = "TRABAJO DE INVESTIGACIÓN PARA OPTAR AL GRADO DE LICENCIADOS EN PSICOLOGÍA"
    p.font.name = FONT_SANS
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(45, 212, 191)
    p.space_after = Pt(12)

    p = tf_main.add_paragraph()
    p.text = "La Medicina Tradicional, Complementaria e Integrativa (MTCI) como Complemento en la Atención Psicológica"
    p.font.name = FONT_SERIF
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(14)

    p = tf_main.add_paragraph()
    p.text = "Estudio Mixto con Estudiantes y Docentes del CUR-Estelí y Facilitadores Locales del Municipio de Estelí"
    p.font.name = FONT_SANS
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_ACCENT

    col_w1 = Inches(3.75)
    gap1 = Inches(0.24)
    meta_top1 = Inches(4.8)
    meta_h1 = Inches(1.9)

    # 1. Autores
    c_s = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), meta_top1, col_w1, meta_h1)
    c_s.adjustments[0] = 0.04; c_s.fill.solid(); c_s.fill.fore_color.rgb = COLOR_DARK_CARD; c_s.line.color.rgb = COLOR_DARK_BORDER
    tf = c_s.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.margin_left = Inches(0.25); tf.margin_right = Inches(0.2)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "AUTORES / SUSTENTANTES"; p.font.name = FONT_SANS; p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = COLOR_GOLD_ACCENT; p.space_after = Pt(8)
    for n in ["• Dina Fabiola García Torres", "• Tatiana Paola López Ramos", "• Engel Enoc Zamora Velásquez"]:
        p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = n; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.color.rgb = COLOR_WHITE; p.space_after = Pt(4)

    # 2. Tutoría
    c_t = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + col_w1 + gap1, meta_top1, col_w1, meta_h1)
    c_t.adjustments[0] = 0.04; c_t.fill.solid(); c_t.fill.fore_color.rgb = COLOR_DARK_CARD; c_t.line.color.rgb = COLOR_DARK_BORDER
    tf = c_t.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.margin_left = Inches(0.25); tf.margin_right = Inches(0.2)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "TUTORÍA ACADÉMICA"; p.font.name = FONT_SANS; p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = RGBColor(45, 212, 191); p.space_after = Pt(8)
    p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "• Dra. Tania Libertad Pérez Guevara"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.space_after = Pt(4)
    p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "Docente Investigadora • CUR-Estelí\nAsesoría Temática y Metodológica"; p.font.name = FONT_SANS; p.font.size = Pt(10.5); p.font.color.rgb = RGBColor(148, 163, 184)

    # 3. Grado & Fecha
    c_g = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + (col_w1 + gap1)*2, meta_top1, col_w1, meta_h1)
    c_g.adjustments[0] = 0.04; c_g.fill.solid(); c_g.fill.fore_color.rgb = COLOR_DARK_CARD; c_g.line.color.rgb = COLOR_DARK_BORDER
    tf = c_g.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.margin_left = Inches(0.25); tf.margin_right = Inches(0.2)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "DEFENSA DE GRADO"; p.font.name = FONT_SANS; p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = COLOR_GOLD_ACCENT; p.space_after = Pt(8)
    p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "Licenciatura en Psicología\nLínea SAL-3 (Salud e Interculturalidad)\nEstelí, Nicaragua • Octubre, 2026"; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.color.rgb = COLOR_WHITE; p.space_after = Pt(4)

    # ==========================================================================
    # SLIDE 2: PLANTEAMIENTO DEL PROBLEMA Y JUSTIFICACIÓN
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, COLOR_LIGHT_CANVAS)
    add_slide_header(s2, "Capítulo I • Planteamiento del Problema", "Encrucijada Asistencial, Vacío Formativo y Pertinencia Social")
    add_slide_footer(s2, 2)

    col_w2 = Inches(5.7)
    card_top = Inches(1.7)
    card_h = Inches(5.1)

    # Left: Planteamiento del Problema
    card_prob = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_top, col_w2, card_h)
    card_prob.adjustments[0] = 0.025; card_prob.fill.solid(); card_prob.fill.fore_color.rgb = COLOR_CARD_LIGHT; card_prob.line.color.rgb = COLOR_BORDER_LIGHT

    tb_p = s2.shapes.add_textbox(Inches(1.1), Inches(1.95), col_w2 - Inches(0.6), Inches(4.6))
    tf_p = tb_p.text_frame; tf_p.word_wrap = True; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0

    p = tf_p.paragraphs[0]; p.text = "PLANTEAMIENTO DEL PROBLEMA"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(14)

    prob_points = [
        ("Asimetría Normativa:", "La Ley 774 garantiza el acceso a MTCI como derecho, mientras la Ley 292 prohíbe tajantemente prescribir fármacos a psicólogos."),
        ("El Ocultamiento Terapéutico:", "Los consultantes utilizan medicina natural pero lo silencian en sesión clínica por temor al rechazo o censura del terapeuta."),
        ("Vacío Curricular Crítico:", "Los futuros graduados egresan sin pautas bioéticas para dialogar, psicoeducar o realizar derivaciones oportunas."),
        ("Pregunta de Investigación:", "¿Cómo fundamenta el diagnóstico de MTCI en Estelí el diseño de un manual ético y pedagógico para Psicología?")
    ]
    for b_title, b_desc in prob_points:
        p = tf_p.add_paragraph(); p.space_after = Pt(14); p.line_spacing = 1.2
        r1 = p.add_run(); r1.text = b_title + " "; r1.font.bold = True; r1.font.size = Pt(12.5); r1.font.color.rgb = COLOR_NAVY_TITLE
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(12); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    # Right: Justificación
    card_just = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), card_top, col_w2, card_h)
    card_just.adjustments[0] = 0.025; card_just.fill.solid(); card_just.fill.fore_color.rgb = COLOR_CARD_LIGHT; card_just.line.color.rgb = COLOR_BORDER_LIGHT

    tb_j = s2.shapes.add_textbox(Inches(7.133), Inches(1.95), col_w2 - Inches(0.6), Inches(4.6))
    tf_j = tb_j.text_frame; tf_j.word_wrap = True; tf_j.margin_left = tf_j.margin_right = tf_j.margin_top = tf_j.margin_bottom = 0

    p = tf_j.paragraphs[0]; p.text = "JUSTIFICACIÓN Y RELEVANCIA"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT; p.space_after = Pt(14)

    just_points = [
        ("Ética y No Maleficencia:", "Conocer las prácticas tradicionales del consultante protege la seguridad clínica y evita interacciones adversas."),
        ("Salud Mental Comunitaria:", "Reconoce y articula la memoria etnobotánica viva y el rol de los facilitadores locales de Estelí."),
        ("Impacto Formativo Directo:", "Dota a estudiantes de 4.° y 5.° año de criterios claros para sus prácticas en la Clínica Psicosocial del CUR-Estelí."),
        ("Aporte Propositivo Concreto:", "Formaliza el primer Manual de Estrategias MTCI (18 págs.) como guía pedagógica y bioética institucional.")
    ]
    for b_title, b_desc in just_points:
        p = tf_j.add_paragraph(); p.space_after = Pt(14); p.line_spacing = 1.2
        r1 = p.add_run(); r1.text = b_title + " "; r1.font.bold = True; r1.font.size = Pt(12.5); r1.font.color.rgb = COLOR_TEAL_ACCENT
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(12); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    # ==========================================================================
    # SLIDE 3: ANTECEDENTES EMPÍRICOS (3 PILARES CON RESPIRO VISUAL)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, COLOR_LIGHT_CANVAS)
    add_slide_header(s3, "Capítulo I • Estado del Arte", "Esquema de Antecedentes Empíricos: Internacional, Nacional y Local")
    add_slide_footer(s3, 3)

    col_w3 = Inches(3.75)
    gap3 = Inches(0.24)

    antecedentes = [
        ("INTERNACIONAL", COLOR_NAVY_TITLE, [
            ("Chafloque-Capuñay et al. (2025):", "Revisión cualitativa (22 estudios). Los pacientes acuden a MTCI buscando escucha empática, autonomía y un trato horizontal ausente en el modelo biomédico."),
            ("Ortega Cadena et al. (2023):", "Estudio en Colombia: el reduccionismo patologiza saberes populares y fractura la comunicación con el consultante."),
            ("Estrategia OMS (2025):", "Insta a integrar medicinas tradicionales seguras y con evidencia en la atención primaria de salud mental.")
        ], "Eje Global: Humanización y autonomía del cuidado asistencial."),
        ("NACIONAL (NICARAGUA)", COLOR_GOLD_ACCENT, [
            ("Ley No. 774 (2012):", "Pionera en Centroamérica: declara el derecho de los ciudadanos al acceso a la medicina natural y terapias complementarias."),
            ("Romero Hernández (2021):", "Etnobotánica en Masaya: sobadores y comadronas actúan como primer escudo de contención psicosomática."),
            ("Cunningham (2021):", "Costa Caribe: articulación horizontal y sinérgica entre medicina occidental y médicos tradicionales miskitos.")
        ], "Eje Nacional: Respaldo legal y demanda de formación clínica."),
        ("LOCAL (CUR-ESTELÍ)", COLOR_TEAL_ACCENT, [
            ("Aguilera Altamirano et al. (2019):", "Arteterapia aplicada a internos de Medicina en el Hospital San Juan de Dios de Estelí: redujo sensiblemente el burnout."),
            ("Mora y Bellorín (2020):", "Dramaterapia en estudiantes de Psicología del CUR-Estelí: incrementó significativamente la autoestima y autoconcepto."),
            ("Hallazgo Articulador Clave:", "Los estudiantes ya utilizan empíricamente la MTCI como recurso de autocuidado somático ante sobrecarga académica.")
        ], "Eje Local: Viabilidad formativa probada en Estelí.")
    ]

    for i, (col_title, title_col, items, takeaway) in enumerate(antecedentes):
        c_left = Inches(0.8) + i * (col_w3 + gap3)
        c_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, card_top, col_w3, card_h)
        c_box.adjustments[0] = 0.025; c_box.fill.solid(); c_box.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_box.line.color.rgb = COLOR_BORDER_LIGHT

        tb = s3.shapes.add_textbox(c_left + Inches(0.25), Inches(1.95), col_w3 - Inches(0.5), Inches(4.6))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]; p.text = col_title; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = title_col; p.space_after = Pt(14)

        for a_auth, a_text in items:
            p = tf.add_paragraph(); p.space_after = Pt(10); p.line_spacing = 1.15
            r1 = p.add_run(); r1.text = a_auth + " "; r1.font.bold = True; r1.font.size = Pt(11); r1.font.color.rgb = title_col
            r2 = p.add_run(); r2.text = a_text; r2.font.size = Pt(10.5); r2.font.color.rgb = COLOR_TEXT_PRIMARY

        p_t = tf.add_paragraph(); p_t.space_before = Pt(8); p_t.space_after = Pt(0); p_t.line_spacing = 1.15
        r_t = p_t.add_run(); r_t.text = "✦ " + takeaway; r_t.font.bold = True; r_t.font.size = Pt(10); r_t.font.color.rgb = COLOR_NAVY_TITLE

    # ==========================================================================
    # SLIDE 4: CONTEXTO DEL ESTUDIO (CUR-ESTELÍ Y FIGURA 1)
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, COLOR_LIGHT_CANVAS)
    add_slide_header(s4, "Capítulo I • Contextualización Institucional", "Coordenadas Territoriales, Dispositivos Clínicos y Vinculación")
    add_slide_footer(s4, 4)

    c_ctx = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_top, col_w2, card_h)
    c_ctx.adjustments[0] = 0.025; c_ctx.fill.solid(); c_ctx.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_ctx.line.color.rgb = COLOR_BORDER_LIGHT

    tb_ctx = s4.shapes.add_textbox(Inches(1.1), Inches(1.95), col_w2 - Inches(0.6), Inches(4.6))
    tf_ctx = tb_ctx.text_frame; tf_ctx.word_wrap = True; tf_ctx.margin_left = tf_ctx.margin_right = tf_ctx.margin_top = tf_ctx.margin_bottom = 0

    p = tf_ctx.paragraphs[0]; p.text = "ESCENARIO INSTITUCIONAL Y TERRITORIAL"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(14)

    ctx_items = [
        ("Municipio de Estelí:", "Cabecera departamental del norte de Nicaragua con fuerte arraigo en etnobotánica viva, sobadores y botánicas populares."),
        ("Recinto Leonel Rugama Rugama:", "Sede del CUR-Estelí donde convergen estudiantes de turnos matutino y sabatino procedentes de diversos municipios."),
        ("Clínica Psicosocial y Comunitaria:", "Dispositivo asistencial clave donde alumnos de 4.° y 5.° año realizan sus prácticas de psicoterapia y talleres."),
        ("Consultorio Médico Universitario:", "Espacio de salud primaria y enlace con el Centro de Salud Leonel Rugama (MINSA)."),
        ("Línea de Investigación SAL-3:", "Sublínea Terapias Alternativas, articulada al Plan Nacional de Lucha contra la Pobreza y Desarrollo Humano.")
    ]
    for c_t, c_d in ctx_items:
        p = tf_ctx.add_paragraph(); p.space_after = Pt(10); p.line_spacing = 1.15
        r1 = p.add_run(); r1.text = c_t + " "; r1.font.bold = True; r1.font.size = Pt(12); r1.font.color.rgb = COLOR_NAVY_TITLE
        r2 = p.add_run(); r2.text = c_d; r2.font.size = Pt(11.5); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    fig1 = "assets/figuras_apa7/figura_01_ubicacion_cur_esteli.png"
    if os.path.exists(fig1):
        s4.shapes.add_picture(fig1, Inches(6.833), Inches(1.7), width=col_w2, height=Inches(4.45))
        cap_box = s4.shapes.add_textbox(Inches(6.833), Inches(6.25), col_w2, Inches(0.5))
        tf_cap = cap_box.text_frame; tf_cap.word_wrap = True
        p_cap = tf_cap.paragraphs[0]; p_cap.text = "Figura 1. Delimitación del CUR-Estelí, recinto Leonel Rugama Rugama, Estelí, Nicaragua (Cartografía Institucional, 2026)."
        p_cap.font.name = FONT_SANS; p_cap.font.size = Pt(10); p_cap.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================================================
    # SLIDE 5: OBJETIVOS DE LA INVESTIGACIÓN (GENERAL HERO + 3 ESPECÍFICOS)
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, COLOR_LIGHT_CANVAS)
    add_slide_header(s5, "Capítulo I • Arquitectura Teleológica", "Esquema Articulador de Objetivos de Investigación")
    add_slide_footer(s5, 5)

    og_h = Inches(1.65)
    c_og = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(11.733), og_h)
    c_og.adjustments[0] = 0.025; c_og.fill.solid(); c_og.fill.fore_color.rgb = COLOR_TINT_BLUE; c_og.line.color.rgb = RGBColor(186, 230, 253)

    tb_og = s5.shapes.add_textbox(Inches(1.15), Inches(1.85), Inches(11.0), Inches(1.3))
    tf_og = tb_og.text_frame; tf_og.word_wrap = True; tf_og.margin_left = tf_og.margin_right = tf_og.margin_top = tf_og.margin_bottom = 0
    p = tf_og.paragraphs[0]; p.text = "OBJETIVO GENERAL"; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(4)
    p = tf_og.add_paragraph()
    p.text = "Explorar la percepción de la Medicina Tradicional, Complementaria e Integrativa (MTCI) como recurso de apoyo en la atención psicológica desde la mirada de actores locales, estudiantes y docentes de Psicología del CUR-Estelí durante el segundo semestre de 2026."
    p.font.name = FONT_SERIF; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.line_spacing = 1.2

    oe_top = Inches(3.6)
    oe_h = Inches(3.2)
    oes_data = [
        ("OBJETIVO ESPECÍFICO 1", "Diagnóstico Cuantitativo",
         "Caracterizar conocimientos conceptuales, normativos y frecuencia de uso en estudiantes de 4.º y 5.º año.",
         "Muestra: 53 de 4.° y 15 de 5.° año (n = 68 participantes).",
         "Vía Cuantitativa • Cuestionario I1 (Likert)", COLOR_TEAL_ACCENT),
        ("OBJETIVO ESPECÍFICO 2", "Exploración Cualitativa",
         "Describir beneficios percibidos y efectos adversos desde facilitadores tradicionales locales de Estelí.",
         "Muestra: 9 terapeutas con hasta 30 años de experiencia.",
         "Vía Cualitativa • Entrevista Semiestructurada I2", COLOR_GOLD_ACCENT),
        ("OBJETIVO ESPECÍFICO 3", "Formulación Propositiva",
         "Proponer estrategias complementarias para el abordaje de la MTCI formalizadas en un manual técnico-ético.",
         "Producto: Manual de 18 páginas (Anexo 16.2 de tesis).",
         "Vía Propositiva • Cuestionario I3 + Manual Clínico", COLOR_NAVY_TITLE)
    ]
    for i, (oe_title, oe_sub, oe_desc, oe_m, oe_inst, col_c) in enumerate(oes_data):
        c_left = Inches(0.8) + i * (col_w3 + gap3)
        c_oe = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, oe_top, col_w3, oe_h)
        c_oe.adjustments[0] = 0.03; c_oe.fill.solid(); c_oe.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_oe.line.color.rgb = COLOR_BORDER_LIGHT

        tb = s5.shapes.add_textbox(c_left + Inches(0.25), oe_top + Inches(0.25), col_w3 - Inches(0.5), Inches(2.7))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]; p.text = oe_title; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = col_c; p.space_after = Pt(2)
        p = tf.add_paragraph(); p.text = oe_sub.upper(); p.font.name = FONT_SANS; p.font.size = Pt(9.5); p.font.color.rgb = COLOR_TEXT_MUTED; p.space_after = Pt(8)
        p = tf.add_paragraph(); p.text = oe_desc; p.font.name = FONT_SANS; p.font.size = Pt(11.5); p.font.bold = True; p.font.color.rgb = COLOR_TEXT_PRIMARY; p.space_after = Pt(8); p.line_spacing = 1.15
        p = tf.add_paragraph(); p.text = "• " + oe_m; p.font.name = FONT_SANS; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_MUTED; p.space_after = Pt(8)
        p = tf.add_paragraph(); p.text = "✦ " + oe_inst; p.font.name = FONT_SANS; p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = col_c

    # ==========================================================================
    # SLIDE 6: MARCO TEÓRICO (1/2: BASES CONCEPTUALES Y NORMATIVAS)
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, COLOR_LIGHT_CANVAS)
    add_slide_header(s6, "Capítulo II • Marco Teórico (1/2)", "Bases Conceptuales de la MTCI, Taxonomía OMS y Leyes Sanitarias")
    add_slide_footer(s6, 6)

    c_c = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_top, col_w2, card_h)
    c_c.adjustments[0] = 0.025; c_c.fill.solid(); c_c.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_c.line.color.rgb = COLOR_BORDER_LIGHT

    tb_c = s6.shapes.add_textbox(Inches(1.1), Inches(1.95), col_w2 - Inches(0.6), Inches(4.6))
    tf_c = tb_c.text_frame; tf_c.word_wrap = True; tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p = tf_c.paragraphs[0]; p.text = "DESLINDE CONCEPTUAL (OMS / OPS)"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(14)

    conc_items = [
        ("Medicina Tradicional (MT):", "Saberes y prácticas ancestrales e indígenas fundamentadas en cosmovisiones comunitarias para el cuidado psicosomático."),
        ("Medicina Complementaria (MC):", "Prácticas de salud foráneas utilizadas como coadyuvantes sin pretender reemplazar a los tratamientos biomédicos."),
        ("Medicina Integrativa (MI):", "Coordinación informada de terapias convencionales y complementarias respaldadas por evidencia de seguridad y eficacia."),
        ("Taxonomía Ley 774 (Art. 12):", "Terapias energéticas (Reiki); manuales (masajes); fitoterapia, aromaterapia; hidroterapia y sistémicas.")
    ]
    for c_title, c_desc in conc_items:
        p = tf_c.add_paragraph(); p.space_after = Pt(14); p.line_spacing = 1.2
        r1 = p.add_run(); r1.text = c_title + " "; r1.font.bold = True; r1.font.size = Pt(12.5); r1.font.color.rgb = COLOR_NAVY_TITLE
        r2 = p.add_run(); r2.text = c_desc; r2.font.size = Pt(12); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    c_l = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), card_top, col_w2, card_h)
    c_l.adjustments[0] = 0.025; c_l.fill.solid(); c_l.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_l.line.color.rgb = COLOR_BORDER_LIGHT

    tb_l = s6.shapes.add_textbox(Inches(7.133), Inches(1.95), col_w2 - Inches(0.6), Inches(4.6))
    tf_l = tb_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p = tf_l.paragraphs[0]; p.text = "MARCO JURÍDICO SANITARIO DE NICARAGUA"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_GOLD_ACCENT; p.space_after = Pt(14)

    law_items = [
        ("Ley No. 774 (2012) — Medicina Natural:", "Reconoce las terapias complementarias como derecho inalienable e instruye su integración en la red pública de salud."),
        ("Ley No. 292 (1998) — Medicamentos y Farmacias:", "Prohíbe de forma tajante al psicólogo prescribir fármacos, plantas medicinales con dosis terapéuticas o remedios alopáticos."),
        ("Ley No. 759 (2011) — Medicina Tradicional Ancestral:", "Salvaguarda el patrimonio etnobotánico y saberes tradicionales de los pueblos originarios y afrodescendientes."),
        ("Delimitación Deontológica del Psicólogo:", "El psicólogo explora y deriva con juicio clínico; nunca invade el acto prescriptivo ni la práctica médica.")
    ]
    for l_title, l_desc in law_items:
        p = tf_l.add_paragraph(); p.space_after = Pt(14); p.line_spacing = 1.2
        r1 = p.add_run(); r1.text = l_title + " "; r1.font.bold = True; r1.font.size = Pt(12.5); r1.font.color.rgb = COLOR_GOLD_ACCENT
        r2 = p.add_run(); r2.text = l_desc; r2.font.size = Pt(12); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    # ==========================================================================
    # SLIDE 7: MARCO TEÓRICO (2/2: TOP-DOWN VS BOTTOM-UP)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, COLOR_LIGHT_CANVAS)
    add_slide_header(s7, "Capítulo II • Marco Teórico (2/2)", "Dimensión Psicofisiológica: Articulación Clínica Top-Down y Bottom-Up")
    add_slide_footer(s7, 7)

    split_h = Inches(3.2)
    c_td = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_top, col_w2, split_h)
    c_td.adjustments[0] = 0.03; c_td.fill.solid(); c_td.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_td.line.color.rgb = COLOR_BORDER_LIGHT
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(1.95), col_w2 - Inches(0.6), Inches(2.7))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.text = "VÍA TOP-DOWN (CORTICAL / REFLEXIVA)"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(8)
    p = tf.add_paragraph(); p.text = "• Mecanismo: Opera mediante la corteza prefrontal, reestructuración cognitiva y narrativa reflexiva autobiográfica."; p.font.size = Pt(12); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.space_after = Pt(6)
    p = tf.add_paragraph(); p.text = "• Técnicas: Psicoterapia verbal, diálogo socrático, toma de decisiones y metacognición."; p.font.size = Pt(12); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.space_after = Pt(6)
    p = tf.add_paragraph(); p.text = "• Límite en Crisis: La hiperactivación simpática y el desborde amigdalino anulan el procesamiento verbal superior."; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_ALERT_RED

    c_bu = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), card_top, col_w2, split_h)
    c_bu.adjustments[0] = 0.03; c_bu.fill.solid(); c_bu.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_bu.line.color.rgb = COLOR_BORDER_LIGHT
    tb = s7.shapes.add_textbox(Inches(7.133), Inches(1.95), col_w2 - Inches(0.6), Inches(2.7))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.text = "VÍA BOTTOM-UP (SOMÁTICA / MTCI)"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT; p.space_after = Pt(8)
    p = tf.add_paragraph(); p.text = "• Mecanismo: Modula directamente el sistema nervioso autónomo, respuesta vagal y tono propioceptivo subcortical."; p.font.size = Pt(12); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.space_after = Pt(6)
    p = tf.add_paragraph(); p.text = "• Técnicas MTCI: Respiración diafragmática, masoterapia tradicional, escaneo corporal e infusiones suaves."; p.font.size = Pt(12); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.space_after = Pt(6)
    p = tf.add_paragraph(); p.text = "• Efecto Facilitador: Reduce hipertonía muscular y devuelve al organismo a su ventana de tolerancia clínica."; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT

    syn_top = Inches(5.1)
    syn_h = Inches(1.7)
    c_syn = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), syn_top, Inches(11.733), syn_h)
    c_syn.adjustments[0] = 0.025; c_syn.fill.solid(); c_syn.fill.fore_color.rgb = COLOR_TINT_TEAL; c_syn.line.color.rgb = RGBColor(153, 246, 228)

    tb_s = s7.shapes.add_textbox(Inches(1.15), syn_top + Inches(0.2), Inches(11.0), Inches(1.3))
    tf_s = tb_s.text_frame; tf_s.word_wrap = True; tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p = tf_s.paragraphs[0]; p.text = "LA SINERGIA CLÍNICA INTEGRATIVA EN SALUD MENTAL"; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT; p.space_after = Pt(4)
    p = tf_s.add_paragraph()
    p.text = "La integración de la MTCI no reemplaza a la psicoterapia verbal; instaura la calma neurovegetativa somática necesaria (vía Bottom-Up) para que el paciente recupere la receptividad cortical y el procesamiento reflexivo (vía Top-Down) pueda ser eficaz."
    p.font.name = FONT_SERIF; p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.line_spacing = 1.25

    # ==========================================================================
    # SLIDE 8: DISEÑO METODOLÓGICO (1/2: TIPOLOGÍA Y 4 FASES DE INVESTIGACIÓN)
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, COLOR_LIGHT_CANVAS)
    add_slide_header(s8, "Capítulo III • Diseño Metodológico (1/2)", "Tipología de Estudio, Paradigma Pragmático y Fases")
    add_slide_footer(s8, 8)

    c_m = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_top, col_w2, card_h)
    c_m.adjustments[0] = 0.025; c_m.fill.solid(); c_m.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_m.line.color.rgb = COLOR_BORDER_LIGHT

    tb_m = s8.shapes.add_textbox(Inches(1.1), Inches(1.95), col_w2 - Inches(0.6), Inches(4.6))
    tf_m = tb_m.text_frame; tf_m.word_wrap = True; tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
    p = tf_m.paragraphs[0]; p.text = "PILARES METODOLÓGICOS"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(14)

    met_points = [
        ("Enfoque Mixto Concurrente (DIAC):", "Articula datos cuantitativos (OE1) con hermenéutica cualitativa (OE2 y OE3), integrándolos dialógicamente en la discusión."),
        ("Paradigma Pragmático (Arias, 2023):", "Supera pugnas dogmáticas; supedita el método a resolver la brecha real de competencias en las aulas y clínica del CUR-Estelí."),
        ("Nivel y Temporalidad:", "Descriptivo con alcance exploratorio y propositivo; diseño no experimental y transversal (segundo semestre 2026)."),
        ("Rigor y Validación:", "Juicio crítico de 4 expertos universitarios para la validez de contenido de los cuestionarios I1, I2 e I3.")
    ]
    for m_t, m_d in met_points:
        p = tf_m.add_paragraph(); p.space_after = Pt(14); p.line_spacing = 1.2
        r1 = p.add_run(); r1.text = m_t + " "; r1.font.bold = True; r1.font.size = Pt(12.5); r1.font.color.rgb = COLOR_NAVY_TITLE
        r2 = p.add_run(); r2.text = m_d; r2.font.size = Pt(12); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    c_f = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), card_top, col_w2, card_h)
    c_f.adjustments[0] = 0.025; c_f.fill.solid(); c_f.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_f.line.color.rgb = COLOR_BORDER_LIGHT

    tb_f = s8.shapes.add_textbox(Inches(7.133), Inches(1.95), col_w2 - Inches(0.6), Inches(4.6))
    tf_f = tb_f.text_frame; tf_f.word_wrap = True; tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0
    p = tf_f.paragraphs[0]; p.text = "LAS CUATRO FASES DE LA INVESTIGACIÓN"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT; p.space_after = Pt(14)

    phases_data = [
        ("FASE 1: Fundamentación", "Delimitación del problema, formulación de objetivos, revisión sistemática y marco de Leyes 774, 759 y 292."),
        ("FASE 2: Validación Instrumental", "Construcción de cuestionarios I1, I2 e I3; juicio crítico de 4 expertos universitarios en pertinencia y redacción."),
        ("FASE 3: Trabajo de Campo", "Levantamiento muestral (N = 86 participantes), procesamiento estadístico en SPSS v26 y análisis temático cualitativo."),
        ("FASE 4: Formulación Propositiva", "Elaboración del Manual de Estrategias MTCI de 18 páginas para la práctica clínica y docente en el CUR-Estelí.")
    ]
    for p_t, p_d in phases_data:
        p = tf_f.add_paragraph(); p.space_after = Pt(14); p.line_spacing = 1.2
        r1 = p.add_run(); r1.text = p_t + " — "; r1.font.bold = True; r1.font.size = Pt(12.5); r1.font.color.rgb = COLOR_TEAL_ACCENT
        r2 = p.add_run(); r2.text = p_d; r2.font.size = Pt(12); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    # ==========================================================================
    # SLIDE 9: DISEÑO METODOLÓGICO (2/2: MUESTRAS, CRITERIOS E INSTRUMENTOS)
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, COLOR_LIGHT_CANVAS)
    add_slide_header(s9, "Capítulo III • Diseño Metodológico (2/2)", "Muestra Participante (N = 86), Criterios e Instrumentos de Campo")
    add_slide_footer(s9, 9)

    fig2 = "assets/figuras_apa7/figura_02_criterios_inclusion_exclusion.png"
    if os.path.exists(fig2):
        s9.shapes.add_picture(fig2, Inches(0.8), Inches(1.7), width=Inches(5.4), height=Inches(4.45))
        cap_box = s9.shapes.add_textbox(Inches(0.8), Inches(6.25), Inches(5.4), Inches(0.5))
        tf_cap = cap_box.text_frame; tf_cap.word_wrap = True
        p_cap = tf_cap.paragraphs[0]; p_cap.text = "Figura 2. Flujograma de criterios de inclusión y exclusión (Elaboración propia, 2026)."
        p_cap.font.name = FONT_SANS; p_cap.font.size = Pt(10); p_cap.font.color.rgb = COLOR_TEXT_MUTED

    w_u = Inches(6.0)
    c_u = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.533), card_top, w_u, card_h)
    c_u.adjustments[0] = 0.025; c_u.fill.solid(); c_u.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_u.line.color.rgb = COLOR_BORDER_LIGHT

    tb_u = s9.shapes.add_textbox(Inches(6.833), Inches(1.95), w_u - Inches(0.6), Inches(4.6))
    tf_u = tb_u.text_frame; tf_u.word_wrap = True; tf_u.margin_left = tf_u.margin_right = tf_u.margin_top = tf_u.margin_bottom = 0

    p = tf_u.paragraphs[0]; p.text = "TRES COLECTIVOS DE ANÁLISIS (N = 86)"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(14)

    actors = [
        ("Estudiantes de Psicología (n = 68):", "53 de 4.° año (77.9%) y 15 de 5.° año (22.1%) en turnos matutino y sabatino.", "Instrumento I1: Cuestionario estandarizado en Google Forms (12 ítems Likert y selección múltiple)."),
        ("Facilitadores Locales de Estelí (n = 9):", "7 mujeres y 2 hombres con amplia trayectoria y reconocimiento en medicina natural.", "Instrumento I2: Entrevista cualitativa semiestructurada (11 preguntas abiertas en profundidad)."),
        ("Claustro Docente de Psicología (n = 9):", "Docentes activos de grado y posgrado con experiencia en tutoría y clínica.", "Instrumento I3: Cuestionario reflexivo docente (14 preguntas abiertas de pertinencia curricular).")
    ]
    for a_t, a_p, a_i in actors:
        p = tf_u.add_paragraph(); p.space_after = Pt(6); p.line_spacing = 1.15
        r1 = p.add_run(); r1.text = a_t + " "; r1.font.bold = True; r1.font.size = Pt(12.5); r1.font.color.rgb = COLOR_NAVY_TITLE
        r2 = p.add_run(); r2.text = a_p; r2.font.size = Pt(12); r2.font.color.rgb = COLOR_TEXT_PRIMARY
        p_sub = tf_u.add_paragraph(); p_sub.space_after = Pt(14); p_sub.line_spacing = 1.15
        r3 = p_sub.add_run(); r3.text = "✦ " + a_i; r3.font.size = Pt(10.5); r3.font.color.rgb = COLOR_TEAL_ACCENT

    # ==========================================================================
    # SLIDE 10: RESULTADOS (1/4: DEMOGRAFÍA Y BRECHA COGNITIVO-NORMATIVA)
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, COLOR_LIGHT_CANVAS)
    add_slide_header(s10, "Capítulo IV • Resultados Empíricos (1/4)", "Caracterización de la Muestra y Brecha de Conocimiento Normativo (OE1)")
    add_slide_footer(s10, 10)

    fig3 = "assets/figuras_apa7/figura_03_demografia_estudiantes.png"
    if os.path.exists(fig3):
        s10.shapes.add_picture(fig3, Inches(0.8), Inches(1.7), width=col_w2, height=Inches(3.2))

    tb_d = s10.shapes.add_textbox(Inches(0.8), Inches(5.1), col_w2, Inches(1.7))
    tf_d = tb_d.text_frame; tf_d.word_wrap = True
    p = tf_d.paragraphs[0]; p.text = "PERFIL SOCIODEMOGRÁFICO ESTUDIANTIL"; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(4)
    p = tf_d.add_paragraph(); p.text = "• Marcada Feminización: 82.4% mujeres (n = 56) y 14.7% varones (n = 10).\n• Colectivo Joven: 61.8% entre 20 y 22 años; 26.5% entre 23 y 25 años.\n• Momento Formativo: 77.9% cursa 4.º año y 22.1% culmina 5.º año en prácticas preprofesionales."; p.font.size = Pt(11.5); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.line_spacing = 1.2

    fig4 = "assets/figuras_apa7/figura_04_dominio_conceptual_normativo_estudiantes.png"
    if os.path.exists(fig4):
        s10.shapes.add_picture(fig4, Inches(6.833), Inches(1.7), width=col_w2, height=Inches(3.2))

    tb_b = s10.shapes.add_textbox(Inches(6.833), Inches(5.1), col_w2, Inches(1.7))
    tf_b = tb_b.text_frame; tf_b.word_wrap = True
    p = tf_b.paragraphs[0]; p.text = "BRECHA COGNITIVO-NORMATIVA IDENTIFICADA"; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_ALERT_RED; p.space_after = Pt(4)
    p = tf_b.add_paragraph(); p.text = "• Dominio Teórico Parcial: 67.6% acierta el concepto de MTCI según la OMS, pero el 75.0% ignora su aplicación clínica en salud mental.\n• Vacío Normativo Severo: 58.8% desconoce la Ley No. 774 y el 64.7% desconoce que la Ley No. 292 prohíbe formular psicofármacos."; p.font.size = Pt(11.5); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.line_spacing = 1.2

    # ==========================================================================
    # SLIDE 11: RESULTADOS (2/4: LA PARADOJA FORMATIVA Y FRECUENCIA DE USO)
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11, COLOR_LIGHT_CANVAS)
    add_slide_header(s11, "Capítulo IV • Resultados Empíricos (2/4)", "La Paradoja Formativa y la Eficacia Subjetiva del Autocuidado (OE1)")
    add_slide_footer(s11, 11)

    c_par = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_top, col_w2, card_h)
    c_par.adjustments[0] = 0.025; c_par.fill.solid(); c_par.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_par.line.color.rgb = COLOR_BORDER_LIGHT

    tb_p1 = s11.shapes.add_textbox(Inches(1.1), Inches(1.95), col_w2 - Inches(0.6), Inches(4.6))
    tf_p1 = tb_p1.text_frame; tf_p1.word_wrap = True; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p = tf_p1.paragraphs[0]; p.text = "LA GRAN PARADOJA FORMATIVA"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(8)

    p = tf_p1.add_paragraph(); p.text = "89.7%"; p.font.name = FONT_SERIF; p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT
    p = tf_p1.add_paragraph(); p.text = "Considera pertinente y necesario integrar la MTCI en psicología clínica."; p.font.size = Pt(11.5); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.space_after = Pt(10)

    p = tf_p1.add_paragraph(); p.text = "88.2%"; p.font.name = FONT_SERIF; p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = COLOR_ALERT_RED
    p = tf_p1.add_paragraph(); p.text = "Reconoce no haber recibido preparación alguna para orientar o derivar a MTCI."; p.font.size = Pt(11.5); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.space_after = Pt(10)

    p = tf_p1.add_paragraph(); p.text = "86.8%"; p.font.name = FONT_SERIF; p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = COLOR_GOLD_ACCENT
    p = tf_p1.add_paragraph(); p.text = "Autopercibe preparación insuficiente o nula para psicoeducar sobre MTCI."; p.font.size = Pt(11.5); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.space_after = Pt(10)

    p = tf_p1.add_paragraph(); p.text = "✦ Hallazgo Medular: Convicción ética unánime sobre el valor terapéutico, frente a un absoluto desamparo curricular y procedimental."; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE

    # Right: Figura 7 (Frecuencia de Uso y Bienestar)
    fig7 = "assets/figuras_apa7/figura_07_frecuencia_uso_estudiantes.png"
    if os.path.exists(fig7):
        s11.shapes.add_picture(fig7, Inches(6.833), Inches(1.7), width=col_w2, height=Inches(3.2))

    tb_u2 = s11.shapes.add_textbox(Inches(6.833), Inches(5.1), col_w2, Inches(1.7))
    tf_u2 = tb_u2.text_frame; tf_u2.word_wrap = True
    p = tf_u2.paragraphs[0]; p.text = "USO PERSONAL Y EFICACIA SOMÁTICA PERCIBIDA"; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT; p.space_after = Pt(4)
    p = tf_u2.add_paragraph(); p.text = "• Carácter Reactivo: 52.9% no usa MTCI preventivamente; acuden únicamente ante crisis o sobrecarga académica.\n• Eficacia Subjetiva Plena: 86.7% reporta efectos favorables o muy favorables en relajación y distensión muscular.\n• Seguridad Clínica: 0.0% reporta efectos adversos o complicaciones."; p.font.size = Pt(11.5); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.line_spacing = 1.2

    # ==========================================================================
    # SLIDE 12: RESULTADOS (3/4: FACILITADORES LOCALES Y CLAUSTRO DOCENTE)
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12, COLOR_LIGHT_CANVAS)
    add_slide_header(s12, "Capítulo IV • Resultados Empíricos (3/4)", "Perspectiva de Facilitadores Locales de Estelí y Claustro Docente")
    add_slide_footer(s12, 12)

    # Left: Facilitadores Locales (n = 9)
    c_fac = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_top, col_w2, card_h)
    c_fac.adjustments[0] = 0.025; c_fac.fill.solid(); c_fac.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_fac.line.color.rgb = COLOR_BORDER_LIGHT

    tb_f1 = s12.shapes.add_textbox(Inches(1.1), Inches(1.95), col_w2 - Inches(0.6), Inches(4.6))
    tf_f1 = tb_f1.text_frame; tf_f1.word_wrap = True; tf_f1.margin_left = tf_f1.margin_right = tf_f1.margin_top = tf_f1.margin_bottom = 0

    p = tf_f1.paragraphs[0]; p.text = "FACILITADORES LOCALES DE ESTELÍ (n = 9)"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT; p.space_after = Pt(8)

    p = tf_f1.add_paragraph(); p.text = "100%"; p.font.name = FONT_SERIF; p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT
    p = tf_f1.add_paragraph(); p.text = "Constatan alivio inmediato de sobrecarga psicosomática y tensión miofascial."; p.font.size = Pt(11.5); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.space_after = Pt(10)

    fac_insights = [
        ("Perfil Socioterritorial:", "77.8% mujeres; 44.4% acumula entre 20 y 30 años de experiencia continuada en Estelí."),
        ("Apertura Reflexiva (88.9%):", "Tras el alivio somático, los pacientes muestran mayor receptividad afectiva para dialogar con el terapeuta."),
        ("Estigma Sociocultural (100%):", "Identifican con frecuencia mitos, tabúes y prejuicios religiosos respecto a la medicina natural."),
        ("Desafío Económico (77.8%):", "La limitada capacidad económica de consultantes vulnerables interrumpe la continuidad del cuidado.")
    ]
    for f_t, f_d in fac_insights:
        p = tf_f1.add_paragraph(); p.space_after = Pt(8); p.line_spacing = 1.15
        r1 = p.add_run(); r1.text = "• " + f_t + " "; r1.font.bold = True; r1.font.size = Pt(11.5); r1.font.color.rgb = COLOR_TEAL_ACCENT
        r2 = p.add_run(); r2.text = f_d; r2.font.size = Pt(11); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    p_f_call = tf_f1.add_paragraph(); p_f_call.space_before = Pt(8)
    r_f_call = p_f_call.add_run(); r_f_call.text = "✦ Desafío Territorial: Persisten trabas burocráticas de acreditación (22.2%) y asimetría asistencial."; r_f_call.font.bold = True; r_f_call.font.size = Pt(10); r_f_call.font.color.rgb = COLOR_ALERT_RED

    # Right: Claustro Docente (n = 9)
    c_doc = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), card_top, col_w2, card_h)
    c_doc.adjustments[0] = 0.025; c_doc.fill.solid(); c_doc.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_doc.line.color.rgb = COLOR_BORDER_LIGHT

    tb_d1 = s12.shapes.add_textbox(Inches(7.133), Inches(1.95), col_w2 - Inches(0.6), Inches(4.6))
    tf_d1 = tb_d1.text_frame; tf_d1.word_wrap = True; tf_d1.margin_left = tf_d1.margin_right = tf_d1.margin_top = tf_d1.margin_bottom = 0

    p = tf_d1.paragraphs[0]; p.text = "CLAUSTRO DOCENTE-PSICÓLOGOS (n = 9)"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(8)

    p = tf_d1.add_paragraph(); p.text = "100%"; p.font.name = FONT_SERIF; p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE
    p = tf_d1.add_paragraph(); p.text = "Respaldo unánime a la incorporación curricular bajo enfoque crítico y científico."; p.font.size = Pt(11.5); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.space_after = Pt(10)

    doc_insights = [
        ("Metodologías Priorizadas:", "Rechazan la enseñanza memorística; 88.9% prioriza talleres prácticos y 77.8% intercambios dialógicos."),
        ("Competencias Clave a Formar:", "Juicio clínico crítico, prevención de riesgos, consentimiento informado y derivación bioética."),
        ("Capacitación Propia Urgente:", "El profesorado solicita formación en neurobiología somática y regulación Bottom-Up."),
        ("Propuesta Institucional:", "Creación del Comité de Ética y Delimitación Profesional en el CUR-Estelí.")
    ]
    for d_t, d_d in doc_insights:
        p = tf_d1.add_paragraph(); p.space_after = Pt(8); p.line_spacing = 1.15
        r1 = p.add_run(); r1.text = "• " + d_t + " "; r1.font.bold = True; r1.font.size = Pt(11.5); r1.font.color.rgb = COLOR_NAVY_TITLE
        r2 = p.add_run(); r2.text = d_d; r2.font.size = Pt(11); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    p_d_call = tf_d1.add_paragraph(); p_d_call.space_before = Pt(8)
    r_d_call = p_d_call.add_run(); r_d_call.text = "✦ Aporte del Claustro: Demanda urgente de un Comité de Ética y Delimitación en el CUR-Estelí."; r_d_call.font.bold = True; r_d_call.font.size = Pt(10); r_d_call.font.color.rgb = COLOR_NAVY_TITLE

    # ==========================================================================
    # SLIDE 13: RESULTADOS (4/4: PROPUESTA MANUAL MTCI - OE3)
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13, COLOR_LIGHT_CANVAS)
    add_slide_header(s13, "Capítulo V • Propuesta Operativa (OE3)", "Manual de Estrategias de MTCI para la Formación y Práctica Psicológica")
    add_slide_footer(s13, 13)

    w_m_cov = Inches(4.3)
    if os.path.exists(MANUAL_COVER_PATH):
        s13.shapes.add_picture(MANUAL_COVER_PATH, Inches(0.8), Inches(1.7), width=w_m_cov, height=Inches(3.1))

    c_spec = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.95), w_m_cov, Inches(1.85))
    c_spec.adjustments[0] = 0.03; c_spec.fill.solid(); c_spec.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_spec.line.color.rgb = COLOR_BORDER_LIGHT
    tb_spec = s13.shapes.add_textbox(Inches(0.95), Inches(5.05), w_m_cov - Inches(0.3), Inches(1.65))
    tf_spec = tb_spec.text_frame; tf_spec.word_wrap = True; tf_spec.margin_left = tf_spec.margin_right = tf_spec.margin_top = tf_spec.margin_bottom = 0
    p = tf_spec.paragraphs[0]; p.text = "FICHA TÉCNICA DEL PRODUCTO"; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(4)
    p = tf_spec.add_paragraph()
    p.text = "• Extensión: 18 páginas in extenso (Anexo 16.2).\n• Destinatarios: Alumnos y docentes de la Clínica Psicosocial.\n• Propósito: Dotar de discernimiento ético para explorar y derivar, sin habilitar como terapeutas alternativos."
    p.font.size = Pt(10.5); p.font.color.rgb = COLOR_TEXT_PRIMARY; p.line_spacing = 1.15

    # Right: 8 Módulos Temáticos (2 Columnas Limpias)
    w_mod_r = Inches(7.2)
    c_mod = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.333), card_top, w_mod_r, card_h)
    c_mod.adjustments[0] = 0.025; c_mod.fill.solid(); c_mod.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_mod.line.color.rgb = COLOR_BORDER_LIGHT

    tb_mod = s13.shapes.add_textbox(Inches(5.6), Inches(1.95), w_mod_r - Inches(0.5), Inches(4.6))
    tf_mod = tb_mod.text_frame; tf_mod.word_wrap = True; tf_mod.margin_left = tf_mod.margin_right = tf_mod.margin_top = tf_mod.margin_bottom = 0

    p = tf_mod.paragraphs[0]; p.text = "ESTRUCTURA MODULAR DEL MANUAL (8 MÓDULOS)"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT; p.space_after = Pt(10)

    modules_clean = [
        ("Módulo 1: Fundamentos y Marco Legal", "Definición OMS (2025) y articulación de Leyes 774, 759 y 292 de Nicaragua."),
        ("Módulo 2: Principios Deontológicos", "Consentimiento informado intercultural y complementariedad sin sustitución."),
        ("Módulo 3: Mapa de Prácticas", "Clasificación clínica en 4 niveles (directo, psicoeducación, precaución, alerta)."),
        ("Módulo 4: Algoritmo de Derivación", "Protocolo secuencial de 4 pasos para derivación clínica informada."),
        ("Módulo 5: Habilidades de Diálogo", "Técnicas de entrevista abierta para erradicar el ocultamiento terapéutico."),
        ("Módulo 6: Red Intersectorial", "Criterios de referencia bidireccional y trabajo colaborativo con facilitadores."),
        ("Módulo 7: Ruta Formativa", "Secuencia pedagógica en 3 etapas y propuesta de asignatura electiva."),
        ("Módulo 8: Soporte CUR-Estelí", "Creación del Comité de Bioética y plan de capacitación docente continua.")
    ]
    for idx, (m_name, m_sum) in enumerate(modules_clean):
        p = tf_mod.add_paragraph(); p.space_after = Pt(6); p.line_spacing = 1.15
        r1 = p.add_run(); r1.text = f"{idx+1}. {m_name}: "; r1.font.bold = True; r1.font.size = Pt(11); r1.font.color.rgb = COLOR_NAVY_TITLE
        r2 = p.add_run(); r2.text = m_sum; r2.font.size = Pt(10.5); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    p_a = tf_mod.add_paragraph(); p_a.space_before = Pt(8)
    r_a = p_a.add_run(); r_a.text = "✦ Herramienta Anexa: Incorpora la adaptación transcultural del cuestionario I-CAM-Q para tamizaje clínico estandarizado."; r_a.font.bold = True; r_a.font.size = Pt(10); r_a.font.color.rgb = COLOR_TEAL_ACCENT

    # ==========================================================================
    # SLIDE 14: CONCLUSIONES CENTRALES DE LA INVESTIGACIÓN
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14, COLOR_LIGHT_CANVAS)
    add_slide_header(s14, "Capítulo VI • Síntesis Conclusiva", "Conclusiones Centrales de la Investigación (Triangulación de Objetivos)")
    add_slide_footer(s14, 14)

    c_concl = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_top, Inches(11.733), card_h)
    c_concl.adjustments[0] = 0.025; c_concl.fill.solid(); c_concl.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_concl.line.color.rgb = COLOR_BORDER_LIGHT

    tb_c14 = s14.shapes.add_textbox(Inches(1.15), Inches(1.95), Inches(11.0), Inches(4.6))
    tf_c14 = tb_c14.text_frame; tf_c14.word_wrap = True; tf_c14.margin_left = tf_c14.margin_right = tf_c14.margin_top = tf_c14.margin_bottom = 0

    p = tf_c14.paragraphs[0]; p.text = "SÍNTESIS CONCLUSIVA POR OBJETIVOS"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_TITLE; p.space_after = Pt(14)

    conclusiones_text = [
        ("1. Cumplimiento del Objetivo General:", "Los tres colectivos participantes (N = 86) validan unánimemente la MTCI como recurso complementario legítimo en salud mental, condicionado a un ejercicio bioético, científico y respetuoso de los límites profesionales."),
        ("2. Perfil y Paradoja Estudiantil (OE1):", "El estudiantado posee buen dominio conceptual básico (67.6%) y alta satisfacción somática subjetiva (86.7%), pero padece desinformación legal (58.8% desconoce Ley 774; 64.7% desconoce Ley 292) y alta inseguridad para derivar (88.2%)."),
        ("3. Oferta y Resiliencia Territorial (OE2):", "Los facilitadores de Estelí constatan 100% de alivio de sobrecarga muscular y mayor apertura reflexiva (88.9%), enfrentando barreras de estigma sociocultural (100%) y limitaciones económicas de los usuarios (77.8%)."),
        ("4. Consenso Curricular Docente (OE3):", "El 100% del claustro apoya transversalizar la MTCI bajo metodologías activas y vivenciales (88.9%), demandando formación en regulación neurovegetativa y comités de bioética."),
        ("5. Logro Propositivo del Manual de Estrategias:", "Se construyó exitosamente el Manual de Estrategias MTCI de 18 páginas (Anexo 16.2), dotando al CUR-Estelí de algoritmos de decisión clínica, pautas contra el ocultamiento y el inventario I-CAM-Q.")
    ]
    for c_num, c_body in conclusiones_text:
        p = tf_c14.add_paragraph(); p.space_after = Pt(14); p.line_spacing = 1.2
        r1 = p.add_run(); r1.text = c_num + " "; r1.font.bold = True; r1.font.size = Pt(12.5); r1.font.color.rgb = COLOR_NAVY_TITLE
        r2 = p.add_run(); r2.text = c_body; r2.font.size = Pt(12); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    # ==========================================================================
    # SLIDE 15: RECOMENDACIONES ESTRATÉGICAS (4 CUADRANTES AMPLIOS)
    # ==========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15, COLOR_LIGHT_CANVAS)
    add_slide_header(s15, "Capítulo VI • Directrices Prospectivas", "Recomendaciones Estratégicas para Estudiantes, Docentes, Universidad y MINSA")
    add_slide_footer(s15, 15)

    rec_w = Inches(5.7)
    rec_h = Inches(2.45)
    rec_y1 = Inches(1.7)
    rec_y2 = Inches(4.35)

    quads = [
        ("PARA EL ESTAMENTO ESTUDIANTIL", COLOR_TEAL_ACCENT, Inches(0.8), rec_y1, [
            ("Límites Legales:", "Respetar estrictamente las Leyes 774 y 292 (prohibición terminante de formular fármacos)."),
            ("Algoritmo Clínico:", "Aplicar el árbol de decisión del manual en las prácticas de la Clínica Psicosocial."),
            ("Diálogo Abierto:", "Explorar empáticamente el uso de MTCI en consulta para erradicar el ocultamiento terapéutico."),
            ("Autocuidado Personal:", "Vivenciar la regulación somática (respiración diafragmática) ante sobrecarga académica.")
        ]),
        ("PARA EL CLAUSTRO DOCENTE", COLOR_NAVY_TITLE, Inches(6.833), rec_y1, [
            ("Transversalidad Curricular:", "Integrar contenidos de MTCI en Psicología Clínica, Comunitaria y Ética Profesional."),
            ("Pedagogía Vivencial:", "Priorizar análisis de casos clínicos y talleres de autorregulación somática."),
            ("Capacitación Continua:", "Formarse institucionalmente en neurobiología del estrés y regulación Bottom-Up."),
            ("Derivación Ética:", "Instruir en criterios claros de referencia intersectorial hacia facilitadores e interconsulta médica.")
        ]),
        ("PARA LA GESTIÓN DEL CUR-ESTELÍ", COLOR_GOLD_ACCENT, Inches(0.8), rec_y2, [
            ("Adopción Oficial:", "Formalizar la aprobación institucional del Manual de Estrategias MTCI (Anexo 16.2)."),
            ("Comité de Bioética:", "Constituir el Comité de Ética y Delimitación Profesional en el recinto universitario."),
            ("Alianza con MINSA:", "Consolidar convenios interinstitucionales para pasantías y ferias comunitarias de salud."),
            ("Asignatura Electiva:", "Evaluar a mediano plazo la creación formal del curso electivo 'Psicología Integrativa'.")
        ]),
        ("PARA EL SISTEMA DE SALUD Y FACILITADORES", COLOR_TEAL_ACCENT, Inches(6.833), rec_y2, [
            ("Registro Oficial:", "Difundir mecanismos de acreditación para facilitadores contemplados en la Ley No. 774."),
            ("Red de Interconsulta:", "Habilitar canales de referencia bidireccional entre psicólogos y terapeutas locales."),
            ("Atención Primaria:", "Fomentar la exploración desestigmatizada de saberes herbolarios en centros de salud comunitaria."),
            ("Principio Bioético:", "Mantener el compromiso de complementariedad sin pretender sustituir tratamientos médicos.")
        ])
    ]

    for q_title, q_col, q_left, q_top, q_items in quads:
        c_q = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, q_left, q_top, rec_w, rec_h)
        c_q.adjustments[0] = 0.03; c_q.fill.solid(); c_q.fill.fore_color.rgb = COLOR_CARD_LIGHT; c_q.line.color.rgb = COLOR_BORDER_LIGHT

        tb_q = s15.shapes.add_textbox(q_left + Inches(0.25), q_top + Inches(0.18), rec_w - Inches(0.5), Inches(2.15))
        tf_q = tb_q.text_frame; tf_q.word_wrap = True; tf_q.margin_left = tf_q.margin_right = tf_q.margin_top = tf_q.margin_bottom = 0

        p = tf_q.paragraphs[0]; p.text = q_title; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = q_col; p.space_after = Pt(6)

        for it_h, it_t in q_items:
            p = tf_q.add_paragraph(); p.space_after = Pt(4); p.line_spacing = 1.15
            r1 = p.add_run(); r1.text = "✓ " + it_h + " "; r1.font.bold = True; r1.font.size = Pt(11); r1.font.color.rgb = q_col
            r2 = p.add_run(); r2.text = it_t; r2.font.size = Pt(10.5); r2.font.color.rgb = COLOR_TEXT_PRIMARY

    # ==========================================================================
    # SLIDE 16: CIERRE INSTITUCIONAL (DARK CANVAS - "SANDWICH" PRESTIGIOSO)
    # ==========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16, COLOR_DARK_CANVAS)

    if os.path.exists(SHIELD_PATH):
        s16.shapes.add_picture(SHIELD_PATH, Inches(6.0), Inches(0.8), height=Inches(1.4))

    tb_cl = s16.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(11.333), Inches(2.0))
    tf_cl = tb_cl.text_frame; tf_cl.word_wrap = True; tf_cl.margin_left = tf_cl.margin_right = tf_cl.margin_top = tf_cl.margin_bottom = 0

    p = tf_cl.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    p.text = "«¡A la libertad por la Universidad!»"
    p.font.name = FONT_SERIF; p.font.size = Pt(17); p.font.italic = True; p.font.bold = True; p.font.color.rgb = COLOR_GOLD_ACCENT
    p.space_after = Pt(8)

    p = tf_cl.add_paragraph(); p.alignment = PP_ALIGN.CENTER
    p.text = "Muchas Gracias por su Atención"
    p.font.name = FONT_SERIF; p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(10)

    p = tf_cl.add_paragraph(); p.alignment = PP_ALIGN.CENTER
    p.text = "Espacio Abierto para Preguntas, Comentarios y Defensa Oral ante el Honorable Tribunal Examinador"
    p.font.name = FONT_SANS; p.font.size = Pt(13); p.font.color.rgb = RGBColor(148, 163, 184)

    meta_top16 = Inches(4.7)
    meta_h16 = Inches(1.9)

    # 1. Sustentantes
    c_s16 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), meta_top16, col_w1, meta_h16)
    c_s16.adjustments[0] = 0.04; c_s16.fill.solid(); c_s16.fill.fore_color.rgb = COLOR_DARK_CARD; c_s16.line.color.rgb = COLOR_DARK_BORDER
    tf = c_s16.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.margin_left = Inches(0.25); tf.margin_right = Inches(0.2)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "SUSTENTANTES"; p.font.name = FONT_SANS; p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = COLOR_GOLD_ACCENT; p.space_after = Pt(8)
    for n in ["• Dina Fabiola García Torres", "• Tatiana Paola López Ramos", "• Engel Enoc Zamora Velásquez"]:
        p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = n; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.color.rgb = COLOR_WHITE; p.space_after = Pt(4)

    # 2. Tutora
    c_t16 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + col_w1 + gap1, meta_top16, col_w1, meta_h16)
    c_t16.adjustments[0] = 0.04; c_t16.fill.solid(); c_t16.fill.fore_color.rgb = COLOR_DARK_CARD; c_t16.line.color.rgb = COLOR_DARK_BORDER
    tf = c_t16.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.margin_left = Inches(0.25); tf.margin_right = Inches(0.2)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "TUTORÍA ACADÉMICA"; p.font.name = FONT_SANS; p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = RGBColor(45, 212, 191); p.space_after = Pt(8)
    p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "• Dra. Tania Libertad Pérez Guevara"; p.font.name = FONT_SANS; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.space_after = Pt(4)
    p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "Docente Investigadora • CUR-Estelí\nAsesoría Temática y Metodológica"; p.font.name = FONT_SANS; p.font.size = Pt(10.5); p.font.color.rgb = RGBColor(148, 163, 184)

    # 3. Grado & Fecha
    c_g16 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + (col_w1 + gap1)*2, meta_top16, col_w1, meta_h16)
    c_g16.adjustments[0] = 0.04; c_g16.fill.solid(); c_g16.fill.fore_color.rgb = COLOR_DARK_CARD; c_g16.line.color.rgb = COLOR_DARK_BORDER
    tf = c_g16.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.margin_left = Inches(0.25); tf.margin_right = Inches(0.2)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "DEFENSA DE GRADO"; p.font.name = FONT_SANS; p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = COLOR_GOLD_ACCENT; p.space_after = Pt(8)
    p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "Licenciatura en Psicología\nRecinto Leonel Rugama Rugama\nEstelí, Nicaragua • Octubre, 2026"; p.font.name = FONT_SANS; p.font.size = Pt(11); p.font.color.rgb = COLOR_WHITE; p.space_after = Pt(4)

    output_pptx = "Presentacion_Defensa_Tesis_MTCI_UNAN_Modern.pptx"
    prs.save(output_pptx)
    print(f"Modern Presentation created successfully at: {output_pptx}")
    try:
        prs.save("Presentacion_Defensa_Tesis_MTCI_UNAN.pptx")
        print("Also updated Presentacion_Defensa_Tesis_MTCI_UNAN.pptx")
    except Exception as e:
        print("Note: Original file is currently open in PowerPoint:", e)

if __name__ == "__main__":
    create_presentation()
