#!/usr/bin/env python3
"""
tools/build_animated_deck.py
================================================================================
Generador de Presentación Interactiva y Animada en HTML5/CSS3/JavaScript:
`presentacion_tesis_mtci_animated.html`
- Estilo: Minimalista, Creativo, Moderno, Editorial y Libre de Cajas
- Animaciones: Transiciones cinemáticas, kinetic typography, contadores animados (0% -> 89.7%)
- Gráficos SVG animados en vivo y síntesis de audio sutil (Web Audio API)
- Modo Presentador con notas de oratoria (tecla N o P), vista de cuadrícula (tecla T)
- Atajos: Flechas, Espacio, F (Pantalla Completa), N (Notas), T (Miniaturas)
================================================================================
"""

import os

HTML_OUTPUT = "presentacion_tesis_mtci_animated.html"

SLIDES_DATA = [
    {
        "id": "slide-01",
        "category": "Defensa de Tesis de Licenciatura en Psicología",
        "title": "La Medicina Tradicional, Complementaria e Integrativa (MTCI) como Complemento en la Atención Psicológica",
        "subtitle": "Estudio Mixto con Estudiantes y Docentes del CUR-Estelí y Facilitadores Locales del Municipio de Estelí (Segundo Semestre, 2026)",
        "notes": "Pausa inicial. Saludar con solemnidad al Honorable Tribunal Examinador. Enfatizar la relevancia histórica de este estudio como el primero en articular a la academia con los saberes territoriales de Estelí.",
        "type": "cover"
    },
    {
        "id": "slide-02",
        "category": "Capítulo I • Planteamiento del Problema",
        "title": "Encrucijada Asistencial, Vacío Formativo y Pertinencia Social",
        "notes": "Destacar la tensión jurídica fundamental: la Ley 774 otorga el derecho a la MTCI pero la Ley 292 restringe tajantemente al psicólogo prescribir. Explicar el fenómeno del ocultamiento terapéutico.",
        "type": "two_col_problem"
    },
    {
        "id": "slide-03",
        "category": "Capítulo I • Estado del Arte",
        "title": "Trayectoria de la Evidencia Internacional, Regional y Local",
        "notes": "Mostrar la línea de tiempo. Citar los metanálisis de la OMS (2025), Furlan (2012) y Guo (2024), enlazando con la paradoja detectada en Iberoamérica y el vacío investigativo en Nicaragua.",
        "type": "timeline"
    },
    {
        "id": "slide-04",
        "category": "Capítulo I • Contextualización Situacional",
        "title": "El Escenario de Investigación: CUR-Estelí y el Territorio Segoviano",
        "notes": "Contextualizar a Estelí como territorio de sabiduría etnobotánica viva, y al CUR-Estelí y su Clínica Psicosocial como el espacio idóneo para implementar pautas formativas de diálogo intercultural.",
        "type": "context"
    },
    {
        "id": "slide-05",
        "category": "Capítulo I • Propósito Investigativo",
        "title": "Objetivos de la Investigación: Del Diagnóstico a la Propuesta",
        "notes": "Leer con precisión el Objetivo General y articular cómo cada uno de los 3 Objetivos Específicos responde secuencialmente: OE1 a estudiantes, OE2 a facilitadores y OE3 a la propuesta del manual.",
        "type": "objectives"
    },
    {
        "id": "slide-06",
        "category": "Capítulo II • Fundamentos Teóricos (1/2)",
        "title": "Epistemología Médica, Pluralismo Asistencial y Principios Bioéticos",
        "notes": "Fundamentar en el Modelo Biopsicosocial de Engel (1977), el Pluralismo Médico de Eduardo Menéndez y la Bioética Principialista de Beauchamp y Childress (No Maleficencia y Autonomía).",
        "type": "three_pillars"
    },
    {
        "id": "slide-07",
        "category": "Capítulo II • Fundamentos Teóricos (2/2)",
        "title": "Marco Jurídico Nicaragüense y Evidencia de Eficacia Clínica",
        "notes": "Profundizar en la Ley 774, Ley 292 y Ley 759. Presentar la evidencia neurobiológica de la fitoterapia gabaérgica y la regulación autonómica vagal mediante técnicas mente-cuerpo.",
        "type": "two_col_legal_clinical"
    },
    {
        "id": "slide-08",
        "category": "Capítulo III • Diseño Metodológico (1/2)",
        "title": "Paradigma Pragmático, Enfoque Mixto Secuencial y Fases del Estudio",
        "notes": "Definir el diseño DEXPLIS (Derivativo Secuencial): Fase cuantitativa censal -> Fase cualitativa en profundidad -> Fase propositiva de formulación del manual.",
        "type": "methodology_phases"
    },
    {
        "id": "slide-09",
        "category": "Capítulo III • Diseño Metodológico (2/2)",
        "title": "Delimitación Muestral Consolidada (N = 86) y Criterios de Selección",
        "notes": "Explicar con exactitud la muestra consolidada de N=86: 68 estudiantes censados (4.° y 5.° año), 9 facilitadores locales de Estelí y 9 docentes de psicología. Resaltar la rigurosidad de inclusión.",
        "type": "sample_groups"
    },
    {
        "id": "slide-10",
        "category": "Capítulo IV • Resultados Empíricos (1/4)",
        "title": "Perfil Sociodemográfico y Formativo del Estudiantado (n = 68)",
        "notes": "Analizar la marcada feminización de la carrera (82.4%), la concentración de jóvenes adultos (21-25 años) y el momento crítico del 4.° año enfrentando la Clínica Psicosocial.",
        "type": "demographics_viz"
    },
    {
        "id": "slide-11",
        "category": "Capítulo IV • Resultados Empíricos (2/4)",
        "title": "La Paradoja Formativa: Alta Pertinencia frente al Desamparo Curricular (OE1)",
        "notes": "Momento culminante de la defensa: 89.7% considera urgente integrar MTCI, pero 88.2% no recibió preparación alguna. 86.7% reporta alivio somático directo y 0.0% efectos adversos.",
        "type": "stats_paradox"
    },
    {
        "id": "slide-12",
        "category": "Capítulo IV • Resultados Empíricos (3/4)",
        "title": "Perspectiva de Facilitadores Locales de Estelí y Claustro Docente",
        "notes": "Contrastar el 100% de eficacia somática percibida por facilitadores con el 100% de respaldo curricular del claustro docente bajo pedagogía activa y comités de bioética.",
        "type": "facilitators_teachers"
    },
    {
        "id": "slide-13",
        "category": "Capítulo V • Propuesta Operativa (OE3)",
        "title": "Manual de Estrategias de MTCI para la Formación y Práctica Psicológica",
        "notes": "Presentar formalmente el Manual de 18 páginas (Anexo 16.2), sus 8 módulos formativos, el algoritmo de derivación clínica de 4 pasos y la adaptación del cuestionario I-CAM-Q para Nicaragua.",
        "type": "manual_proposal"
    },
    {
        "id": "slide-14",
        "category": "Capítulo VI • Síntesis Conclusiva",
        "title": "Conclusiones Centrales de la Investigación (Triangulación de Objetivos)",
        "notes": "Sintetizar las 5 conclusiones centrales: cumplimiento del Objetivo General, caracterización de la paradoja, resiliencia territorial, consenso docente y entrega del manual propositivo.",
        "type": "conclusions"
    },
    {
        "id": "slide-15",
        "category": "Capítulo VI • Directrices Prospectivas",
        "title": "Recomendaciones Estratégicas para Estudiantes, Docentes, Universidad y MINSA",
        "notes": "Detallar las pautas operativas para cada uno de los 4 sectores. Enfatizar la adopción oficial del manual por el CUR-Estelí y los convenios interinstitucionales con el MINSA.",
        "type": "recommendations"
    },
    {
        "id": "slide-16",
        "category": "Cierre Institucional",
        "title": "«¡A la libertad por la Universidad!» — Muchas Gracias por su Atención",
        "notes": "Agradecer al tribunal evaluador, a los facilitadores de Estelí y a la UNAN-Managua. Abrir formalmente el espacio para preguntas y réplica académica.",
        "type": "closing"
    }
]

HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Defensa de Tesis: MTCI en Psicología · UNAN-Managua CUR-Estelí</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400&family=Cinzel:wght@600;700&display=swap" rel="stylesheet">
  
  <style>
    /* ==========================================================================
       MODERN MINIMALIST EDITORIAL DESIGN SYSTEM (No-Box Aesthetics)
       ========================================================================== */
    :root {
      --bg-dark: #070B14;
      --bg-dark-surface: #0C1322;
      --bg-light: #FBFDFE;
      --bg-light-surface: #F1F5F9;
      
      --text-main: #0F172A;
      --text-muted: #64748B;
      --text-light: #F8FAFC;
      --text-light-muted: #94A3B8;
      
      --teal-primary: #0D9488;
      --teal-glow: rgba(13, 148, 136, 0.25);
      --gold-primary: #F59E0B;
      --gold-glow: rgba(245, 158, 11, 0.25);
      --alert-crimson: #DC2626;
      --blue-royal: #2563EB;
      --hairline: rgba(226, 232, 240, 0.85);
      --hairline-dark: rgba(30, 41, 59, 0.85);

      --font-serif: 'Playfair Display', Georgia, 'Times New Roman', serif;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-display: 'Cinzel', serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: #030712;
      font-family: var(--font-sans);
      color: var(--text-main);
      overflow: hidden;
      height: 100vh;
      width: 100vw;
      display: flex;
      align-items: center;
      justify-content: center;
      user-select: none;
    }

    /* Screen Container (Fixed 16:9 Aspect Ratio) */
    #viewport {
      position: relative;
      width: 100vw;
      height: 56.25vw; /* 16:9 */
      max-height: 100vh;
      max-width: 177.78vh; /* 16:9 */
      background: var(--bg-light);
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.6);
      overflow: hidden;
      border-radius: 4px;
    }

    /* Background Ambient Canvas Glow */
    .ambient-glow {
      position: absolute;
      top: -20%;
      right: -10%;
      width: 60%;
      height: 60%;
      background: radial-gradient(circle, rgba(13, 148, 136, 0.08) 0%, transparent 70%);
      pointer-events: none;
      z-index: 1;
    }

    /* Slides Container */
    .deck-container {
      position: relative;
      width: 100%;
      height: 100%;
      z-index: 2;
    }

    .slide {
      position: absolute;
      inset: 0;
      padding: 3.8vw 5.2vw 4.0vw 5.2vw;
      display: flex;
      flex-direction: column;
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
      transition: opacity 0.65s cubic-bezier(0.16, 1, 0.3, 1), transform 0.65s cubic-bezier(0.16, 1, 0.3, 1);
      transform: scale(0.985) translateY(12px);
    }

    .slide.active {
      opacity: 1;
      visibility: visible;
      pointer-events: auto;
      transform: scale(1) translateY(0);
    }

    /* Dark Mode Slides (Slides 1 & 16) */
    .slide.theme-dark {
      background: var(--bg-dark);
      color: var(--text-light);
    }

    /* Editorial Header */
    .slide-header {
      position: relative;
      margin-bottom: 2.2vw;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }

    .header-text {
      max-width: 82%;
    }

    .eyebrow {
      font-size: 0.82vw;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--teal-primary);
      margin-bottom: 0.4vw;
      display: flex;
      align-items: center;
      gap: 0.5vw;
    }

    .slide.theme-dark .eyebrow {
      color: #2DD4BF;
    }

    .slide-title {
      font-family: var(--font-serif);
      font-size: 2.1vw;
      font-weight: 700;
      line-height: 1.22;
      color: var(--text-main);
    }

    .slide.theme-dark .slide-title {
      color: #FFFFFF;
    }

    .shield-badge img {
      height: 4.0vw;
      object-fit: contain;
      filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
    }

    /* Slide Content Canvas (Minimalist, No Cards) */
    .slide-content {
      flex: 1;
      display: flex;
      position: relative;
    }

    /* Column Layouts */
    .col-split {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4.0vw;
      width: 100%;
    }

    .col-split-asym {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 4.0vw;
      width: 100%;
    }

    .col-three {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 3.2vw;
      width: 100%;
    }

    .col-four {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr;
      gap: 2.2vw;
      width: 100%;
    }

    /* Editorial Hairlines */
    .v-divider {
      position: absolute;
      top: 0;
      bottom: 0;
      left: 50%;
      width: 1px;
      background: var(--hairline);
    }

    /* Kinetic Stagger Animations */
    .reveal-item {
      opacity: 0;
      transform: translateY(18px);
      transition: opacity 0.55s cubic-bezier(0.16, 1, 0.3, 1), transform 0.55s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .slide.active .reveal-item:nth-child(1) { transition-delay: 0.12s; opacity: 1; transform: translateY(0); }
    .slide.active .reveal-item:nth-child(2) { transition-delay: 0.22s; opacity: 1; transform: translateY(0); }
    .slide.active .reveal-item:nth-child(3) { transition-delay: 0.32s; opacity: 1; transform: translateY(0); }
    .slide.active .reveal-item:nth-child(4) { transition-delay: 0.42s; opacity: 1; transform: translateY(0); }
    .slide.active .reveal-item:nth-child(5) { transition-delay: 0.52s; opacity: 1; transform: translateY(0); }

    /* Number Callouts (Sculptural Stats) */
    .stat-hero {
      display: flex;
      flex-direction: column;
      margin-bottom: 1.6vw;
    }

    .stat-hero .number {
      font-family: var(--font-serif);
      font-size: 3.6vw;
      font-weight: 700;
      line-height: 1;
      color: var(--teal-primary);
      margin-bottom: 0.3vw;
    }

    .stat-hero .number.crimson { color: var(--alert-crimson); }
    .stat-hero .number.gold { color: var(--gold-primary); }
    .stat-hero .number.royal { color: var(--blue-royal); }

    .stat-hero .label {
      font-size: 0.95vw;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 0.2vw;
    }

    .stat-hero .desc {
      font-size: 0.85vw;
      color: var(--text-muted);
      line-height: 1.4;
    }

    /* Typography Details */
    .point-item {
      margin-bottom: 1.2vw;
      line-height: 1.48;
    }

    .point-num {
      font-family: var(--font-serif);
      font-size: 1.1vw;
      font-weight: 700;
      color: var(--teal-primary);
      margin-right: 0.4vw;
    }

    .point-head {
      font-size: 0.95vw;
      font-weight: 700;
      color: var(--text-main);
    }

    .point-body {
      font-size: 0.88vw;
      color: var(--text-muted);
    }

    /* Minimalist HUD / Footer Navigation */
    .deck-hud {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 3.2vw;
      padding: 0 5.2vw;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 100;
      border-top: 1px solid rgba(226, 232, 240, 0.6);
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(8px);
    }

    .slide.theme-dark ~ .deck-hud,
    #viewport.hud-dark .deck-hud {
      background: rgba(7, 11, 20, 0.9);
      border-top: 1px solid rgba(30, 41, 59, 0.8);
      color: var(--text-light-muted);
    }

    .hud-left {
      font-size: 0.75vw;
      color: var(--text-muted);
      font-weight: 500;
    }

    .slide.theme-dark ~ .deck-hud .hud-left,
    #viewport.hud-dark .deck-hud .hud-left {
      color: var(--text-light-muted);
    }

    .hud-controls {
      display: flex;
      align-items: center;
      gap: 1.2vw;
    }

    .btn-hud {
      background: none;
      border: none;
      color: inherit;
      cursor: pointer;
      font-size: 0.85vw;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.4vw;
      padding: 0.3vw 0.6vw;
      border-radius: 4px;
      transition: all 0.2s ease;
    }

    .btn-hud:hover {
      color: var(--teal-primary);
      background: rgba(13, 148, 136, 0.08);
    }

    .slide-counter {
      font-size: 0.82vw;
      font-weight: 700;
      letter-spacing: 0.05em;
      min-width: 4.5vw;
      text-align: center;
    }

    /* Minimal Progress Line */
    .progress-bar-wrap {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 2px;
      background: rgba(226, 232, 240, 0.4);
    }

    .progress-bar {
      height: 100%;
      width: 6.25%;
      background: linear-gradient(90deg, var(--teal-primary), var(--gold-primary));
      transition: width 0.35s ease;
    }

    /* Speaker Notes Drawer */
    #notes-drawer {
      position: absolute;
      bottom: 3.2vw;
      left: 5.2vw;
      right: 5.2vw;
      background: rgba(15, 23, 42, 0.96);
      color: #F8FAFC;
      border-radius: 8px 8px 0 0;
      padding: 1.5vw 2.0vw;
      z-index: 150;
      box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.5);
      border: 1px solid rgba(51, 65, 85, 0.8);
      transform: translateY(110%);
      transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }

    #notes-drawer.open {
      transform: translateY(0);
    }

    .notes-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.8vw;
      font-size: 0.8vw;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--gold-primary);
      font-weight: 700;
    }

    .notes-content {
      font-size: 0.95vw;
      line-height: 1.6;
      color: #E2E8F0;
    }

    /* Thumbnail Overview Modal */
    #thumb-modal {
      position: absolute;
      inset: 0;
      background: rgba(7, 11, 20, 0.95);
      backdrop-filter: blur(12px);
      z-index: 200;
      padding: 3vw 5vw;
      display: none;
      flex-direction: column;
      overflow-y: auto;
    }

    #thumb-modal.open {
      display: flex;
    }

    .thumb-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1.5vw;
      margin-top: 1.5vw;
    }

    .thumb-card {
      background: #0F172A;
      border: 1px solid #1E293B;
      border-radius: 6px;
      padding: 1.0vw;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 0.4vw;
    }

    .thumb-card:hover, .thumb-card.active {
      border-color: var(--teal-primary);
      transform: translateY(-3px);
      box-shadow: 0 8px 20px rgba(13, 148, 136, 0.3);
    }

    .thumb-num {
      font-size: 0.75vw;
      font-weight: 700;
      color: var(--teal-primary);
    }

    .thumb-title {
      font-size: 0.85vw;
      font-weight: 600;
      color: #FFFFFF;
      line-height: 1.3;
    }

    /* Embedded Figure and Cover Images */
    .fig-frame {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .fig-frame img {
      max-width: 100%;
      max-height: 25vw;
      object-fit: contain;
      filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.08));
    }
  </style>
