#!/usr/bin/env python3
"""
tools/consolidate_docx_apa7.py
==============================
Consolidates all 25 APA 7 figures into the thesis DOCX document:
'assets/MTCI Octubre 15 ultimo.docx' -> 'assets/MTCI_Consolidado_Final_APA7.docx'.

Follows:
- APA 7th Edition Standards (Manual Moderno / UNAN-Managua).
- CitaAPA Guidelines (citaapa.com/formato-apa/tablas-figuras/).

Key Actions:
1. Strips drawing runs from text paragraphs where they were accidentally embedded.
2. Injects formal APA 7 narrative in-text citations '(véase la Figura X)' into the
   preceding narrative paragraphs, ensuring every figure is introduced before its appearance.
3. Replaces old inconsistent figure captions with canonical APA 7 4-element blocks:
     - Element 1: **Figura X** (Bold, 12pt, left-aligned)
     - Element 2: *Título descriptivo* (Italic, 12pt, left-aligned, sentence case)
     - Element 3: Centered 300-DPI graphic without internal text
     - Element 4: *Nota.* Explicación, tamaño muestral (n), significancia y fuente (10pt, left-aligned)
4. Sincronizes preliminary 'Índice de figuras' with all 25 normalized titles.
5. Preserves all document sections, headers, footers, tables, and typography.
"""

import os
import sys
import docx
from PIL import Image
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX_IN = os.path.join(REPO_ROOT, "assets", "MTCI Octubre 15 ultimo.docx")
DOCX_OUT = os.path.join(REPO_ROOT, "assets", "MTCI_Consolidado_Final_APA7.docx")
FIG_DIR = os.path.join(REPO_ROOT, "assets", "figuras_apa7")

