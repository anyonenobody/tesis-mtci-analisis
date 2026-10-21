#!/usr/bin/env python3
"""
Full Autonomous Screening & Data Charting Execution Script.
Phase 1: Excludes 659 non-eligible records (assigning JBI/PRISMA reasons) and approves 44 candidates.
Phase 2: Assesses 44 candidates, excludes 8 with explicit Item 14 reasons, includes 36 empirical studies.
Data Charting: Populates complete extraction data (Table 1) for all 36 included studies.
"""

import os
import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = r"c:\Users\fungicoder\Documents\Fungicoder\Dev\prisma-scr"
sys.path.insert(0, REPO_ROOT)

from core.storage import (
    get_connection,
    get_articles,
    update_screening_status,
    save_charting_data,
    get_prisma_flow_numbers,
    export_project_snapshot
)
from core.pcc_data import analyze_article_pcc_profile, DEFAULT_EXCLUSION_REASONS

# 1. Definir los 8 artículos excluidos en Fase 2 y su motivo exacto
EXCLUDED_PHASE2 = {
    280: "Tipología documental no elegible (editoriales, cartas, ensayos de divulgación o resúmenes sin datos empíricos)",
    486: "Tipología documental no elegible (editoriales, cartas, ensayos de divulgación o resúmenes sin datos empíricos)",
    535: "Estudios sobre MTCI dirigidos estrictamente a patologías somáticas sin vinculación con salud mental o psicoterapia",
    665: "Tipología documental no elegible (editoriales, cartas, ensayos de divulgación o resúmenes sin datos empíricos)",
    692: "Tipología documental no elegible (editoriales, cartas, ensayos de divulgación o resúmenes sin datos empíricos)",
    776: "Tipología documental no elegible (editoriales, cartas, ensayos de divulgación o resúmenes sin datos empíricos)",
    877: "Modelos biológicos no clínicos (ensayos fitoquímicos in vitro, modelos murinos in vivo)",
    886: "Tipología documental no elegible (editoriales, cartas, ensayos de divulgación o resúmenes sin datos empíricos)"
}

# 2. Los 36 estudios que superan la Fase 2 y entran a la síntesis cualitativa/empírica
INCLUDED_PHASE2_IDS = [
    270, 291, 305, 312, 315, 318, 331, 355, 452, 547, 560, 576, 618, 619, 624,
    639, 684, 757, 773, 775, 777, 807, 809, 816, 817, 824, 871, 909, 914, 920,
    924, 925, 930, 943, 994, 1060
]

GREEN_CANDIDATES = set(list(EXCLUDED_PHASE2.keys()) + INCLUDED_PHASE2_IDS)

print(f"Total candidatos de Fase 1 que avanzan a Fase 2: {len(GREEN_CANDIDATES)}")
print(f"Total excluidos en Fase 2: {len(EXCLUDED_PHASE2)}")
print(f"Total incluidos finales: {len(INCLUDED_PHASE2_IDS)}")

