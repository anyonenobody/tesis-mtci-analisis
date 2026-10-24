import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# COLOR PALETTE (UNAN-Managua & Academic Healthcare Design System)
# ==============================================================================
COLOR_NAVY = RGBColor(13, 44, 84)        # Deep UNAN Blue #0D2C54
COLOR_TEAL = RGBColor(25, 110, 115)     # Deep Academic Teal #196E73
COLOR_GOLD = RGBColor(212, 139, 56)      # Amber Gold Accent #D48B38
COLOR_DARK = RGBColor(33, 37, 41)        # Main Body Charcoal #212529
COLOR_MUTED = RGBColor(108, 117, 125)    # Secondary / Notes #6C757D
COLOR_BG_CARD = RGBColor(255, 255, 255)  # Card Background
COLOR_BORDER = RGBColor(222, 226, 230)   # Light Border #DEE2E6
COLOR_SOFT_BLUE = RGBColor(238, 244, 251)# Soft Blue Tint #EEF4FB
COLOR_SOFT_TEAL = RGBColor(236, 246, 245)# Soft Teal Tint #ECF6F5
COLOR_SOFT_GOLD = RGBColor(254, 249, 238)# Soft Gold Tint #FEF9EE
COLOR_RED_ALERT = RGBColor(186, 24, 27)  # Alert / Prohibition #BA181B
COLOR_GREEN = RGBColor(40, 138, 86)      # Success / Positive #288A56