FIGURES_META = {
    1: {
        "file": "figura_01_ubicacion_cur_esteli.png",
        "title": "Ubicación geográfica del Centro Universitario Regional (CUR-Estelí)",
        "note": "Delimitación del Centro Universitario Regional (CUR-Estelí) de la UNAN-Managua, recinto Leonel Rugama Rugama, ubicado en el municipio de Estelí, departamento de Estelí, Nicaragua. Fuente: Cartografía institucional del CUR-Estelí, 2026.",
        "width": 4.5,
        "citation_anchor": "Específicamente, la investigación tendrá lugar en el Centro Universitario Regional (CUR-Estelí)",
        "citation_text": " (véase la Figura 1)."
    },
    2: {
        "file": "figura_02_criterios_inclusion_exclusion.png",
        "title": "Diagrama de flujo de criterios de inclusión y exclusión de las unidades de análisis",
        "note": "Criterios muestrales aplicados para la delimitación de estudiantes de 4.º y 5.º año (n = 68), facilitadores locales de MTCI (n = 9) y cuerpo docente-psicólogo (n = 9). Fuente: Elaboración propia, 2026.",
        "width": 5.8,
        "citation_anchor": "La población se refiere al conjunto total de individuos, objetos o elementos que poseen características comunes",
        "citation_text": " Para garantizar la representatividad y el rigor del muestreo concurrente entre estudiantes, facilitadores y docentes, se aplicaron criterios específicos de delimitación muestral (véase la Figura 2)."
    },
    3: {
        "file": "figura_03_demografia_estudiantes.png",
        "title": "Distribución sociodemográfica y formativa de la muestra estudiantil",
        "note": "n = 68 estudiantes de la carrera de Licenciatura en Psicología del CUR-Estelí. Los paneles desglosan: A) Año de carrera (4.º año: 77.9%, 5.º año: 22.1%); B) Sexo (Femenino: 82.4%, Masculino: 14.7%, Prefiere no decir: 2.9%); C) Rango de edad en años. Fuente: Cuestionario estructurado I1, 2026.",
        "width": 6.0,
        "citation_anchor": "77.9% cursa 4.º año (53 estudiantes)",
        "citation_text": " Estos datos configuran una muestra con marcado predominio femenino y distribuida entre los dos últimos años de formación académica (véase la Figura 3)."
    },
    4: {
        "file": "figura_04_dominio_conceptual_normativo_estudiantes.png",
        "title": "Nivel de dominio conceptual y normativo sobre MTCI en estudiantes de Psicología",
        "note": "n = 68. Comparación entre acierto técnico objetivo y niveles de desconocimiento o concepción errónea respecto a la definición de la OMS, los principios integradores de la Ley No. 774 y la inhabilitación para prescribir psicofármacos según la Ley No. 292. Fuente: Cuestionario estructurado I1, 2026.",
        "width": 5.8,
        "citation_anchor": "Solo el 35.3% identificó con exactitud",
        "citation_text": " Estos resultados evidencian brechas sustantivas en el dominio técnico y jurídico de las leyes sanitarias que regulan el ejercicio profesional (véase la Figura 4)."
    },
    5: {
        "file": "figura_05_reconocimiento_practicas_1_estudiantes.png",
        "title": "Reconocimiento de prácticas de MTCI en estudiantes: Medicina natural y terapias manuales",
        "note": "n = 68. Respuestas de selección múltiple sobre la identificación de prácticas reconocidas en el marco de la salud natural y técnicas corporales. Fuente: Cuestionario estructurado I1, 2026.",
        "width": 5.8,
        "citation_anchor": "Masajes terapéuticos (77.9%), aromaterapia/floral/arteterapia (77.9%)",
        "citation_text": " Los hallazgos revelan un reconocimiento ampliamente mayoritario de las terapias manuales corporales y la medicina natural tradicional (véase la Figura 5)"
    },
    6: {
        "file": "figura_06_reconocimiento_practicas_2_estudiantes.png",
        "title": "Reconocimiento de prácticas de MTCI en estudiantes: Terapias psicoemocionales y energéticas",
        "note": "n = 68. Respuestas de selección múltiple sobre modalidades de regulación mente-cuerpo, bioenergía y abordajes complementarios. Fuente: Cuestionario estructurado I1, 2026.",
        "width": 5.8,
        "citation_anchor": None, # Handled alongside Fig 5
        "citation_text": " en contraste con una familiaridad diferenciada respecto a las modalidades bioenergéticas y psicoemocionales (véase la Figura 6)."
    },
    7: {
        "file": "figura_07_frecuencia_uso_estudiantes.png",
        "title": "Frecuencia de uso personal de MTCI y efectos psicofisiológicos experimentados",
        "note": "Panel A: Frecuencia de uso en el último año para autocuidado general y manejo del estrés (n = 68). Panel B: Efectos sobre el bienestar subjetivo reportados por estudiantes con experiencia empírica de uso (n = 30). Fuente: Cuestionario estructurado I1, 2026.",
        "width": 6.0,
        "citation_anchor": "El uso es reactivo y esporádico (52.9% nunca la usa",
        "citation_text": " Esta dinámica evidencia que el recurso a las MTCI obedece principalmente a necesidades reactivas, asociándose con vivencias positivas de distensión corporal y relajación (véase la Figura 7)."
    },
    8: {
        "file": "figura_08_sexo_actores_locales.png",
        "title": "Distribución por sexo de los facilitadores y actores locales de MTCI",
        "note": "n = 9 facilitadores y terapeutas holísticos del municipio de Estelí (Mujeres: 77.8%, n = 7; Hombres: 22.2%, n = 2). Fuente: Cuestionario I2, 2026.",
        "width": 4.5,
        "citation_anchor": "En Estelí este patrón parece repetirse: son mayoritariamente mujeres",
        "citation_text": " Esta distribución confirma una notoria preponderancia femenina en la conducción de consultorios y prácticas comunitarias de MTCI en el municipio (véase la Figura 8)."
    },
    9: {
        "file": "figura_09_edad_actores_locales.png",
        "title": "Distribución por rangos de edad de los facilitadores locales de MTCI",
        "note": "n = 9. Rango etario de terapeutas y guías en Estelí (30 a 39 años: 55.6%; 40 a 49 años: 22.2%; 50 a 58 años: 22.2%). Fuente: Cuestionario I2, 2026.",
        "width": 5.2,
        "citation_anchor": "Esto sugiere que la oferta de MTCI en el municipio no depende únicamente",
        "citation_text": " Se aprecia una concentración de los facilitadores en etapas de plena madurez y productividad profesional (véase la Figura 9)."
    },
    10: {
        "file": "figura_10_experiencia_actores_locales.png",
        "title": "Años de experiencia profesional en el ejercicio de la MTCI de los facilitadores",
        "note": "n = 9. Trayectoria en el ejercicio de terapias complementarias y saberes tradicionales en Estelí. Fuente: Cuestionario I2, 2026.",
        "width": 5.2,
        "citation_anchor": "El 44.4% de los facilitadores (4 de 9) acumula entre 20 y 30 años",
        "citation_text": " Lo anterior da cuenta de una trayectoria acumulada y consolidada de varias décadas en el ejercicio terapéutico en la región (véase la Figura 10)."
    },
    11: {
        "file": "figura_11_procedencia_actores_locales.png",
        "title": "Procedencia geográfica de los facilitadores locales de MTCI",
        "note": "n = 9. Localización territorial de consultorios y centros de bienestar consultados. Fuente: Cuestionario I2, 2026.",
        "width": 5.2,
        "citation_anchor": "El 77.8% de los facilitadores proviene de Estelí",
        "citation_text": " La localización territorial refleja una marcada centralización de la oferta terapéutica en el casco urbano del municipio de Estelí (véase la Figura 11)."
    },
    12: {
        "file": "figura_12_practicas_actores_locales.png",
        "title": "Modalidades terapéuticas de MTCI utilizadas habitualmente en la atención profesional",
        "note": "n = 9. Selección múltiple de técnicas corporales, energéticas y naturales aplicadas en la atención local. Fuente: Cuestionario I2, 2026.",
        "width": 5.8,
        "citation_anchor": "Los masajes, la reflexología/acupuntura, la aromaterapia y la medicina ayurveda",
        "citation_text": " En el repertorio asistencial destaca la articulación de masajes terapéuticos, preparados fitoterápicos y recursos de autorregulación (véase la Figura 12)."
    },
    13: {
        "file": "figura_13_cambios_estres_ansiedad_actores.png",
        "title": "Percepción de cambios en los niveles de estrés y ansiedad en usuarios atendidos",
        "note": "n = 9. Reporte unánime (100.0%) de los facilitadores sobre la disminución de la sobrecarga y tensión acumulada en consultantes. Fuente: Cuestionario I2, 2026.",
        "width": 4.5,
        "citation_anchor": "El 100% de los facilitadores (9 de 9) reportó cambios positivos",
        "citation_text": " Este dato refleja una percepción unánime entre los terapeutas respecto al alivio de la sobrecarga tensional y el estrés en las personas atendidas (véase la Figura 13)."
    },
    14: {
        "file": "figura_14_apertura_emocional_usuarios_actores.png",
        "title": "Grado de apertura emocional y receptividad observado en los usuarios",
        "note": "n = 9. Valoración sobre el incremento en la disposición personal y el desbloqueo psicofisiológico de los consultantes. Fuente: Cuestionario I2, 2026.",
        "width": 4.5,
        "citation_anchor": "El 88.9% de los facilitadores (8 de 9) describió cambios significativos",
        "citation_text": " Dicha evolución evidencia un progresivo desbloqueo y mayor receptividad para dialogar sobre vivencias afectivas profundas (véase la Figura 14)."
    },
    15: {
        "file": "figura_15_efectos_observados_actores.png",
        "title": "Frecuencia de efectos desfavorables o reacciones emocionales adversas observadas",
        "note": "n = 9. Ausencia total de efectos desfavorables o crisis emocionales iatrogénicas observadas en los consultorios (100.0% seguridad percibida). Fuente: Cuestionario I2, 2026.",
        "width": 4.5,
        "citation_anchor": "Ninguno de los nueve facilitadores reportó haber presenciado un efecto",
        "citation_text": " Este hallazgo subraya la percepción de inocuidad y la ausencia de crisis desfavorables en la práctica cotidiana de las terapias aplicadas (véase la Figura 15)."
    },
    16: {
        "file": "figura_16_interaccion_profesionales_salud.png",
        "title": "Nivel de interacción y coordinación con profesionales e instituciones de salud locales",
        "note": "n = 9. Calificación de las relaciones de trabajo y derivación interdisciplinaria con médicos, psicólogos y centros de salud. Fuente: Cuestionario I2, 2026.",
        "width": 5.2,
        "citation_anchor": "Aquí el panorama es mayormente favorable, pero no del todo parejo",
        "citation_text": " La dinámica muestra canales informales de derivación que requieren avanzar hacia mecanismos sistemáticos de coordinación intersectorial (véase la Figura 16)."
    },
    17: {
        "file": "figura_17_dificultades_normativas_actores.png",
        "title": "Nivel de dificultad normativa y burocrática experimentada por los facilitadores",
        "note": "n = 9. Autopercepción sobre facilidades legales y barreras administrativas en el ejercicio comunitario de MTCI en Estelí. Fuente: Cuestionario I2, 2026.",
        "width": 5.0,
        "citation_anchor": "El 77.8% de los facilitadores dijo no tener dificultades significativas",
        "citation_text": " La valoración indica condiciones mayormente propicias para el ejercicio, aunque un sector minoritario enfrenta trámites burocráticos exigentes (véase la Figura 17)."
    },
    18: {
        "file": "figura_18_reservas_socioculturales_usuarios.png",
        "title": "Frecuencia de usuarios con creencias o reservas socioculturales y religiosas hacia la MTCI",
        "note": "n = 9. Incidencia de mitos, prejuicios y dudas socioculturales atendidas en la práctica cotidiana. Fuente: Cuestionario I2, 2026.",
        "width": 5.0,
        "citation_anchor": "Un 77.8% de los facilitadores señaló que se encuentra “ocasionalmente”",
        "citation_text": " Los testimonios dan cuenta de reticencias comunitarias que son abordadas mediante psicoeducación y diálogo empático (véase la Figura 18)."
    },
    19: {
        "file": "figura_19_incidencia_factor_economico.png",
        "title": "Incidencia del factor económico en el acceso y continuidad de las terapias de MTCI",
        "note": "n = 9. Percepción sobre cómo la disponibilidad financiera condiciona el seguimiento de procesos de autocuidado y bienestar. Fuente: Cuestionario I2, 2026.",
        "width": 5.0,
        "citation_anchor": "El 77.8% de los facilitadores considera que el factor económico incide moderadamente",
        "citation_text": " Este factor sitúa la capacidad de pago como una variable condicionante para sostener la adherencia a largo plazo (véase la Figura 19)."
    },
    20: {
        "file": "figura_20_sexo_docentes.png",
        "title": "Distribución por sexo del cuerpo docente de Psicología consultado",
        "note": "n = 9 docentes de la carrera de Psicología del CUR-Estelí (Mujeres: 77.8%, n = 7; Hombres: 22.2%, n = 2). Fuente: Cuestionario I3, 2026.",
        "width": 4.5,
        "citation_anchor": "Este apartado presenta el perfil general de los nueve docentes participantes",
        "citation_text": " La caracterización sociodemográfica exhibe una notable preponderancia de docentes mujeres en el colectivo consultado (véase la Figura 20)."
    },
    21: {
        "file": "figura_21_edad_docentes.png",
        "title": "Distribución por grupos de edad del cuerpo docente de Psicología",
        "note": "n = 9. Rango etario de docentes universitarios participantes (media = 34.2 años, concentración en 22 a 36 años). Fuente: Cuestionario I3, 2026.",
        "width": 5.2,
        "citation_anchor": "Las edades reportadas oscilan entre los 22 y los 70 años",
        "citation_text": " Los datos muestran un claustro mayoritariamente joven y en fase activa de desarrollo docente universitario (véase la Figura 21)."
    },
    22: {
        "file": "figura_22_especialidad_docentes.png",
        "title": "Distribución de docentes según área de especialidad profesional",
        "note": "n = 9. Especialidades declaradas: Psicología Clínica (55.6%), Infantil/Educativa (22.2%), Comunitaria (11.1%), Salud y Epidemiología (11.1%). Fuente: Cuestionario I3, 2026.",
        "width": 5.5,
        "citation_anchor": "Todos los participantes son licenciados en Psicología",
        "citation_text": " Entre las áreas declaradas destaca el predominio de la psicología clínica como el campo de posgrado más representativo (véase la Figura 22)."
    },
    23: {
        "file": "figura_23_experiencia_docente.png",
        "title": "Años de experiencia en la docencia universitaria de los participantes",
        "note": "n = 9. Años de trayectoria pedagógica en la formación superior en UNAN-Managua / CUR-Estelí. Fuente: Cuestionario I3, 2026.",
        "width": 5.0,
        "citation_anchor": "En cuanto al grado académico, el grupo se reparte entre licenciatura",
        "citation_text": " La experiencia acumulada refleja un grupo docente con concentración en los primeros quinquenios de labor universitaria (véase la Figura 23)."
    },
    24: {
        "file": "figura_24_estrategias_academicas_docentes.png",
        "title": "Estrategias pedagógicas priorizadas por docentes para abordar la MTCI",
        "note": "n = 9. Selección múltiple de metodologías formativas recomendadas para incorporar en el plan de estudios. Fuente: Cuestionario I3, 2026.",
        "width": 5.8,
        "citation_anchor": "Al consultarles qué estrategias académicas consideran más pertinentes",
        "citation_text": " El profesorado prioriza metodologías vivenciales, talleres prácticos e investigaciones formativas en el currículo (véase la Figura 24)."
    },
    25: {
        "file": "figura_25_experiencias_favorables_docentes.png",
        "title": "Experiencias formativas consideradas más favorables para la integración de la MTCI",
        "note": "n = 9. Modalidades de aprendizaje experiencial y vinculación comunitaria priorizadas por el profesorado. Fuente: Cuestionario I3, 2026.",
        "width": 5.8,
        "citation_anchor": "La experiencia formativa más valorada, por amplio margen",
        "citation_text": " En este ámbito se destaca el intercambio con terapeutas tradicionales como la vivencia con mayor potencial pedagógico (véase la Figura 25)."
    }
}