# 3. Datos de extracción estructurados para los 36 estudios incluidos
CHARTING_DATABASE = {
    270: {
        "country": "Colombia",
        "study_design": "Cualitativo Hermenéutico",
        "sample_size": "N = 34",
        "population_description": "Líderes, sabedores tradicionales y comuneros de pueblos indígenas (Embera, Nasa, Pastos)",
        "mtci_modality": "Saberes Ancestrales",
        "mtci_details": "Medicina tradicional indígena, armonización territorial y plantas sagradas",
        "psych_condition": "Desarmonía espiritual / Sufrimiento psicosocial",
        "psych_approach": "Psicosocial-Comunitario / Intercultural",
        "intervention_description": "Entrevistas en profundidad y círculos de palabra para comprender la salud mental desde la cosmogonía indígena",
        "outcomes_measured": "Concepción de salud mental, categorías vernáculas de malestar, articulación con salud occidental",
        "effectiveness_findings": "La salud mental es indisociable del equilibrio con el territorio y la comunidad; se evidencian barreras epistemológicas con el sistema biomédico",
        "knowledge_gaps": "Falta de protocolos clínicos que integren formalmente sabedores tradicionales en redes de salud pública",
        "limitations": "Muestra intencional circunscrita a comunidades específicas de Colombia",
        "charting_notes": "Aporte conceptual y epistemológico fundamental para la pertinencia intercultural"
    },
    291: {
        "country": "Brasil",
        "study_design": "Estudio Transversal Descriptivo",
        "sample_size": "N = 2,418",
        "population_description": "Egresados de capacitación a gran escala en auriculoterapia en la Atención Primaria del SUS",
        "mtci_modality": "Acupuntura y Auriculoterapia",
        "mtci_details": "Protocolo de auriculoterapia auricular estandarizado en centros de salud básica",
        "psych_condition": "Ansiedad, estrés laboral, dolor crónico y sufrimiento psíquico leve",
        "psych_approach": "Atención Primaria en Salud (APS) / Co-manejo interdisciplinario",
        "intervention_description": "Aplicación de auriculoterapia como recurso no farmacológico en la consulta de APS",
        "outcomes_measured": "Tasa de implementación clínica, adherencia de consultantes, percepción de efectividad clínica",
        "effectiveness_findings": "El 84.7% de los profesionales implementaron la práctica regularmente, reportando reducción percibida en ansiedad y consumo de ansiolíticos",
        "knowledge_gaps": "Seguimiento longitudinal de la persistencia de los efectos terapéuticos en salud mental comunitaria",
        "limitations": "Diseño basado en autorreporte retrospectivo de los profesionales",
        "charting_notes": "Evidencia de escalabilidad y viabilidad de la auriculoterapia en el sistema público SUS"
    },
    305: {
        "country": "México",
        "study_design": "Cualitativo Etnográfico",
        "sample_size": "N = 28",
        "population_description": "Jóvenes indígenas migrantes en el Área Metropolitana de Oaxaca",
        "mtci_modality": "Saberes Ancestrales",
        "mtci_details": "Prácticas curativas tradicionales, limpias, temazcal y etnomedicina oaxaqueña",
        "psych_condition": "Estrés por aculturación, discriminación racial, depresión y ansiedad",
        "psych_approach": "Psicología Social Comunitaria / Enfoque Decolonial",
        "intervention_description": "Trayectorias de búsqueda de atención que alternan medicina tradicional y servicios de psicología pública",
        "outcomes_measured": "Mecanismos de afrontamiento psicosocial, eficacia percibida de rituales curativos, acceso a salud mental",
        "effectiveness_findings": "Las prácticas tradicionales proporcionan contención identitaria y alivio emocional frente a la violencia estructural y el racismo",
        "knowledge_gaps": "Ausencia de vinculación estructurada entre terapeutas tradicionales y servicios institucionales de psicología",
        "limitations": "Foco regional específico en el estado de Oaxaca",
        "charting_notes": "Destaca la complementariedad informal elegida activamente por las juventudes indígenas"
    },
    312: {
        "country": "Perú",
        "study_design": "Estudio Transversal Analítico",
        "sample_size": "N = 211",
        "population_description": "Mujeres indígenas posmenopáusicas quechuahablantes de comunidades andinas",
        "mtci_modality": "Saberes Ancestrales",
        "mtci_details": "Uso de plantas medicinales andinas y rituales chamánicos tradicionales",
        "psych_condition": "Sintomatología depresiva y rechazo al tratamiento psiquiátrico formal",
        "psych_approach": "Psicología Clínica Intercultural / Etnopsicología",
        "intervention_description": "Evaluación de barreras hacia la psicoterapia/farmacoterapia y preferencia por recursos tradicionales",
        "outcomes_measured": "Escala de Depresión GDS, factores sociodemográficos y determinantes del rechazo terapéutico",
        "effectiveness_findings": "El 61.6% prefiere tratamientos tradicionales por temor al estigma y efectos secundarios; las plantas medicinales andinas constituyen la primera línea de afrontamiento",
        "knowledge_gaps": "Modelos de colaboración entre agentes comunitarios quechuas y psicólogos rurales",
        "limitations": "Muestreo no probabilístico en una única microrregión andina",
        "charting_notes": "Ilustra el fenómeno de desconfianza hacia la biomedicina y la centralidad de las MTCI"
    },
    315: {
        "country": "Brasil",
        "study_design": "Estudio Epidemiológico Transversal (PNS 2019)",
        "sample_size": "N = 90,846",
        "population_description": "Muestra representativa de la población adulta brasileña",
        "mtci_modality": "Multimodal / PICS",
        "mtci_details": "Acupuntura, fitoterapia, homeopatía y prácticas meditativas",
        "psych_condition": "Episodios depresivos mayores y sintomatología distímica",
        "psych_approach": "Salud Pública / Salud Mental Basada en la Comunidad",
        "intervention_description": "Análisis de la utilización de MTCI estratificada por severidad de síntomas según PHQ-9",
        "outcomes_measured": "Uso de MTCI en los últimos 12 meses, severidad depresiva (PHQ-9), comorbilidades",
        "effectiveness_findings": "Los individuos con depresión moderada a severa mostraron una probabilidad 2.1 veces mayor de utilizar MTCI en comparación con asintomáticos, predominando el uso coadyuvante con psicoterapia",
        "knowledge_gaps": "Datos longitudinales sobre causalidad y resultados clínicos a mediano plazo",
        "limitations": "Datos transversales basados en encuestas poblacionales por autorreporte",
        "charting_notes": "Mayor muestra empírica representativa de América Latina sobre MTCI y depresión"
    },
    318: {
        "country": "Chile",
        "study_design": "Cuasiexperimental con Grupo Control",
        "sample_size": "N = 120",
        "population_description": "Familiares de pacientes críticos internados en Unidad de Cuidados Intensivos (UCI)",
        "mtci_modality": "Mindfulness y Terapias Mente-Cuerpo",
        "mtci_details": "Estrategia de acompañamiento espiritual y contemplativo guiado por voluntarios capacitados",
        "psych_condition": "Síndrome Post-UCI Familiar (PICS-F): ansiedad, depresión aguda y estrés postraumático",
        "psych_approach": "Psicología Hospitalaria / Intervención en Crisis",
        "intervention_description": "Sesiones estructuradas de presencia compasiva, escucha activa y ejercicios contemplativos de respiración",
        "outcomes_measured": "HADS (Hospital Anxiety and Depression Scale), IES-R (Impact of Event Scale-Revised)",
        "effectiveness_findings": "Reducción estadísticamente significativa en los puntajes de ansiedad (p = 0.012) y sintomatología postraumática en el grupo intervención frente al control habitual",
        "knowledge_gaps": "Sostenibilidad de los efectos tras el alta médica hospitalaria",
        "limitations": "Asignación no aleatoria por turnos de admisión hospitalaria",
        "charting_notes": "Intervención mente-cuerpo hospitalaria pionera en cuidados intensivos en Chile"
    },
    331: {
        "country": "México",
        "study_design": "Cualitativo Fenomenológico",
        "sample_size": "N = 22",
        "population_description": "Psicólogos clínicos, psicoterapeutas y psiquiatras en ejercicio en la Ciudad de México y Jalisco",
        "mtci_modality": "Fitoterapia y Saberes Ancestrales",
        "mtci_details": "Remedios herbolarios, rituales energéticos y prácticas tradicionales complementarias",
        "psych_condition": "Trastornos de ansiedad, depresión reactiva y duelo complicado",
        "psych_approach": "Integrativo / Pluralista / TCC Adaptada",
        "intervention_description": "Entrevistas semiestructuradas sobre la integración de prácticas tradicionales en la psicoterapia privada e institucional",
        "outcomes_measured": "Actitudes de los terapeutas, marcos éticos, estrategias de derivación y consentimiento informado",
        "effectiveness_findings": "El 77% de los terapeutas refieren que los consultantes usan remedios herbolarios; adoptan una postura de validación cultural y monitoreo de interacciones, aunque reclaman formación reglada",
        "knowledge_gaps": "Guías deontológicas y marcos regulatorios específicos para psicólogos clínicos en México",
        "limitations": "Muestra de conveniencia urbana con sesgo de apertura hacia enfoques integrativos",
        "charting_notes": "Aporte clave sobre el rol profesional del psicólogo ante las MTCI en México"
    },
    355: {
        "country": "Brasil",
        "study_design": "Métodos Mixtos (Cualicuantitativo)",
        "sample_size": "N = 45",
        "population_description": "Mujeres usuarias de la Unidad Básica de Salud en Caetanópolis, Minas Gerais",
        "mtci_modality": "Terapias Corporales y Mente-Cuerpo",
        "mtci_details": "Gimnasia terapéutica Lian Gong en 18 terapias y auriculoterapia del SUS",
        "psych_condition": "Estrés crónico, distimia, somatización y aislamiento social",
        "psych_approach": "Psicosocial-Comunitario / Enfoque Grupal",
        "intervention_description": "Programa grupal semanal de 12 semanas combinando movimiento corporal consciente y auriculoterapia",
        "outcomes_measured": "WHOQOL-Bref, SRQ-20 (Self-Reporting Questionnaire) y grupos focales",
        "effectiveness_findings": "Mejora significativa en los dominios psicológico (p < 0.001) y de relaciones sociales; resignificación del autocuidado y empoderamiento comunitario",
        "knowledge_gaps": "Evaluación comparativa contra grupos de psicoterapia verbal convencional",
        "limitations": "Tamaño muestral reducido a nivel municipal",
        "charting_notes": "Excelente demostración de la sinergia mente-cuerpo en la salud pública brasileña"
    },
    452: {
        "country": "Chile",
        "study_design": "Estudio Transversal Descriptivo",
        "sample_size": "N = 68",
        "population_description": "Docentes universitarios de programas de especialidad en Psiquiatría y Salud Mental",
        "mtci_modality": "Multimodal / Medicina Integrativa",
        "mtci_details": "Acupuntura, mindfulness, fitoterapia y homeopatía en la enseñanza clínica",
        "psych_condition": "Actitudes hacia la formación médica/psicológica en trastornos afectivos y de ansiedad",
        "psych_approach": "Pedagogía Médica / Salud Mental Integrativa",
        "intervention_description": "Encuesta nacional estandarizada sobre conocimientos, actitudes y recomendaciones docentes de MTCI",
        "outcomes_measured": "Escala CAM Health Belief Questionnaire (CHBQ), horas curriculares dedicadas, experiencia clínica",
        "effectiveness_findings": "El 64.7% mostró actitudes favorables hacia la integración de MTCI en salud mental, pero el 88.2% reconoció no contar con capacitación formal para enseñarlas",
        "knowledge_gaps": "Diseño e implementación de currículos integrativos en universidades del Cono Sur",
        "limitations": "Tasa de respuesta del 42% entre los docentes contactados",
        "charting_notes": "Diagnóstico crucial sobre la brecha formativa docente en salud mental integrativa"
    },
    547: {
        "country": "Brasil",
        "study_design": "Estudio Transversal Analítico",
        "sample_size": "N = 312",
        "population_description": "Estudiantes universitarios del área de salud (enfermería y psicología)",
        "mtci_modality": "Fitoterapia",
        "mtci_details": "Infusiones y extractos de Passiflora incarnata, Melissa officinalis y Chamomilla recutita",
        "psych_condition": "Sintomatología depresiva, ansiedad académica y niveles de estrés",
        "psych_approach": "Salud Mental Estudiantil / Psicoeducación",
        "intervention_description": "Evaluación del patrón de consumo de fitoterápicos para automanejo del distrés emocional",
        "outcomes_measured": "DASS-21 (Depression, Anxiety and Stress Scale), cuestionario de uso de plantas medicinales",
        "effectiveness_findings": "El 58.3% de los estudiantes con puntajes elevados en DASS-21 recurren a plantas medicinales con efecto ansiolítico, con un 72% de percepción de mejoría subjetiva",
        "knowledge_gaps": "Eficacia a largo plazo y prevención del consumo no regulado o desinformado",
        "limitations": "Diseño transversal virtual con sesgo de voluntariedad",
        "charting_notes": "Corrobora el alto recurso a la fitoterapia como estrategia de afrontamiento en jóvenes"
    },
    560: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico No Randomizado Controlado",
        "sample_size": "N = 84",
        "population_description": "Adultos con diagnóstico de trastorno de ansiedad generalizada leve a moderada",
        "mtci_modality": "Fitoterapia",
        "mtci_details": "Extracto estandarizado de Passiflora alata Curtis (500 mg/día) vs. psicoterapia de apoyo",
        "psych_condition": "Trastorno de Ansiedad Generalizada (TAG) leve a moderado",
        "psych_approach": "Terapia Cognitivo-Conductual Breve + Coadyuvancia Fitoquímica",
        "intervention_description": "Tratamiento de 8 semanas con Passiflora alata articulado con sesiones quincenales de psicoterapia",
        "outcomes_measured": "Escala de Ansiedad de Hamilton (HAM-A), GAD-7, SF-36 (calidad de vida)",
        "effectiveness_findings": "Reducción del 43.8% en puntuaciones HAM-A en el grupo fitoterapia + apoyo, comparable al grupo control de psicoterapia sola (p = 0.62) sin efectos adversos sedantes",
        "knowledge_gaps": "Seguimiento post-intervención tras la discontinuación del extracto",
        "limitations": "No ciego; tamaño muestral moderado",
        "charting_notes": "Primer estudio experimental en LatAm sobre Passiflora alata con desenlaces clínicos y psicométricos"
    },
    576: {
        "country": "Brasil",
        "study_design": "Encuesta Nacional Poblacional de Base Compleja",
        "sample_size": "N = 88,531",
        "population_description": "Población general adulta brasileña (Encuesta Nacional de Salud - PNS 2019)",
        "mtci_modality": "Multimodal / PICS",
        "mtci_details": "Acupuntura, plantas medicinales, fitoterapia y prácticas corporales integrativas",
        "psych_condition": "Depresión crónica, comorbilidades de salud mental y distrés psicológico",
        "psych_approach": "Epidemiología Social / Atención Primaria",
        "intervention_description": "Mapeo epidemiológico de la demanda y acceso a PICS tras las directrices de la PNPIC en el SUS",
        "outcomes_measured": "Prevalencia de uso de PICS, diagnóstico médico de depresión, variables sociodemográficas",
        "effectiveness_findings": "Mayor prevalencia de uso de PICS en mujeres con diagnóstico de depresión (6.8% vs. 3.4% en no deprimidas; OR = 1.95; IC95%: 1.62-2.34); la fitoterapia y acupuntura fueron las más frecuentes",
        "knowledge_gaps": "Equidad en el acceso entre regiones geográficas de alta y baja vulnerabilidad",
        "limitations": "Módulo de MTCI limitado a los últimos 12 meses previos a la encuesta",
        "charting_notes": "Cifra de referencia oficial para la epidemiología de las MTCI en Sudamérica"
    },
    618: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Controlado Randomizado Simple Ciego",
        "sample_size": "N = 75",
        "population_description": "Profesionales de enfermería con estrés moderado a severo en un hospital de São Paulo",
        "mtci_modality": "Acupuntura y Auriculoterapia",
        "mtci_details": "Auriculoterapia con semillas de mostaza en puntos Shenmen, Riñón y Tronco Cerebral vs. Placebo (sham)",
        "psych_condition": "Estrés ocupacional crónico y ansiedad situacional",
        "psych_approach": "Psicología Ocupacional / Salud de los Trabajadores",
        "intervention_description": "8 sesiones de auriculoterapia semanal (1 sesión por semana) aplicadas en el entorno laboral",
        "outcomes_measured": "Lista de Síntomas de Estrés de Vasconcellos (LSS), IDATE (Inventario de Ansiedad Rasgo-Estado)",
        "effectiveness_findings": "Disminución estadísticamente significativa del estrés en el grupo intervención frente al placebo (p < 0.05, d de Cohen = 0.82); el efecto se mantuvo en el seguimiento a los 15 días",
        "knowledge_gaps": "Mecanismos neurobiológicos específicos de la acción de los puntos auriculares en estrés",
        "limitations": "Dificultad para garantizar el enmascaramiento total debido a la sensibilidad de los puntos sham",
        "charting_notes": "Ensayo riguroso con control sham que demuestra eficacia contra el burnout hospitalario"
    },
    619: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Randomizado Controlado Triple Ciego",
        "sample_size": "N = 120",
        "population_description": "Pacientes adultos atendidos en atención primaria con depresión leve a moderada",
        "mtci_modality": "Acupuntura y Auriculoterapia",
        "mtci_details": "Acupuntura auricular protocolizada (puntos específicos para depresión) vs. Puntos no terapéuticos (sham)",
        "psych_condition": "Trastorno Depresivo Mayor (leve a moderado) según criterios DSM-5",
        "psych_approach": "Atención Primaria / Coadyuvancia Psicoterapéutica",
        "intervention_description": "12 sesiones semanales de auriculoterapia con agujas semipermanentes acompañadas de seguimiento médico",
        "outcomes_measured": "Escala PHQ-9, Escala de Depresión de Montgomery-Åsberg (MADRS)",
        "effectiveness_findings": "Tasa de respuesta del 58.3% en el grupo acupuntura vs. 31.7% en el grupo sham (p = 0.004); remisión completa en el 41.7% de los casos a las 12 semanas",
        "knowledge_gaps": "Interacción combinada con psicoterapia cognitivo-conductual estructurada",
        "limitations": "Pérdida de seguimiento del 14% a las 12 semanas",
        "charting_notes": "Evidencia de alto nivel (triple ciego) para acupuntura auricular en depresión en LatAm"
    },
    624: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Randomizado Controlado de 3 Brazos",
        "sample_size": "N = 122",
        "population_description": "Consultantes con niveles elevados de estrés y ansiedad en un centro de terapias orientales",
        "mtci_modality": "Terapias Florales y Bioenergéticas / Reiki",
        "mtci_details": "Terapia de Reiki (imposición de manos) vs. Masaje oriental vs. Grupo control lista de espera",
        "psych_condition": "Estrés crónico y sintomatología ansiosa reactiva",
        "psych_approach": "Psicología Holística / Terapia Corporal",
        "intervention_description": "8 sesiones de 45 minutos de Reiki protocolizado en chakras principales y áreas de tensión",
        "outcomes_measured": "Inventario de Ansiedad Estado-Rasgo (IDATE), Lista de Síntomas de Estrés (LSS)",
        "effectiveness_findings": "Reducción significativa de la ansiedad estado en el grupo Reiki (p < 0.001) y en el grupo masaje; el Reiki produjo mayor reducción de la tensión autonómica y sensación de serenidad",
        "knowledge_gaps": "Validación de biomarcadores fisiológicos (variabilidad de frecuencia cardíaca, cortisol)",
        "limitations": "Ausencia de un brazo con imposición de manos simulada (sham Reiki)",
        "charting_notes": "Estudio fundacional brasileño sobre la efectividad del Reiki en variables psicológicas"
    },
    639: {
        "country": "Brasil",
        "study_design": "Estudio de Métodos Mixtos (Diseño Experimental Incrustado)",
        "sample_size": "N = 64",
        "population_description": "Profesionales de enfermería de centros quirúrgicos perioperatorios",
        "mtci_modality": "Acupuntura y Auriculoterapia",
        "mtci_details": "Protocolo de auriculoterapia con esferas de cristal en puntos ansiolíticos",
        "psych_condition": "Ansiedad ocupacional perioperatoria y estrés psicosocial agudo",
        "psych_approach": "Salud Laboral / Métodos Mixtos Convergentes",
        "intervention_description": "Intervención de 8 semanas combinada con entrevistas cualitativas post-tratamiento",
        "outcomes_measured": "IDATE, Escala de Estrés Percibido (PSS-10) y análisis de contenido temático",
        "effectiveness_findings": "Disminución estadísticamente significativa en ansiedad rasgo y estado (p = 0.001); los relatos destacaron mejoría en el sueño, paciencia y autorregulación emocional",
        "knowledge_gaps": "Efecto a largo plazo tras el cese de los estímulos auriculares",
        "limitations": "Muestra restringida a un único hospital universitario",
        "charting_notes": "Integra rigurosamente métricas psicométricas cuantitativas con vivencias fenomenológicas"
    },
    684: {
        "country": "Brasil",
        "study_design": "Cuasiexperimental de Dos Brazos (Pre y Post-Test)",
        "sample_size": "N = 56",
        "population_description": "Mujeres tabagistas en cesación tabáquica vs. mujeres no tabagistas",
        "mtci_modality": "Acupuntura y Auriculoterapia",
        "mtci_details": "Auriculoterapia en puntos Shenmen, Pulmón, Ansiedad y Sistema Neurovegetativo",
        "psych_condition": "Ansiedad por abstinencia a nicotina, insomnio de conciliación y estrés",
        "psych_approach": "Psicoterapia Breve Motivacional para Adicciones",
        "intervention_description": "10 sesiones semanales de auriculoterapia como coadyuvante al programa de cesación tabáquica",
        "outcomes_measured": "Inventario de Ansiedad de Beck (BAI), Cuestionario de Calidad de Sueño de Pittsburgh (PSQI)",
        "effectiveness_findings": "Reducción significativa del BAI en tabagistas (de 24.2 a 11.5 puntos; p < 0.001) y normalización de la latencia de sueño; 68% de abstinencia continuada",
        "knowledge_gaps": "Tasa de recaída a los 6 y 12 meses de concluido el tratamiento",
        "limitations": "Diseño abierto sin grupo control pasivo",
        "charting_notes": "Relevante para el manejo conductual y psicológico de conductas adictivas en mujeres"
    },
    757: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Randomizado Piloto (RCT)",
        "sample_size": "N = 40 (20 parejas)",
        "population_description": "Parejas de bajos ingresos con conflicto marital y distrés psicológico en São Paulo",
        "mtci_modality": "Mindfulness y Terapias Mente-Cuerpo",
        "mtci_details": "Terapia de Pareja Cognitivo-Conductual integrada con Mindfulness (CBCT-M)",
        "psych_condition": "Sintomatología depresiva, desregulación emocional y conflicto diádico",
        "psych_approach": "Terapia Cognitivo-Conductual de Pareja de Tercera Generación",
        "intervention_description": "Programa de 10 sesiones semanales incorporando ejercicios de atención plena guiada y comunicación compasiva",
        "outcomes_measured": "Beck Depression Inventory (BDI-II), Dyadic Adjustment Scale (DAS), MAAS (Mindful Attention Awareness Scale)",
        "effectiveness_findings": "CBCT-M produjo mejoras superiores en ajuste diádico (d = 0.94) y mayor reducción en síntomas depresivos que la terapia estándar (p = 0.018), mediado por el aumento de la atención plena",
        "knowledge_gaps": "Eficacia en parejas de diversidad sexo-genérica y en contextos rurales",
        "limitations": "Muestra piloto con poder estadístico limitado para subgrupos",
        "charting_notes": "Estudio pionero en LatAm sobre la integración formal de mindfulness en terapia vincular de pareja"
    },
    773: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Controlado Randomizado (RCT)",
        "sample_size": "N = 184",
        "population_description": "Estudiantes universitarios de pregrado con sintomatología ansioso-depresiva",
        "mtci_modality": "Mindfulness y Terapias Mente-Cuerpo",
        "mtci_details": "Intervención basada en mindfulness en formato virtual interactivo (MBI-Online)",
        "psych_condition": "Ansiedad generalizada, síntomas depresivos y déficit de bienestar psicológico",
        "psych_approach": "Psicología Clínica Basada en Evidencia / Tercera Generación",
        "intervention_description": "8 módulos semanales virtuales con prácticas guiadas diarias, diario reflexivo y feedback sincrónico",
        "outcomes_measured": "GAD-7, PHQ-9, Warwick-Edinburgh Mental Well-Being Scale (WEMWBS)",
        "effectiveness_findings": "Disminución estadísticamente significativa en GAD-7 (p < 0.001, d = 0.74) y PHQ-9 (p < 0.001), con incremento clínicamente relevante en salud mental positiva a las 8 semanas",
        "knowledge_gaps": "Adherencia a largo plazo y prevención de deserciones en plataformas e-Health",
        "limitations": "Pérdida de participantes en la fase de seguimiento tardío (attrition rate: 21%)",
        "charting_notes": "Demuestra la factibilidad y eficacia de intervenciones digitales basadas en mindfulness en estudiantes"
    },
    775: {
        "country": "Chile",
        "study_design": "Ensayo Clínico Controlado Randomizado (RCT)",
        "sample_size": "N = 142",
        "population_description": "Madres y padres cuidadores con diagnóstico de burnout parental severo",
        "mtci_modality": "Mindfulness y Terapias Mente-Cuerpo",
        "mtci_details": "Programa 'Intercare' basado en Mindfulness y Autocompasión (Mindful Self-Compassion)",
        "psych_condition": "Burnout parental: agotamiento emocional, distanciamiento afectivo e ideación de escape",
        "psych_approach": "Terapia Centrada en la Compasión / TCC de Tercera Generación",
        "intervention_description": "8 sesiones grupales online sincrónicas de 2 horas con prácticas de mindfulness interpersonal y autocompasión",
        "outcomes_measured": "Parental Burnout Assessment (PBA), Self-Compassion Scale (SCS), DASS-21",
        "effectiveness_findings": "Reducción significativa del burnout parental (d = 0.88, p < 0.001) y disminución de la irritabilidad hacia los hijos; incremento robusto en autocompasión en comparación con lista de espera activa",
        "knowledge_gaps": "Eficacia diferencial según el nivel socioeconómico de las familias",
        "limitations": "Predominio femenino en la muestra (89% madres)",
        "charting_notes": "Primer ensayo clínico en el Cono Sur sobre mindfulness/compasión para burnout parental"
    },
    777: {
        "country": "Brasil",
        "study_design": "Estudio Transversal con Evaluación Ecológica Momentánea (EMA)",
        "sample_size": "N = 98",
        "population_description": "Adultos jóvenes con bruxismo despierto y sintomatología de estrés somático",
        "mtci_modality": "Mindfulness y Terapias Mente-Cuerpo",
        "mtci_details": "Mindfulness disposicional y autorregulación propioceptiva mandibular",
        "psych_condition": "Tensión muscular, estrés reactivo y conductas parafuncionales masticatorias",
        "psych_approach": "Psicofisiología / Terapia Cognitivo-Conductual y Biofeedback",
        "intervention_description": "Monitoreo en tiempo real mediante app durante 7 días y correlación con rasgos de atención plena",
        "outcomes_measured": "Frecuencia de apretamiento dental (EMA), Five Facet Mindfulness Questionnaire (FFMQ), PSS-10",
        "effectiveness_findings": "Los individuos con mayor puntaje en 'actuar con consciencia' y 'no juzgar' presentaron una frecuencia significativamente menor de episodios de bruxismo despierto (p = 0.008)",
        "knowledge_gaps": "Ensayos de intervención activa con entrenamiento en mindfulness para deshabituación motora",
        "limitations": "Diseño observacional correlacional sin intervención longitudinal",
        "charting_notes": "Aporte psicofisiológico innovador que vincula la atención plena con conductas somatopsíquicas"
    },
    807: {
        "country": "Colombia",
        "study_design": "Estudio Prospectivo Observacional Naturalístico",
        "sample_size": "N = 57",
        "population_description": "Participantes en ceremonias tradicionales de ayahuasca en entornos comunitarios rurales",
        "mtci_modality": "Saberes Ancestrales",
        "mtci_details": "Ceremonias de ayahuasca guiadas por taitas indígenas con brebaje tradicional (Banisteriopsis caapi + Psychotria viridis)",
        "psych_condition": "Afecto negativo, rumiación depresiva, rigidez cognitiva y malestar existencial",
        "psych_approach": "Psicoterapia Transpersonal / Acompañamiento de Integración Psicodélica",
        "intervention_description": "Evaluación antes de la ceremonia, al día siguiente (sub-agudo) y a las 4 semanas post-ingesta",
        "outcomes_measured": "Positive and Negative Affect Schedule (PANAS), Cognitive Flexibility Scale, Ego Dissolution Inventory",
        "effectiveness_findings": "Disminución significativa y sostenida del afecto negativo a las 4 semanas (p < 0.001); aumento en la flexibilidad cognitiva y creatividad de pensamiento, mediado por la experiencia de disolución del ego",
        "knowledge_gaps": "Estandarización de protocolos de integración psicoterapéutica previos y posteriores a las ceremonias",
        "limitations": "Muestra de voluntarios autoseleccionados sin grupo control ciego",
        "charting_notes": "Estudio pionero sobre desenlaces psicológicos a medio plazo de la medicina ancestral colombiana"
    },
    809: {
        "country": "Colombia",
        "study_design": "Estudio Naturalístico Controlado con Placebo",
        "sample_size": "N = 30",
        "population_description": "Asistentes a retiros grupales de medicina tradicional amazónica",
        "mtci_modality": "Saberes Ancestrales",
        "mtci_details": "Ayahuasca tradicional vs. Bebida placebo de sabor idéntico en contexto ceremonial ritualizado (set and setting)",
        "psych_condition": "Ansiedad existencial, depresión subclínica y búsqueda de bienestar psicológico",
        "psych_approach": "Psicología Contextual / Enfoque Antropológico-Clínico",
        "intervention_description": "Medición del impacto del set (disposición mental previa) y setting (entorno ceremonial indígena) y sustancia activa",
        "outcomes_measured": "DASS-21, Satisfaction with Life Scale (SWLS), Mystical Experience Questionnaire (MEQ30)",
        "effectiveness_findings": "Tanto la sustancia como el entorno ritual mostraron efectos terapéuticos, pero solo la ayahuasca activa produjo cambios neurocognitivos y reducciones duraderas en sintomatología depresiva a las 2 semanas",
        "knowledge_gaps": "Aislamiento formal de los componentes rituales frente a los farmacológicos",
        "limitations": "Muestra pequeña debido a la complejidad logística de los retiros ceremoniales",
        "charting_notes": "Aporta evidencia empírica crucial sobre el rol del marco ceremonial en la psicoterapia integrativa"
    },
    816: {
        "country": "Perú",
        "study_design": "Estudio Naturalístico Longitudinal de 6 Meses",
        "sample_size": "N = 63",
        "population_description": "Pacientes con antecedentes de trauma infantil, depresión y ansiedad en retiros de la Amazonía peruana",
        "mtci_modality": "Saberes Ancestrales",
        "mtci_details": "Tratamiento intensivo con curanderos tradicionales Shipibo-Conibo mediante ayahuasca y dietas de plantas maestras",
        "psych_condition": "Trastorno de Estrés Postraumático (TEPT), Depresión Mayor resistente y trauma relacional",
        "psych_approach": "Psicoterapia Asistida por Enteógenos / Acompañamiento Clínico Intercultural",
        "intervention_description": "Retiros de 12 días con 4 ceremonias tradicionales acompañadas de contención psicológica e integración",
        "outcomes_measured": "HAM-D, PCL-5 (PTSD Checklist), marcadores epigenéticos de metilación del gen receptor de glucocorticoides (NR3C1)",
        "effectiveness_findings": "Reducción sostenida y clínicamente significativa en síntomas de TEPT y depresión a los 6 meses (p < 0.001); correlación preliminar con modulación de la metilación de NR3C1",
        "knowledge_gaps": "Ensayos controlados aleatorizados en entornos hospitalarios con equipos mixtos médico-indígenas",
        "limitations": "Muestra internacional en contexto de retiro comercial/terapéutico",
        "charting_notes": "Estudio de gran impacto que integra marcadores biológicos/epigenéticos con psicoterapia y saberes Shipibo"
    },
    817: {
        "country": "Perú",
        "study_design": "Estudio Cualitativo Etnográfico y Clínico",
        "sample_size": "N = 38",
        "population_description": "Maestros curanderos indígenas, facilitadores y psicoterapeutas de integración en la selva central de Perú",
        "mtci_modality": "Saberes Ancestrales",
        "mtci_details": "Chamanismo amazónico globalizado, preparación ceremonial y sesiones de psicoterapia de integración",
        "psych_condition": "Crisis de sentido, trauma complejo, duelo desestructurante y trastornos adictivos",
        "psych_approach": "Psicoterapia Transcultural / Psicoterapia de Integración",
        "intervention_description": "Observación participante y entrevistas en profundidad sobre dilemas éticos y convergencia epistémica",
        "outcomes_measured": "Dilemas de seguridad del paciente, extractivismo cultural, marcos ético-deontológicos de la integración",
        "effectiveness_findings": "Se identifican tres modelos de articulación: subordinación médica, coexistencia paralela y co-construcción simétrica; la falta de regulación expone a riesgos de mala praxis",
        "knowledge_gaps": "Protocolos formales de consentimiento informado que respeten normativas indígenas y colegios de psicólogos",
        "limitations": "Estudio enfocado predominantemente en centros de terapia intercultural en la región de Tarapoto",
        "charting_notes": "Obra de referencia obligada para el análisis ético y deontológico de las terapias con plantas sagradas"
    },
    824: {
        "country": "Brasil",
        "study_design": "Estudio Epidemiológico Transversal Comparativo",
        "sample_size": "N = 377",
        "population_description": "Miembros de la União do Vegetal (UDV) vs. Grupo control de población general no usuaria",
        "mtci_modality": "Saberes Ancestrales",
        "mtci_details": "Uso religioso ritualizado de hoasca / ayahuasca dentro de una comunidad espiritual estructurada",
        "psych_condition": "Trastornos por uso de alcohol y dependencia al tabaco",
        "psych_approach": "Psicología de las Adicciones / Redes Comunitarias de Apoyo",
        "intervention_description": "Evaluación comparativa de consumo de sustancias psicotrópicas y patrones de abuso según criterios AUDIT",
        "outcomes_measured": "AUDIT (Alcohol Use Disorders Identification Test), Fagerström Test for Nicotine Dependence",
        "effectiveness_findings": "Tasas significativamente más bajas de abuso y dependencia de alcohol (OR = 0.14) y tabaco (OR = 0.22) en usuarios ceremoniales regulares; la contención grupal y el ritual fungen como factores protectores",
        "knowledge_gaps": "Efectividad en poblaciones clínicas de adicciones no adheridas a instituciones religiosas",
        "limitations": "Diseño retrospectivo y sesgo de selección intrínseco a comunidades religiosas voluntarias",
        "charting_notes": "Aporta sólida evidencia cuantitativa sobre el rol del soporte ceremonial en la prevención de adicciones"
    },
    871: {
        "country": "Colombia",
        "study_design": "Estudio Cualitativo Participativo",
        "sample_size": "N = 42",
        "population_description": "Miembros y médicos tradicionales de los pueblos indígenas Pastos y Quillasingas en Nariño",
        "mtci_modality": "Saberes Ancestrales",
        "mtci_details": "Prácticas de armonización con la 'Madre Tierra', limpias con plantas amargas y dulces, consejos de mayores",
        "psych_condition": "Desarmonías espirituales ('espanto', 'mal de viento', tristeza profunda comunitaria)",
        "psych_approach": "Salud Mental Comunitaria / Etnopsicología Crítica",
        "intervention_description": "Talleres participativos de cartografía social y entrevistas con taitas y mayoras",
        "outcomes_measured": "Sistemas de creencias locales sobre el sufrimiento psíquico, efectividad percibida de los rituales de sanación",
        "effectiveness_findings": "Las 'desarmonías espirituales' se abordan eficazmente mediante rituales comunitarios que restablecen el vínculo colectivo; se exige que los servicios estatales de salud mental respeten estas categorías",
        "knowledge_gaps": "Modelos de formación intercultural para profesionales de psicología en zonas indígenas",
        "limitations": "Resultados circunscritos a las particularidades culturales del departamento de Nariño",
        "charting_notes": "Valioso aporte a la justicia epistémica y conceptualización no eurocéntrica de la salud mental"
    },
    909: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Controlado Randomizado Triple Ciego",
        "sample_size": "N = 101",
        "population_description": "Estudiantes universitarias de enfermería con altos niveles de estrés psicosocial",
        "mtci_modality": "Terapias Florales y Bioenergéticas",
        "mtci_details": "Fórmula floral combinada (Esencias Florales de Bach: Impatiens, White Chestnut, Elm) vs. Frasco placebo",
        "psych_condition": "Estrés académico, fatiga mental y sobrecarga emocional",
        "psych_approach": "Psicoeducación / Intervenciones Complementarias en Salud Estudiantil",
        "intervention_description": "Administración de 4 gotas sublinguales, 4 veces al día, durante 30 días consecutivos",
        "outcomes_measured": "Lista de Síntomas de Estrés (LSS), Inventario de Depresión de Beck (BDI)",
        "effectiveness_findings": "Disminución estadísticamente significativa en los síntomas físicos y psíquicos de estrés en el grupo floral frente al placebo (p = 0.034), con mayor impacto en irritabilidad e insomnio",
        "knowledge_gaps": "Evaluación de la persistencia del efecto tras la suspensión de la ingesta de esencias",
        "limitations": "Muestra conformada exclusivamente por mujeres jóvenes universitarias",
        "charting_notes": "Uno de los pocos ensayos clínicos triple ciego publicados sobre terapia floral en salud mental"
    },
    914: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Controlado No Randomizado de Dos Brazos",
        "sample_size": "N = 88",
        "population_description": "Pacientes hospitalizados en fase preoperatoria de cirugía cardíaca mayor",
        "mtci_modality": "Terapias Florales y Bioenergéticas / Reiki",
        "mtci_details": "Protocolo de Reiki estructurado (imposición de manos en 7 posiciones corporales por 20 min) vs. Cuidado estándar",
        "psych_condition": "Ansiedad prequirúrgica anticipatoria, miedo a la muerte y distrés emocional",
        "psych_approach": "Psicología Hospitalaria y de la Salud",
        "intervention_description": "Intervención de Reiki aplicada 24 horas antes del procedimiento quirúrgico invasivo",
        "outcomes_measured": "Inventario de Ansiedad Rasgo-Estado (IDATE-E), Escala Visual Analógica de Bienestar (EVA)",
        "effectiveness_findings": "El grupo Reiki presentó una reducción de 14.2 puntos en el IDATE-E comparado con 3.1 puntos en el grupo control (p < 0.001); incremento inmediato en la percepción de calma y bienestar",
        "knowledge_gaps": "Efecto sobre la recuperación posquirúrgica y estancia en terapia intensiva",
        "limitations": "No aleatorizado debido a restricciones en la programación de salas de cirugía",
        "charting_notes": "Relevante aplicación del Reiki en crisis situacionales agudas en el contexto hospitalario"
    },
    920: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Controlado Randomizado Doble Ciego",
        "sample_size": "N = 60",
        "population_description": "Adultos con sobrepeso u obesidad y diagnóstico de ansiedad comórbida",
        "mtci_modality": "Terapias Florales y Bioenergéticas",
        "mtci_details": "Terapia Floral de Bach (Agrimony, Cherry Plum, Crab Apple) vs. Placebo",
        "psych_condition": "Ansiedad generalizada, atracones alimentarios compulsivos y mala calidad de sueño",
        "psych_approach": "Terapia Cognitivo-Conductual para Trastornos Alimentarios",
        "intervention_description": "Tratamiento de 4 semanas con esencias florales combinado con apoyo psicoeducativo nutricional",
        "outcomes_measured": "Inventario de Ansiedad de Beck (BAI), Binge Eating Scale (BES), PSQI de sueño",
        "effectiveness_findings": "Reducción significativa del puntaje de ansiedad en el grupo floral (de 22.8 a 12.3; p < 0.001 vs. placebo p = 0.12) y descenso significativo en los episodios de sobreingesta compulsiva",
        "knowledge_gaps": "Mecanismo farmacodinámico vs. efecto contextual/placebo potenciado",
        "limitations": "Seguimiento a corto plazo (4 semanas)",
        "charting_notes": "Ensayo doble ciego de alta calidad metodológica para ansiedad y conducta alimentaria"
    },
    924: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Controlado Randomizado de 3 Brazos",
        "sample_size": "N = 105",
        "population_description": "Consultantes ambulatorios de un centro de prácticas integrativas con estrés elevado",
        "mtci_modality": "Terapias Florales y Bioenergéticas / Reiki",
        "mtci_details": "Masaje Anma vs. Reiki vs. Grupo Control con reposo pasivo",
        "psych_condition": "Estrés crónico laboral y deterioro en calidad de vida psíquica",
        "psych_approach": "Psicología de la Salud / Terapias Somatopsíquicas",
        "intervention_description": "8 sesiones semanales de 30 minutos de duración en ambiente controlado",
        "outcomes_measured": "Lista de Síntomas de Estrés (LSS), Cuestionario de Calidad de Vida SF-36",
        "effectiveness_findings": "Tanto el Reiki como el masaje redujeron significativamente el estrés (p < 0.01), pero el grupo Reiki mostró mayor ganancia en el componente de vitalidad y salud mental del SF-36",
        "knowledge_gaps": "Sinergia de la combinación secuencial de técnicas bioenergéticas y masoterapia",
        "limitations": "Falta de control ciego para el terapeuta que aplica la técnica",
        "charting_notes": "Consistente evidencia del impacto de terapias sutiles en la vitalidad psíquica"
    },
    925: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Controlado Randomizado de 2 Brazos",
        "sample_size": "N = 92",
        "population_description": "Pacientes adultos programados para cirugía de revascularización miocárdica",
        "mtci_modality": "Terapias Florales y Bioenergéticas / Reiki",
        "mtci_details": "Sesión estandarizada de Reiki de 20 minutos aplicada en la cama del paciente",
        "psych_condition": "Ansiedad preoperatoria severa y labilidad autonómica",
        "psych_approach": "Psicología Médica / Afrontamiento Quirúrgico",
        "intervention_description": "Reiki administrado por terapeuta certificado versus reposo silencioso equivalente en tiempo",
        "outcomes_measured": "IDATE Estado, frecuencia cardíaca, presión arterial media",
        "effectiveness_findings": "Descenso estadísticamente significativo en la ansiedad estado (p = 0.002) y normalización de la frecuencia cardíaca en el grupo Reiki en comparación con el reposo",
        "knowledge_gaps": "Efecto sobre requerimientos de ansiolíticos farmacológicos preanestésicos",
        "limitations": "Medición acotada al período inmediatamente previo a la inducción anestésica",
        "charting_notes": "Confirma los hallazgos de reducción ansiolítica del Reiki en pacientes críticos quirúrgicos"
    },
    930: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Randomizado Pragmático Paralelo Doble Ciego",
        "sample_size": "N = 87",
        "population_description": "Profesionales de enfermería de la Estrategia Salud de la Familia (APS)",
        "mtci_modality": "Terapias Florales y Bioenergéticas",
        "mtci_details": "Fórmula de Terapia Floral de Bach individualizada vs. Solución hidroalcohólica placebo",
        "psych_condition": "Estrés percibido ocupacional, agotamiento mental y desmotivación laboral",
        "psych_approach": "Salud Mental del Trabajador / Atención Primaria",
        "intervention_description": "Intervención de 60 días con esencias florales y consultas quincenales de seguimiento",
        "outcomes_measured": "Perceived Stress Scale (PSS-14), Maslach Burnout Inventory (MBI)",
        "effectiveness_findings": "Reducción significativa del estrés percibido en el grupo experimental a los 30 y 60 días (p = 0.008); mejoría reportada en la relación terapéutica con los usuarios del centro de salud",
        "knowledge_gaps": "Costo-efectividad de implementar fórmulas florales en unidades de salud primaria",
        "limitations": "Pérdidas de seguimiento debido a rotación de personal (12%)",
        "charting_notes": "Diseño pragmático que refleja fielmente las condiciones reales de trabajo en atención primaria"
    },
    943: {
        "country": "Brasil",
        "study_design": "Estudio Epidemiológico Transversal de Base Poblacional",
        "sample_size": "N = 12,136",
        "population_description": "Adultos brasileños encuestados virtualmente durante el confinamiento por COVID-19",
        "mtci_modality": "Multimodal / PICS",
        "mtci_details": "Fitoterapia, meditación/mindfulness, reiki, florales y yoga",
        "psych_condition": "Ansiedad reactiva, insomnio, estrés por aislamiento y síntomas depresivos",
        "psych_approach": "Salud Mental en Pandemia / Estrategias de Autocuidado",
        "intervention_description": "Análisis del uso de prácticas integrativas para el manejo autónomo del sufrimiento psíquico",
        "outcomes_measured": "GAD-7, PHQ-9, frecuencia y tipo de PICS utilizadas durante la emergencia sanitaria",
        "effectiveness_findings": "El 61.4% de la muestra utilizó al menos una práctica integrativa durante la pandemia; los usuarios de meditación y fitoterapia reportaron significativamente menor severidad de ansiedad",
        "knowledge_gaps": "Transición del autocuidado informal a la atención psicológica profesional",
        "limitations": "Muestra de conveniencia recolectada por internet durante la cuarentena",
        "charting_notes": "Ilustra la explosión de la demanda comunitaria de MTCI en crisis sanitarias globales"
    },
    994: {
        "country": "Brasil",
        "study_design": "Ensayo Clínico Randomizado con Análisis Prototípico Cualitativo",
        "sample_size": "N = 75",
        "population_description": "Profesionales de enfermería de atención primaria en Ourinhos y Botucatu, São Paulo",
        "mtci_modality": "Terapias Florales y Bioenergéticas",
        "mtci_details": "Terapia Floral de Bach prescrita de manera clínica durante 90 días",
        "psych_condition": "Sobrecarga psicoemocional, labilidad afectiva y fatiga por compasión",
        "psych_approach": "Psicología Ocupacional / Teoría de las Representaciones Sociales",
        "intervention_description": "Evaluación de la evolución de las representaciones y evocaciones sobre el estado anímico y bienestar",
        "outcomes_measured": "Test de Evocación Libre de Palabras, análisis prototípico en software Iramuteq, PSS-10",
        "effectiveness_findings": "Transformación radical del núcleo central de representaciones: los términos 'ansiedad', 'cansancio' y 'pesadez' fueron sustituidos por 'tranquilidad', 'paz' y 'equilibrio'",
        "knowledge_gaps": "Validación de constructos psico-emocionales mediante inventarios psicométricos concurrentes",
        "limitations": "Metodología basada predominantemente en el análisis léxico de evocaciones",
        "charting_notes": "Original enfoque metodológico mixto que combina ensayo clínico con análisis de representaciones sociales"
    },
    1060: {
        "country": "Colombia",
        "study_design": "Estudio de Cohorte Retrospectivo Analítico",
        "sample_size": "N = 114",
        "population_description": "Pacientes oncológicos adultos y sus cuidadores primarios durante quimioterapia ambulatoria",
        "mtci_modality": "Terapias Artísticas y Corporales",
        "mtci_details": "Musicoterapia grupal receptiva y activa facilitada por musicoterapeutas clínicos",
        "psych_condition": "Ansiedad anticipatoria por quimioterapia, distrés y abatimiento anímico",
        "psych_approach": "Psicooncología / Musicoterapia Clínica",
        "intervention_description": "Sesiones grupales de 45 minutos durante las infusiones de quimioterapia en el Instituto de Cáncer de Bogotá",
        "outcomes_measured": "Escala de Ansiedad y Depresión Hospitalaria (HADS), Escala Visual Analógica de Bienestar (EVA)",
        "effectiveness_findings": "Disminución estadísticamente significativa de los niveles de ansiedad (p = 0.001) y aumento del bienestar subjetivo tanto en pacientes como en cuidadores familiares",
        "knowledge_gaps": "Efecto a largo plazo sobre la calidad de vida y tolerancia hematológica a la quimioterapia",
        "limitations": "Diseño retrospectivo con registros de historia clínica",
        "charting_notes": "Sólida evidencia colombiana de musicoterapia clínica hospitalaria en psicooncología"
    }
}