FONT_TITLE = "Calibri"
FONT_BODY = "Calibri"

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    def set_slide_background(slide, color=RGBColor(248, 249, 251)):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, badge_text, title_text, subtitle_text=None):
        # Category Badge
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.35))
        tf_b = badge_box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text.upper()
        p_b.font.name = FONT_TITLE
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_TEAL

        # Slide Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.55))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY

        # Accent Rule
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.32), Inches(11.733), Inches(0.025))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_GOLD
        line.line.color.rgb = COLOR_GOLD

    def add_footer(slide, current_slide, total_slides=16):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(10.0), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "UNAN-Managua • CUR-Estelí | Departamento de Educación y Humanidades • Carrera de Psicología (2026)"
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_MUTED

        num_box = slide.shapes.add_textbox(Inches(11.0), Inches(7.05), Inches(1.5), Inches(0.3))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"{current_slide} / {total_slides}"
        p_n.font.name = FONT_BODY
        p_n.font.size = Pt(8.5)
        p_n.font.bold = True
        p_n.font.color.rgb = COLOR_TEAL

    def add_card(slide, left, top, width, height, bg_color=COLOR_BG_CARD, border_color=COLOR_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # ==========================================================================
    # SLIDE 1: PORTADA INSTITUCIONAL
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, RGBColor(244, 247, 250))

    # Decorative header color bar
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_GOLD
    top_bar.line.fill.background()

    # Watermark background shield if available
    shield_path = "assets/extracted/watermark_sec_1_rId2_image3.png"
    if os.path.exists(shield_path):
        s1.shapes.add_picture(shield_path, Inches(8.5), Inches(1.2), height=Inches(5.0))

    # Main Institutional Logo
    logo_path = "assets/extracted/cover_img_0_rId8_image1.png"
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(0.8), Inches(0.6), height=Inches(1.3))

    # Institutional Text
    inst_box = s1.shapes.add_textbox(Inches(2.2), Inches(0.65), Inches(9.5), Inches(1.2))
    tf_inst = inst_box.text_frame
    tf_inst.word_wrap = True
    p0 = tf_inst.paragraphs[0]
    p0.text = "UNIVERSIDAD NACIONAL AUTÓNOMA DE NICARAGUA, MANAGUA"
    p0.font.bold = True
    p0.font.size = Pt(13)
    p0.font.color.rgb = COLOR_NAVY
    p1 = tf_inst.add_paragraph()
    p1.text = "CENTRO UNIVERSITARIO REGIONAL DE ESTELÍ (CUR-ESTELÍ) • RECINTO LEONEL RUGAMA RUGAMA"
    p1.font.size = Pt(10)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEAL
    p2 = tf_inst.add_paragraph()
    p2.text = "DEPARTAMENTO DE EDUCACIÓN Y HUMANIDADES | CARRERA DE PSICOLOGÍA"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_MUTED

    # Main Card for Title
    add_card(s1, Inches(0.8), Inches(2.1), Inches(8.2), Inches(4.7), COLOR_BG_CARD, COLOR_BORDER)

    t_box = s1.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(7.6), Inches(4.3))
    tf = t_box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "TRABAJO DE INVESTIGACIÓN DE GRADO"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p = tf.add_paragraph()
    p.text = "La Medicina Tradicional, Complementaria e Integrativa (MTCI) como Complemento en la Atención Psicológica"
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    p = tf.add_paragraph()
    p.text = "Estudio Mixto con Estudiantes y Docentes del CUR-Estelí y Facilitadores Locales del Municipio de Estelí (Segundo Semestre, 2026)"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_DARK
    p.space_after = Pt(16)

    # Divider line
    p = tf.add_paragraph()
    p.text = "—" * 38
    p.font.color.rgb = COLOR_BORDER

    p = tf.add_paragraph()
    p.text = "Para Optar al Título de Licenciados en Psicología"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    p = tf.add_paragraph()
    p.text = "Autores:\n • Dina Fabiola García Torres\n • Tatiana Paola López Ramos\n • Engel Enoc Zamora Velásquez"
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_DARK

    p = tf.add_paragraph()
    p.text = "Tutora:\n • Dra. Tania Libertad Pérez Guevara"
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_DARK

    p = tf.add_paragraph()
    p.text = "Estelí, Nicaragua • Octubre, 2026"
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = COLOR_MUTED

    # ==========================================================================
    # SLIDE 2: PLANTEAMIENTO DEL PROBLEMA Y JUSTIFICACIÓN
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Capítulo I • Planteamiento del Problema", "Encrucijada Asistencial, Vacío Formativo y Pertinencia Social")
    add_footer(s2, 2)

    # Left Column: Planteamiento del Problema (Card)
    add_card(s2, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    box = s2.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "PLANTEAMIENTO DEL PROBLEMA"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    points_prob = [
        ("Asimetría Legal y Sanitaria:", " La Ley No. 774 reconoce a la MTCI como derecho humano e intercultural, mientras la Ley No. 292 prohíbe tajantemente al psicólogo prescribir fármacos. Los usuarios acuden a la herbolaria y masajes, pero el psicólogo carece de formación sistemática sobre cómo interactuar con ellos."),
        ("El Fenómeno del 'Ocultamiento Terapéutico':", " El consultante silencia sus prácticas tradicionales y complementarias por temor a ser censurado o descalificado moralmente, elevando el riesgo de abandono del tratamiento e interacciones adversas."),
        ("Brecha Formativa en la Carrera:", " La malla curricular carece de asignaturas sobre salud intercultural y abordajes somáticos. Los egresados no disponen de pautas éticas ni operativas para psicoeducar o derivar responsablemente."),
        ("Pregunta Motriz:", " ¿Cuáles son las características de los saberes, vivencias y oferta de MTCI en Estelí, y cómo fundamentan el diseño de un manual ético y pedagógico para Psicología en el CUR-Estelí?")
    ]
    for bold_txt, norm_txt in points_prob:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + bold_txt
        run1.font.bold = True
        run1.font.size = Pt(10.5)
        run1.font.color.rgb = COLOR_TEAL
        run2 = p.add_run()
        run2.text = norm_txt
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # Right Column: Justificación Multidimensional (Card)
    add_card(s2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    box2 = s2.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf2 = box2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "JUSTIFICACIÓN Y PERTINENCIA DEL ESTUDIO"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    points_just = [
        ("Pertinencia Ética y Deontológica:", " Velar por la alternabilidad terapéutica exige que el profesional conozca qué consume el paciente para evitar juicios dogmáticos y garantizar la no maleficencia."),
        ("Aporte a la Salud Mental y Comunitaria:", " Visibiliza a los facilitadores populares y saberes ancestrales del norte nicaragüense, legitimando el autocuidado culturalmente congruente."),
        ("Impacto Formativo Directo (CUR-Estelí):", " Provee una guía estructurada para practicantes en la Clínica Psicosocial y Comunitaria, cerrando el abismo entre la teoría clínica y la vida territorial."),
        ("Alineación con Agendas de Desarrollo:", " Responde a la línea institucional SAL-3 (Salud e Interculturalidad), a las metas del SETEC (2025) y al Plan Nacional de Lucha contra la Pobreza (2022–2026).")
    ]
    for bold_txt, norm_txt in points_just:
        p = tf2.add_paragraph()
        run1 = p.add_run()
        run1.text = "▶ " + bold_txt
        run1.font.bold = True
        run1.font.size = Pt(10.5)
        run1.font.color.rgb = COLOR_GOLD
        run2 = p.add_run()
        run2.text = norm_txt
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(8)

    # ==========================================================================
    # SLIDE 3: ANTECEDENTES (INTERNACIONALES, NACIONALES Y LOCALES)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Capítulo I • Estado del Arte", "Esquema de Antecedentes Empíricos: Internacional, Nacional y Local")
    add_footer(s3, 3)

    # 3 Horizontal Cards for 3 levels of antecedentes
    col_w = Inches(3.75)
    gap = Inches(0.24)

    # Level 1: Internacional
    add_card(s3, Inches(0.8), Inches(1.5), col_w, Inches(5.3), COLOR_BG_CARD, COLOR_BORDER)
    box = s3.shapes.add_textbox(Inches(0.95), Inches(1.65), col_w - Inches(0.3), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ANTECEDENTES INTERNACIONALES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    sub_items = [
        ("Chafloque-Capuñay et al. (2025):", "Revisión sistemática cualitativa (22 estudios). Concluye que el uso de MTCI responde al anhelo de autonomía, bienestar espiritual y trato horizontal que el modelo biomédico mecanicista no provee."),
        ("Ortega Cadena et al. (2023):", "Investigación en Colombia sobre barreras de interculturalidad. Constata que el reduccionismo positivista patologiza las cosmovisiones populares y genera muros de incomunicación asistencial."),
        ("OPS (2023) & OMS (2025):", "Estrategias globales demandan un diálogo intercultural activo y la integración de terapias tradicionales en la atención primaria.")
    ]
    for b_txt, n_txt in sub_items:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL
        r2 = p.add_run()
        r2.text = " " + n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(8)

    # Level 2: Nacional
    add_card(s3, Inches(0.8) + col_w + gap, Inches(1.5), col_w, Inches(5.3), COLOR_BG_CARD, COLOR_BORDER)
    box = s3.shapes.add_textbox(Inches(0.95) + col_w + gap, Inches(1.65), col_w - Inches(0.3), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ANTECEDENTES NACIONALES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    sub_items_nac = [
        ("Marco Normativo Ley No. 774 (2012):", "Hito centroamericano que institucionaliza la medicina natural y terapias complementarias bajo principios de alternabilidad e interculturalidad."),
        ("Romero Hernández (2021):", "Patrimonio etnobotánico en Catarina (Masaya). Documenta que curanderos y sobadores son la primera línea de contención psicosomática comunitaria."),
        ("Cunningham / Cultural Survival (2021):", "Modelo de salud intercultural en Costa Caribe: médicos y parteras colaboran horizontalmente complementando saberes."),
        ("MINSA (2024):", "Instituto de Medicina Natural sistematiza experiencias nacionales: la salud es indisociable de la comunidad y la naturaleza.")
    ]
    for b_txt, n_txt in sub_items_nac:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_GOLD
        r2 = p.add_run()
        r2.text = " " + n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # Level 3: Local (CUR-Estelí)
    add_card(s3, Inches(0.8) + (col_w + gap) * 2, Inches(1.5), col_w, Inches(5.3), COLOR_BG_CARD, COLOR_BORDER)
    box = s3.shapes.add_textbox(Inches(0.95) + (col_w + gap) * 2, Inches(1.65), col_w - Inches(0.3), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ANTECEDENTES LOCALES (CUR-ESTELÍ)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    sub_items_loc = [
        ("Aguilera Altamirano et al. (2019):", "Arteterapia aplicada a internos de Medicina en el Hospital Escuela San Juan de Dios de Estelí. Comprueba reducción sensible del agotamiento psicofisiológico y estrés hospitalario."),
        ("Mora Mejías y Bellorín (2020):", "Dramaterapia en estudiantes de primer año de Psicología del CUR-Estelí. Evidencia mejoría significativa en autoestima y autoconcepto."),
        ("Hallazgo Clave Articulador:", "Los estudiantes de Psicología de la UNAN-Managua no son analistas teóricos externos: ellos mismos emplean empíricamente la MTCI ante la sobrecarga del estrés universitario.")
    ]
    for b_txt, n_txt in sub_items_loc:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL
        r2 = p.add_run()
        r2.text = " " + n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(8)

    # ==========================================================================
    # SLIDE 4: CONTEXTO DEL ESTUDIO
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Capítulo I • Contextualización Institucional", "Coordenadas Territoriales, Dispositivos Clínicos y Vinculación Comunitaria")
    add_footer(s4, 4)

    # Left Column: Information Cards
    add_card(s4, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.3))
    box = s4.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.6), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "EL ESCENARIO GEOGRÁFICO E INSTITUCIONAL"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    ctx_items = [
        ("Municipio de Estelí (Norte de Nicaragua):", "Epicentro socioeconómico con arraigadas prácticas tradicionales de etnobotánica, sobadores y reciente proliferación de centros holísticos y botánicas comunitarias."),
        ("Recinto Leonel Rugama Rugama (CUR-Estelí):", "Sede donde convergen estudiantes de turno matutino y por encuentro sabatino procedentes de diversos municipios del norte del país."),
        ("Clínica Psicosocial y Comunitaria:", "Dispositivo asistencial clave donde los estudiantes de 4.° y 5.° año realizan sus prácticas formativas, brindando psicoterapia y talleres a la población local."),
        ("Consultorio Médico Comunitario:", "Espacio de prevención en salud primaria que articula ferias integrales y campañas interinstitucionales en convenio con el MINSA."),
        ("Línea de Investigación Institucional:", "Inscrito formalmente en la línea SAL-3: Salud e Interculturalidad (Sublínea SAL-3.1: Medicina natural y terapias alternativas).")
    ]
    for b_txt, n_txt in ctx_items:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "✔ " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_TEAL
        r2 = p.add_run()
        r2.text = " " + n_txt
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # Right Column: Map Figure 1
    add_card(s4, Inches(7.1), Inches(1.5), Inches(5.4), Inches(5.3))
    fig1_path = "assets/figuras_apa7/figura_01_ubicacion_cur_esteli.png"
    if os.path.exists(fig1_path):
        s4.shapes.add_picture(fig1_path, Inches(7.25), Inches(1.65), width=Inches(5.1))
    
    caption_box = s4.shapes.add_textbox(Inches(7.2), Inches(6.1), Inches(5.2), Inches(0.6))
    tf_c = caption_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = "Figura 1. Delimitación geográfica del CUR-Estelí, recinto Leonel Rugama Rugama, Estelí, Nicaragua (Cartografía Institucional, 2026)."
    p_c.font.size = Pt(8.5)
    p_c.font.italic = True
    p_c.font.color.rgb = COLOR_MUTED

    # ==========================================================================
    # SLIDE 5: OBJETIVOS DE LA INVESTIGACIÓN (ESQUEMA INTEGRAL)
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Capítulo I • Arquitectura Teleológica", "Esquema Articulador de Objetivos de Investigación")
    add_footer(s5, 5)

    # Top Full Card: Objetivo General
    add_card(s5, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.5), COLOR_SOFT_BLUE, COLOR_TEAL)
    box = s5.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(1.3))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "OBJETIVO GENERAL DE LA INVESTIGACIÓN"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.space_after = Pt(4)
    p2 = tf.add_paragraph()
    p2.text = "Explorar la percepción de la Medicina Tradicional, Complementaria e Integrativa (MTCI) como recurso de apoyo en la atención psicológica desde la mirada de actores locales, estudiantes y docentes de Psicología del CUR-Estelí durante el segundo semestre del año 2026."
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_NAVY

    # Bottom 3 Cards: Objetivos Específicos
    col_w3 = Inches(3.75)
    gap3 = Inches(0.24)

    oes = [
        ("OBJETIVO ESPECÍFICO 1", "Diagnóstico Cuantitativo (Estudiantes)",
         "Caracterizar los conocimientos conceptuales, normativos y la frecuencia de uso de la MTCI en estudiantes de 4.º y 5.º año de la carrera de Licenciatura en Psicología del CUR-Estelí.",
         "Vía Cuantitativa: Cuestionario I1 (n = 68)", COLOR_TEAL),
        ("OBJETIVO ESPECÍFICO 2", "Exploración Cualitativa (Facilitadores)",
         "Describir los beneficios percibidos y los posibles efectos desfavorables de la MTCI en el bienestar emocional y mental, desde la perspectiva de facilitadores locales del municipio de Estelí.",
         "Vía Cualitativa: Cuestionario I2 (n = 9)", COLOR_GOLD),
        ("OBJETIVO ESPECÍFICO 3", "Formulación Propositiva (Docentes y Alumnos)",
         "Proponer estrategias complementarias para abordar la MTCI en la formación de estudiantes de Psicología del CUR-Estelí, formalizadas en un manual técnico-ético de 18 páginas.",
         "Vía Cualitativa / Propositiva: I3 (n = 9) + Manual", COLOR_NAVY)
    ]

    for i, (oe_title, oe_sub, oe_desc, oe_tool, oe_color) in enumerate(oes):
        left_pos = Inches(0.8) + i * (col_w3 + gap3)
        add_card(s5, left_pos, Inches(3.2), col_w3, Inches(3.6), COLOR_BG_CARD, COLOR_BORDER)

        box_oe = s5.shapes.add_textbox(left_pos + Inches(0.15), Inches(3.35), col_w3 - Inches(0.3), Inches(3.3))
        tf_oe = box_oe.text_frame
        tf_oe.word_wrap = True

        p = tf_oe.paragraphs[0]
        p.text = oe_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = oe_color

        p = tf_oe.add_paragraph()
        p.text = oe_sub
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(8)

        p = tf_oe.add_paragraph()
        p.text = oe_desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_DARK
        p.space_after = Pt(12)

        p = tf_oe.add_paragraph()
        p.text = "▶ Instrumento: " + oe_tool
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = oe_color

    # ==========================================================================
    # SLIDE 6: MARCO TEÓRICO (LÁMINA 1: BASES CONCEPTUALES Y NORMATIVAS)
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Capítulo II • Marco Teórico (1/2)", "Bases Conceptuales de la MTCI, Taxonomía OMS y Marco Jurídico Nicaragüense")
    add_footer(s6, 6)

    # Left Card: Conceptos y Taxonomía OMS (OMS 2022, 2025; OPS 2023)
    add_card(s6, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    box = s6.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DESLINDE CONCEPTUAL Y TAXONOMÍA (OMS / OPS)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    concepts = [
        ("Medicina Tradicional (MT):", " Saberes ancestrales, indígenas y consuetudinarios transmitidos comunitariamente para salvaguardar la salud biopsicosocial (OMS, 2022, 2025). En Nicaragua se arraiga en la etnobotánica popular."),
        ("Medicina Complementaria (MC):", " Amplio repertorio de recursos terapéuticos que no forman parte del sistema biomédico hegemónico pero se emplean de forma coadyuvante sin desplazar a la alopatía (OMS, 2022)."),
        ("Medicina Integrativa (MI):", " Articulación interdisciplinaria de tratamientos convencionales y complementarios bajo estándares de seguridad y rigor científico, concibiendo al individuo en su totalidad (OPS, 2023)."),
        ("Taxonomía de Prácticas (Ley 774 Art. 12):", " Energéticas (Reiki, Bioenergética); Manuales (Masajes, Quiropraxia, Reflexología); Basadas en elementos (Hidroterapia, Sauna); Plantas (Fitoterapia, Aromaterapia); Herramientas específicas (Acupuntura, Terapia Neural); y Sistémicas (Constelaciones).")
    ]
    for b_txt, n_txt in concepts:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL
        r2 = p.add_run()
        r2.text = n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # Right Card: Marco Jurídico Nicaragüense
    add_card(s6, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    box2 = s6.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "MARCO JURÍDICO DE SALUD EN NICARAGUA"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    laws = [
        ("Ley No. 774 (Asamblea Nacional, 2012):", " Ley de Medicina Natural, Terapias Complementarias y Productos Naturales en Nicaragua.\n ▶ Consagra el acceso a la MTCI como un derecho ciudadano inalienable.\n ▶ Mandata la incorporación en la red pública de salud.\n ▶ Rige principios de complementariedad, equidad e interculturalidad."),
        ("Ley No. 292 (Asamblea Nacional, 1998):", " Ley de Medicamentos y Farmacias.\n ▶ Prohíbe formal y tajantemente la prescripción farmacológica a profesionales de la Psicología.\n ▶ Limita el campo legal al diagnóstico, psicoterapia y acompañamiento."),
        ("Ley No. 759 (Asamblea Nacional, 2011):", " Ley de Medicina Tradicional Ancestral.\n ▶ Protege y salvaguarda los saberes originarios y afrodescendientes."),
        ("Implicación Deontológica Central:", " El psicólogo debe conocer la MTCI no para prescribir remedios ni reemplazar la ciencia, sino para psicoeducar, prevenir riesgos y derivar éticamente.")
    ]
    for b_txt, n_txt in laws:
        p = tf2.add_paragraph()
        r1 = p.add_run()
        r1.text = "⚖ " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_GOLD if "774" in b_txt else COLOR_RED_ALERT if "292" in b_txt else COLOR_TEAL
        r2 = p.add_run()
        r2.text = n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # ==========================================================================
    # SLIDE 7: MARCO TEÓRICO (LÁMINA 2: MODELO PSICOFISIOLÓGICO TOP-DOWN / BOTTOM-UP)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Capítulo II • Marco Teórico (2/2)", "Dimensión Psicofisiológica: Articulación Clínica Top-Down y Bottom-Up")
    add_footer(s7, 7)

    # Card Left: Top-Down
    add_card(s7, Inches(0.8), Inches(1.5), Inches(5.7), Inches(3.6), COLOR_BG_CARD, COLOR_BORDER)
    box = s7.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(3.3))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "VÍA TOP-DOWN (DE ARRIBA HACIA ABAJO)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(6)

    td_items = [
        ("Mecanismo Neurocognitivo Cortical:", " Opera mediante la corteza prefrontal, el lenguaje reflexivo, la resignificación de creencias y la narrativa autobiográfica (Laricchiuta et al., 2023)."),
        ("Técnicas Propias:", " Psicoterapia verbal, reestructuración cognitiva, diálogo socrático y formulación reflexiva de metas."),
        ("Limitación Clínica:", " Ante un estado de hiperactivación simpática y desborde amigdalino por estrés o trauma, la capacidad reflexiva cortical se bloquea, esterilizando la intervención puramente verbal.")
    ]
    for b_txt, n_txt in td_items:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL
        r2 = p.add_run()
        r2.text = " " + n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # Card Right: Bottom-Up
    add_card(s7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.6), COLOR_BG_CARD, COLOR_BORDER)
    box2 = s7.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(3.3))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "VÍA BOTTOM-UP (DE ABAJO HACIA ARRIBA)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.space_after = Pt(6)

    bu_items = [
        ("Mecanismo Somático y Vagal:", " Incide directamente sobre el sistema nervioso autónomo, la respuesta vagal ventral y los centros subcorticales mediante la modulación propioceptiva (Thomson, 2023)."),
        ("Aporte Específico de la MTCI:", " Respiración consciente diafragmática, masoterapia relajante, fitoterapia ansiolítica suave (manzanilla, tilo, valeriana) y escaneo somático."),
        ("Efecto Sinergístico:", " Disipa la sobrecarga miofascial e hipertonía, devolviendo al organismo a su ventana de tolerancia psicofisiológica y habilitando el procesamiento reflexivo superior.")
    ]
    for b_txt, n_txt in bu_items:
        p = tf2.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_GOLD
        r2 = p.add_run()
        r2.text = " " + n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # Bottom Full Card: Síntesis del Modelo Integrativo
    add_card(s7, Inches(0.8), Inches(5.3), Inches(11.733), Inches(1.5), COLOR_SOFT_TEAL, COLOR_TEAL)
    box_syn = s7.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(11.3), Inches(1.3))
    tf_s = box_syn.text_frame
    tf_s.word_wrap = True
    p = tf_s.paragraphs[0]
    p.text = "LA SINERGIA CLÍNICA INTEGRATIVA EN PSICOLOGÍA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(4)
    p2 = tf_s.add_paragraph()
    p2.text = "La integración de la MTCI en el ejercicio psicológico no busca reemplazar el método científico ni improvisar en terapias complejas. Fundamenta un modelo biopsicosocial integral: modular primero la sobrecarga somática neurovegetativa (Bottom-Up) para instaurar una base de calma que optimice y potencie la psicoterapia reflexiva y la reestructuración cognitiva (Top-Down), blindando la alianza terapéutica con pertinencia cultural."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = COLOR_DARK

    # ==========================================================================
    # SLIDE 8: DISEÑO METODOLÓGICO (LÁMINA 1: TIPOLOGÍA, PARADIGMA Y FASES)
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Capítulo III • Diseño Metodológico (1/2)", "Tipología de Estudio, Paradigma Pragmático y Fases de la Investigación")
    add_footer(s8, 8)

    # Left Column: Tipología Metodológica (Tabla resumida en Card)
    add_card(s8, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    box = s8.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TIPOLOGÍA Y PARADIGMA METODOLÓGICO"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    met_crit = [
        ("Enfoque Epistemológico:", " Mixto Concurrente (DIAC). Articula la medición cuantitativa estandarizada (OE1) con el análisis hermenéutico cualitativo (OE2 y OE3), integrándolos dialógicamente en la discusión."),
        ("Paradigma Filosófico:", " Pragmático (Arias, 2023). Primacía de la resolución del problema real sobre disputas dogmáticas; combina ontología objetiva de encuestas con fenomenología intersubjetiva de relatos."),
        ("Nivel de Profundidad:", " Descriptivo con alcance exploratorio y propositivo."),
        ("Diseño Temporal y Manipulación:", " No experimental y transversal (segundo semestre lectivo 2026)."),
        ("Adscripción Institucional:", " Campo UNESCO 0313 (Psicología) y Línea SAL-3 (Salud e interculturalidad) de la UNAN-Managua.")
    ]
    for b_txt, n_txt in met_crit:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "✔ " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL
        r2 = p.add_run()
        r2.text = n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # Right Column: 4 Fases de Investigación
    add_card(s8, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    box2 = s8.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "LAS CUATRO FASES DE LA INVESTIGACIÓN"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    phases = [
        ("FASE 1: Preliminar y Fundamentación:", " Delimitación del problema, formulación de objetivos, revisión de literatura nacional e internacional y sistematización del marco jurídico (Leyes No. 774, 759 y 292)."),
        ("FASE 2: Diseño y Validación Instrumental:", " Construcción de instrumentos I1, I2 e I3. Juicio crítico de 4 expertos universitarios para afinar pertinencia sociocultural, rigor psicométrico y redacción."),
        ("FASE 3: Trabajo de Campo y Análisis Empírico:", " Administración en el CUR-Estelí (n=68 estudiantes, n=9 docentes) y facilitadores del municipio (n=9). Procesamiento descriptivo en SPSS v26 y análisis de contenido temático con matrices categoriales."),
        ("FASE 4: Formulación Propositiva del Manual (OE3):", " Articulación inductivo-deductiva para traducir las brechas y demandas empíricas en el Manual de Estrategias MTCI de 18 páginas para la práctica psicológica universitaria.")
    ]
    for b_txt, n_txt in phases:
        p = tf2.add_paragraph()
        r1 = p.add_run()
        r1.text = "▶ " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_GOLD
        r2 = p.add_run()
        r2.text = n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(7)

    # ==========================================================================
    # SLIDE 9: DISEÑO METODOLÓGICO (LÁMINA 2: MUESTRAS, CRITERIOS E INSTRUMENTOS)
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Capítulo III • Diseño Metodológico (2/2)", "Unidades de Análisis, Muestra Participante (N = 86) e Instrumentos de Campo")
    add_footer(s9, 9)

    # Left Card: Diagram of Inclusion/Exclusion (Figura 2)
    add_card(s9, Inches(0.8), Inches(1.5), Inches(5.4), Inches(5.3))
    fig2_path = "assets/figuras_apa7/figura_02_criterios_inclusion_exclusion.png"
    if os.path.exists(fig2_path):
        s9.shapes.add_picture(fig2_path, Inches(0.95), Inches(1.65), width=Inches(5.1))
    
    caption_box = s9.shapes.add_textbox(Inches(0.9), Inches(6.15), Inches(5.2), Inches(0.55))
    tf_c = caption_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = "Figura 2. Diagrama de flujo de criterios de selección muestral (Inclusión / Exclusión) para las 3 unidades de análisis (Elaboración propia, 2026)."
    p_c.font.size = Pt(8.5)
    p_c.font.italic = True
    p_c.font.color.rgb = COLOR_MUTED

    # Right Card: 3 Unidades de Análisis y Matriz de Instrumentos
    add_card(s9, Inches(6.5), Inches(1.5), Inches(6.0), Inches(5.3))
    box = s9.shapes.add_textbox(Inches(6.7), Inches(1.65), Inches(5.6), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "UNIDADES DE ANÁLISIS E INSTRUMENTOS (N = 86)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    units_data = [
        ("1. Estudiantes de Psicología (n = 68):",
         " • 53 alumnos de 4.º año (77.9%) y 15 de 5.º año (22.1%) en turnos matutino y sabatino.\n • Instrumento I1: Cuestionario psicométrico autoadministrado en Google Forms (12 reactivos Likert y opción múltiple). Mide conocimientos, uso y actitudes."),
        ("2. Facilitadores Locales de MTCI (n = 9):",
         " • 7 mujeres (77.8%) y 2 hombres (22.2%) con trayectorias de hasta 30 años en Estelí.\n • Instrumento I2: Cuestionario cualitativo semiestructurado (11 reactivos abiertos). Mide beneficios somáticos, barreras burocráticas y estigmas."),
        ("3. Cuerpo Docente-Psicólogos (n = 9):",
         " • Profesores activos con posgrados en áreas clínica, educativa y comunitaria.\n • Instrumento I3: Cuestionario cualitativo reflexivo (14 reactivos abiertos). Evalúa pertinencia curricular, metodologías y demandas bioéticas."),
        ("Rigor y Validación:",
         " • Juicio de 4 expertos (metodológico y de contenido).\n • Triangulación concurrente de fuentes y métodos.")
    ]
    for b_txt, n_txt in units_data:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL if "1." in b_txt else COLOR_GOLD if "2." in b_txt else COLOR_NAVY
        r2 = p.add_run()
        r2.text = "\n" + n_txt
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # ==========================================================================
    # SLIDE 10: RESULTADOS (LÁMINA 1: CARACTERIZACIÓN Y BRECHA NORMATIVA - OE1)
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Capítulo IV • Resultados Empíricos (1/4)", "Caracterización de la Muestra Estudiantil y Brecha de Conocimiento Normativo (OE1)")
    add_footer(s10, 10)

    # Left Card: Fig 3 (Demografía)
    add_card(s10, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    fig3_path = "assets/figuras_apa7/figura_03_demografia_estudiantes.png"
    if os.path.exists(fig3_path):
        s10.shapes.add_picture(fig3_path, Inches(0.95), Inches(1.65), width=Inches(5.4))
    
    caption_box = s10.shapes.add_textbox(Inches(0.95), Inches(4.5), Inches(5.4), Inches(2.2))
    tf = caption_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "HALLAZGOS SOCIODEMOGRÁFICOS (n = 68)"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(4)
    dem_pts = [
        "• Feminización de la matrícula: 82.4% mujeres (n=56), 14.7% varones (n=10).",
        "• Juventud académica: 61.8% entre 20 y 22 años; 26.5% entre 23 y 25 años.",
        "• Nivel de formación: 77.9% cursa 4.º año y 22.1% en 5.º año preprofesional."
    ]
    for pt in dem_pts:
        p = tf.add_paragraph()
        p.text = pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_DARK

    # Right Card: Fig 4 (Conocimiento Normativo y Conceptual)
    add_card(s10, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    fig4_path = "assets/figuras_apa7/figura_04_dominio_conceptual_normativo_estudiantes.png"
    if os.path.exists(fig4_path):
        s10.shapes.add_picture(fig4_path, Inches(6.95), Inches(1.65), width=Inches(5.4))

    caption_box2 = s10.shapes.add_textbox(Inches(6.95), Inches(4.5), Inches(5.4), Inches(2.2))
    tf2 = caption_box2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "BRECHA COGNITIVO-NORMATIVA CRÍTICA"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED_ALERT
    p.space_after = Pt(4)
    norm_pts = [
        "• Dominio Conceptual: 67.6% acierta la definición OMS, pero el 75.0% confiesa familiaridad práctica baja o nula con sus terapias.",
        "• Desconocimiento Ley No. 774: El 58.8% desconoce el marco legal que institucionaliza la MTCI en el Sistema Nacional de Salud.",
        "• Desconocimiento Ley No. 292: El 64.7% desconoce la norma que prohíbe taxativamente la prescripción de fármacos a los psicólogos."
    ]
    for pt in norm_pts:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_DARK

    # ==========================================================================
    # SLIDE 11: RESULTADOS (LÁMINA 2: PARADOJA FORMATIVA Y FRECUENCIA DE USO - OE1)
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Capítulo IV • Resultados Empíricos (2/4)", "La Paradoja Formativa y la Eficacia Subjetiva del Autocuidado Somático (OE1)")
    add_footer(s11, 11)

    # Left Column: La Gran Paradoja (3 Metrics Cards)
    add_card(s11, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    box = s11.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LA PARADOJA FORMATIVA EN EL ESTUDIANTADO"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    paradox_items = [
        ("89.7% Valora la Pertinencia Clínica:", " Abrumadora mayoría considera legítimo y necesario abordar la MTCI en psicoterapia mediante psicoeducación y derivación ética a facilitadores autorizados."),
        ("88.2% Sin Preparación para Derivar:", " Confiesan poseer una preparación nula o insuficiente para realizar derivaciones clínicas fundamentadas a terapeutas certificados."),
        ("86.8% Sin Competencia para Psicoeducar:", " Reportan preparación nula o insuficiente para psicoeducar a consultantes sobre beneficios, riesgos e interacciones de la MTCI."),
        ("Conclusión Diagnóstica:", " Los estudiantes reconocen el valor terapéutico del autocuidado pero la carrera los egresa sin herramientas operativas ni éticas para gestionarlo en consulta.")
    ]
    for b_txt, n_txt in paradox_items:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "▶ " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_GOLD if "89.7%" in b_txt else COLOR_RED_ALERT if "88.2%" in b_txt or "86.8%" in b_txt else COLOR_NAVY
        r2 = p.add_run()
        r2.text = n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # Right Column: Fig 7 (Uso Personal y Bienestar)
    add_card(s11, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    fig7_path = "assets/figuras_apa7/figura_07_frecuencia_uso_estudiantes.png"
    if os.path.exists(fig7_path):
        s11.shapes.add_picture(fig7_path, Inches(6.95), Inches(1.65), width=Inches(5.4))

    caption_box2 = s11.shapes.add_textbox(Inches(6.95), Inches(5.0), Inches(5.4), Inches(1.7))
    tf2 = caption_box2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "VIVENCIA PERSONAL Y EFICACIA SOMÁTICA"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.space_after = Pt(4)
    use_pts = [
        "• Carácter Reactivo: 52.9% no utiliza la MTCI preventivamente; recurren a ella ante episodios de sobrecarga académica.",
        "• Alivio Somático: El 86.7% de quienes la han usado reporta bienestar favorable o muy favorable (distensión muscular, calma).",
        "• Seguridad: 0.0% de efectos adversos reportados en la muestra."
    ]
    for pt in use_pts:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_DARK

    # ==========================================================================
    # SLIDE 12: RESULTADOS (LÁMINA 3: PERSPECTIVA DE FACILITADORES Y DOCENTES - OE2 Y OE3)
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Capítulo IV • Resultados Empíricos (3/4)", "Perspectiva de Facilitadores Locales de Estelí y Claustro Docente (OE2 y OE3)")
    add_footer(s12, 12)

    # Left Card: Facilitadores Locales (OE2)
    add_card(s12, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    box = s12.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FACILITADORES LOCALES DE ESTELÍ (n = 9)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    fac_items = [
        ("Perfil Socioterritorial:", " 77.8% mujeres; 44.4% acumula entre 20 y 30 años de experiencia continuada en Estelí. Oferta concentrada en masoterapia, fitoterapia, ayurveda y reflexología."),
        ("Beneficios Psicosomáticos (100%):", " Unánimemente reportan que sus terapias reducen drásticamente la hiperactivación fisiológica y tensión muscular; el 88.9% constata mayor apertura emocional y receptividad reflexiva."),
        ("Barreras Socioculturales (100%):", " Identifican de forma ocasional o frecuente mitos, prejuicios religiosos y estigmas sobre la medicina natural en la población urbana y rural."),
        ("Factor Económico y Burocracia:", " El 77.8% señala que la limitada capacidad económica interrumpe la continuidad del cuidado; el 22.2% refiere trabas de acreditación y escepticismo médico formal.")
    ]
    for b_txt, n_txt in fac_items:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_GOLD
        r2 = p.add_run()
        r2.text = n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # Right Card: Claustro Docente-Psicólogos (OE3)
    add_card(s12, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    box2 = s12.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "CLAUSTRO DOCENTE-PSICÓLOGOS (n = 9)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    doc_items = [
        ("Respaldo Institucional Unánime (100%):", " La totalidad del cuerpo docente apoya incorporar la MTCI en el plan de estudios, condicionando dicha inserción a un enfoque crítico, laico, bioético y con base científica."),
        ("Metodologías Formativas Priorizadas:", " Descarta la enseñanza teórica memorística; prioriza talleres prácticos y vivenciales (88.9%), intercambios dialógicos con terapeutas comunitarios (77.8%) y proyectos formativos (66.7%)."),
        ("Competencias Indispensables a Formar:", " Juicio clínico crítico, delimitación del rol, identificación de interacciones adversas y protocolos éticos de derivación interprofesional."),
        ("Demanda de Capacitación Propia:", " Los docentes solicitan capacitación institucional en neurobiología de las terapias somáticas y la creación de un Comité de Ética y Delimitación Profesional en el CUR-Estelí.")
    ]
    for b_txt, n_txt in doc_items:
        p = tf2.add_paragraph()
        r1 = p.add_run()
        r1.text = "✔ " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL
        r2 = p.add_run()
        r2.text = n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # ==========================================================================
    # SLIDE 13: RESULTADOS (LÁMINA 4: PROPUESTA MANUAL MTCI - OE3 PROPOSITIVO)
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Capítulo V • Propuesta Operativa (OE3)", "Manual de Estrategias de MTCI para la Formación y Práctica Psicológica")
    add_footer(s13, 13)

    # Left Column: Portada del Manual (Foto)
    add_card(s13, Inches(0.8), Inches(1.5), Inches(4.2), Inches(5.3))
    manual_cover_path = "assets/extracted/portada_manual.jpg"
    if os.path.exists(manual_cover_path):
        s13.shapes.add_picture(manual_cover_path, Inches(0.95), Inches(1.65), width=Inches(3.9))
    
    caption_box = s13.shapes.add_textbox(Inches(0.95), Inches(4.5), Inches(3.9), Inches(2.2))
    tf = caption_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FICHA TÉCNICA DEL MANUAL (18 PÁGS.)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(4)
    man_data = [
        "• Destinatarios: Docentes y estudiantes de 4.º y 5.º año (Clínica Psicosocial CUR-Estelí).",
        "• Enfoque: No habilita como terapeutas tradicionales; entrena el discernimiento ético y la derivación.",
        "• Anexo: Reproducido in extenso en Anexo 16.2."
    ]
    for pt in man_data:
        p = tf.add_paragraph()
        p.text = pt
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_DARK

    # Right Column: Estructura Modular del Manual (8 Módulos en 2 Sub-Cards)
    add_card(s13, Inches(5.2), Inches(1.5), Inches(7.333), Inches(5.3))
    box2 = s13.shapes.add_textbox(Inches(5.4), Inches(1.65), Inches(6.9), Inches(5.0))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "ESTRUCTURA MODULAR Y HERRAMIENTAS OPERATIVAS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(6)

    modules = [
        ("Módulo 1: Fundamentos y Marco Legal:", "Definición OMS (2025); marco de Leyes No. 774, 759 y 292."),
        ("Módulo 2: Principios Éticos y Deontológicos:", "Consentimiento informado intercultural; regla de oro: la MTCI como coadyuvante, nunca sustituto de la evidencia."),
        ("Módulo 3: Mapa Analítico de Prácticas:", "Clasificación en 4 niveles de rol (dentro del rol directo, psicoeducar, precaución médica y alerta por riesgo)."),
        ("Módulo 4: Algoritmo de Decisión Clínica:", "Protocolo secuencial de 4 pasos para evaluar riesgos y derivar éticamente."),
        ("Módulo 5: Habilidades Comunicacionales:", "Guía de entrevista abierta para erradicar el ocultamiento terapéutico."),
        ("Módulo 6: Articulación Intersectorial:", "Criterios de idoneidad, protocolos de referencia/contrarreferencia y alianzas con facilitadores de Estelí."),
        ("Módulo 7: Ruta Formativa Universitaria:", "Secuencia didáctica en 3 etapas y propuesta de asignatura optativa."),
        ("Módulo 8: Soporte y Comité Institucional:", "Comité de Ética en CUR-Estelí y 4 acciones anuales de capacitación docente.")
    ]
    for b_txt, n_txt in modules:
        p = tf2.add_paragraph()
        r1 = p.add_run()
        r1.text = "▶ " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_TEAL
        r2 = p.add_run()
        r2.text = " " + n_txt
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(3)

    # ==========================================================================
    # SLIDE 14: CONCLUSIONES
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Capítulo VI • Síntesis Conclusiva", "Conclusiones Centrales de la Investigación (Triangulación de Objetivos)")
    add_footer(s14, 14)

    # Card with 5 structured conclusions
    add_card(s14, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.3))
    box = s14.shapes.add_textbox(Inches(1.1), Inches(1.65), Inches(11.1), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SÍNTESIS DE CONCLUSIONES POR OBJETIVO DE INVESTIGACIÓN"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    concl_items = [
        ("1. Cumplimiento del Objetivo General:", " Los tres colectivos participantes (N = 86) validan unánimemente la pertinencia de la MTCI como coadyuvante del bienestar emocional, coincidiendo en que su abordaje demanda rigor científico, criterios deontológicos firmes y respeto irrestricto a los límites legales del psicólogo."),
        ("2. Perfil y Paradoja Estudiantil (OE1):", " El estudiantado muestra un adecuado conocimiento conceptual general (67.6%) y una alta eficacia percibida en su uso personal reactivo frente al estrés (86.7%), pero presenta alarmantes vacíos normativos (58.8% desconoce la Ley No. 774 y 64.7% desconoce la Ley No. 292) y una profunda desprotección operativa (el 88.2% se siente sin preparación para derivar a facilitadores y el 86.8% para psicoeducar)."),
        ("3. Oferta Real y Barreras Territoriales (OE2):", " La red comunitaria de Estelí está sostenida por facilitadores con hasta 30 años de labor que reportan una reducción sensible de la tensión psicofisiológica y mayor apertura afectiva en los usuarios (100%), debiendo sortear prejuicios socioculturales (100%), barreras económicas de consultantes vulnerables (77.8%) y trabas burocráticas."),
        ("4. Consenso y Demanda Docente (OE3):", " El 100% del cuerpo docente respalda la inserción curricular crítica y laica de la MTCI mediante metodologías vivenciales y activas, señalando la urgencia de recibir formación profesoral en neurobiología del estrés y delimitar comités bioéticos."),
        ("5. Logro Propositivo:", " Se materializó con éxito el Manual de Estrategias MTCI de 18 páginas (Anexo 16.2), dotando al CUR-Estelí de algoritmos de decisión clínica, pautas contra el ocultamiento terapéutico y el inventario I-CAM-Q adaptado.")
    ]
    for b_txt, n_txt in concl_items:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = b_txt
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL if "1." in b_txt or "5." in b_txt else COLOR_GOLD if "2." in b_txt else COLOR_NAVY
        r2 = p.add_run()
        r2.text = n_txt
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # ==========================================================================
    # SLIDE 15: RECOMENDACIONES
    # ==========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Capítulo VI • Directrices Prospectivas", "Recomendaciones Estratégicas para Estudiantes, Docentes, Universidad y MINSA")
    add_footer(s15, 15)

    # 4 Cards for 4 sectors
    rw = Inches(5.7)
    rh = Inches(2.5)

    # 1. Estudiantes
    add_card(s15, Inches(0.8), Inches(1.5), rw, rh)
    box = s15.shapes.add_textbox(Inches(1.0), Inches(1.6), rw - Inches(0.3), rh - Inches(0.2))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PARA EL ESTAMENTO ESTUDIANTIL"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.space_after = Pt(4)
    pts_e = [
        "• Apropiarse de las Leyes 774, 759 y la prohibición expresa de la Ley 292.",
        "• Aplicar el algoritmo de toma de decisiones del manual en la Clínica Psicosocial.",
        "• Superar el ocultamiento terapéutico con entrevistas empáticas libres de juicios."
    ]
    for pt in pts_e:
        p = tf.add_paragraph()
        p.text = pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_DARK

    # 2. Docentes
    add_card(s15, Inches(6.8), Inches(1.5), rw, rh)
    box = s15.shapes.add_textbox(Inches(7.0), Inches(1.6), rw - Inches(0.3), rh - Inches(0.2))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PARA EL CLAUSTRO DOCENTE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(4)
    pts_d = [
        "• Transversalizar la salud intercultural en asignaturas clínicas y comunitarias.",
        "• Priorizar metodologías activas: análisis de casos y talleres vivenciales somáticos.",
        "• Actualizarse en neurobiología de regulación Bottom-Up e interacciones adversas."
    ]
    for pt in pts_d:
        p = tf.add_paragraph()
        p.text = pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_DARK

    # 3. CUR-Estelí
    add_card(s15, Inches(0.8), Inches(4.2), rw, rh)
    box = s15.shapes.add_textbox(Inches(1.0), Inches(4.3), rw - Inches(0.3), rh - Inches(0.2))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PARA LA GESTIÓN INSTITUCIONAL (CUR-ESTELÍ)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(4)
    pts_u = [
        "• Formalizar la aprobación del Manual de Estrategias MTCI para la carrera.",
        "• Constituir el Comité de Ética y Delimitación Profesional del centro universitario.",
        "• Evaluar la incorporación de la asignatura electiva 'Psicología Integrativa'."
    ]
    for pt in pts_u:
        p = tf.add_paragraph()
        p.text = pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_DARK

    # 4. Salud Pública y Facilitadores
    add_card(s15, Inches(6.8), Inches(4.2), rw, rh)
    box = s15.shapes.add_textbox(Inches(7.0), Inches(4.3), rw - Inches(0.3), rh - Inches(0.2))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PARA EL SISTEMA SANITARIO Y MINSA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(4)
    pts_m = [
        "• Fortalecer la difusión del registro de terapeutas tradicionales bajo la Ley 774.",
        "• Habilitar canales de interconsulta médica bidireccional con psicólogos.",
        "• Compromiso ético de complementariedad sin pretender sustituir tratamientos."
    ]
    for pt in pts_m:
        p = tf.add_paragraph()
        p.text = pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_DARK

    # ==========================================================================
    # SLIDE 16: CIERRE INSTITUCIONAL Y AGRADECIMIENTOS
    # ==========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16, RGBColor(244, 247, 250))

    # Decorative header bar
    top_bar2 = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    top_bar2.fill.solid()
    top_bar2.fill.fore_color.rgb = COLOR_GOLD
    top_bar2.line.fill.background()

    # Watermark shield in background
    if os.path.exists(shield_path):
        s16.shapes.add_picture(shield_path, Inches(8.5), Inches(1.2), height=Inches(5.0))

    # Institutional Logo
    if os.path.exists(logo_path):
        s16.shapes.add_picture(logo_path, Inches(0.8), Inches(0.6), height=Inches(1.3))

    # Center-Left Closing Card
    add_card(s16, Inches(0.8), Inches(2.1), Inches(8.2), Inches(4.7), COLOR_BG_CARD, COLOR_BORDER)
    box = s16.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(7.6), Inches(4.3))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "UNIVERSIDAD NACIONAL AUTÓNOMA DE NICARAGUA, MANAGUA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p = tf.add_paragraph()
    p.text = "¡A la libertad por la Universidad!"
    p.font.size = Pt(16)
    p.font.italic = True
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "Muchas Gracias por su Atención"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Espacio Abierto para Preguntas, Comentarios y Defensa Oral ante el Honorable Tribunal Examinador"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK
    p.space_after = Pt(16)

    p = tf.add_paragraph()
    p.text = "Sustentantes:\n • Dina Fabiola García Torres\n • Tatiana Paola López Ramos\n • Engel Enoc Zamora Velásquez\n\nTutora: Dra. Tania Libertad Pérez Guevara\nCUR-Estelí • Octubre, 2026"
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_MUTED

    output_pptx = "Presentacion_Defensa_Tesis_MTCI_UNAN.pptx"
    prs.save(output_pptx)
    print(f"Presentation successfully created and saved at: {output_pptx}")

if __name__ == "__main__":
    create_presentation()
