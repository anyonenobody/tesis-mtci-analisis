import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# PREMIUM ACADEMIC DESIGN SYSTEM (UNAN-Managua & Healthcare Integrativa)
# ==============================================================================
COLOR_NAVY_DARK    = RGBColor(15, 32, 67)       # #0F2043 Executive Deep Navy
COLOR_NAVY_HEADER  = RGBColor(27, 54, 93)       # #1B365D Card Header Navy
COLOR_NAVY_LIGHT   = RGBColor(30, 58, 138)      # #1E3A8A Blue Accent
COLOR_TEAL_DARK    = RGBColor(13, 110, 93)      # #0D6E5D Deep Academic Teal
COLOR_TEAL_HEADER  = RGBColor(15, 118, 110)     # #0F766E Card Header Teal
COLOR_GOLD_ACCENT  = RGBColor(217, 119, 6)      # #D97706 Warm Amber Gold
COLOR_GOLD_DARK    = RGBColor(180, 83, 9)       # #B45309 Deep Gold
COLOR_SLATE_DARK   = RGBColor(30, 41, 59)       # #1E293B High Contrast Body Text
COLOR_SLATE_MUTED  = RGBColor(100, 116, 139)    # #64748B Secondary Text
COLOR_BG_CANVAS    = RGBColor(248, 250, 252)    # #F8FAFC Canvas Background
COLOR_CARD_BG      = RGBColor(255, 255, 255)    # #FFFFFF Pure White
COLOR_CARD_BORDER  = RGBColor(203, 213, 225)    # #CBD5E1 Defined Border

# Modular Row Tints & Accents
COLOR_ROW_BG       = RGBColor(248, 250, 252)    # #F8FAFC Clean Row Fill
COLOR_ROW_BORDER   = RGBColor(226, 232, 240)    # #E2E8F0 Subtle Row Border
COLOR_BLUE_TINT    = RGBColor(239, 246, 255)    # #EFF6FF
COLOR_BLUE_BORDER  = RGBColor(186, 230, 253)    # #BAE6FD
COLOR_TEAL_TINT    = RGBColor(240, 253, 250)    # #F0FDF4
COLOR_TEAL_BORDER  = RGBColor(153, 246, 228)    # #99F6E4
COLOR_GOLD_TINT    = RGBColor(254, 243, 199)    # #FEF3C7
COLOR_GOLD_BORDER  = RGBColor(253, 230, 138)    # #FDE68A
COLOR_ALERT_TINT   = RGBColor(254, 242, 242)    # #FEF2F2
COLOR_ALERT_BORDER = RGBColor(254, 202, 202)    # #FECACA
COLOR_ALERT_TEXT   = RGBColor(185, 28, 28)      # #B91C1C

FONT_HEADING = "Calibri"
FONT_BODY    = "Calibri"

LOGO_CLEAN_PATH   = "assets/extracted/unan_logo_clean.png"
SHIELD_PATH       = "assets/extracted/unan_shield_only.png"
MANUAL_COVER_PATH = "assets/extracted/portada_manual.jpg"

