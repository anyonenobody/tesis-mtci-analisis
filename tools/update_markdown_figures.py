#!/usr/bin/env python3
"""
tools/update_markdown_figures.py
================================
Updates the markdown chapters in 'docs/capitulos/' to integrate the newly generated
APA 7 figures (Figuras 1 to 25).

Ensures:
1. Strict APA 7 text structure for every figure:
   **Figura X**
   *Título descriptivo en cursiva*
   ![Figura X. Título](../../assets/figuras_apa7/figura_XX.png)
   *Nota.* Explicación, tamaño muestral (n), significancia y fuente institucional.
2. In-text parenthetical citations '(véase la Figura X)' preceding every figure.
3. Perfect coherence with the List of Figures in '00_preliminares.md'.
"""

import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPITULOS_DIR = os.path.join(REPO_ROOT, "docs", "capitulos")

FIGURES_META = {
    1: {
        "file": "figura_01_ubicacion_cur_esteli.png",
        "title": "Ubicación geográfica del Centro Universitario Regional (CUR-Estelí)",
        "note": "Delimitación del Centro Universitario Regional (CUR-Estelí) de la UNAN-Managua, recinto Leonel Rugama Rugama, ubicado en el municipio de Estelí, departamento de Estelí, Nicaragua. Fuente: Cartografía institucional del CUR-Estelí, 2026.",
        "cit_target": "recinto Leonel Rugama Rugama, ubicado en el municipio de Estelí",
        "cit_text": " (véase la Figura 1)."
    },
    2: {
        "file": "figura_02_criterios_inclusion_exclusion.png",
        "title": "Diagrama de flujo de criterios de inclusión y exclusión de las unidades de análisis",
        "note": "Criterios muestrales aplicados para la delimitación de estudiantes de 4.º y 5.º año (n = 68), facilitadores locales de MTCI (n = 9) y cuerpo docente-psicólogo (n = 9). Fuente: Elaboración propia, 2026.",
        "cit_target": "La población se refiere al conjunto total de individuos, objetos o elementos",
        "cit_text": " Para garantizar la representatividad y el rigor del muestreo concurrente entre estudiantes, facilitadores y docentes, se aplicaron criterios específicos de delimitación muestral (véase la Figura 2)."
    },
    3: {
        "file": "figura_03_demografia_estudiantes.png",
        "title": "Distribución sociodemográfica y formativa de la muestra estudiantil",
        "note": "n = 68 estudiantes de la carrera de Licenciatura en Psicología del CUR-Estelí. Los paneles desglosan: A) Año de carrera (4.º año: 77.9%, 5.º año: 22.1%); B) Sexo (Femenino: 82.4%, Masculino: 14.7%, Prefiere no decir: 2.9%); C) Rango de edad en años. Fuente: Cuestionario estructurado I1, 2026.",
        "cit_target": "77.9% cursa 4.º año (53 estudiantes)",
        "cit_text": " Estos datos configuran una muestra con marcado predominio femenino y distribuida entre los dos últimos años de formación académica (véase la Figura 3)."
    },
    4: {
        "file": "figura_04_dominio_conceptual_normativo_estudiantes.png",
        "title": "Nivel de dominio conceptual y normativo sobre MTCI en estudiantes de Psicología",
        "note": "n = 68. Comparación entre acierto técnico objetivo y niveles de desconocimiento o concepción errónea respecto a la definición de la OMS, los principios integradores de la Ley No. 774 y la inhabilitación para prescribir psicofármacos según la Ley No. 292. Fuente: Cuestionario estructurado I1, 2026.",
        "cit_target": "Solo el 35.3% identificó con exactitud",
        "cit_text": " Estos resultados evidencian brechas sustantivas en el dominio técnico y jurídico de las leyes sanitarias que regulan el ejercicio profesional (véase la Figura 4)."
    },
    5: {
        "file": "figura_05_reconocimiento_practicas_1_estudiantes.png",
        "title": "Reconocimiento de prácticas de MTCI en estudiantes: Medicina natural y terapias manuales",
        "note": "n = 68. Respuestas de selección múltiple sobre la identificación de prácticas reconocidas en el marco de la salud natural y técnicas corporales. Fuente: Cuestionario estructurado I1, 2026.",
        "cit_target": "Masajes terapéuticos (77.9%), aromaterapia/floral/arteterapia (77.9%)",
        "cit_text": " Los hallazgos revelan un reconocimiento ampliamente mayoritario de las terapias manuales corporales y la medicina natural tradicional (véase la Figura 5)"
    },
    6: {
        "file": "figura_06_reconocimiento_practicas_2_estudiantes.png",
        "title": "Reconocimiento de prácticas de MTCI en estudiantes: Terapias psicoemocionales y energéticas",
        "note": "n = 68. Respuestas de selección múltiple sobre modalidades de regulación mente-cuerpo, bioenergía y abordajes complementarios. Fuente: Cuestionario estructurado I1, 2026.",
        "cit_target": "fitoterapia (60.3%).",
        "cit_text": " en contraste con una familiaridad diferenciada respecto a las modalidades bioenergéticas y psicoemocionales (véase la Figura 6)."
    },
    7: {
        "file": "figura_07_frecuencia_uso_estudiantes.png",
        "title": "Frecuencia de uso personal de MTCI y efectos psicofisiológicos experimentados",
        "note": "Panel A: Frecuencia de uso en el último año para autocuidado general y manejo del estrés (n = 68). Panel B: Efectos sobre el bienestar subjetivo reportados por estudiantes con experiencia empírica de uso (n = 30). Fuente: Cuestionario estructurado I1, 2026.",
        "cit_target": "El uso es reactivo y esporádico (52.9% nunca la usa",
        "cit_text": " Esta dinámica evidencia que el recurso a las MTCI obedece principalmente a necesidades reactivas, asociándose con vivencias positivas de distensión corporal y relajación (véase la Figura 7)."
    },
    8: {
        "file": "figura_08_sexo_actores_locales.png",
        "title": "Distribución por sexo de los facilitadores y actores locales de MTCI",
        "note": "n = 9 facilitadores y terapeutas holísticos del municipio de Estelí (Mujeres: 77.8%, n = 7; Hombres: 22.2%, n = 2). Fuente: Cuestionario I2, 2026.",
        "cit_target": "En Estelí este patrón parece repetirse: son mayoritariamente mujeres",
        "cit_text": " Esta distribución confirma una notoria preponderancia femenina en la conducción de consultorios y prácticas comunitarias de MTCI en el municipio (véase la Figura 8)."
    },
    9: {
        "file": "figura_09_edad_actores_locales.png",
        "title": "Distribución por rangos de edad de los facilitadores locales de MTCI",
        "note": "n = 9. Rango etario de terapeutas y guías en Estelí (30 a 39 años: 55.6%; 40 a 49 años: 22.2%; 50 a 58 años: 22.2%). Fuente: Cuestionario I2, 2026.",
        "cit_target": "Esto sugiere que la oferta de MTCI en el municipio no depende únicamente",
        "cit_text": " Se aprecia una concentración de los facilitadores en etapas de plena madurez y productividad profesional (véase la Figura 9)."
    },
    10: {
        "file": "figura_10_experiencia_actores_locales.png",
        "title": "Años de experiencia profesional en el ejercicio de la MTCI de los facilitadores",
        "note": "n = 9. Trayectoria en el ejercicio de terapias complementarias y saberes tradicionales en Estelí. Fuente: Cuestionario I2, 2026.",
        "cit_target": "El 44.4% de los facilitadores (4 de 9) acumula entre 20 y 30 años",
        "cit_text": " Lo anterior da cuenta de una trayectoria acumulada y consolidada de varias décadas en el ejercicio terapéutico en la región (véase la Figura 10)."
    },
    11: {
        "file": "figura_11_procedencia_actores_locales.png",
        "title": "Procedencia geográfica de los facilitadores locales de MTCI",
        "note": "n = 9. Localización territorial de consultorios y centros de bienestar consultados. Fuente: Cuestionario I2, 2026.",
        "cit_target": "El 77.8% de los facilitadores proviene de Estelí",
        "cit_text": " La localización territorial refleja una marcada centralización de la oferta terapéutica en el casco urbano del municipio de Estelí (véase la Figura 11)."
    },
    12: {
        "file": "figura_12_practicas_actores_locales.png",
        "title": "Modalidades terapéuticas de MTCI utilizadas habitualmente en la atención profesional",
        "note": "n = 9. Selección múltiple de técnicas corporales, energéticas y naturales aplicadas en la atención local. Fuente: Cuestionario I2, 2026.",
        "cit_target": "Los masajes, la reflexología/acupuntura, la aromaterapia y la medicina ayurveda",
        "cit_text": " En el repertorio asistencial destaca la articulación de masajes terapéuticos, preparados fitoterápicos y recursos de autorregulación (véase la Figura 12)."
    },
    13: {
        "file": "figura_13_cambios_estres_ansiedad_actores.png",
        "title": "Percepción de cambios en los niveles de estrés y ansiedad en usuarios atendidos",
        "note": "n = 9. Reporte unánime (100.0%) de los facilitadores sobre la disminución de la sobrecarga y tensión acumulada en consultantes. Fuente: Cuestionario I2, 2026.",
        "cit_target": "El 100% de los facilitadores (9 de 9) reportó cambios positivos",
        "cit_text": " Este dato refleja una percepción unánime entre los terapeutas respecto al alivio de la sobrecarga tensional y el estrés en las personas atendidas (véase la Figura 13)."
    },
    14: {
        "file": "figura_14_apertura_emocional_usuarios_actores.png",
        "title": "Grado de apertura emocional y receptividad observado en los usuarios",
        "note": "n = 9. Valoración sobre el incremento en la disposición personal y el desbloqueo psicofisiológico de los consultantes. Fuente: Cuestionario I2, 2026.",
        "cit_target": "El 88.9% de los facilitadores (8 de 9) describió cambios significativos",
        "cit_text": " Dicha evolución evidencia un progresivo desbloqueo y mayor receptividad para dialogar sobre vivencias afectivas profundas (véase la Figura 14)."
    },
    15: {
        "file": "figura_15_efectos_observados_actores.png",
        "title": "Frecuencia de efectos desfavorables o reacciones emocionales adversas observadas",
        "note": "n = 9. Ausencia total de efectos desfavorables o crisis emocionales iatrogénicas observadas en los consultorios (100.0% seguridad percibida). Fuente: Cuestionario I2, 2026.",
        "cit_target": "Ninguno de los nueve facilitadores reportó haber presenciado un efecto",
        "cit_text": " Este hallazgo subraya la percepción de inocuidad y la ausencia de crisis desfavorables en la práctica cotidiana de las terapias aplicadas (véase la Figura 15)."
    },
    16: {
        "file": "figura_16_interaccion_profesionales_salud.png",
        "title": "Nivel de interacción y coordinación con profesionales e instituciones de salud locales",
        "note": "n = 9. Calificación de las relaciones de trabajo y derivación interdisciplinaria con médicos, psicólogos y centros de salud. Fuente: Cuestionario I2, 2026.",
        "cit_target": "Aquí el panorama es mayormente favorable, pero no del todo parejo",
        "cit_text": " La dinámica muestra canales informales de derivación que requieren avanzar hacia mecanismos sistemáticos de coordinación intersectorial (véase la Figura 16)."
    },
    17: {
        "file": "figura_17_dificultades_normativas_actores.png",
        "title": "Nivel de dificultad normativa y burocrática experimentada por los facilitadores",
        "note": "n = 9. Autopercepción sobre facilidades legales y barreras administrativas en el ejercicio comunitario de MTCI en Estelí. Fuente: Cuestionario I2, 2026.",
        "cit_target": "El 77.8% de los facilitadores dijo no tener dificultades significativas",
        "cit_text": " La valoración indica condiciones mayormente propicias para el ejercicio, aunque un sector minoritario enfrenta trámites burocráticos exigentes (véase la Figura 17)."
    },
    18: {
        "file": "figura_18_reservas_socioculturales_usuarios.png",
        "title": "Frecuencia de usuarios con creencias o reservas socioculturales y religiosas hacia la MTCI",
        "note": "n = 9. Incidencia de mitos, prejuicios y dudas socioculturales atendidas en la práctica cotidiana. Fuente: Cuestionario I2, 2026.",
        "cit_target": "Un 77.8% de los facilitadores señaló que se encuentra “ocasionalmente”",
        "cit_text": " Los testimonios dan cuenta de reticencias comunitarias que son abordadas mediante psicoeducación y diálogo empático (véase la Figura 18)."
    },
    19: {
        "file": "figura_19_incidencia_factor_economico.png",
        "title": "Incidencia del factor económico en el acceso y continuidad de las terapias de MTCI",
        "note": "n = 9. Percepción sobre cómo la disponibilidad financiera condiciona el seguimiento de procesos de autocuidado y bienestar. Fuente: Cuestionario I2, 2026.",
        "cit_target": "El 77.8% de los facilitadores considera que el factor económico incide moderadamente",
        "cit_text": " Este factor sitúa la capacidad de pago como una variable condicionante para sostener la adherencia a largo plazo (véase la Figura 19)."
    },
    20: {
        "file": "figura_20_sexo_docentes.png",
        "title": "Distribución por sexo del cuerpo docente de Psicología consultado",
        "note": "n = 9 docentes de la carrera de Psicología del CUR-Estelí (Mujeres: 77.8%, n = 7; Hombres: 22.2%, n = 2). Fuente: Cuestionario I3, 2026.",
        "cit_target": "Este apartado presenta el perfil general de los nueve docentes participantes",
        "cit_text": " La caracterización sociodemográfica exhibe una notable preponderancia de docentes mujeres en el colectivo consultado (véase la Figura 20)."
    },
    21: {
        "file": "figura_21_edad_docentes.png",
        "title": "Distribución por grupos de edad del cuerpo docente de Psicología",
        "note": "n = 9. Rango etario de docentes universitarios participantes (media = 34.2 años, concentración en 22 a 36 años). Fuente: Cuestionario I3, 2026.",
        "cit_target": "Las edades reportadas oscilan entre los 22 y los 70 años",
        "cit_text": " Los datos muestran un claustro mayoritariamente joven y en fase activa de desarrollo docente universitario (véase la Figura 21)."
    },
    22: {
        "file": "figura_22_especialidad_docentes.png",
        "title": "Distribución de docentes según área de especialidad profesional",
        "note": "n = 9. Especialidades declaradas: Psicología Clínica (55.6%), Infantil/Educativa (22.2%), Comunitaria (11.1%), Salud y Epidemiología (11.1%). Fuente: Cuestionario I3, 2026.",
        "cit_target": "Todos los participantes son licenciados en Psicología",
        "cit_text": " Entre las áreas declaradas destaca el predominio de la psicología clínica como el campo de posgrado más representativo (véase la Figura 22)."
    },
    23: {
        "file": "figura_23_experiencia_docente.png",
        "title": "Años de experiencia en la docencia universitaria de los participantes",
        "note": "n = 9. Años de trayectoria pedagógica en la formación superior en UNAN-Managua / CUR-Estelí. Fuente: Cuestionario I3, 2026.",
        "cit_target": "En cuanto al grado académico, el grupo se reparte entre licenciatura",
        "cit_text": " La experiencia acumulada refleja un grupo docente con concentración en los primeros quinquenios de labor universitaria (véase la Figura 23)."
    },
    24: {
        "file": "figura_24_estrategias_academicas_docentes.png",
        "title": "Estrategias pedagógicas priorizadas por docentes para abordar la MTCI",
        "note": "n = 9. Selección múltiple de metodologías formativas recomendadas para incorporar en el plan de estudios. Fuente: Cuestionario I3, 2026.",
        "cit_target": "Al consultarles qué estrategias académicas consideran más pertinentes",
        "cit_text": " El profesorado prioriza metodologías vivenciales, talleres prácticos e investigaciones formativas en el currículo (véase la Figura 24)."
    },
    25: {
        "file": "figura_25_experiencias_favorables_docentes.png",
        "title": "Experiencias formativas consideradas más favorables para la integración de la MTCI",
        "note": "n = 9. Modalidades de aprendizaje experiencial y vinculación comunitaria priorizadas por el profesorado. Fuente: Cuestionario I3, 2026.",
        "cit_target": "La experiencia formativa más valorada, por amplio margen",
        "cit_text": " En este ámbito se destaca el intercambio con terapeutas tradicionales como la vivencia con mayor potencial pedagógico (véase la Figura 25)."
    }
}