def remove_p_element(p_or_elm):
    """Removes a paragraph element cleanly from its parent XML node."""
    if p_or_elm is None:
        return
    elm = p_or_elm._p if hasattr(p_or_elm, '_p') else p_or_elm
    parent = elm.getparent()
    if parent is not None:
        parent.remove(elm)

def strip_drawing_runs(p):
    """Removes all drawing or pict runs from a paragraph, leaving pure text."""
    for r in list(p.runs):
        if r._r.xpath('.//a:blip') or r._r.xpath('.//w:drawing') or r._r.xpath('.//w:pict'):
            r._r.getparent().remove(r._r)

def insert_apa7_figure_block(anchor_p, fig_num, meta, img_path):
    """
    Inserts a standard APA 7 figure block immediately before anchor_p:
      1. Paragraph: Figura X (Bold, 12pt, Times New Roman, line spacing 1.5, space after 0)
      2. Paragraph: Título descriptivo (Italic, 12pt, Times New Roman, line spacing 1.5, space after 6pt)
      3. Paragraph: Graphic (Centered, width per metadata, space after 6pt)
      4. Paragraph: Nota. Explicación... (10pt, Times New Roman, line spacing 1.15, space after 18pt)
    """
    # 1. Number
    p_num = anchor_p.insert_paragraph_before()
    p_num.paragraph_format.line_spacing = 1.5
    p_num.paragraph_format.space_before = Pt(12)
    p_num.paragraph_format.space_after = Pt(0)
    r_num = p_num.add_run(f"Figura {fig_num}")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(12)
    r_num.bold = True

    # 2. Title
    p_title = anchor_p.insert_paragraph_before()
    p_title.paragraph_format.line_spacing = 1.5
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run(meta["title"])
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(12)
    r_title.italic = True

    # 3. Graphic
    p_img = anchor_p.insert_paragraph_before()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.line_spacing = 1.0
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(6)
    r_img = p_img.add_run()
    r_img.add_picture(img_path, width=Inches(meta["width"]))

    # 4. Note
    p_note = anchor_p.insert_paragraph_before()
    p_note.paragraph_format.line_spacing = 1.15
    p_note.paragraph_format.space_before = Pt(0)
    p_note.paragraph_format.space_after = Pt(18)
    r_lbl = p_note.add_run("Nota. ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(10)
    r_lbl.italic = True
    r_txt = p_note.add_run(meta["note"])
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(10)

def main():
    print(f"📖 Cargando documento maestro: {DOCX_IN}")
    doc = docx.Document(DOCX_IN)
    print(f"   Párrafos iniciales: {len(doc.paragraphs)}, Tablas: {len(doc.tables)}, Secciones: {len(doc.sections)}")

    # 0. Ensure 300 DPI on Fig 1
    fig1_path = os.path.join(FIG_DIR, "figura_01_ubicacion_cur_esteli.png")
    if os.path.exists(fig1_path):
        with Image.open(fig1_path) as im:
            im.save(fig1_path, dpi=(300, 300))

    # 1. Clean mixed paragraphs (strip drawing runs from text paragraphs)
    print("\n🧹 Limpiando dibujos incrustados en párrafos de texto...")
    mixed_signatures = [
        "El contexto de la investigación se refiere al entorno",
        "La población se refiere al conjunto total de individuos",
        "77.9% cursa 4.º año (53 estudiantes)",
        "El uso es reactivo y esporádico (52.9% nunca la usa",
        "Todos los participantes son licenciados en Psicología"
    ]
    for p in doc.paragraphs:
        txt = p.text.strip()
        for sig in mixed_signatures:
            if sig.lower() in txt.lower():
                strip_drawing_runs(p)
                print(f"   ✓ Dibujo removido de párrafo: '{sig[:40]}...'")

    # 2. Inject parenthetical citations '(véase la Figura X)' into preceding narrative paragraphs
    print("\n✍️ Insertando citas en el texto '(véase la Figura X)' según APA 7...")
    for num, meta in FIGURES_META.items():
        anchor = meta.get("citation_anchor")
        cit_text = meta.get("citation_text")
        if not anchor or not cit_text:
            continue
        
        matches = [p for p in doc.paragraphs if anchor.lower() in p.text.lower()]
        if matches:
            target_p = matches[0]
            if f"Figura {num}" not in target_p.text:
                target_p.add_run(cit_text)
                print(f"   ✓ Cita inyectada para Figura {num:2d} en párrafo con '{anchor[:35]}...'")

    # Special handling for Fig 5 and Fig 6 combined in p[500]
    p500_matches = [p for p in doc.paragraphs if "Masajes terapéuticos (77.9%), aromaterapia/floral/arteterapia (77.9%)".lower() in p.text.lower()]
    if p500_matches:
        p500 = p500_matches[0]
        if "Figura 6" not in p500.text:
            p500.add_run(FIGURES_META[6]["citation_text"])
            print(f"   ✓ Cita inyectada para Figura  6 en p[500]")

    # 3. Consolidate figures in reverse order (Fig 25 down to Fig 1)
    print("\n🖼️ Consolidando Figuras APA 7 en el cuerpo del manuscrito (orden inverso)...")

    # Fig 25
    p_targets = [p for p in doc.paragraphs if "25 Figura. Experiencias favorables sobre MTCI".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        img_path = os.path.join(FIG_DIR, FIGURES_META[25]["file"])
        insert_apa7_figure_block(pt, 25, FIGURES_META[25], img_path)
        remove_p_element(pt)
        print("   ✓ Figura 25 consolidada con éxito")

    # Fig 24
    p_targets = [p for p in doc.paragraphs if "24 Figura. Estrategias académicas".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        img_path = os.path.join(FIG_DIR, FIGURES_META[24]["file"])
        insert_apa7_figure_block(pt, 24, FIGURES_META[24], img_path)
        remove_p_element(pt)
        print("   ✓ Figura 24 consolidada con éxito")

    # Fig 23
    p_targets = [p for p in doc.paragraphs if "23 Figura, Años de experiencia docente".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_elm = pt._p.getnext()
        img_path = os.path.join(FIG_DIR, FIGURES_META[23]["file"])
        insert_apa7_figure_block(pt, 23, FIGURES_META[23], img_path)
        remove_p_element(pt)
        if next_elm is not None and bool(next_elm.xpath('.//a:blip')):
            remove_p_element(next_elm)
        print("   ✓ Figura 23 consolidada con éxito")

    # Fig 22
    p_targets = [p for p in doc.paragraphs if "22 Figura. Área de especialidad de los docentes".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        img_path = os.path.join(FIG_DIR, FIGURES_META[22]["file"])
        insert_apa7_figure_block(pt, 22, FIGURES_META[22], img_path)
        remove_p_element(pt)
        print("   ✓ Figura 22 consolidada con éxito")

    # Fig 21
    p_targets = [p for p in doc.paragraphs if "21 Figura. Edad de los docentes encuestados".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_elm = pt._p.getnext()
        img_path = os.path.join(FIG_DIR, FIGURES_META[21]["file"])
        insert_apa7_figure_block(pt, 21, FIGURES_META[21], img_path)
        remove_p_element(pt)
        if next_elm is not None and bool(next_elm.xpath('.//a:blip')):
            remove_p_element(next_elm)
        print("   ✓ Figura 21 consolidada con éxito")

    # Fig 20
    p_targets = [p for p in doc.paragraphs if "20 Figura. Distribución por sexo de los docentes".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_elm = pt._p.getnext()
        img_path = os.path.join(FIG_DIR, FIGURES_META[20]["file"])
        insert_apa7_figure_block(pt, 20, FIGURES_META[20], img_path)
        remove_p_element(pt)
        if next_elm is not None and bool(next_elm.xpath('.//a:blip')):
            remove_p_element(next_elm)
        print("   ✓ Figura 20 consolidada con éxito")

    # Fig 19
    p_targets = [p for p in doc.paragraphs if "19 Figura. Incidencia del factor económico".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_cand = pt._p.getnext()
        to_remove = []
        while next_cand is not None and next_cand.tag.endswith('p'):
            has_blip = bool(next_cand.xpath('.//a:blip'))
            txt = "".join(next_cand.xpath('.//w:t/text()')).strip()
            if has_blip or not txt:
                to_remove.append(next_cand)
                next_cand = next_cand.getnext()
            else:
                break
        img_path = os.path.join(FIG_DIR, FIGURES_META[19]["file"])
        insert_apa7_figure_block(pt, 19, FIGURES_META[19], img_path)
        remove_p_element(pt)
        for r_elm in to_remove:
            remove_p_element(r_elm)
        print("   ✓ Figura 19 consolidada con éxito")

    # Fig 18
    p_targets = [p for p in doc.paragraphs if "18 Figura. Usuarios con reservas socioculturales".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_elm = pt._p.getnext()
        img_path = os.path.join(FIG_DIR, FIGURES_META[18]["file"])
        insert_apa7_figure_block(pt, 18, FIGURES_META[18], img_path)
        remove_p_element(pt)
        if next_elm is not None and bool(next_elm.xpath('.//a:blip')):
            remove_p_element(next_elm)
        print("   ✓ Figura 18 consolidada con éxito")

    # Fig 17
    p_targets = [p for p in doc.paragraphs if "17 Figura. Dificultades percibidas".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_elm = pt._p.getnext()
        img_path = os.path.join(FIG_DIR, FIGURES_META[17]["file"])
        insert_apa7_figure_block(pt, 17, FIGURES_META[17], img_path)
        remove_p_element(pt)
        if next_elm is not None and bool(next_elm.xpath('.//a:blip')):
            remove_p_element(next_elm)
        print("   ✓ Figura 17 consolidada con éxito")

    # Fig 16
    p_targets = [p for p in doc.paragraphs if "16 Figura. Interacción con otros profesionales de la Salud".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_elm = pt._p.getnext()
        img_path = os.path.join(FIG_DIR, FIGURES_META[16]["file"])
        insert_apa7_figure_block(pt, 16, FIGURES_META[16], img_path)
        remove_p_element(pt)
        if next_elm is not None and bool(next_elm.xpath('.//a:blip')):
            remove_p_element(next_elm)
        print("   ✓ Figura 16 consolidada con éxito")

    # Fig 15
    p_targets = [p for p in doc.paragraphs if "15 Figura. Efectos observados".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_elm = pt._p.getnext()
        img_path = os.path.join(FIG_DIR, FIGURES_META[15]["file"])
        insert_apa7_figure_block(pt, 15, FIGURES_META[15], img_path)
        remove_p_element(pt)
        if next_elm is not None and bool(next_elm.xpath('.//a:blip')):
            remove_p_element(next_elm)
        print("   ✓ Figura 15 consolidada con éxito")

    # Fig 14
    p_targets = [p for p in doc.paragraphs if "14 Figura. Disposición de los usuarios".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_elm = pt._p.getnext()
        img_path = os.path.join(FIG_DIR, FIGURES_META[14]["file"])
        insert_apa7_figure_block(pt, 14, FIGURES_META[14], img_path)
        remove_p_element(pt)
        if next_elm is not None and bool(next_elm.xpath('.//a:blip')):
            remove_p_element(next_elm)
        print("   ✓ Figura 14 consolidada con éxito")

    # Fig 13
    p_targets = [p for p in doc.paragraphs if "13 Figura. Cambios percibidos".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_elm = pt._p.getnext()
        img_path = os.path.join(FIG_DIR, FIGURES_META[13]["file"])
        insert_apa7_figure_block(pt, 13, FIGURES_META[13], img_path)
        remove_p_element(pt)
        if next_elm is not None and bool(next_elm.xpath('.//a:blip')):
            remove_p_element(next_elm)
        print("   ✓ Figura 13 consolidada con éxito")

    # Fig 12
    p_targets = [p for p in doc.paragraphs if "12 Figura. prácticas utilizadas por actores locales".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_cand = pt._p.getnext()
        to_remove = []
        while next_cand is not None and next_cand.tag.endswith('p'):
            has_blip = bool(next_cand.xpath('.//a:blip'))
            txt = "".join(next_cand.xpath('.//w:t/text()')).strip()
            if has_blip or not txt:
                to_remove.append(next_cand)
                next_cand = next_cand.getnext()
            else:
                break
        img_path = os.path.join(FIG_DIR, FIGURES_META[12]["file"])
        insert_apa7_figure_block(pt, 12, FIGURES_META[12], img_path)
        remove_p_element(pt)
        for r_elm in to_remove:
            remove_p_element(r_elm)
        print("   ✓ Figura 12 consolidada con éxito")

    # Fig 11
    p_targets = [p for p in doc.paragraphs if "11 Figura. Procedencia de actores locales".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        img_path = os.path.join(FIG_DIR, FIGURES_META[11]["file"])
        insert_apa7_figure_block(pt, 11, FIGURES_META[11], img_path)
        remove_p_element(pt)
        print("   ✓ Figura 11 consolidada con éxito")

    # Fig 10
    p_targets = [p for p in doc.paragraphs if "10 Figura. Años de experiencia ejerciendo".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        img_path = os.path.join(FIG_DIR, FIGURES_META[10]["file"])
        insert_apa7_figure_block(pt, 10, FIGURES_META[10], img_path)
        remove_p_element(pt)
        print("   ✓ Figura 10 consolidada con éxito")

    # Fig 9
    p_targets = [p for p in doc.paragraphs if "9 Figura. Edad por rango de los facilitadores".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        img_path = os.path.join(FIG_DIR, FIGURES_META[9]["file"])
        insert_apa7_figure_block(pt, 9, FIGURES_META[9], img_path)
        remove_p_element(pt)
        print("   ✓ Figura 9 consolidada con éxito")

    # Fig 8
    p_targets = [p for p in doc.paragraphs if "8Figura. Sexo de actores locales".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        next_elm = pt._p.getnext()
        img_path = os.path.join(FIG_DIR, FIGURES_META[8]["file"])
        insert_apa7_figure_block(pt, 8, FIGURES_META[8], img_path)
        remove_p_element(pt)
        if next_elm is not None and bool(next_elm.xpath('.//a:blip')):
            remove_p_element(next_elm)
        print("   ✓ Figura 8 consolidada con éxito")

    # Fig 7
    p_targets = [p for p in doc.paragraphs if "El uso es reactivo y esporádico (52.9% nunca la usa".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        p_idx = [i for i, p in enumerate(doc.paragraphs) if p._p == pt._p][0]
        target_p = doc.paragraphs[p_idx + 1]
        img_path = os.path.join(FIG_DIR, FIGURES_META[7]["file"])
        insert_apa7_figure_block(target_p, 7, FIGURES_META[7], img_path)
        if not target_p.text.strip():
            remove_p_element(target_p)
        print("   ✓ Figura 7 consolidada con éxito")

    # Fig 6
    p_targets = [p for p in doc.paragraphs if "6 Figura. Reconocimiento de las prácticas 2".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        prev_elm = pt._p.getprevious()
        img_path = os.path.join(FIG_DIR, FIGURES_META[6]["file"])
        insert_apa7_figure_block(pt, 6, FIGURES_META[6], img_path)
        remove_p_element(pt)
        if prev_elm is not None and bool(prev_elm.xpath('.//a:blip')):
            remove_p_element(prev_elm)
        print("   ✓ Figura 6 consolidada con éxito")

    # Fig 5
    p_targets = [p for p in doc.paragraphs if "5 Figura. Reconocimiento de las prácticas 1".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        prev_elm = pt._p.getprevious()
        img_path = os.path.join(FIG_DIR, FIGURES_META[5]["file"])
        insert_apa7_figure_block(pt, 5, FIGURES_META[5], img_path)
        remove_p_element(pt)
        if prev_elm is not None and bool(prev_elm.xpath('.//a:blip')):
            remove_p_element(prev_elm)
        print("   ✓ Figura 5 consolidada con éxito")

    # Fig 4
    p_targets = [p for p in doc.paragraphs if "4Figura. Dominio conceptual de los estudiantes".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        img_path = os.path.join(FIG_DIR, FIGURES_META[4]["file"])
        insert_apa7_figure_block(pt, 4, FIGURES_META[4], img_path)
        remove_p_element(pt)
        print("   ✓ Figura 4 consolidada con éxito")

    # Fig 3
    p_targets = [p for p in doc.paragraphs if "77.9% cursa 4.º año (53 estudiantes)".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        p_idx = [i for i, p in enumerate(doc.paragraphs) if p._p == pt._p][0]
        target_p = doc.paragraphs[p_idx + 1]
        img_path = os.path.join(FIG_DIR, FIGURES_META[3]["file"])
        insert_apa7_figure_block(target_p, 3, FIGURES_META[3], img_path)
        if not target_p.text.strip():
            remove_p_element(target_p)
        print("   ✓ Figura 3 consolidada con éxito")

    # Fig 2
    p_targets = [p for p in doc.paragraphs if p.text.strip().lower() == "criterios de exclusión".lower()]
    if p_targets:
        pt = p_targets[0]
        prev_elm = pt._p.getprevious()
        img_path = os.path.join(FIG_DIR, FIGURES_META[2]["file"])
        insert_apa7_figure_block(pt, 2, FIGURES_META[2], img_path)
        if prev_elm is not None and not "".join(prev_elm.xpath('.//w:t/text()')).strip():
            remove_p_element(prev_elm)
        print("   ✓ Figura 2 consolidada con éxito")

    # Fig 1
    p_targets = [p for p in doc.paragraphs if "Específicamente, la investigación tendrá lugar en el Centro Universitario Regional (CUR-Estelí)".lower() in p.text.lower()]
    if p_targets:
        pt = p_targets[0]
        p_idx = [i for i, p in enumerate(doc.paragraphs) if p._p == pt._p][0]
        target_p = doc.paragraphs[p_idx + 1]
        img_path = os.path.join(FIG_DIR, FIGURES_META[1]["file"])
        insert_apa7_figure_block(target_p, 1, FIGURES_META[1], img_path)
        print("   ✓ Figura 1 consolidada con éxito")

    # 4. Update preliminary List of Figures (Índice de figuras)
    print("\n📋 Actualizando Índice de figuras en las páginas preliminares...")
    intro_targets = [p for p in doc.paragraphs if p.text.strip().lower() == "introducción".lower()]
    if intro_targets:
        anchor_p = intro_targets[0]
        for num in range(1, 26):
            meta = FIGURES_META[num]
            p_item = anchor_p.insert_paragraph_before()
            p_item.paragraph_format.line_spacing = 1.5
            p_item.paragraph_format.space_before = Pt(0)
            p_item.paragraph_format.space_after = Pt(2)
            r_num = p_item.add_run(f"Figura {num}. ")
            r_num.font.name = "Times New Roman"
            r_num.font.size = Pt(12)
            r_num.bold = True
            r_title = p_item.add_run(meta["title"])
            r_title.font.name = "Times New Roman"
            r_title.font.size = Pt(12)

        print("   ✓ 25 entradas añadidas al Índice de figuras con tipografía APA 7")

    # 5. Save consolidated document
    print(f"\n💾 Guardando documento consolidado en: {DOCX_OUT}...")
    saved_path = DOCX_OUT
    try:
        doc.save(DOCX_OUT)
        print(f"✅ ¡Consolidación exitosa! Archivo generado con tamaño: {os.path.getsize(DOCX_OUT):,} bytes")
    except PermissionError:
        saved_path = os.path.join(REPO_ROOT, "assets", "MTCI_Consolidado_Final_APA7_Actualizado.docx")
        doc.save(saved_path)
        print(f"⚠️ El archivo principal está abierto en Microsoft Word.")
        print(f"✅ ¡Guardado con éxito en archivo alternativo!: {saved_path} ({os.path.getsize(saved_path):,} bytes)")

if __name__ == "__main__":
    main()