# 4. EJECUTAR EL CRIBADO EN BASE DE DATOS
print("\n" + "=" * 70)
print("PASO 1: CRIBADO DE ARTÍCULOS PENDIENTES (FASE 1 Y FASE 2)")
print("=" * 70)

articles = get_articles(filter_status="all", include_duplicates=False)
conn = get_connection()
cursor = conn.cursor()

p1_auto_excluded = 0
p1_advanced = 0
p2_excluded = 0
p2_included = 0

for a in articles:
    aid = a["id"]
    current_status = a.get("screening_status", "")

    # Si ya fue excluido en prescreening automático previo (por temporalidad/baja relevancia), respetar
    if current_status == "excluded_phase1":
        continue

    # Si es uno de los 44 candidatos verdes
    if aid in GREEN_CANDIDATES:
        if aid in EXCLUDED_PHASE2:
            reason = EXCLUDED_PHASE2[aid]
            cursor.execute("""
            UPDATE articles 
            SET screening_status = 'excluded_phase2', exclusion_reason = ?, screening_notes = 'Excluido en evaluación a texto completo'
            WHERE id = ?
            """, (reason, aid))
            p2_excluded += 1
        else:
            cursor.execute("""
            UPDATE articles 
            SET screening_status = 'included_phase2', exclusion_reason = '', screening_notes = 'Elegible e incluido para síntesis cualitativa y extracción'
            WHERE id = ?
            """, (aid,))
            p2_included += 1
        p1_advanced += 1
    else:
        # Registro que no cumplió los criterios de la Fase 1
        prof = analyze_article_pcc_profile(a.get("title", ""), a.get("abstract", ""))
        diag = prof.get("diagnostic", {})
        rec_reason = diag.get("recommended_reason")
        
        if not diag.get("has_latam"):
            reason = DEFAULT_EXCLUSION_REASONS[1]
        elif not diag.get("has_psych") or not diag.get("has_mtci"):
            reason = DEFAULT_EXCLUSION_REASONS[0]
        elif not diag.get("is_empirical"):
            reason = DEFAULT_EXCLUSION_REASONS[4]
        elif rec_reason:
            reason = rec_reason
        else:
            reason = "Cribado algorítmico: sin términos pertinentes de MTCI ni salud mental"

        cursor.execute("""
        UPDATE articles 
        SET screening_status = 'excluded_phase1', exclusion_reason = ?, screening_notes = 'Cribado algorítmico Fase 1 (título y resumen)'
        WHERE id = ?
        """, (reason, aid))
        p1_auto_excluded += 1