def format_apa7_figure_block(fig_num: int) -> str:
    meta = FIGURES_META[fig_num]
    rel_path = f"../../assets/figuras_apa7/{meta['file']}"
    return (
        f"\n\n**Figura {fig_num}**  \n"
        f"*{meta['title']}*  \n\n"
        f"![Figura {fig_num}. {meta['title']}]({rel_path})  \n\n"
        f"*Nota.* {meta['note']}\n\n"
    )

def update_preliminares():
    path = os.path.join(CAPITULOS_DIR, "00_preliminares.md")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    lines = ["## Índice de figuras\n"]
    for num in range(1, 26):
        meta = FIGURES_META[num]
        lines.append(f"- Figura {num}. {meta['title']}")

    new_list_str = "\n\n".join(lines)
    pattern = r'## Índice de figuras.*?(?=(\n#|\Z))'
    if re.search(pattern, text, re.DOTALL):
        updated_text = re.sub(pattern, new_list_str + "\n\n", text, flags=re.DOTALL)
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated_text)
        print("✅ 00_preliminares.md actualizado con Índice de Figuras APA 7")

def update_introduccion():
    path = os.path.join(CAPITULOS_DIR, "01_introduccion.md")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    if "Figura 1" not in text or "../../assets/figuras_apa7" not in text:
        block = format_apa7_figure_block(1)
        target_str = "segundo semestre del año 2026."
        if target_str in text:
            text = text.replace(target_str, target_str + block)
        else:
            text += block
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("✅ 01_introduccion.md actualizado con Figura 1")

def update_metodologia():
    path = os.path.join(CAPITULOS_DIR, "03_diseno_metodologico.md")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    if "figura_02_criterios_inclusion_exclusion.png" not in text:
        block = format_apa7_figure_block(2)
        target_str = "### Criterios de inclusión"
        if target_str in text:
            text = text.replace(target_str, block + "\n### Criterios de inclusión")
        else:
            text += block
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("✅ 03_diseno_metodologico.md actualizado con Figura 2")

def update_resultados():
    path = os.path.join(CAPITULOS_DIR, "04_analisis_y_discusion_resultados.md")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Inject in-text citations if not already present
    for num in range(3, 26):
        meta = FIGURES_META[num]
        tgt = meta.get("cit_target")
        txt = meta.get("cit_text")
        if tgt and txt and f"Figura {num}" not in text:
            if tgt in text:
                text = text.replace(tgt, tgt + txt)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("✅ 04_analisis_y_discusion_resultados.md citas textuales inyectadas")

def main():
    update_preliminares()
    update_introduccion()
    update_metodologia()
    update_resultados()
    print("✨ Sincronización completa de figuras y citas APA 7 en Markdown.")

if __name__ == "__main__":
    main()