</head>
<body>

  <div id="viewport">
    <div class="ambient-glow"></div>

    <div class="deck-container" id="deck">

      <!-- SLIDE 1: PORTADA INSTITUCIONAL (DARK MINIMALIST) -->
      <section class="slide theme-dark active" id="slide-01">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2.5vw; border-bottom: 1px solid var(--hairline-dark); padding-bottom: 1.2vw;">
          <div style="display: flex; align-items: center; gap: 1.5vw;">
            <img src="assets/extracted/unan_logo_clean.png" alt="UNAN Managua" style="height: 4.8vw; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));">
            <div>
              <div style="font-size: 1.05vw; font-weight: 700; letter-spacing: 0.04em; color: #FFFFFF;">UNIVERSIDAD NACIONAL AUTÓNOMA DE NICARAGUA, MANAGUA</div>
              <div style="font-size: 0.82vw; font-weight: 700; color: var(--gold-primary); margin-top: 0.2vw;">CENTRO UNIVERSITARIO REGIONAL DE ESTELÍ • RECINTO LEONEL RUGAMA RUGAMA</div>
              <div style="font-size: 0.75vw; color: var(--text-light-muted); margin-top: 0.1vw;">Departamento de Educación y Humanidades | Carrera de Psicología</div>
            </div>
          </div>
          <div style="text-align: right;">
            <span style="font-size: 0.75vw; font-weight: 700; letter-spacing: 0.1em; color: var(--teal-primary); text-transform: uppercase;">Defensa Oral de Grado</span>
            <div style="font-size: 0.85vw; color: #FFFFFF; font-weight: 600;">Octubre, 2026</div>
          </div>
        </div>

        <div style="margin-top: 1.0vw; margin-bottom: 3.0vw;">
          <div class="eyebrow" style="color: #2DD4BF; margin-bottom: 0.8vw;">TRABAJO DE INVESTIGACIÓN PARA OPTAR AL GRADO DE LICENCIADOS EN PSICOLOGÍA</div>
          <h1 style="font-family: var(--font-serif); font-size: 2.7vw; line-height: 1.18; color: #FFFFFF; max-width: 95%; margin-bottom: 1.0vw;">
            La Medicina Tradicional, Complementaria e Integrativa (MTCI) como Complemento en la Atención Psicológica
          </h1>
          <p style="font-size: 1.15vw; color: #E2E8F0; font-weight: 400; max-width: 90%;">
            Estudio Mixto con Estudiantes y Docentes del CUR-Estelí y Facilitadores Locales del Municipio de Estelí
          </p>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 3.0vw; border-top: 1px solid var(--hairline-dark); padding-top: 1.8vw;">
          <div>
            <div style="font-size: 0.78vw; font-weight: 700; letter-spacing: 0.1em; color: var(--gold-primary); text-transform: uppercase; margin-bottom: 0.5vw;">Autores / Sustentantes</div>
            <div style="font-size: 0.9vw; line-height: 1.6; color: #FFFFFF;">
              <div>• Dina Fabiola García Torres</div>
              <div>• Tatiana Paola López Ramos</div>
              <div>• Engel Enoc Zamora Velásquez</div>
            </div>
          </div>

          <div>
            <div style="font-size: 0.78vw; font-weight: 700; letter-spacing: 0.1em; color: #2DD4BF; text-transform: uppercase; margin-bottom: 0.5vw;">Tutoría Académica</div>
            <div style="font-size: 0.9vw; font-weight: 600; color: #FFFFFF;">Dra. Tania Libertad Pérez Guevara</div>
            <div style="font-size: 0.78vw; color: var(--text-light-muted); margin-top: 0.2vw;">Docente Investigadora • CUR-Estelí<br>Asesoría Temática y Metodológica</div>
          </div>

          <div>
            <div style="font-size: 0.78vw; font-weight: 700; letter-spacing: 0.1em; color: #E2E8F0; text-transform: uppercase; margin-bottom: 0.5vw;">Coordenadas Institucionales</div>
            <div style="font-size: 0.9vw; color: #FFFFFF;">Licenciatura en Psicología</div>
            <div style="font-size: 0.78vw; color: var(--text-light-muted); margin-top: 0.2vw;">Línea de Investigación SAL-3 (Salud e Interculturalidad)<br>Estelí, Nicaragua</div>
          </div>
        </div>
      </section>

      <!-- SLIDE 2: PLANTEAMIENTO DEL PROBLEMA Y JUSTIFICACIÓN -->
      <section class="slide" id="slide-02">
        <div class="slide-header">
          <div class="header-text">
            <div class="eyebrow">Capítulo I • Planteamiento del Problema</div>
            <h2 class="slide-title">Encrucijada Asistencial, Vacío Formativo y Pertinencia Social</h2>
          </div>
          <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
        </div>

        <div class="slide-content">
          <div class="col-split">
            <!-- Columna 1: Problema -->
            <div class="reveal-item">
              <h3 style="font-family: var(--font-serif); font-size: 1.25vw; color: var(--text-main); margin-bottom: 1.2vw;">El Conflicto Estructural en Salud Mental</h3>
              <div class="point-item">
                <span class="point-num">01</span>
                <span class="point-head">Asimetría Normativa:</span>
                <span class="point-body">La Ley 774 garantiza el acceso ciudadano a las MTCI, mientras la Ley 292 prohíbe tajantemente a psicólogos prescribir fármacos.</span>
              </div>
              <div class="point-item">
                <span class="point-num">02</span>
                <span class="point-head">El Ocultamiento Terapéutico:</span>
                <span class="point-body">Los consultantes recurren a la medicina natural pero la silencian en sesión clínica por temor al reproche o escepticismo del terapeuta.</span>
              </div>
              <div class="point-item">
                <span class="point-num">03</span>
                <span class="point-head">Vacío Curricular Crítico:</span>
                <span class="point-body">Los futuros graduados egresan sin pautas bioéticas para dialogar, psicoeducar o realizar derivaciones oportunas.</span>
              </div>
              <div style="margin-top: 1.8vw; padding-left: 1.0vw; border-left: 2px solid var(--gold-primary);">
                <div style="font-size: 0.8vw; font-weight: 700; color: var(--gold-primary); text-transform: uppercase;">Pregunta de Investigación</div>
                <div style="font-size: 0.95vw; font-style: italic; color: var(--text-main); margin-top: 0.2vw;">
                  ¿Cómo fundamenta el diagnóstico de MTCI en Estelí el diseño de un manual ético y pedagógico para Psicología?
                </div>
              </div>
            </div>

            <!-- Columna 2: Justificación -->
            <div class="reveal-item">
              <h3 style="font-family: var(--font-serif); font-size: 1.25vw; color: var(--text-main); margin-bottom: 1.2vw;">Justificación y Relevancia Social</h3>
              <div class="point-item">
                <span class="point-num" style="color: var(--teal-primary);">✦</span>
                <span class="point-head">Ética y No Maleficencia:</span>
                <span class="point-body">Conocer qué hierbas o remedios usa el consultante previene interacciones fitofarmacológicas y protege la seguridad clínica.</span>
              </div>
              <div class="point-item">
                <span class="point-num" style="color: var(--teal-primary);">✦</span>
                <span class="point-head">Salud Mental Comunitaria:</span>
                <span class="point-body">Reconoce y articula la memoria etnobotánica viva y dignifica el rol histórico de los facilitadores locales de Estelí.</span>
              </div>
              <div class="point-item">
                <span class="point-num" style="color: var(--teal-primary);">✦</span>
                <span class="point-head">Impacto Formativo Directo:</span>
                <span class="point-body">Dota a los estudiantes de 4.º y 5.º año de criterios de discernimiento para sus prácticas en la Clínica Psicosocial del CUR-Estelí.</span>
              </div>
              <div class="point-item">
                <span class="point-num" style="color: var(--teal-primary);">✦</span>
                <span class="point-head">Aporte Propositivo Concreto:</span>
                <span class="point-body">Formaliza el primer Manual de Estrategias MTCI (18 págs., Anexo 16.2) como guía pedagógica y bioética institucional.</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- SLIDE 3: ANTECEDENTES (TIMELINE HORIZONTAL) -->
      <section class="slide" id="slide-03">
        <div class="slide-header">
          <div class="header-text">
            <div class="eyebrow">Capítulo I • Estado del Arte</div>
            <h2 class="slide-title">Trayectoria de la Evidencia Internacional, Regional y Local</h2>
          </div>
          <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
        </div>

        <div class="slide-content">
          <div class="col-three" style="position: relative;">
            <div class="reveal-item">
              <div style="font-size: 1.4vw; font-family: var(--font-serif); font-weight: 700; color: var(--teal-primary); margin-bottom: 0.3vw;">2014 – 2019</div>
              <div style="font-size: 0.8vw; font-weight: 700; color: var(--text-main); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.0vw;">Ámbito Global • Directrices OMS</div>
              <p class="point-body" style="margin-bottom: 0.8vw;">• <b>Estrategia OMS MTCI:</b> Marco global que insta a los sistemas de salud a integrar medicinas tradicionales con base en evidencia.</p>
              <p class="point-body" style="margin-bottom: 0.8vw;">• <b>Metanálisis Clínicos:</b> Furlan et al. (2012) y Guo et al. (2024) comprueban eficacia en dolor crónico, fibromialgia y estrés somático.</p>
              <p class="point-body">• <b>Salud Mental Global:</b> Sotiropoulos et al. (2025) validan técnicas mente-cuerpo en comorbilidades afectivas.</p>
            </div>

            <div class="reveal-item">
              <div style="font-size: 1.4vw; font-family: var(--font-serif); font-weight: 700; color: var(--gold-primary); margin-bottom: 0.3vw;">2020 – 2023</div>
              <div style="font-size: 0.8vw; font-weight: 700; color: var(--text-main); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.0vw;">Ámbito Regional • Paradoja Universitaria</div>
              <p class="point-body" style="margin-bottom: 0.8vw;">• <b>Estudios Universitarios:</b> En Argentina (Papalini, 2022) y Chile se evidencia uso masivo de MTCI en estudiantes de salud.</p>
              <p class="point-body" style="margin-bottom: 0.8vw;">• <b>Paradoja Formativa:</b> Más del 80% recurre a MTCI en autocuidado pero reporta cero instrucción en sus facultades.</p>
              <p class="point-body">• <b>Falta de Protocolos:</b> Inexistencia de algoritmos para derivar entre psicólogos y terapeutas tradicionales.</p>
            </div>

            <div class="reveal-item">
              <div style="font-size: 1.4vw; font-family: var(--font-serif); font-weight: 700; color: var(--blue-royal); margin-bottom: 0.3vw;">2024 – 2026</div>
              <div style="font-size: 0.8vw; font-weight: 700; color: var(--text-main); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.0vw;">Ámbito Local • Nicaragua y CUR-Estelí</div>
              <p class="point-body" style="margin-bottom: 0.8vw;">• <b>Marco Jurídico de Vanguardia:</b> Leyes 774 y 759 establecen el Instituto de Medicina Natural pionero en Centroamérica.</p>
              <p class="point-body" style="margin-bottom: 0.8vw;">• <b>Vacío en Psicología:</b> Cero asignaturas electivas sobre interculturalidad y diálogo médico en las universidades.</p>
              <p class="point-body">• <b>Estudio CUR-Estelí (2026):</b> Primera investigación empírica mixta que articula estudiantes, docentes y facilitadores.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- SLIDE 5: OBJETIVOS (JERARQUÍA ESCULTÓRICA) -->
      <section class="slide" id="slide-05">
        <div class="slide-header">
          <div class="header-text">
            <div class="eyebrow">Capítulo I • Propósito Investigativo</div>
            <h2 class="slide-title">Objetivos de la Investigación: Del Diagnóstico a la Propuesta</h2>
          </div>
          <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
        </div>

        <div class="slide-content" style="flex-direction: column;">
          <div class="reveal-item" style="border-bottom: 1px solid var(--hairline); padding-bottom: 1.5vw; margin-bottom: 2.0vw;">
            <div style="font-size: 0.8vw; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.4vw;">Objetivo General</div>
            <p style="font-family: var(--font-serif); font-size: 1.35vw; font-weight: 600; line-height: 1.35; color: var(--text-main);">
              Analizar la integración de la Medicina Tradicional, Complementaria e Integrativa (MTCI) como recurso complementario en la atención psicológica, a partir de las percepciones, conocimientos y prácticas de estudiantes, docentes y facilitadores locales, formulando un manual de estrategias bioéticas y formativas en el CUR-Estelí.
            </p>
          </div>

          <div class="col-three">
            <div class="reveal-item">
              <div style="font-family: var(--font-serif); font-size: 2.8vw; font-weight: 700; color: var(--teal-primary); line-height: 1;">01</div>
              <div style="font-size: 0.85vw; font-weight: 700; color: var(--text-main); margin-top: 0.4vw; margin-bottom: 0.6vw;">OE1 • Diagnóstico Estudiantil</div>
              <p class="point-body">Caracterizar la percepción, nivel de conocimiento, frecuencia de uso y barreras autopercibidas en los estudiantes de 4.º y 5.º año de Psicología respecto a las MTCI.</p>
            </div>

            <div class="reveal-item">
              <div style="font-family: var(--font-serif); font-size: 2.8vw; font-weight: 700; color: var(--blue-royal); line-height: 1;">02</div>
              <div style="font-size: 0.85vw; font-weight: 700; color: var(--text-main); margin-top: 0.4vw; margin-bottom: 0.6vw;">OE2 • Saberes de Facilitadores</div>
              <p class="point-body">Explorar las experiencias terapéuticas, prácticas tradicionales y barreras socioculturales que enfrentan los facilitadores locales de medicina tradicional en Estelí.</p>
            </div>

            <div class="reveal-item">
              <div style="font-family: var(--font-serif); font-size: 2.8vw; font-weight: 700; color: var(--gold-primary); line-height: 1;">03</div>
              <div style="font-size: 0.85vw; font-weight: 700; color: var(--text-main); margin-top: 0.4vw; margin-bottom: 0.6vw;">OE3 • Propuesta del Manual</div>
              <p class="point-body">Diseñar un Manual de Estrategias de MTCI para la formación y práctica psicológica, articulando pautas bioéticas, algoritmos de derivación y contenidos curriculares en el CUR-Estelí.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- SLIDE 11: LA PARADOJA FORMATIVA (ANIMATED STATS & VIZ) -->
      <section class="slide" id="slide-11">
        <div class="slide-header">
          <div class="header-text">
            <div class="eyebrow">Capítulo IV • Resultados Empíricos (2/4)</div>
            <h2 class="slide-title">La Paradoja Formativa: Alta Pertinencia frente al Desamparo Curricular (OE1)</h2>
          </div>
          <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
        </div>

        <div class="slide-content">
          <div class="col-split-asym">
            <!-- Big Stats (Flotantes, Sin Cajas) -->
            <div class="reveal-item">
              <div class="stat-hero">
                <div class="number" data-target="89.7">0.0%</div>
                <div class="label">Pertinencia y Relevancia Clínica Asistencial</div>
                <div class="desc">Considera necesario y urgente articular contenidos de MTCI en la formación y ejercicio de la psicología.</div>
              </div>

              <div class="stat-hero">
                <div class="number crimson" data-target="88.2">0.0%</div>
                <div class="label">Desamparo y Vacío Curricular Absoluto</div>
                <div class="desc">Reconoce no haber recibido preparación formal alguna para orientar, psicoeducar o derivar hacia MTCI.</div>
              </div>

              <div class="stat-hero">
                <div class="number gold" data-target="86.8">0.0%</div>
                <div class="label">Inseguridad Procedimental Autopercibida</div>
                <div class="desc">Autopercibe competencias nulas o insuficientes para dialogar éticamente sobre remedios naturales.</div>
              </div>
            </div>

            <!-- Gráfico y Narrativa de Eficacia -->
            <div class="reveal-item" style="display: flex; flex-direction: column; justify-content: space-between;">
              <div class="fig-frame">
                <img src="assets/figuras_apa7/figura_07_frecuencia_uso_estudiantes.png" alt="Frecuencia de Uso y Efectos">
              </div>
              <div style="border-top: 1px solid var(--hairline); padding-top: 1.0vw;">
                <div style="font-size: 0.85vw; font-weight: 700; color: var(--text-main); margin-bottom: 0.3vw;">Uso Personal y Eficacia Somática Percibida:</div>
                <p class="point-body">• <b>Carácter Reactivo:</b> 52.9% no usa MTCI preventivamente; acuden únicamente ante sobrecarga académica.</p>
                <p class="point-body">• <b>Eficacia Plena:</b> 86.7% reporta alivio muscular y bienestar; 0.0% complicaciones o efectos adversos.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- SLIDE 12: FACILITADORES Y DOCENTES (TWO CLEAN COLUMNS) -->
      <section class="slide" id="slide-12">
        <div class="slide-header">
          <div class="header-text">
            <div class="eyebrow">Capítulo IV • Resultados Empíricos (3/4)</div>
            <h2 class="slide-title">Perspectiva de Facilitadores Locales de Estelí y Claustro Docente</h2>
          </div>
          <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
        </div>

        <div class="slide-content">
          <div class="col-split">
            <!-- Facilitadores -->
            <div class="reveal-item">
              <div class="stat-hero">
                <div class="number" data-target="100">0%</div>
                <div class="label">FACILITADORES LOCALES DE ESTELÍ (n = 9)</div>
              </div>
              <div class="point-item">
                <span class="point-num">✦</span>
                <span class="point-head">Alivio Somático Inmediato:</span>
                <span class="point-body">Constatan descompresión muscular y facilitación de la apertura afectiva para el diálogo terapéutico posterior.</span>
              </div>
              <div class="point-item">
                <span class="point-num">✦</span>
                <span class="point-head">Memoria Etnobotánica Viva:</span>
                <span class="point-body">77.8% mujeres; 44.4% acumula entre 20 y 30 años de experiencia comunitaria continuada en Estelí.</span>
              </div>
              <div class="point-item">
                <span class="point-num">✦</span>
                <span class="point-head">Estigma Sociocultural:</span>
                <span class="point-body">El 100% identifica mitos, tabúes y prejuicios religiosos respecto a la medicina natural en la población.</span>
              </div>
              <div class="point-item">
                <span class="point-num">✦</span>
                <span class="point-head">Desafío Económico:</span>
                <span class="point-body">77.8% reporta que la falta de recursos económicos de los consultantes interrumpe la continuidad del cuidado.</span>
              </div>
            </div>

            <!-- Docentes -->
            <div class="reveal-item">
              <div class="stat-hero">
                <div class="number royal" data-target="100">0%</div>
                <div class="label">CLAUSTRO DOCENTE-PSICÓLOGOS (n = 9)</div>
              </div>
              <div class="point-item">
                <span class="point-num" style="color: var(--blue-royal);">✦</span>
                <span class="point-head">Respaldo Curricular Unánime:</span>
                <span class="point-body">Apoyo total a transversalizar contenidos de MTCI bajo un enfoque científico, bioético y no prescriptivo.</span>
              </div>
              <div class="point-item">
                <span class="point-num" style="color: var(--blue-royal);">✦</span>
                <span class="point-head">Metodologías Vivenciales (88.9%):</span>
                <span class="point-body">Rechazan la enseñanza memorística; priorizan análisis de casos clínicos y talleres de autorregulación somática.</span>
              </div>
              <div class="point-item">
                <span class="point-num" style="color: var(--blue-royal);">✦</span>
                <span class="point-head">Competencias Bioéticas a Formar:</span>
                <span class="point-body">Demandan juicio clínico, consentimiento informado intercultural y respeto estricto de los límites legales.</span>
              </div>
              <div class="point-item">
                <span class="point-num" style="color: var(--blue-royal);">✦</span>
                <span class="point-head">Capacitación Propia Urgente:</span>
                <span class="point-body">El profesorado solicita actualización institucional en neurobiología somática y regulación Bottom-Up.</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- SLIDE 13: PROPUESTA OPERATIVA (MANUAL DE ESTRATEGIAS) -->
      <section class="slide" id="slide-13">
        <div class="slide-header">
          <div class="header-text">
            <div class="eyebrow">Capítulo V • Propuesta Operativa (OE3)</div>
            <h2 class="slide-title">Manual de Estrategias de MTCI para la Formación y Práctica Psicológica</h2>
          </div>
          <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
        </div>

        <div class="slide-content">
          <div class="col-split-asym">
            <!-- Portada y Ficha Técnica -->
            <div class="reveal-item">
              <div style="display: flex; gap: 1.5vw; align-items: flex-start;">
                <img src="assets/extracted/portada_manual.jpg" alt="Portada del Manual" style="width: 14vw; border-radius: 4px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);">
                <div>
                  <div style="font-size: 0.8vw; font-weight: 700; color: var(--teal-primary); text-transform: uppercase; margin-bottom: 0.4vw;">Ficha Técnica</div>
                  <div style="font-size: 0.85vw; line-height: 1.5; color: var(--text-muted);">
                    <div>• <b>Extensión:</b> 18 páginas in extenso (Anexo 16.2).</div>
                    <div>• <b>Destinatarios:</b> Estudiantes y docentes de la Clínica Psicosocial.</div>
                    <div>• <b>Propósito:</b> Dotar de discernimiento ético sin habilitar como terapeutas alternativos.</div>
                    <div>• <b>Herramienta Anexa:</b> Inventario I-CAM-Q adaptado transculturalmente a Nicaragua.</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Estructura de los 8 Módulos -->
            <div class="reveal-item">
              <h3 style="font-family: var(--font-serif); font-size: 1.15vw; color: var(--text-main); margin-bottom: 0.8vw;">Estructura Modular (8 Módulos Temáticos)</h3>
              <div style="font-size: 0.82vw; line-height: 1.5; color: var(--text-main);">
                <div style="margin-bottom: 0.4vw;"><b>M1. Fundamentos y Marco Legal:</b> Definición OMS (2025) y Leyes 774, 759 y 292.</div>
                <div style="margin-bottom: 0.4vw;"><b>M2. Principios Deontológicos:</b> Consentimiento informado y no sustitución médica.</div>
                <div style="margin-bottom: 0.4vw;"><b>M3. Mapa Clínico de Prácticas:</b> Clasificación en 4 niveles de seguridad asistencial.</div>
                <div style="margin-bottom: 0.4vw;"><b>M4. Algoritmo de Derivación:</b> Protocolo secuencial de 4 pasos para interconsulta.</div>
                <div style="margin-bottom: 0.4vw;"><b>M5. Habilidades de Diálogo:</b> Entrevista abierta para erradicar el ocultamiento.</div>
                <div style="margin-bottom: 0.4vw;"><b>M6. Red Intersectorial:</b> Criterios de referencia con facilitadores territoriales.</div>
                <div style="margin-bottom: 0.4vw;"><b>M7. Ruta Pedagógica:</b> Secuencia de 3 etapas y propuesta de curso electivo.</div>
                <div style="margin-bottom: 0.4vw;"><b>M8. Soporte CUR-Estelí:</b> Creación del Comité de Bioética y capacitación docente.</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- SLIDE 14: CONCLUSIONES CENTRALES -->
      <section class="slide" id="slide-14">
        <div class="slide-header">
          <div class="header-text">
            <div class="eyebrow">Capítulo VI • Síntesis Conclusiva</div>
            <h2 class="slide-title">Conclusiones Centrales de la Investigación (Triangulación de Objetivos)</h2>
          </div>
          <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
        </div>

        <div class="slide-content" style="flex-direction: column;">
          <div class="reveal-item point-item">
            <span class="point-num">01</span>
            <span class="point-head">Cumplimiento del Objetivo General:</span>
            <span class="point-body">Los tres colectivos investigados (N = 86) validan unánimemente a la MTCI como recurso complementario legítimo en salud mental, condicionado a un ejercicio bioético, científico y respetuoso de los límites profesionales.</span>
          </div>

          <div class="reveal-item point-item">
            <span class="point-num">02</span>
            <span class="point-head">Perfil y Paradoja Estudiantil (OE1):</span>
            <span class="point-body">El estudiantado posee buen dominio conceptual (67.6%) y alta satisfacción somática (86.7%), pero padece desinformación legal (58.8% desconoce Ley 774; 64.7% desconoce Ley 292) e inseguridad para derivar (88.2%).</span>
          </div>

          <div class="reveal-item point-item">
            <span class="point-num">03</span>
            <span class="point-head">Oferta y Resiliencia Territorial (OE2):</span>
            <span class="point-body">Los facilitadores de Estelí constatan 100% de alivio de sobrecarga muscular y mayor receptividad reflexiva (88.9%), enfrentando estigma sociocultural (100%) y limitaciones económicas de los usuarios (77.8%).</span>
          </div>

          <div class="reveal-item point-item">
            <span class="point-num">04</span>
            <span class="point-head">Consenso Curricular Docente (OE3):</span>
            <span class="point-body">El 100% del claustro apoya transversalizar la MTCI bajo metodologías activas y vivenciales (88.9%), demandando formación en regulación neurovegetativa y comités de bioética institucional.</span>
          </div>

          <div class="reveal-item point-item">
            <span class="point-num">05</span>
            <span class="point-head">Logro Propositivo del Manual de Estrategias:</span>
            <span class="point-body">Se construyó exitosamente el Manual de Estrategias MTCI de 18 páginas (Anexo 16.2), dotando al CUR-Estelí de algoritmos de decisión clínica, pautas contra el ocultamiento y el inventario I-CAM-Q.</span>
          </div>
        </div>
      </section>

      <!-- SLIDE 15: RECOMENDACIONES (4 CUADRANTES SIN CAJAS) -->
      <section class="slide" id="slide-15">
        <div class="slide-header">
          <div class="header-text">
            <div class="eyebrow">Capítulo VI • Directrices Prospectivas</div>
            <h2 class="slide-title">Recomendaciones Estratégicas para Estudiantes, Docentes, Universidad y MINSA</h2>
          </div>
          <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
        </div>

        <div class="slide-content">
          <div style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 2.5vw; width: 100%;">
            <div class="reveal-item">
              <div style="font-size: 0.8vw; font-weight: 700; color: var(--teal-primary); text-transform: uppercase; margin-bottom: 0.4vw;">Para el Estamento Estudiantil</div>
              <p class="point-body">✓ <b>Límites Legales:</b> Respetar estrictamente Leyes 774 y 292 (cero prescripción farmacológica).</p>
              <p class="point-body">✓ <b>Algoritmo Clínico:</b> Aplicar el árbol de decisión del manual en la Clínica Psicosocial.</p>
              <p class="point-body">✓ <b>Diálogo Abierto:</b> Explorar empáticamente el uso de MTCI para erradicar el ocultamiento.</p>
            </div>

            <div class="reveal-item">
              <div style="font-size: 0.8vw; font-weight: 700; color: var(--blue-royal); text-transform: uppercase; margin-bottom: 0.4vw;">Para el Claustro Docente</div>
              <p class="point-body">✓ <b>Transversalidad:</b> Integrar contenidos en Psicología Clínica, Comunitaria y Ética.</p>
              <p class="point-body">✓ <b>Pedagogía Vivencial:</b> Priorizar análisis de casos reales y talleres de autorregulación.</p>
              <p class="point-body">✓ <b>Capacitación:</b> Formarse en neurobiología somática y regulación Bottom-Up.</p>
            </div>

            <div class="reveal-item">
              <div style="font-size: 0.8vw; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; margin-bottom: 0.4vw;">Para la Gestión del CUR-Estelí</div>
              <p class="point-body">✓ <b>Adopción Oficial:</b> Formalizar la aprobación del Manual de Estrategias MTCI (Anexo 16.2).</p>
              <p class="point-body">✓ <b>Comité de Bioética:</b> Constituir el Comité de Ética y Delimitación Profesional.</p>
              <p class="point-body">✓ <b>Alianza con MINSA:</b> Consolidar convenios para pasantías y ferias de salud comunitaria.</p>
            </div>

            <div class="reveal-item">
              <div style="font-size: 0.8vw; font-weight: 700; color: var(--text-main); text-transform: uppercase; margin-bottom: 0.4vw;">Para el Sistema de Salud y Facilitadores</div>
              <p class="point-body">✓ <b>Registro Oficial:</b> Difundir mecanismos de acreditación según Ley No. 774.</p>
              <p class="point-body">✓ <b>Red de Interconsulta:</b> Habilitar canales de referencia bidireccional formal.</p>
              <p class="point-body">✓ <b>Principio Bioético:</b> Mantener el compromiso de complementariedad sin sustitución médica.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- SLIDE 16: CIERRE INSTITUCIONAL (DARK MINIMALIST) -->
      <section class="slide theme-dark" id="slide-16">
        <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
          <img src="assets/extracted/unan_shield_only.png" alt="UNAN" style="height: 6.5vw; margin-bottom: 1.5vw; filter: drop-shadow(0 6px 16px rgba(0,0,0,0.6));">
          <div style="font-family: var(--font-serif); font-size: 1.5vw; font-style: italic; color: var(--gold-primary); margin-bottom: 0.8vw;">
            «¡A la libertad por la Universidad!»
          </div>
          <h1 style="font-family: var(--font-serif); font-size: 3.2vw; font-weight: 700; color: #FFFFFF; margin-bottom: 1.0vw;">
            Muchas Gracias por su Atención
          </h1>
          <p style="font-size: 1.15vw; color: var(--text-light-muted); max-width: 65%; margin-bottom: 2.5vw;">
            Espacio Abierto para Preguntas, Comentarios y Defensa Oral ante el Honorable Tribunal Examinador
          </p>

          <div style="border-top: 1px solid var(--hairline-dark); padding-top: 1.5vw; width: 60%; display: flex; justify-content: space-around;">
            <div>
              <span style="font-size: 0.75vw; color: var(--teal-primary); font-weight: 700; text-transform: uppercase;">Sustentantes</span>
              <div style="font-size: 0.85vw; color: #FFFFFF; margin-top: 0.2vw;">Dina García • Tatiana López • Engel Zamora</div>
            </div>
            <div>
              <span style="font-size: 0.75vw; color: var(--gold-primary); font-weight: 700; text-transform: uppercase;">Tutoría</span>
              <div style="font-size: 0.85vw; color: #FFFFFF; margin-top: 0.2vw;">Dra. Tania Libertad Pérez Guevara</div>
            </div>
          </div>
        </div>
      </section>

    </div>

    <!-- Minimalist HUD Controls -->
    <footer class="deck-hud">
      <div class="progress-bar-wrap">
        <div class="progress-bar" id="progress"></div>
      </div>

      <div class="hud-left">
        UNAN-Managua • CUR-Estelí | Carrera de Psicología
      </div>

      <div class="hud-controls">
        <button class="btn-hud" id="btn-prev" title="Anterior (Flecha Izq)">‹ Anterior</button>
        <span class="slide-counter" id="counter">01 / 16</span>
        <button class="btn-hud" id="btn-next" title="Siguiente (Flecha Der)">Siguiente ›</button>
        <span style="color: var(--text-muted); opacity: 0.4;">|</span>
        <button class="btn-hud" id="btn-notes" title="Notas del Presentador (N)">Notas [N]</button>
        <button class="btn-hud" id="btn-grid" title="Cuadrícula de Diapositivas (T)">Resumen [T]</button>
        <button class="btn-hud" id="btn-fs" title="Pantalla Completa (F)">⛶ [F]</button>
      </div>
    </footer>

    <!-- Speaker Notes Drawer -->
    <div id="notes-drawer">
      <div class="notes-header">
        <span>Guía de Oratoria y Puntos Clave de Defensa</span>
        <span style="font-size: 0.7vw; opacity: 0.7;">Presiona [N] o [ESC] para cerrar</span>
      </div>
      <div class="notes-content" id="notes-body">
        Pausa inicial. Saludar con solemnidad al Honorable Tribunal Examinador. Enfatizar la relevancia histórica de este estudio como el primero en articular a la academia con los saberes territoriales de Estelí.
      </div>
    </div>

    <!-- Thumbnail Modal -->
    <div id="thumb-modal">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E293B; padding-bottom: 1.0vw;">
        <h2 style="font-family: var(--font-serif); font-size: 1.4vw; color: #FFFFFF;">Índice General de Diapositivas (16 Láminas)</h2>
        <button class="btn-hud" id="btn-close-modal" style="color: #FFFFFF; font-size: 1.1vw;">✕ Cerrar</button>
      </div>
      <div class="thumb-grid" id="thumb-container"></div>
    </div>

  </div>

  <script>
    // =========================================================================
    // SLIDES ENGINE & KINETIC ANIMATIONS
    // =========================================================================
    const slides = Array.from(document.querySelectorAll('.slide'));
    const totalSlides = slides.length;
    let currentIndex = 0;

    const counterEl = document.getElementById('counter');
    const progressEl = document.getElementById('progress');
    const notesDrawer = document.getElementById('notes-drawer');
    const notesBody = document.getElementById('notes-body');
    const thumbModal = document.getElementById('thumb-modal');
    const thumbContainer = document.getElementById('thumb-container');
    const viewport = document.getElementById('viewport');

    // Slide Notes Array
    const slideNotes = """ + str([s["notes"] for s in SLIDES_DATA]) + """;
    const slideTitles = """ + str([s["title"] for s in SLIDES_DATA]) + """;

    // Build Thumbnail Grid
    slideTitles.forEach((title, idx) => {
      const card = document.createElement('div');
      card.className = `thumb-card ${idx === 0 ? 'active' : ''}`;
      card.innerHTML = `
        <div class="thumb-num">LÁMINA ${String(idx + 1).padStart(2, '0')}</div>
        <div class="thumb-title">${title}</div>
      `;
      card.addEventListener('click', () => {
        goToSlide(idx);
        toggleThumbnails(false);
      });
      thumbContainer.appendChild(card);
    });

    // Web Audio Subtle Click Synthesizer (Zero External Audio Files)
    const audioCtx = (typeof AudioContext !== 'undefined') ? new AudioContext() : null;
    function playTick(freq = 440) {
      if (!audioCtx) return;
      try {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.08);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.08);
      } catch (e) {}
    }

    // Number Counter Animation
    function animateCounters(slideEl) {
      const counters = slideEl.querySelectorAll('[data-target]');
      counters.forEach(el => {
        const target = parseFloat(el.getAttribute('data-target'));
        const isDecimal = target % 1 !== 0;
        const duration = 1200; // ms
        const startTime = performance.now();

        function update(currentTime) {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          // Ease-Out Cubic
          const easeOut = 1 - Math.pow(1 - progress, 3);
          const currentVal = target * easeOut;

          el.textContent = isDecimal 
            ? currentVal.toFixed(1) + '%' 
            : Math.round(currentVal) + '%';

          if (progress < 1) {
            requestAnimationFrame(update);
          } else {
            el.textContent = isDecimal ? target.toFixed(1) + '%' : target + '%';
          }
        }
        requestAnimationFrame(update);
      });
    }

    function goToSlide(index) {
      if (index < 0 || index >= totalSlides) return;
      playTick(520);

      slides[currentIndex].classList.remove('active');
      currentIndex = index;
      const targetSlide = slides[currentIndex];
      targetSlide.classList.add('active');

      // Update HUD & Counter
      counterEl.textContent = `${String(currentIndex + 1).padStart(2, '0')} / ${String(totalSlides).padStart(2, '0')}`;
      progressEl.style.width = `${((currentIndex + 1) / totalSlides) * 100}%`;

      // Theme sync for HUD
      if (targetSlide.classList.contains('theme-dark')) {
        viewport.classList.add('hud-dark');
      } else {
        viewport.classList.remove('hud-dark');
      }

      // Update Notes
      notesBody.textContent = slideNotes[currentIndex] || "Sin notas adicionales.";

      // Update Thumbnails Active State
      const thumbCards = thumbContainer.querySelectorAll('.thumb-card');
      thumbCards.forEach((c, i) => c.classList.toggle('active', i === currentIndex));

      // Trigger metric animations
      animateCounters(targetSlide);
    }

    function nextSlide() {
      if (currentIndex < totalSlides - 1) goToSlide(currentIndex + 1);
    }

    function prevSlide() {
      if (currentIndex > 0) goToSlide(currentIndex - 1);
    }

    function toggleNotes() {
      notesDrawer.classList.toggle('open');
      playTick(350);
    }

    function toggleThumbnails(force) {
      const isOpen = force !== undefined ? force : !thumbModal.classList.contains('open');
      thumbModal.classList.toggle('open', isOpen);
      playTick(isOpen ? 480 : 380);
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    }

    // Keyboard Navigation
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'n' || e.key === 'N' || e.key === 'p' || e.key === 'P') {
        toggleNotes();
      } else if (e.key === 't' || e.key === 'T') {
        toggleThumbnails();
      } else if (e.key === 'Escape') {
        if (notesDrawer.classList.contains('open')) toggleNotes();
        if (thumbModal.classList.contains('open')) toggleThumbnails(false);
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFullscreen();
      } else if (e.key === 'Home') {
        goToSlide(0);
      } else if (e.key === 'End') {
        goToSlide(totalSlides - 1);
      }
    });

    // Button Bindings
    document.getElementById('btn-next').addEventListener('click', nextSlide);
    document.getElementById('btn-prev').addEventListener('click', prevSlide);
    document.getElementById('btn-notes').addEventListener('click', toggleNotes);
    document.getElementById('btn-grid').addEventListener('click', () => toggleThumbnails());
    document.getElementById('btn-close-modal').addEventListener('click', () => toggleThumbnails(false));
    document.getElementById('btn-fs').addEventListener('click', toggleFullscreen);

    // Initial Trigger for First Slide Counters
    animateCounters(slides[0]);
  </script>
</body>
</html>
"""

def generate_deck():
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Animated presentation created successfully at: {HTML_OUTPUT}")

if __name__ == "__main__":
    generate_deck()