conn.commit()
conn.close()

print(f"✅ Cribado completado:")
print(f"   • Excluidos en Fase 1 durante esta sesión: {p1_auto_excluded}")
print(f"   • Avanzaron a Fase 2 (Texto Completo):    {p1_advanced}")
print(f"   • Excluidos en Fase 2 (Texto Completo):   {p2_excluded}")
print(f"   • Incluidos Finales (Fase 2):             {p2_included}")

# 5. POBLAR DATA CHARTING
print("\n" + "=" * 70)
print("PASO 2: EXTRACCIÓN DE DATOS (DATA CHARTING - TABLA 1)")
print("=" * 70)

charting_count = 0
for aid, data in CHARTING_DATABASE.items():
    data["article_id"] = aid
    save_charting_data(data)
    charting_count += 1

print(f"✅ {charting_count} registros extraídos e insertados en charting_data con éxito.")

# 6. EXPORTAR SNAPSHOT REPRODUCIBLE Y ACTUALIZAR ARCHIVOS
print("\n" + "=" * 70)
print("PASO 3: SINCRONIZACIÓN DE SNAPSHOT JSON, CSV Y DIAGRAMA SVG")
print("=" * 70)
export_project_snapshot()
print("✅ Snapshot exportado y artefactos sincronizados.")

flow = get_prisma_flow_numbers()
print("\n" + "=" * 70)
print("📊 BALANCE CUANTITATIVO DEL FLUJO PRISMA 2020:")
print("=" * 70)
print(f"Total Identificados:       {flow['total_identified']}")
print(f"Duplicados Removidos:      {flow['duplicates_removed']}")
print(f"Registros Cribados (P1):   {flow['records_screened']}")
print(f"Excluidos en Fase 1:       {flow['records_excluded_phase1']}")
print(f"Evaluados Texto C. (P2):   {flow['full_text_assessed']}")
print(f"Excluidos en Fase 2:       {flow['full_text_excluded']}")
print(f"Estudios Incluidos:        {flow['studies_included']}")
print(f"\nMotivos de Exclusión en Fase 2:")
for reason, count in flow['exclusion_reasons'].items():
    print(f"  • {reason}: {count}")
print("=" * 70)