def create_presentation():
    prs = Presentation()
    prs.slide_width  = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout     = prs.slide_layouts[6]

    def set_canvas(slide):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG_CANVAS

    def add_header(slide, badge_text, title_text):
        top_accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
        top_accent.fill.solid()
        top_accent.fill.fore_color.rgb = COLOR_GOLD_ACCENT
        top_accent.line.fill.background()

        pill_w = Inches(len(badge_text) * 0.088 + 0.45)
        if pill_w < Inches(2.3):
            pill_w = Inches(2.3)
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.32), pill_w, Inches(0.32))
        badge.adjustments[0] = 0.35
        badge.fill.solid()
        badge.fill.fore_color.rgb = COLOR_TEAL_TINT
        badge.line.color.rgb = COLOR_TEAL_BORDER
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = False
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_b.margin_left = tf_b.margin_right = Inches(0.12)
        tf_b.margin_top = tf_b.margin_bottom = 0
        pb = tf_b.paragraphs[0]
        pb.alignment = PP_ALIGN.CENTER
        pb.text = badge_text.upper()
        pb.font.name = FONT_HEADING
        pb.font.size = Pt(9)
        pb.font.bold = True
        pb.font.color.rgb = COLOR_TEAL_DARK

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(10.5), Inches(0.55))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        pt = tf_t.paragraphs[0]
        pt.text = title_text
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(20)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_NAVY_DARK

        if os.path.exists(SHIELD_PATH):
            slide.shapes.add_picture(SHIELD_PATH, Inches(12.1), Inches(0.25), height=Inches(0.85))

        bar1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.30), Inches(9.2), Inches(0.025))
        bar1.fill.solid()
        bar1.fill.fore_color.rgb = COLOR_NAVY_HEADER
        bar1.line.fill.background()

        bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(10.05), Inches(1.30), Inches(2.48), Inches(0.025))
        bar2.fill.solid()
        bar2.fill.fore_color.rgb = COLOR_GOLD_ACCENT
        bar2.line.fill.background()

    def add_footer(slide, current_slide, total_slides=16):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.02), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_CARD_BORDER
        line.line.fill.background()

        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(10.0), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "UNAN-Managua • CUR-Estelí | Departamento de Educación y Humanidades • Carrera de Psicología (2026)"
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_SLATE_MUTED

        num_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.7), Inches(7.06), Inches(0.833), Inches(0.26))
        num_pill.adjustments[0] = 0.4
        num_pill.fill.solid()
        num_pill.fill.fore_color.rgb = COLOR_BLUE_TINT
        num_pill.line.color.rgb = COLOR_BLUE_BORDER
        num_pill.line.width = Pt(0.75)
        tf_n = num_pill.text_frame
        tf_n.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
        pn = tf_n.paragraphs[0]
        pn.alignment = PP_ALIGN.CENTER
        pn.text = f"{current_slide} / {total_slides}"
        pn.font.name = FONT_BODY
        pn.font.size = Pt(8)
        pn.font.bold = True
        pn.font.color.rgb = COLOR_NAVY_DARK

    def create_card_container(slide, left, top, width, height, header_title, header_bg=COLOR_NAVY_HEADER, header_icon="", border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.adjustments[0] = 0.03
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1)

        hdr_h = Inches(0.48)
        hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, hdr_h)
        hdr.adjustments[0] = 0.08
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = header_bg
        hdr.line.fill.background()

        tf_h = hdr.text_frame
        tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_h.margin_left = Inches(0.22)
        tf_h.margin_right = Inches(0.2)
        tf_h.margin_top = tf_h.margin_bottom = 0
        p = tf_h.paragraphs[0]
        full_title = f"{header_icon} {header_title}".strip()
        p.text = full_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

        return card

    def add_item_card(slide, left, top, width, height, title, desc, icon="", tint_bg=COLOR_ROW_BG, border_c=COLOR_ROW_BORDER, title_c=COLOR_NAVY_DARK, body_c=COLOR_SLATE_DARK, font_sz=9.5):
        """Creates an individual modular row/card with clean LEFT ALIGNMENT, padding and spacing."""
        row = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        row.adjustments[0] = 0.08
        row.fill.solid()
        row.fill.fore_color.rgb = tint_bg
        row.line.color.rgb = border_c
        row.line.width = Pt(0.75)

        tf = row.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.04)
        tf.margin_bottom = Inches(0.04)

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.15
        
        lead = f"{icon} {title}".strip() + " " if title else ""
        if lead:
            r1 = p.add_run()
            r1.text = lead
            r1.font.name = FONT_HEADING
            r1.font.bold = True
            r1.font.size = Pt(font_sz)
            r1.font.color.rgb = title_c

        if desc:
            r2 = p.add_run()
            r2.text = desc
            r2.font.name = FONT_BODY
            r2.font.size = Pt(font_sz - 0.5)
            r2.font.color.rgb = body_c

        return row

    def add_metric_pill(slide, left, top, width, height, val_text, label_text, tint_bg=COLOR_TEAL_TINT, border_c=COLOR_TEAL_BORDER, text_c=COLOR_TEAL_DARK):
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        pill.adjustments[0] = 0.15
        pill.fill.solid()
        pill.fill.fore_color.rgb = tint_bg
        pill.line.color.rgb = border_c
        pill.line.width = Pt(1)

        tf = pill.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        p1.text = val_text
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = text_c

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.text = label_text
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_SLATE_DARK

    def add_callout_box(slide, left, top, width, height, title_prefix, text_content, tint_bg=COLOR_BLUE_TINT, border_c=COLOR_BLUE_BORDER, text_c=COLOR_NAVY_DARK):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.adjustments[0] = 0.08
        box.fill.solid()
        box.fill.fore_color.rgb = tint_bg
        box.line.color.rgb = border_c
        box.line.width = Pt(1)

        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.06)
        tf.margin_bottom = Inches(0.06)

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.15
        r1 = p.add_run()
        r1.text = title_prefix + ": "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = text_c

        r2 = p.add_run()
        r2.text = text_content
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_SLATE_DARK

    # ==========================================================================
    # SLIDE 1: PORTADA INSTITUCIONAL
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_canvas(s1)

    top_banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.3))
    top_banner.fill.solid(); top_banner.fill.fore_color.rgb = COLOR_NAVY_DARK; top_banner.line.fill.background()

    gold_stripe = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.3), Inches(13.333), Inches(0.06))
    gold_stripe.fill.solid(); gold_stripe.fill.fore_color.rgb = COLOR_GOLD_ACCENT; gold_stripe.line.fill.background()

    if os.path.exists(LOGO_CLEAN_PATH):
        s1.shapes.add_picture(LOGO_CLEAN_PATH, Inches(0.8), Inches(0.18), height=Inches(0.92))

    banner_text = s1.shapes.add_textbox(Inches(3.2), Inches(0.22), Inches(9.2), Inches(0.85))
    tf_b = banner_text.text_frame; tf_b.word_wrap = True
    p0 = tf_b.paragraphs[0]; p0.text = "UNIVERSIDAD NACIONAL AUTÓNOMA DE NICARAGUA, MANAGUA"; p0.font.bold = True; p0.font.size = Pt(13); p0.font.color.rgb = RGBColor(255, 255, 255)
    p1 = tf_b.add_paragraph(); p1.text = "CENTRO UNIVERSITARIO REGIONAL DE ESTELÍ (CUR-ESTELÍ) • RECINTO LEONEL RUGAMA RUGAMA"; p1.font.bold = True; p1.font.size = Pt(9.5); p1.font.color.rgb = COLOR_GOLD_ACCENT
    p2 = tf_b.add_paragraph(); p2.text = "DEPARTAMENTO DE EDUCACIÓN Y HUMANIDADES | CARRERA DE PSICOLOGÍA"; p2.font.size = Pt(8.5); p2.font.color.rgb = RGBColor(203, 213, 225)

    card_w = Inches(11.733)
    card_h = Inches(5.35)
    c1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.60), card_w, card_h)
    c1.adjustments[0] = 0.03; c1.fill.solid(); c1.fill.fore_color.rgb = COLOR_CARD_BG; c1.line.color.rgb = COLOR_CARD_BORDER; c1.line.width = Pt(1)

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.85), Inches(10.9), Inches(2.2))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p = tf.paragraphs[0]; p.text = "TRABAJO DE INVESTIGACIÓN PARA OPTAR AL GRADO DE LICENCIADOS EN PSICOLOGÍA"; p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_DARK; p.space_after = Pt(8)
    p = tf.add_paragraph(); p.text = "La Medicina Tradicional, Complementaria e Integrativa (MTCI) como Complemento en la Atención Psicológica"; p.font.size = Pt(23); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_DARK; p.space_after = Pt(10)
    p = tf.add_paragraph(); p.text = "Estudio Mixto con Estudiantes y Docentes del CUR-Estelí y Facilitadores Locales del Municipio de Estelí (Segundo Semestre, 2026)"; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = COLOR_GOLD_DARK

    div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(4.15), Inches(10.9), Inches(0.02))
    div.fill.solid(); div.fill.fore_color.rgb = COLOR_CARD_BORDER; div.line.fill.background()

    meta_w = Inches(3.45)
    meta_gap = Inches(0.27)
    meta_top = Inches(4.35)
    meta_h = Inches(2.35)

    # Col 1: Sustentantes (Left Aligned)
    s_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), meta_top, meta_w, meta_h)
    s_box.adjustments[0] = 0.06; s_box.fill.solid(); s_box.fill.fore_color.rgb = COLOR_BLUE_TINT; s_box.line.color.rgb = COLOR_BLUE_BORDER; s_box.line.width = Pt(1)
    tf_s = s_box.text_frame; tf_s.vertical_anchor = MSO_ANCHOR.MIDDLE; tf_s.margin_left = Inches(0.25); tf_s.margin_right = Inches(0.20)
    p = tf_s.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "👤 AUTORES / SUSTENTANTES"; p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = COLOR_NAVY_DARK; p.space_after = Pt(8)
    for name in ["• Dina Fabiola García Torres", "• Tatiana Paola López Ramos", "• Engel Enoc Zamora Velásquez"]:
        p = tf_s.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = name; p.font.size = Pt(10); p.font.color.rgb = COLOR_SLATE_DARK; p.space_after = Pt(4)

    # Col 2: Tutoría (Left Aligned)
    t_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2) + meta_w + meta_gap, meta_top, meta_w, meta_h)
    t_box.adjustments[0] = 0.06; t_box.fill.solid(); t_box.fill.fore_color.rgb = COLOR_TEAL_TINT; t_box.line.color.rgb = COLOR_TEAL_BORDER; t_box.line.width = Pt(1)
    tf_t = t_box.text_frame; tf_t.vertical_anchor = MSO_ANCHOR.MIDDLE; tf_t.margin_left = Inches(0.25); tf_t.margin_right = Inches(0.20)
    p = tf_t.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "🎓 TUTORÍA ACADÉMICA"; p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEAL_DARK; p.space_after = Pt(8)
    p = tf_t.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "• Dra. Tania Libertad Pérez Guevara"; p.font.bold = True; p.font.size = Pt(10.5); p.font.color.rgb = COLOR_SLATE_DARK; p.space_after = Pt(4)
    p = tf_t.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "Docente Investigadora • CUR-Estelí\nAsesoría Temática y Metodológica"; p.font.size = Pt(9.5); p.font.color.rgb = COLOR_SLATE_MUTED

    # Col 3: Adscripción y Fecha (Left Aligned)
    a_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2) + (meta_w + meta_gap)*2, meta_top, meta_w, meta_h)
    a_box.adjustments[0] = 0.06; a_box.fill.solid(); a_box.fill.fore_color.rgb = COLOR_GOLD_TINT; a_box.line.color.rgb = COLOR_GOLD_BORDER; a_box.line.width = Pt(1)
    tf_a = a_box.text_frame; tf_a.vertical_anchor = MSO_ANCHOR.MIDDLE; tf_a.margin_left = Inches(0.25); tf_a.margin_right = Inches(0.20)
    p = tf_a.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "🏛 LÍNEA Y CONTEXTO"; p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = COLOR_GOLD_DARK; p.space_after = Pt(8)
    p = tf_a.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "Línea: SAL-3 (Salud e Interculturalidad)\nSublínea: Terapias Alternativas\nRecinto Leonel Rugama Rugama\nEstelí, Nicaragua • Octubre, 2026"; p.font.size = Pt(9.5); p.font.color.rgb = COLOR_SLATE_DARK

    # ==========================================================================
    # SLIDE 2: PLANTEAMIENTO DEL PROBLEMA Y JUSTIFICACIÓN
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_canvas(s2)
    add_header(s2, "Capítulo I • Planteamiento del Problema", "Encrucijada Asistencial, Vacío Formativo y Pertinencia Social")
    add_footer(s2, 2)

    col_w = Inches(5.7)
    card_h = Inches(5.35)

    create_card_container(s2, Inches(0.8), Inches(1.5), col_w, card_h, "PLANTEAMIENTO DEL PROBLEMA Y BRECHA FORMATIVA", COLOR_NAVY_HEADER, "🛑")
    prob_items = [
        ("Asimetría Legal y Sanitaria:", "La Ley No. 774 garantiza acceso a la MTCI; empero, la Ley No. 292 prohíbe tajantemente la prescripción farmacológica a psicólogos.", "⚖️"),
        ("El 'Ocultamiento Terapéutico':", "Los consultantes recurren a medicina natural pero lo callan en consulta por temor a descalificación del terapeuta.", "🤐"),
        ("Vacío en la Malla Curricular:", "Los futuros graduados del CUR-Estelí egresan sin directrices deontológicas para dialogar, psicoeducar o derivar.", "🎓"),
        ("Pregunta Central de Investigación:", "¿Cómo fundamenta el diagnóstico de MTCI en Estelí el diseño de un manual ético y pedagógico para el CUR-Estelí?", "❓")
    ]
    row_h2 = Inches(0.82)
    row_gap2 = Inches(0.08)
    row_top2 = Inches(2.08)
    for i, (t, d, ic) in enumerate(prob_items):
        add_item_card(s2, Inches(1.05), row_top2 + i*(row_h2 + row_gap2), col_w - Inches(0.5), row_h2,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_TEAL_DARK, COLOR_SLATE_DARK, 9.5)

    add_callout_box(s2, Inches(1.05), Inches(5.75), col_w - Inches(0.5), Inches(0.92),
                    "⚠ Encrucijada Práctica",
                    "La población acude cotidianamente a la medicina tradicional; ignorar estos saberes fragmenta la alianza clínica y eleva el riesgo de abandono terapéutico.",
                    COLOR_ALERT_TINT, COLOR_ALERT_BORDER, COLOR_ALERT_TEXT)

    create_card_container(s2, Inches(6.833), Inches(1.5), col_w, card_h, "JUSTIFICACIÓN Y RELEVANCIA MULTIDIMENSIONAL", COLOR_TEAL_HEADER, "💡")
    just_items = [
        ("Pertinencia Ética y Deontológica:", "El principio de beneficencia y alternabilidad exige conocer las prácticas del consultante para resguardar la seguridad clínica.", "🛡️"),
        ("Aporte a la Salud Mental Comunitaria:", "Rescata y visibiliza la memoria viva de facilitadores y la etnobotánica de Estelí dentro del tejido de apoyo psicosocial.", "🌿"),
        ("Impacto Formativo Directo (CUR-Estelí):", "Provee directrices claras para los practicantes en la Clínica Psicosocial y Comunitaria, cerrando la brecha teoría-praxis.", "🏥"),
        ("Alineación con Agendas de Desarrollo:", "Responde a la línea institucional SAL-3 (UNAN-Managua), a las metas SETEC (2025) y al Plan Nacional de Desarrollo Humano.", "🎯")
    ]
    for i, (t, d, ic) in enumerate(just_items):
        add_item_card(s2, Inches(7.083), row_top2 + i*(row_h2 + row_gap2), col_w - Inches(0.5), row_h2,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_GOLD_DARK, COLOR_SLATE_DARK, 9.5)

    add_callout_box(s2, Inches(7.083), Inches(5.75), col_w - Inches(0.5), Inches(0.92),
                    "✨ Aporte Concreto",
                    "Construcción del primer manual ético-propositivo para delimitar las competencias del psicólogo frente a las terapias tradicionales en Nicaragua.",
                    COLOR_GOLD_TINT, COLOR_GOLD_BORDER, COLOR_GOLD_DARK)

    # ==========================================================================
    # SLIDE 3: ANTECEDENTES (3 COLUMNAS CON TARJETAS MODULARES)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_canvas(s3)
    add_header(s3, "Capítulo I • Estado del Arte", "Esquema de Antecedentes Empíricos: Internacional, Nacional y Local")
    add_footer(s3, 3)

    col3_w = Inches(3.75)
    gap3 = Inches(0.24)
    h3 = Inches(5.35)

    # 1. Internacional
    create_card_container(s3, Inches(0.8), Inches(1.5), col3_w, h3, "INTERNACIONAL", COLOR_NAVY_HEADER, "🌐")
    int_items = [
        ("Chafloque-Capuñay et al. (2025):", "Revisión sistemática (22 estudios). Los adultos recurren a la MTCI buscando autonomía, contención y un trato empático ausente en la biomedicina.", "🔍"),
        ("Ortega Cadena et al. (2023):", "Estudio en Colombia: el reduccionismo patologiza saberes populares y crea muros de incomunicación asistencial.", "🌎"),
        ("OMS / OPS (2023, 2025):", "Estrategia Mundial sobre Medicina Tradicional: insta a integrar recursos comunitarios seguros en atención primaria.", "🌍")
    ]
    int_h = Inches(1.08)
    int_gap = Inches(0.12)
    for i, (t, d, ic) in enumerate(int_items):
        add_item_card(s3, Inches(0.98), Inches(2.10) + i*(int_h + int_gap), col3_w - Inches(0.36), int_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_TEAL_DARK, COLOR_SLATE_DARK, 9)

    add_callout_box(s3, Inches(0.98), Inches(5.75), col3_w - Inches(0.36), Inches(0.92),
                    "Eje Global", "Transición hacia modelos asistenciales culturalmente congruentes y centrados en la autonomía del paciente.",
                    COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)

    # 2. Nacional
    create_card_container(s3, Inches(0.8) + col3_w + gap3, Inches(1.5), col3_w, h3, "NACIONAL (NICARAGUA)", COLOR_GOLD_DARK, "🏛")
    nac_items = [
        ("Ley No. 774 (2012):", "Marco jurídico de vanguardia regional que reconoce la medicina natural como derecho en la salud pública.", "📜"),
        ("Romero Hernández (2021):", "Patrimonio etnobotánico en Masaya. Sobadores fungen como escudo de contención psicosomática.", "🌿"),
        ("Cunningham (2021):", "Costa Caribe: articulación horizontal y sinérgica entre médicos convencionales y terapeutas miskitos.", "🤝"),
        ("MINSA (2024):", "Instituto de Medicina Natural respalda la visión holística de salud vinculada a la comunidad.", "🏥")
    ]
    nac_h = Inches(0.80)
    nac_gap = Inches(0.08)
    for i, (t, d, ic) in enumerate(nac_items):
        add_item_card(s3, Inches(0.98) + col3_w + gap3, Inches(2.10) + i*(nac_h + nac_gap), col3_w - Inches(0.36), nac_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_GOLD_DARK, COLOR_SLATE_DARK, 9)

    add_callout_box(s3, Inches(0.98) + col3_w + gap3, Inches(5.75), col3_w - Inches(0.36), Inches(0.92),
                    "Eje Nacional", "Existencia de respaldo normativo con imperiosa necesidad de traducción clínica en las aulas universitarias.",
                    COLOR_GOLD_TINT, COLOR_GOLD_BORDER, COLOR_GOLD_DARK)

    # 3. Local (CUR-Estelí)
    create_card_container(s3, Inches(0.8) + (col3_w + gap3)*2, Inches(1.5), col3_w, h3, "LOCAL (CUR-ESTELÍ)", COLOR_TEAL_HEADER, "📍")
    loc_items = [
        ("Aguilera Altamirano et al. (2019):", "Arteterapia aplicada a internos de Medicina en el Hospital San Juan de Dios de Estelí con disminución de agotamiento emocional.", "🎨"),
        ("Mora Mejías y Bellorín (2020):", "Dramaterapia en estudiantes de Psicología del CUR-Estelí con avances significativos en autoestima.", "🎭"),
        ("Hallazgo Articulador Clave:", "Los estudiantes de Psicología ya utilizan empíricamente la MTCI como estrategia de autocuidado ante sobrecarga académica.", "✨")
    ]
    for i, (t, d, ic) in enumerate(loc_items):
        add_item_card(s3, Inches(0.98) + (col3_w + gap3)*2, Inches(2.10) + i*(int_h + int_gap), col3_w - Inches(0.36), int_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_TEAL_DARK, COLOR_SLATE_DARK, 9)

    add_callout_box(s3, Inches(0.98) + (col3_w + gap3)*2, Inches(5.75), col3_w - Inches(0.36), Inches(0.92),
                    "Eje Local", "Evidencia empírica directa de la viabilidad formativa de técnicas somáticas en el campus Estelí.",
                    COLOR_TEAL_TINT, COLOR_TEAL_BORDER, COLOR_TEAL_DARK)

    # ==========================================================================
    # SLIDE 4: CONTEXTO DEL ESTUDIO (CUR-ESTELÍ Y MAPA)
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_canvas(s4)
    add_header(s4, "Capítulo I • Contextualización Institucional", "Coordenadas Territoriales, Dispositivos Clínicos y Vinculación Comunitaria")
    add_footer(s4, 4)

    w_left = Inches(5.8)
    create_card_container(s4, Inches(0.8), Inches(1.5), w_left, h3, "ESCENARIO TERRITORIAL E INSTITUCIONAL", COLOR_NAVY_HEADER, "🏛")
    ctx_pts = [
        ("Municipio de Estelí:", "Cabecera con dinámico comercio y arraigada tradición comunitaria en flora medicinal y sobadores.", "📍"),
        ("Recinto Leonel Rugama Rugama:", "Sede del CUR-Estelí donde convergen alumnos matutinos y sabatinos de todo el norte.", "🏫"),
        ("Clínica Psicosocial y Comunitaria:", "Dispositivo asistencial clave donde practicantes de 4.° y 5.° año brindan atención psicoterapéutica.", "🧠"),
        ("Consultorio Médico Comunitario:", "Espacio de salud primaria y campañas preventivas articulado estrechamente con el MINSA.", "🩺"),
        ("Línea Institucional SAL-3:", "Inscrito en la sublínea SAL-3.1 (Medicina natural), vinculado al Plan Nacional de Desarrollo Humano.", "📈")
    ]
    ctx_h = Inches(0.66)
    ctx_gap = Inches(0.08)
    for i, (t, d, ic) in enumerate(ctx_pts):
        add_item_card(s4, Inches(1.02), Inches(2.08) + i*(ctx_h + ctx_gap), w_left - Inches(0.44), ctx_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_TEAL_DARK, COLOR_SLATE_DARK, 9.5)

    add_callout_box(s4, Inches(1.02), Inches(5.80), w_left - Inches(0.44), Inches(0.88),
                    "Pertinencia Situada", "Investigación conectada con las necesidades de salud mental de las comunidades urbanas y rurales de Estelí.",
                    COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)

    # Right: Map Figure 1
    w_right = Inches(5.6)
    create_card_container(s4, Inches(6.933), Inches(1.5), w_right, h3, "MAPA DE UBICACIÓN (CUR-ESTELÍ)", COLOR_TEAL_HEADER, "🗺")
    fig1 = "assets/figuras_apa7/figura_01_ubicacion_cur_esteli.png"
    if os.path.exists(fig1):
        s4.shapes.add_picture(fig1, Inches(7.133), Inches(2.10), width=Inches(5.2), height=Inches(3.55))

    add_callout_box(s4, Inches(7.133), Inches(5.80), Inches(5.2), Inches(0.88),
                    "Figura 1 (APA 7)", "Delimitación del CUR-Estelí, recinto Leonel Rugama Rugama, Estelí, Nicaragua (Cartografía Institucional, 2026).",
                    COLOR_TEAL_TINT, COLOR_TEAL_BORDER, COLOR_TEAL_DARK)

    # ==========================================================================
    # SLIDE 5: OBJETIVOS DE LA INVESTIGACIÓN (FILAS MODULARES POR OE)
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_canvas(s5)
    add_header(s5, "Capítulo I • Arquitectura Teleológica", "Esquema Articulador de Objetivos de Investigación")
    add_footer(s5, 5)

    # Top: Objetivo General Box
    og_h = Inches(1.80)
    create_card_container(s5, Inches(0.8), Inches(1.5), Inches(11.733), og_h, "OBJETIVO GENERAL DE LA INVESTIGACIÓN", COLOR_NAVY_HEADER, "🎯")
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(11.1), Inches(1.15))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    p.text = "Explorar la percepción de la Medicina Tradicional, Complementaria e Integrativa (MTCI) como recurso de apoyo en la atención psicológica desde la mirada de actores locales, estudiantes y docentes de Psicología del CUR-Estelí durante el segundo semestre del año 2026."
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(6)

    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.LEFT
    p2.text = "▶ Articulación Metodológica: Triangulación concurrente de datos cuantitativos (estudiantes) y cualitativos (facilitadores territoriales y claustro docente)."
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_GOLD_DARK

    # Bottom: 3 Objetivos Específicos
    oe_top = Inches(3.50)
    oe_h = Inches(3.35)
    oes = [
        ("OBJETIVO ESPECÍFICO 1", "DIAGNÓSTICO CUANTITATIVO",
         "Caracterizar conocimientos conceptuales, normativos y frecuencia de uso en estudiantes de 4.º y 5.º año.",
         "Muestra y Alcance:", "53 de 4.° año y 15 de 5.° año preprofesional (n = 68 participantes).",
         "Vía Cuantitativa", "I1: Escala Likert estandarizada (n = 68)", COLOR_TEAL_HEADER),
        ("OBJETIVO ESPECÍFICO 2", "EXPLORACIÓN CUALITATIVA",
         "Describir beneficios percibidos y posibles efectos adversos desde facilitadores locales de Estelí.",
         "Muestra y Alcance:", "9 terapeutas tradicionales y holísticos con hasta 30 años de experiencia.",
         "Vía Cualitativa", "I2: Cuestionario semiestructurado (n = 9)", COLOR_GOLD_DARK),
        ("OBJETIVO ESPECÍFICO 3", "FORMULACIÓN PROPOSITIVA",
         "Proponer estrategias complementarias para abordar la MTCI formalizadas en un manual técnico-ético.",
         "Producto Tangible:", "Manual de 18 páginas con algoritmos de decisión clínica (Anexo 16.2).",
         "Vía Propositiva", "I3 (n = 9) + Manual Técnico de 18 págs.", COLOR_NAVY_HEADER)
    ]
    for i, (oe_t, oe_sub, oe_desc, scope_t, scope_d, via_t, inst_t, hdr_c) in enumerate(oes):
        left_i = Inches(0.8) + i * (col3_w + gap3)
        create_card_container(s5, left_i, oe_top, col3_w, oe_h, oe_t, hdr_c, "📌")

        # Item 1: Main objective
        add_item_card(s5, left_i + Inches(0.18), oe_top + Inches(0.55), col3_w - Inches(0.36), Inches(0.95),
                      oe_sub + ":", oe_desc, "🎯", COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_NAVY_DARK, COLOR_SLATE_DARK, 9.5)

        # Item 2: Scope & sample
        add_item_card(s5, left_i + Inches(0.18), oe_top + Inches(1.58), col3_w - Inches(0.36), Inches(0.95),
                      scope_t, scope_d, "👥", COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_TEAL_DARK, COLOR_SLATE_DARK, 9)

        # Bottom Instrument Callout
        add_callout_box(s5, left_i + Inches(0.18), oe_top + Inches(2.62), col3_w - Inches(0.36), Inches(0.60),
                        via_t, inst_t, COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)

    # ==========================================================================
    # SLIDE 6: MARCO TEÓRICO (1/2: BASES CONCEPTUALES Y NORMATIVAS)
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_canvas(s6)
    add_header(s6, "Capítulo II • Marco Teórico (1/2)", "Bases Conceptuales de la MTCI, Taxonomía OMS y Marco Jurídico Nicaragüense")
    add_footer(s6, 6)

    create_card_container(s6, Inches(0.8), Inches(1.5), col_w, card_h, "DESLINDE CONCEPTUAL Y TAXONOMÍA (OMS/OPS)", COLOR_NAVY_HEADER, "📚")
    concepts = [
        ("Medicina Tradicional (MT):", "Saberes ancestrales transmitidos oralmente para salvaguardar la salud biopsicosocial (OMS, 2025). En Nicaragua se arraiga en la etnobotánica viva.", "🌱"),
        ("Medicina Complementaria (MC):", "Prácticas de atención en salud no autóctonas utilizadas coadyuvantemente sin sustituir a la alopatía (OMS, 2022).", "🌿"),
        ("Medicina Integrativa (MI):", "Coordinación sinérgica de tratamientos convencionales y complementarios bajo evidencia científica (OPS, 2023).", "🔬"),
        ("Taxonomía Ley 774 (Art. 12):", "Terapias energéticas (Reiki); manuales (masajes); fitoterapia, aromaterapia; hidroterapia y sistémicas.", "📑")
    ]
    for i, (t, d, ic) in enumerate(concepts):
        add_item_card(s6, Inches(1.05), row_top2 + i*(row_h2 + row_gap2), col_w - Inches(0.5), row_h2,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_TEAL_DARK, COLOR_SLATE_DARK, 9.5)

    add_callout_box(s6, Inches(1.05), Inches(5.75), col_w - Inches(0.5), Inches(0.92),
                    "Paradigma Holístico", "El bienestar supera la ausencia de enfermedad; implica el equilibrio armónico entre mente, cuerpo y entorno social.",
                    COLOR_TEAL_TINT, COLOR_TEAL_BORDER, COLOR_TEAL_DARK)

    # Right: Marco Jurídico Nicaragüense
    create_card_container(s6, Inches(6.833), Inches(1.5), col_w, card_h, "MARCO JURÍDICO SANITARIO DE NICARAGUA", COLOR_GOLD_DARK, "⚖")
    laws = [
        ("Ley No. 774 (Asamblea Nacional, 2012):", "Ley de Medicina Natural, Terapias Complementarias y Productos Naturales. Consagra el acceso a la MTCI como derecho inalienable y mandata su integración pública.", "📜"),
        ("Ley No. 292 (Asamblea Nacional, 1998):", "Ley de Medicamentos y Farmacias. Prohíbe de forma terminante al profesional de la Psicología prescribir psicofármacos o productos medicinales.", "⛔"),
        ("Ley No. 759 (Asamblea Nacional, 2011):", "Ley de Medicina Tradicional Ancestral. Salvaguarda, promueve y reconoce el patrimonio de los pueblos originarios y afrodescendientes.", "🏛️")
    ]
    law_h = Inches(1.10)
    law_gap = Inches(0.12)
    for i, (t, d, ic) in enumerate(laws):
        add_item_card(s6, Inches(7.083), Inches(2.08) + i*(law_h + law_gap), col_w - Inches(0.5), law_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_GOLD_DARK, COLOR_SLATE_DARK, 9.5)

    add_callout_box(s6, Inches(7.083), Inches(5.75), col_w - Inches(0.5), Inches(0.92),
                    "Delimitación Deontológica", "El psicólogo debe alfabetizarse en MTCI no para prescribir fármacos, sino para dialogar, psicoeducar y derivar éticamente.",
                    COLOR_ALERT_TINT, COLOR_ALERT_BORDER, COLOR_ALERT_TEXT)

    # ==========================================================================
    # SLIDE 7: MARCO TEÓRICO (2/2: DIMENSIÓN PSICOFISIOLÓGICA TOP-DOWN / BOTTOM-UP)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_canvas(s7)
    add_header(s7, "Capítulo II • Marco Teórico (2/2)", "Dimensión Psicofisiológica: Articulación Clínica Top-Down y Bottom-Up")
    add_footer(s7, 7)

    td_h = Inches(3.40)
    create_card_container(s7, Inches(0.8), Inches(1.5), col_w, td_h, "VÍA TOP-DOWN (CORTICAL / REFLEXIVA)", COLOR_NAVY_HEADER, "🧠")
    td_items = [
        ("Mecanismo Neurocognitivo:", "Opera mediante la corteza prefrontal, el lenguaje reflexivo y la resignificación de creencias (Laricchiuta et al., 2023).", "⚡"),
        ("Técnicas Propias:", "Psicoterapia verbal, diálogo socrático, narrativa autobiográfica y toma de decisiones conscientes.", "🗣️"),
        ("Limitación en Crisis:", "La hiperactivación simpática y el desborde amigdalino bloquean el procesamiento cortical superior.", "⚠️")
    ]
    td_row_h = Inches(0.80)
    td_gap = Inches(0.08)
    for i, (t, d, ic) in enumerate(td_items):
        add_item_card(s7, Inches(1.02), Inches(2.08) + i*(td_row_h + td_gap), col_w - Inches(0.44), td_row_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_TEAL_DARK, COLOR_SLATE_DARK, 9.5)

    create_card_container(s7, Inches(6.833), Inches(1.5), col_w, td_h, "VÍA BOTTOM-UP (SOMÁTICA / MTCI)", COLOR_TEAL_HEADER, "🌿")
    bu_items = [
        ("Mecanismo Neurovegetativo:", "Incide sobre el sistema nervioso autónomo, la respuesta vagal ventral y los centros subcorticales (Thomson, 2023).", "🫀"),
        ("Aporte Específico MTCI:", "Respiración diafragmática, masoterapia, fitoterapia ansiolítica suave (manzanilla, tilo) y escaneo somático.", "🫁"),
        ("Efecto Facilitador:", "Desactiva la hipertonía miofascial y devuelve al organismo a su ventana de tolerancia neurofisiológica.", "✨")
    ]
    for i, (t, d, ic) in enumerate(bu_items):
        add_item_card(s7, Inches(7.053), Inches(2.08) + i*(td_row_h + td_gap), col_w - Inches(0.44), td_row_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_GOLD_DARK, COLOR_SLATE_DARK, 9.5)

    syn_top = Inches(5.05)
    syn_h = Inches(1.80)
    create_card_container(s7, Inches(0.8), syn_top, Inches(11.733), syn_h, "LA SINERGIA CLÍNICA INTEGRATIVA EN SALUD MENTAL", COLOR_GOLD_DARK, "🔄")
    tb_syn = s7.shapes.add_textbox(Inches(1.1), syn_top + Inches(0.55), Inches(11.1), Inches(1.15))
    tf_syn = tb_syn.text_frame; tf_syn.word_wrap = True; tf_syn.margin_left = tf_syn.margin_right = tf_syn.margin_top = tf_syn.margin_bottom = 0
    p = tf_syn.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    p.text = "La integración de la MTCI en psicología no sustituye el rigor científico; fundamenta un modelo biopsicosocial completo:"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(6)

    p2 = tf_syn.add_paragraph(); p2.alignment = PP_ALIGN.LEFT
    p2.text = "Al calmar la sobrecarga somática y neurovegetativa mediante recursos Bottom-Up (masajes, respiración consciente, fitoterapia suave), se instaura una base neurofisiológica de seguridad que optimiza y potencia la psicoterapia reflexiva Top-Down (reestructuración cognitiva y narrativa reflexiva), consolidando una alianza terapéutica culturalmente sensible."
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_SLATE_DARK

    # ==========================================================================
    # SLIDE 8: DISEÑO METODOLÓGICO (1/2: TIPOLOGÍA, PARADIGMA Y 4 FASES)
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_canvas(s8)
    add_header(s8, "Capítulo III • Diseño Metodológico (1/2)", "Tipología de Estudio, Paradigma Pragmático y Fases de la Investigación")
    add_footer(s8, 8)

    create_card_container(s8, Inches(0.8), Inches(1.5), col_w, card_h, "TIPOLOGÍA Y PARADIGMA METODOLÓGICO", COLOR_NAVY_HEADER, "📐")
    met_items = [
        ("Enfoque Mixto Concurrente (DIAC):", "Articula la medición cuantitativa (OE1) con la hermenéutica cualitativa (OE2 y OE3) en discusión dialógica.", "📊"),
        ("Paradigma Pragmático (Arias, 2023):", "Supera disputas dogmáticas; supedita el método a resolver el problema real en la clínica y aulas del CUR-Estelí.", "🧩"),
        ("Nivel y Diseño Temporal:", "Descriptivo con alcance exploratorio y propositivo; diseño no experimental y transversal (segundo semestre 2026).", "⏱️"),
        ("Adscripción Institucional:", "Campo UNESCO 0313 (Psicología), Línea SAL-3 (UNAN-Managua) y Agenda Nacional de Investigación SETEC.", "🏛️")
    ]
    for i, (t, d, ic) in enumerate(met_items):
        add_item_card(s8, Inches(1.05), row_top2 + i*(row_h2 + row_gap2), col_w - Inches(0.5), row_h2,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_TEAL_DARK, COLOR_SLATE_DARK, 9.5)

    add_callout_box(s8, Inches(1.05), Inches(5.75), col_w - Inches(0.5), Inches(0.92),
                    "Rigor Metodológico", "Validación de instrumentos mediante juicio crítico de 4 expertos universitarios y triangulación concurrente de fuentes.",
                    COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)

    create_card_container(s8, Inches(6.833), Inches(1.5), col_w, card_h, "LAS CUATRO FASES DE LA INVESTIGACIÓN", COLOR_TEAL_HEADER, "🔄")
    phases = [
        ("FASE 1: Preliminar y Fundamentación", "Delimitación del problema, formulación de objetivos, revisión sistemática y marco de Leyes 774, 759 y 292.", "1️⃣"),
        ("FASE 2: Diseño y Validación Instrumental", "Construcción de cuestionarios I1, I2 e I3; juicio crítico de 4 expertos universitarios en pertinencia y escala.", "2️⃣"),
        ("FASE 3: Trabajo de Campo y Análisis Empírico", "Levantamiento muestral (n = 68 alumnos, n = 9 facilitadores, n = 9 docentes), SPSS v26 y análisis temático.", "3️⃣"),
        ("FASE 4: Formulación Propositiva del Manual (OE3)", "Traducción de brechas diagnósticas en el Manual de Estrategias MTCI de 18 páginas para la práctica clínica.", "4️⃣")
    ]
    for i, (t, d, ic) in enumerate(phases):
        add_item_card(s8, Inches(7.083), row_top2 + i*(row_h2 + row_gap2), col_w - Inches(0.5), row_h2,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_GOLD_DARK, COLOR_SLATE_DARK, 9.5)

    add_callout_box(s8, Inches(7.083), Inches(5.75), col_w - Inches(0.5), Inches(0.92),
                    "Producto Final Tangible", "El proceso investigativo culmina en una herramienta aplicable in extenso en el Anexo 16.2 de la tesis.",
                    COLOR_GOLD_TINT, COLOR_GOLD_BORDER, COLOR_GOLD_DARK)

    # ==========================================================================
    # SLIDE 9: DISEÑO METODOLÓGICO (2/2: MUESTRAS, CRITERIOS E INSTRUMENTOS)
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_canvas(s9)
    add_header(s9, "Capítulo III • Diseño Metodológico (2/2)", "Unidades de Análisis, Muestra Participante (N = 86) e Instrumentos de Campo")
    add_footer(s9, 9)

    w_fig = Inches(5.4)
    create_card_container(s9, Inches(0.8), Inches(1.5), w_fig, card_h, "CRITERIOS DE SELECCIÓN MUESTRAL", COLOR_NAVY_HEADER, "🔍")
    fig2 = "assets/figuras_apa7/figura_02_criterios_inclusion_exclusion.png"
    if os.path.exists(fig2):
        s9.shapes.add_picture(fig2, Inches(0.95), Inches(2.10), width=Inches(5.1), height=Inches(3.55))

    add_callout_box(s9, Inches(0.95), Inches(5.80), Inches(5.1), Inches(0.88),
                    "Figura 2 (APA 7)", "Flujograma de inclusión y exclusión aplicado a estudiantes, facilitadores y docentes (Elaboración propia, 2026).",
                    COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)

    w_units = Inches(6.0)
    create_card_container(s9, Inches(6.533), Inches(1.5), w_units, card_h, "TRES UNIDADES DE ANÁLISIS (N = 86)", COLOR_TEAL_HEADER, "👥")

    pill_w = Inches(1.8)
    add_metric_pill(s9, Inches(6.75), Inches(2.10), pill_w, Inches(0.8), "n = 68", "Estudiantes", COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)
    add_metric_pill(s9, Inches(6.75) + pill_w + Inches(0.12), Inches(2.10), pill_w, Inches(0.8), "n = 9", "Facilitadores", COLOR_GOLD_TINT, COLOR_GOLD_BORDER, COLOR_GOLD_DARK)
    add_metric_pill(s9, Inches(6.75) + (pill_w + Inches(0.12))*2, Inches(2.10), pill_w, Inches(0.8), "n = 9", "Docentes", COLOR_TEAL_TINT, COLOR_TEAL_BORDER, COLOR_TEAL_DARK)

    u_pts = [
        ("1. Estudiantes de Psicología (n = 68):", "53 de 4.° año (77.9%) y 15 de 5.° año (22.1%) en turnos matutino y sabatino. Cuestionario I1 (12 ítems Likert y selección múltiple en Google Forms).", "🎓"),
        ("2. Facilitadores Locales (n = 9):", "7 mujeres y 2 hombres con amplia trayectoria en Estelí. Cuestionario cualitativo semiestructurado I2 (11 preguntas abiertas).", "🌿"),
        ("3. Claustro Docente-Psicólogos (n = 9):", "Profesores activos de grado y posgrado. Cuestionario reflexivo I3 (14 preguntas abiertas sobre pertinencia curricular).", "👨‍🏫")
    ]
    u_h = Inches(0.80)
    u_gap = Inches(0.08)
    for i, (t, d, ic) in enumerate(u_pts):
        add_item_card(s9, Inches(6.75), Inches(3.08) + i*(u_h + u_gap), w_units - Inches(0.44), u_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER,
                      COLOR_TEAL_DARK if i==0 else COLOR_GOLD_DARK if i==1 else COLOR_NAVY_DARK,
                      COLOR_SLATE_DARK, 9.5)

    add_callout_box(s9, Inches(6.75), Inches(5.80), w_units - Inches(0.44), Inches(0.88),
                    "Triangulación Concurrente", "Convergencia metodológica de la medición estandarizada con la fenomenología territorial y pedagógica.",
                    COLOR_TEAL_TINT, COLOR_TEAL_BORDER, COLOR_TEAL_DARK)

    # ==========================================================================
    # SLIDE 10: RESULTADOS (1/4: CARACTERIZACIÓN Y BRECHA NORMATIVA - OE1)
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_canvas(s10)
    add_header(s10, "Capítulo IV • Resultados Empíricos (1/4)", "Caracterización de la Muestra Estudiantil y Brecha de Conocimiento Normativo (OE1)")
    add_footer(s10, 10)

    create_card_container(s10, Inches(0.8), Inches(1.5), col_w, card_h, "CARACTERIZACIÓN SOCIODEMOGRÁFICA (n = 68)", COLOR_NAVY_HEADER, "📊")
    fig3 = "assets/figuras_apa7/figura_03_demografia_estudiantes.png"
    if os.path.exists(fig3):
        s10.shapes.add_picture(fig3, Inches(1.0), Inches(2.10), width=col_w - Inches(0.4), height=Inches(2.55))

    add_item_card(s10, Inches(1.05), Inches(4.75), col_w - Inches(0.5), Inches(0.88),
                  "Perfil Sociodemográfico:",
                  "Feminización: 82.4% mujeres (n = 56). Colectivo joven: 61.8% entre 20 y 22 años. Formación: 77.9% en 4.º año y 22.1% en 5.º año preprofesional.",
                  "👥", COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_NAVY_DARK, COLOR_SLATE_DARK, 9)

    add_callout_box(s10, Inches(1.05), Inches(5.75), col_w - Inches(0.5), Inches(0.92),
                    "Perfil Formativo", "Población colectivamente femenina, joven y en culminación de prácticas clínicas.",
                    COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)

    create_card_container(s10, Inches(6.833), Inches(1.5), col_w, card_h, "BRECHA COGNITIVO-NORMATIVA EN ESTUDIANTES", COLOR_GOLD_DARK, "⚠️")
    fig4 = "assets/figuras_apa7/figura_04_dominio_conceptual_normativo_estudiantes.png"
    if os.path.exists(fig4):
        s10.shapes.add_picture(fig4, Inches(7.033), Inches(2.10), width=col_w - Inches(0.4), height=Inches(2.55))

    add_item_card(s10, Inches(7.083), Inches(4.75), col_w - Inches(0.5), Inches(0.88),
                  "Disparidad Cognitiva:",
                  "67.6% acierta concepto OMS pero 75% ignora aplicación clínica. 58.8% desconoce Ley 774 y 64.7% desconoce Ley 292 (prohibición de prescribir fármacos).",
                  "⚠️", COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_ALERT_TEXT, COLOR_SLATE_DARK, 9)

    add_callout_box(s10, Inches(7.083), Inches(5.75), col_w - Inches(0.5), Inches(0.92),
                    "Alerta Formativa", "La brecha jurídica expone a los futuros profesionales a dilemas deontológicos y riesgos de mala praxis.",
                    COLOR_ALERT_TINT, COLOR_ALERT_BORDER, COLOR_ALERT_TEXT)

    # ==========================================================================
    # SLIDE 11: RESULTADOS (2/4: PARADOJA FORMATIVA Y BIENESTAR - OE1)
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_canvas(s11)
    add_header(s11, "Capítulo IV • Resultados Empíricos (2/4)", "La Paradoja Formativa y la Eficacia Subjetiva del Autocuidado Somático (OE1)")
    add_footer(s11, 11)

    create_card_container(s11, Inches(0.8), Inches(1.5), col_w, card_h, "LA GRAN PARADOJA FORMATIVA ESTUDIANTIL", COLOR_NAVY_HEADER, "⚖️")

    badge_w = col_w - Inches(0.5)
    badge_h = Inches(1.02)
    b_top1 = Inches(2.10)
    b_top2 = b_top1 + badge_h + Inches(0.14)
    b_top3 = b_top2 + badge_h + Inches(0.14)

    add_metric_pill(s11, Inches(1.05), b_top1, badge_w, badge_h,
                    "89.7%", "VALIDA LA PERTINENCIA CLÍNICA DE LA MTCI EN PSICOTERAPIA",
                    COLOR_TEAL_TINT, COLOR_TEAL_BORDER, COLOR_TEAL_DARK)

    add_metric_pill(s11, Inches(1.05), b_top2, badge_w, badge_h,
                    "88.2%", "AUTOPERCIBE PREPARACIÓN INSUFICIENTE O NULA PARA DERIVAR",
                    COLOR_ALERT_TINT, COLOR_ALERT_BORDER, COLOR_ALERT_TEXT)

    add_metric_pill(s11, Inches(1.05), b_top3, badge_w, badge_h,
                    "86.8%", "AUTOPERCIBE PREPARACIÓN INSUFICIENTE O NULA PARA PSICOEDUCAR",
                    COLOR_ALERT_TINT, COLOR_ALERT_BORDER, COLOR_ALERT_TEXT)

    add_callout_box(s11, Inches(1.05), Inches(5.75), badge_w, Inches(0.92),
                    "Paradoja Medular", "Convicción ética plena sobre el valor de la MTCI, pero con total desamparo procedimental y curricular.",
                    COLOR_GOLD_TINT, COLOR_GOLD_BORDER, COLOR_GOLD_DARK)

    create_card_container(s11, Inches(6.833), Inches(1.5), col_w, card_h, "USO PERSONAL Y EFICACIA SOMÁTICA PERCIBIDA", COLOR_TEAL_HEADER, "🧘")
    fig7 = "assets/figuras_apa7/figura_07_frecuencia_uso_estudiantes.png"
    if os.path.exists(fig7):
        s11.shapes.add_picture(fig7, Inches(7.033), Inches(2.10), width=col_w - Inches(0.4), height=Inches(2.55))

    add_item_card(s11, Inches(7.083), Inches(4.75), col_w - Inches(0.5), Inches(0.88),
                  "Patrón de Uso Empírico:",
                  "Carácter reactivo: 52.9% no usa la MTCI preventivamente. 86.7% reporta alivio somático favorable en estrés. 0.0% reporta efectos adversos.",
                  "🌿", COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_TEAL_DARK, COLOR_SLATE_DARK, 9)

    add_callout_box(s11, Inches(7.083), Inches(5.75), col_w - Inches(0.5), Inches(0.92),
                    "Eficacia Somática", "El estudiantado experimenta en primera persona la eficacia del alivio somático frente al estrés académico.",
                    COLOR_TEAL_TINT, COLOR_TEAL_BORDER, COLOR_TEAL_DARK)

    # ==========================================================================
    # SLIDE 12: RESULTADOS (3/4: FACILITADORES Y DOCENTES)
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_canvas(s12)
    add_header(s12, "Capítulo IV • Resultados Empíricos (3/4)", "Perspectiva de Facilitadores Locales de Estelí y Claustro Docente (OE2 y OE3)")
    add_footer(s12, 12)

    create_card_container(s12, Inches(0.8), Inches(1.5), col_w, card_h, "FACILITADORES LOCALES DE ESTELÍ (n = 9)", COLOR_TEAL_HEADER, "🌿")

    p_w = Inches(1.68)
    p_gap = Inches(0.08)
    add_metric_pill(s12, Inches(1.05), Inches(2.08), p_w, Inches(0.72), "77.8%", "Mujeres (n=7)", COLOR_TEAL_TINT, COLOR_TEAL_BORDER, COLOR_TEAL_DARK)
    add_metric_pill(s12, Inches(1.05) + p_w + p_gap, Inches(2.08), p_w, Inches(0.72), "44.4%", ">20 Años Exp.", COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)
    add_metric_pill(s12, Inches(1.05) + (p_w + p_gap)*2, Inches(2.08), p_w, Inches(0.72), "100%", "Alivio Somático", COLOR_GOLD_TINT, COLOR_GOLD_BORDER, COLOR_GOLD_DARK)

    fac_pts = [
        ("Cobertura Territorial y Terapias:", "Concentrados en Estelí urbano (77.8%); oferta en masoterapia, fitoterapia, reflexología y reiki.", "📍"),
        ("Alivio Somático Directo (100%):", "Reducción drástica de hiperactivación simpática; 88.9% constata mayor receptividad reflexiva.", "⚡"),
        ("Estigma Sociocultural (100%):", "Enfrentan con frecuencia mitos, tabúes y prejuicios religiosos en la población sobre medicina natural.", "🛑"),
        ("Factor Económico y Adherencia (77.8%):", "La limitada capacidad adquisitiva interrumpe la continuidad y adherencia de los usuarios.", "💼")
    ]
    f_row_h = Inches(0.66)
    f_row_gap = Inches(0.07)
    f_top = Inches(2.88)
    for i, (t, d, ic) in enumerate(fac_pts):
        add_item_card(s12, Inches(1.05), f_top + i*(f_row_h + f_row_gap), col_w - Inches(0.5), f_row_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_TEAL_DARK, COLOR_SLATE_DARK, 9.5)

    add_callout_box(s12, Inches(1.05), Inches(5.80), col_w - Inches(0.5), Inches(0.88),
                    "Desafío Territorial", "Persisten trabas burocráticas de acreditación (22.2%) y asimetría con el sistema biomédico hegemónico.",
                    COLOR_ALERT_TINT, COLOR_ALERT_BORDER, COLOR_ALERT_TEXT)

    create_card_container(s12, Inches(6.833), Inches(1.5), col_w, card_h, "CLAUSTRO DOCENTE-PSICÓLOGOS (n = 9)", COLOR_NAVY_HEADER, "🎓")

    add_metric_pill(s12, Inches(7.083), Inches(2.08), p_w, Inches(0.72), "100%", "Apoyo Curricular", COLOR_TEAL_TINT, COLOR_TEAL_BORDER, COLOR_TEAL_DARK)
    add_metric_pill(s12, Inches(7.083) + p_w + p_gap, Inches(2.08), p_w, Inches(0.72), "88.9%", "Talleres Vivenciales", COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)
    add_metric_pill(s12, Inches(7.083) + (p_w + p_gap)*2, Inches(2.08), p_w, Inches(0.72), "100%", "Base en Evidencia", COLOR_GOLD_TINT, COLOR_GOLD_BORDER, COLOR_GOLD_DARK)

    doc_pts = [
        ("Inserción Curricular Unánime:", "La totalidad del claustro (100%) respalda incorporar la MTCI bajo enfoque crítico, bioético y científico.", "🏛️"),
        ("Metodologías Formativas Priorizadas:", "Rechazan enseñanza memorística; priorizan talleres prácticos (88.9%) e intercambios con facilitadores.", "🛠️"),
        ("Competencias Indispensables a Formar:", "Juicio clínico crítico, delimitación de rol, prevención de riesgos adversos y derivación ética.", "⚖️"),
        ("Demanda de Capacitación Propia:", "El profesorado solicita formación continua en neurobiología somática y regulación Bottom-Up.", "📚")
    ]
    for i, (t, d, ic) in enumerate(doc_pts):
        add_item_card(s12, Inches(7.083), f_top + i*(f_row_h + f_row_gap), col_w - Inches(0.5), f_row_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_NAVY_DARK, COLOR_SLATE_DARK, 9.5)

    add_callout_box(s12, Inches(7.083), Inches(5.80), col_w - Inches(0.5), Inches(0.88),
                    "Propuesta Docente", "Creación urgente de un Comité de Ética y Delimitación Profesional en el CUR-Estelí.",
                    COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)

    # ==========================================================================
    # SLIDE 13: RESULTADOS (4/4: PROPUESTA MANUAL MTCI - CUADRÍCULA DE 8 MÓDULOS)
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_canvas(s13)
    add_header(s13, "Capítulo V • Propuesta Operativa (OE3)", "Manual de Estrategias de MTCI para la Formación y Práctica Psicológica")
    add_footer(s13, 13)

    w_man = Inches(4.3)
    create_card_container(s13, Inches(0.8), Inches(1.5), w_man, card_h, "PRODUCTO PROPOSITIVO (OE3)", COLOR_NAVY_HEADER, "📘")
    if os.path.exists(MANUAL_COVER_PATH):
        s13.shapes.add_picture(MANUAL_COVER_PATH, Inches(1.0), Inches(2.10), width=w_man - Inches(0.4), height=Inches(2.45))

    add_item_card(s13, Inches(1.0), Inches(4.68), w_man - Inches(0.4), Inches(0.95),
                  "Ficha Técnica del Manual:",
                  "Manual Técnico-Ético (18 págs in extenso en Anexo 16.2). Diseñado para docentes y practicantes de 4.° y 5.° año en la Clínica Psicosocial.",
                  "📋", COLOR_ROW_BG, COLOR_ROW_BORDER, COLOR_NAVY_DARK, COLOR_SLATE_DARK, 9)

    add_callout_box(s13, Inches(1.0), Inches(5.75), w_man - Inches(0.4), Inches(0.92),
                    "Propósito Central", "No habilita como terapeutas alternativos; dota de discernimiento ético para explorar y derivar.",
                    COLOR_GOLD_TINT, COLOR_GOLD_BORDER, COLOR_GOLD_DARK)

    # Right: Cuadrícula Modular (8 Módulos en 2x4 con 2 líneas: Título + Descripción)
    w_mod = Inches(7.2)
    create_card_container(s13, Inches(5.333), Inches(1.5), w_mod, card_h, "ESTRUCTURA MODULAR DEL MANUAL (8 MÓDULOS TEMÁTICOS)", COLOR_TEAL_HEADER, "📋")

    mod_col_w = Inches(3.28)
    mod_gap_x = Inches(0.18)
    mod_row_h = Inches(0.80)
    mod_gap_y = Inches(0.08)
    mod_top = Inches(2.10)

    modules = [
        ("Módulo 1: Marco Legal", "Definición OMS (2025); marco de Leyes 774, 759 y 292.", "1️⃣", 0, 0),
        ("Módulo 2: Deontología Clínica", "Consentimiento intercultural; regla: complementar sin sustituir.", "2️⃣", 0, 1),
        ("Módulo 3: Mapa de Prácticas", "Clasificación en 4 niveles (directo, psicoeducación, alerta).", "3️⃣", 0, 2),
        ("Módulo 4: Algoritmo Clínico", "Protocolo de 4 pasos para derivación clínica informada.", "4️⃣", 0, 3),
        ("Módulo 5: Habilidades de Diálogo", "Entrevista abierta para superar el ocultamiento terapéutico.", "5️⃣", 1, 0),
        ("Módulo 6: Red Intersectorial", "Criterios de referencia bidireccional con facilitadores.", "6️⃣", 1, 1),
        ("Módulo 7: Ruta Formativa", "Secuencia pedagógica en 3 etapas y electiva universitaria.", "7️⃣", 1, 2),
        ("Módulo 8: Soporte Institucional", "Creación de Comité de Ética y capacitación docente.", "8️⃣", 1, 3),
    ]

    for title, desc, ic, col_idx, row_idx in modules:
        c_left = Inches(5.55) + col_idx * (mod_col_w + mod_gap_x)
        c_top = mod_top + row_idx * (mod_row_h + mod_gap_y)
        
        tile = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, c_top, mod_col_w, mod_row_h)
        tile.adjustments[0] = 0.08; tile.fill.solid(); tile.fill.fore_color.rgb = COLOR_ROW_BG; tile.line.color.rgb = COLOR_ROW_BORDER; tile.line.width = Pt(0.75)
        tf_tile = tile.text_frame; tf_tile.word_wrap = True; tf_tile.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_tile.margin_left = tf_tile.margin_right = Inches(0.14); tf_tile.margin_top = tf_tile.margin_bottom = Inches(0.02)
        
        p1 = tf_tile.paragraphs[0]; p1.alignment = PP_ALIGN.LEFT
        r1 = p1.add_run(); r1.text = f"{ic} {title}"; r1.font.name = FONT_HEADING; r1.font.bold = True; r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_TEAL_DARK if col_idx==0 else COLOR_GOLD_DARK
        
        p2 = tf_tile.add_paragraph(); p2.alignment = PP_ALIGN.LEFT; p2.line_spacing = 1.12
        r2 = p2.add_run(); r2.text = desc; r2.font.name = FONT_BODY; r2.font.size = Pt(8.5); r2.font.color.rgb = COLOR_SLATE_DARK

    add_callout_box(s13, Inches(5.55), Inches(5.75), w_mod - Inches(0.44), Inches(0.92),
                    "Herramienta Diagnóstica Anexa", "El manual incorpora la adaptación transcultural del inventario I-CAM-Q para la exploración clínica estandarizada en Nicaragua.",
                    COLOR_BLUE_TINT, COLOR_BLUE_BORDER, COLOR_NAVY_DARK)

    # ==========================================================================
    # SLIDE 14: CONCLUSIONES (5 FILAS MODULARES CON PERFECTO BALANCE)
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_canvas(s14)
    add_header(s14, "Capítulo VI • Síntesis Conclusiva", "Conclusiones Centrales de la Investigación (Triangulación de Objetivos)")
    add_footer(s14, 14)

    create_card_container(s14, Inches(0.8), Inches(1.5), Inches(11.733), card_h, "SÍNTESIS DE CONCLUSIONES POR OBJETIVO DE INVESTIGACIÓN", COLOR_NAVY_HEADER, "🎯")

    concl_items = [
        ("Cumplimiento del Objetivo General:", "Los tres colectivos participantes (N = 86) validan unánimemente la pertinencia de la MTCI como coadyuvante en atención psicológica, condicionada a límites bioéticos y base científica.", "1️⃣", COLOR_TEAL_DARK),
        ("Perfil y Paradoja Estudiantil (OE1):", "El estudiantado posee buen dominio conceptual (67.6%) y eficacia subjetiva (86.7%), pero padece vacíos normativos (58.8% desconoce Ley 774; 64.7% desconoce Ley 292) y alta desprotección formativa.", "2️⃣", COLOR_GOLD_DARK),
        ("Oferta Territorial y Barreras de Estelí (OE2):", "Facilitadores con hasta 30 años de labor constatan 100% de alivio de sobrecarga muscular y mayor apertura reflexiva (88.9%), sorteando prejuicios socioculturales (100%) y barreras económicas.", "3️⃣", COLOR_NAVY_DARK),
        ("Consenso Curricular del Claustro Docente (OE3):", "100% del profesorado apoya la inserción transversal de la MTCI bajo metodologías activas y vivenciales (88.9%), demandando formación en regulación somática y comités éticos.", "4️⃣", COLOR_TEAL_DARK),
        ("Logro Propositivo del Manual de Estrategias:", "Se construyó exitosamente el Manual de Estrategias MTCI de 18 páginas (Anexo 16.2), dotando al CUR-Estelí de algoritmos de decisión clínica, pautas contra el ocultamiento y el inventario I-CAM-Q.", "5️⃣", COLOR_GOLD_DARK)
    ]
    concl_h = Inches(0.70)
    concl_gap = Inches(0.08)
    concl_top = Inches(2.08)
    for i, (t, d, ic, col_c) in enumerate(concl_items):
        add_item_card(s14, Inches(1.05), concl_top + i*(concl_h + concl_gap), Inches(11.233), concl_h,
                      t, d, ic, COLOR_ROW_BG, COLOR_ROW_BORDER, col_c, COLOR_SLATE_DARK, 9.5)

    add_callout_box(s14, Inches(1.05), Inches(5.80), Inches(11.233), Inches(0.85),
                    "Conclusión Fundamental", "La MTCI constituye un recurso de apoyo legítimo que robustece la alianza terapéutica cuando se aplica con rigor deontológico y delimitación estricta del rol profesional.",
                    COLOR_GOLD_TINT, COLOR_GOLD_BORDER, COLOR_GOLD_DARK)

    # ==========================================================================
    # SLIDE 15: RECOMENDACIONES (2x2 GRID CON FILAS ESTRUCTURADAS)
    # ==========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_canvas(s15)
    add_header(s15, "Capítulo VI • Directrices Prospectivas", "Recomendaciones Estratégicas para Estudiantes, Docentes, Universidad y MINSA")
    add_footer(s15, 15)

    rec_w = Inches(5.7)
    rec_h = Inches(2.60)
    rec_top1 = Inches(1.5)
    rec_top2 = Inches(4.28)

    rec_sections = [
        ("PARA EL ESTAMENTO ESTUDIANTIL", COLOR_TEAL_HEADER, "👩‍🎓", Inches(0.8), rec_top1, [
            ("Marco Normativo:", "Respetar estrictamente las Leyes 774 y 292 (prohibición terminante de prescribir fármacos)."),
            ("Algoritmo Clínico:", "Aplicar el árbol de decisión clínica del manual durante las prácticas en la Clínica Psicosocial."),
            ("Diálogo Abierto:", "Explorar empáticamente el uso de MTCI en consulta para erradicar el ocultamiento terapéutico."),
            ("Autocuidado Personal:", "Vivenciar la regulación somática (respiración diafragmática y escaneo) ante sobrecarga.")
        ]),
        ("PARA EL CLAUSTRO DOCENTE", COLOR_NAVY_HEADER, "👨‍🏫", Inches(6.833), rec_top1, [
            ("Transversalidad Curricular:", "Integrar contenidos de MTCI en asignaturas de Psicología Clínica, Comunitaria y Ética."),
            ("Pedagogía Vivencial:", "Priorizar metodologías activas: análisis de casos clínicos y talleres de autorregulación somática."),
            ("Derivación Interdisciplinar:", "Enseñar la referencia ética hacia facilitadores certificados y médicos tratantes."),
            ("Capacitación Docente:", "Formarse institucionalmente en neurobiología del estrés y regulación somática Bottom-Up.")
        ]),
        ("PARA LA GESTIÓN DEL CUR-ESTELÍ", COLOR_GOLD_DARK, "🏛", Inches(0.8), rec_top2, [
            ("Aprobación Institucional:", "Formalizar la adopción oficial del Manual de Estrategias MTCI (Anexo 16.2 de tesis)."),
            ("Comité de Bioética:", "Constituir el Comité de Ética y Delimitación Profesional en el recinto universitario."),
            ("Alianza con MINSA-Estelí:", "Consolidar convenios de cooperación interinstitucional para pasantías y ferias de salud."),
            ("Asignatura Electiva:", "Evaluar a mediano plazo la creación formal del curso electivo 'Psicología Integrativa'.")
        ]),
        ("PARA EL SISTEMA DE SALUD Y FACILITADORES", COLOR_TEAL_HEADER, "🌿", Inches(6.833), rec_top2, [
            ("Habilitación Sanitaria:", "Difundir mecanismos de registro oficial para facilitadores contemplados en la Ley No. 774."),
            ("Red de Interconsulta:", "Habilitar canales de referencia bidireccional entre psicólogos clínicos y terapeutas locales."),
            ("Atención Primaria:", "Fomentar la exploración desestigmatizada de saberes herbolarios en centros de salud comunitaria."),
            ("Principio de Complementariedad:", "Mantener el compromiso bioético de sumar recursos sin pretender sustituir tratamientos.")
        ])
    ]

    rec_row_h = Inches(0.46)
    rec_row_gap = Inches(0.04)

    for hdr_title, hdr_col, hdr_ic, left_pos, top_pos, items in rec_sections:
        create_card_container(s15, left_pos, top_pos, rec_w, rec_h, hdr_title, hdr_col, hdr_ic)
        for idx, (it_title, it_desc) in enumerate(items):
            r_top = top_pos + Inches(0.52) + idx * (rec_row_h + rec_row_gap)
            add_item_card(s15, left_pos + Inches(0.18), r_top, rec_w - Inches(0.36), rec_row_h,
                          it_title, it_desc, "✓", COLOR_ROW_BG, COLOR_ROW_BORDER,
                          hdr_col, COLOR_SLATE_DARK, 8.5)

    # ==========================================================================
    # SLIDE 16: CIERRE INSTITUCIONAL Y AGRADECIMIENTOS (REDISEÑO TOTAL!)
    # ==========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_canvas(s16)

    top_b = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.3))
    top_b.fill.solid(); top_b.fill.fore_color.rgb = COLOR_NAVY_DARK; top_b.line.fill.background()

    gold_s = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.3), Inches(13.333), Inches(0.06))
    gold_s.fill.solid(); gold_s.fill.fore_color.rgb = COLOR_GOLD_ACCENT; gold_s.line.fill.background()

    if os.path.exists(LOGO_CLEAN_PATH):
        s16.shapes.add_picture(LOGO_CLEAN_PATH, Inches(0.8), Inches(0.18), height=Inches(0.92))

    tb_h = s16.shapes.add_textbox(Inches(3.2), Inches(0.25), Inches(9.2), Inches(0.8))
    tf_h = tb_h.text_frame; tf_h.word_wrap = True
    p = tf_h.paragraphs[0]; p.text = "UNIVERSIDAD NACIONAL AUTÓNOMA DE NICARAGUA, MANAGUA"; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = RGBColor(255, 255, 255)
    p = tf_h.add_paragraph(); p.text = "CENTRO UNIVERSITARIO REGIONAL DE ESTELÍ • RECINTO LEONEL RUGAMA RUGAMA"; p.font.bold = True; p.font.size = Pt(9.5); p.font.color.rgb = COLOR_GOLD_ACCENT

    # Main Hero Closing Card
    c_close = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.60), card_w, card_h)
    c_close.adjustments[0] = 0.03; c_close.fill.solid(); c_close.fill.fore_color.rgb = COLOR_CARD_BG; c_close.line.color.rgb = COLOR_CARD_BORDER; c_close.line.width = Pt(1)

    if os.path.exists(SHIELD_PATH):
        s16.shapes.add_picture(SHIELD_PATH, Inches(6.05), Inches(1.80), height=Inches(1.25))

    tb_c = s16.shapes.add_textbox(Inches(1.2), Inches(3.12), Inches(10.9), Inches(1.25))
    tf_c = tb_c.text_frame; tf_c.word_wrap = True

    p = tf_c.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; p.text = "¡A la libertad por la Universidad!"; p.font.size = Pt(17); p.font.italic = True; p.font.bold = True; p.font.color.rgb = COLOR_NAVY_DARK; p.space_after = Pt(4)
    p = tf_c.add_paragraph(); p.alignment = PP_ALIGN.CENTER; p.text = "Muchas Gracias por su Atención"; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = COLOR_GOLD_DARK; p.space_after = Pt(6)
    p = tf_c.add_paragraph(); p.alignment = PP_ALIGN.CENTER; p.text = "Espacio Abierto para Preguntas, Comentarios y Defensa Oral ante el Honorable Tribunal Examinador"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_SLATE_DARK

    # 3 Bottom Symmetrical Metadata Cards (Left Aligned with clean padding)
    c_w = Inches(3.45)
    c_gap = Inches(0.27)
    c_top = Inches(4.50)
    c_h = Inches(2.20)

    # 1. Autores
    box1 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), c_top, c_w, c_h)
    box1.adjustments[0] = 0.06; box1.fill.solid(); box1.fill.fore_color.rgb = COLOR_BLUE_TINT; box1.line.color.rgb = COLOR_BLUE_BORDER; box1.line.width = Pt(1)
    tf1 = box1.text_frame; tf1.vertical_anchor = MSO_ANCHOR.MIDDLE; tf1.margin_left = Inches(0.25); tf1.margin_right = Inches(0.20)
    p = tf1.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "👤 SUSTENTANTES"; p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = COLOR_NAVY_DARK; p.space_after = Pt(8)
    for n in ["• Dina Fabiola García Torres", "• Tatiana Paola López Ramos", "• Engel Enoc Zamora Velásquez"]:
        p = tf1.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = n; p.font.size = Pt(10); p.font.color.rgb = COLOR_SLATE_DARK; p.space_after = Pt(3)

    # 2. Tutora
    box2 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2) + c_w + c_gap, c_top, c_w, c_h)
    box2.adjustments[0] = 0.06; box2.fill.solid(); box2.fill.fore_color.rgb = COLOR_TEAL_TINT; box2.line.color.rgb = COLOR_TEAL_BORDER; box2.line.width = Pt(1)
    tf2 = box2.text_frame; tf2.vertical_anchor = MSO_ANCHOR.MIDDLE; tf2.margin_left = Inches(0.25); tf2.margin_right = Inches(0.20)
    p = tf2.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "🎓 TUTORÍA ACADÉMICA"; p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEAL_DARK; p.space_after = Pt(8)
    p = tf2.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "• Dra. Tania Libertad Pérez Guevara"; p.font.bold = True; p.font.size = Pt(10.5); p.font.color.rgb = COLOR_SLATE_DARK; p.space_after = Pt(3)
    p = tf2.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "Docente Investigadora • CUR-Estelí\nAsesoría Temática y Metodológica"; p.font.size = Pt(9.5); p.font.color.rgb = COLOR_SLATE_MUTED

    # 3. Sede y Grado
    box3 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2) + (c_w + c_gap)*2, c_top, c_w, c_h)
    box3.adjustments[0] = 0.06; box3.fill.solid(); box3.fill.fore_color.rgb = COLOR_GOLD_TINT; box3.line.color.rgb = COLOR_GOLD_BORDER; box3.line.width = Pt(1)
    tf3 = box3.text_frame; tf3.vertical_anchor = MSO_ANCHOR.MIDDLE; tf3.margin_left = Inches(0.25); tf3.margin_right = Inches(0.20)
    p = tf3.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; p.text = "🏛 DEFENSA DE GRADO"; p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = COLOR_GOLD_DARK; p.space_after = Pt(8)
    p = tf3.add_paragraph(); p.alignment = PP_ALIGN.LEFT; p.text = "Licenciatura en Psicología\nRecinto Leonel Rugama Rugama\nEstelí, Nicaragua • Octubre, 2026"; p.font.size = Pt(10); p.font.color.rgb = COLOR_SLATE_DARK

    output_pptx = "Presentacion_Defensa_Tesis_MTCI_UNAN_v3.pptx"
    prs.save(output_pptx)
    print(f"Premium Presentation v3 created successfully at: {output_pptx}")
    try:
        prs.save("Presentacion_Defensa_Tesis_MTCI_UNAN.pptx")
        print("Also updated Presentacion_Defensa_Tesis_MTCI_UNAN.pptx")
    except Exception as e:
        print("Note: Original file is currently open in PowerPoint:", e)

if __name__ == "__main__":
    create_presentation()
