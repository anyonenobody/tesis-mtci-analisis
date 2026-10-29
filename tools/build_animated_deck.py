#!/usr/bin/env python3
"""
tools/build_animated_deck.py
================================================================================
Generador de Lienzo Espacial Interactivo (Estilo Prezi / ZUI) con Diseño
Editorial e Infográfico de Alto Impacto en cada lámina:
`presentacion_tesis_mtci_animated.html`
================================================================================
"""

import json

HTML_OUTPUT = "presentacion_tesis_mtci_animated.html"

SLIDES_METADATA = [
    {
        "id": "slide-01", "num": "01", "chapter": "Portada",
        "category": "Defensa de Tesis de Licenciatura en Psicología",
        "short": "Portada Institucional", "metric": "N = 86 Actores",
        "title": "La Medicina Tradicional, Complementaria e Integrativa (MTCI) como Complemento en la Atención Psicológica",
        "x": 0, "y": -150, "scale": 1.18, "rot": 0, "cluster": "hub",
        "notes": "Pausa inicial. Saludar con solemnidad al Honorable Tribunal Examinador. Enfatizar que este estudio mixto aborda por primera vez en la UNAN-Managua CUR-Estelí la articulación entre formación académica y saberes territoriales en salud mental."
    },
    {
        "id": "slide-02", "num": "02", "chapter": "Cap. I",
        "category": "Capítulo I • Introducción",
        "short": "Problema y Justificación", "metric": "Ley 774 vs 292",
        "title": "Planteamiento del Problema y Justificación de la Investigación",
        "x": -3100, "y": -2050, "scale": 0.88, "rot": -3, "cluster": "cap1",
        "notes": "Fundamentar la tensión jurídica central: la Ley 774 garantiza el derecho ciudadano a la MTCI, pero la Ley 292 inscribe el límite legal de no prescripción para psicólogos. Explicar el fenómeno clínico del ocultamiento terapéutico y la pregunta de investigación."
    },
    {
        "id": "slide-03", "num": "03", "chapter": "Cap. I",
        "category": "Capítulo I • Introducción",
        "short": "Antecedentes (OMS, Región, Local)", "metric": "2014 – 2026",
        "title": "Antecedentes de la Investigación: Ámbitos Internacional, Regional y Local",
        "x": -4950, "y": -1750, "scale": 0.88, "rot": -1.5, "cluster": "cap1",
        "notes": "Detallar los tres hitos temporales: las directrices de la OMS (2014-2019) y metanálisis clínicos; los hallazgos en universidades de Iberoamérica (2020-2023) sobre la brecha formativa; y el marco legal nicaragüense frente al vacío curricular existente."
    },
    {
        "id": "slide-04", "num": "04", "chapter": "Cap. I",
        "category": "Capítulo I • Introducción",
        "short": "Contexto: Estelí y CUR-Estelí", "metric": "Las Segovias",
        "title": "Contexto del Estudio: Territorio de Estelí y UNAN-Managua CUR-Estelí",
        "x": -4950, "y": -550, "scale": 0.88, "rot": 1.5, "cluster": "cap1",
        "notes": "Contextualizar la confluencia entre la tradición etnobotánica viva del norte segoviano y el papel formador del CUR-Estelí y su Clínica Psicosocial, destacando las barreras de articulación institucional."
    },
    {
        "id": "slide-05", "num": "05", "chapter": "Cap. I",
        "category": "Capítulo I • Introducción",
        "short": "Objetivos de Investigación", "metric": "OG + 3 OE",
        "title": "Objetivos de la Investigación: General y Específicos",
        "x": -3100, "y": -550, "scale": 0.88, "rot": 0, "cluster": "cap1",
        "notes": "Exponer el Objetivo General y los tres Específicos: diagnóstico en estudiantes (OE1), experiencias de facilitadores locales (OE2) y criterios docentes con diseño del manual (OE3)."
    },
    {
        "id": "slide-06", "num": "06", "chapter": "Cap. II",
        "category": "Capítulo II • Marco Teórico (1/2)",
        "short": "Epistemología y Bioética", "metric": "3 Pilares",
        "title": "Fundamentos Epistemológicos y Principios Bioéticos en Salud Mental",
        "x": 2900, "y": -2050, "scale": 0.88, "rot": 2.5, "cluster": "cap2",
        "notes": "Explicar los tres pilares conceptuales: el Modelo Biopsicosocial de Engel (1977) y neurobiología somática; el Pluralismo Médico de Menéndez (2020); y la Bioética de Beauchamp y Childress (No Maleficencia y Autonomía)."
    },
    {
        "id": "slide-07", "num": "07", "chapter": "Cap. II",
        "category": "Capítulo II • Marco Teórico (2/2)",
        "short": "Marco Legal y Eficacia Clínica", "metric": "Leyes 774 / 292 / 759",
        "title": "Marco Normativo Nicaragüense y Evidencia de Eficacia Clínica",
        "x": 4800, "y": -1600, "scale": 0.88, "rot": 4, "cluster": "cap2",
        "notes": "Analizar la articulación de las Leyes 774, 292 y 759 de Nicaragua, complementándola con la evidencia neuroquímica gabaérgica de la fitoterapia y la regulación vagal de las técnicas mente-cuerpo."
    },
    {
        "id": "slide-08", "num": "08", "chapter": "Cap. III",
        "category": "Capítulo III • Marco Metodológico (1/2)",
        "short": "Diseño Mixto Secuencial DEXPLIS", "metric": "3 Fases",
        "title": "Paradigma Pragmático, Enfoque Mixto Secuencial y Fases del Estudio",
        "x": 4950, "y": -150, "scale": 0.88, "rot": -2, "cluster": "cap3",
        "notes": "Describir el paradigma pragmático y el diseño DEXPLIS (Derivativo Secuencial): Fase cuantitativa censal -> Fase cualitativa de profundización -> Fase propositiva del manual."
    },
    {
        "id": "slide-09", "num": "09", "chapter": "Cap. III",
        "category": "Capítulo III • Marco Metodológico (2/2)",
        "short": "Muestra Consolidada (N = 86)", "metric": "68 + 9 + 9",
        "title": "Delimitación Muestral Consolidada (N = 86) y Criterios de Selección",
        "x": 3100, "y": 250, "scale": 0.88, "rot": 0, "cluster": "cap3",
        "notes": "Presentar con exactitud los 3 grupos muestrales que suman N=86: 68 estudiantes censados (77.9% 4.° año, 22.1% 5.° año), 9 facilitadores locales de Estelí y 9 docentes-psicólogos del claustro universitario."
    },
    {
        "id": "slide-10", "num": "10", "chapter": "Cap. IV",
        "category": "Capítulo IV • Resultados en Estudiantes (1/2)",
        "short": "Dominio Conceptual y Legal", "metric": "64.7% Brecha Ley 292",
        "title": "Perfil Sociodemográfico y Grado de Dominio Conceptual y Normativo",
        "x": 3150, "y": 2150, "scale": 0.90, "rot": 2.5, "cluster": "cap4",
        "notes": "Mostrar la Figura 4. Contrastar el 67.6% de acierto en el concepto de la OMS frente al 58.8% de desconocimiento de la Ley 774 y el 64.7% de desconocimiento de la inhabilitación para prescribir fármacos (Ley 292)."
    },
    {
        "id": "slide-11", "num": "11", "chapter": "Cap. IV",
        "category": "Capítulo IV • Resultados en Estudiantes (2/2)",
        "short": "Pertinencia vs Brecha Formativa", "metric": "89.7% vs 88.2%",
        "title": "Frecuencia de Uso, Bienestar Percibido y Brecha Formativa (OE1)",
        "x": 1150, "y": 2450, "scale": 0.90, "rot": 0.8, "cluster": "cap4",
        "notes": "Mostrar la Figura 7 y las métricas clave: 89.7% considera pertinente integrar la MTCI, pero 88.2% reporta preparación insuficiente para derivar y 86.8% para psicoeducar. El 86.7% de usuarios reporta alivio muscular y 0.0% efectos adversos."
    },
    {
        "id": "slide-12", "num": "12", "chapter": "Cap. IV",
        "category": "Capítulo IV • Resultados en Facilitadores Locales",
        "short": "Facilitadores: Alivio Somático", "metric": "100% Alivio • 88.9% Apertura",
        "title": "Modalidades Terapéuticas, Eficacia Somática y Barreras en Estelí (OE2)",
        "x": -950, "y": 2450, "scale": 0.90, "rot": -0.8, "cluster": "cap4",
        "notes": "Mostrar la Figura 12 y la Figura 14. Destacar que el 100% de facilitadores constata alivio de sobrecarga somática y el 88.9% apertura emocional. Explicar las barreras socioculturales (77.8%) y económicas (77.8%)."
    },
    {
        "id": "slide-13", "num": "13", "chapter": "Cap. IV",
        "category": "Capítulo IV • Resultados en el Claustro Docente",
        "short": "Claustro Docente: Consenso", "metric": "100% Respaldo • 88.9% Talleres",
        "title": "Estrategias Pedagógicas, Didáctica Vivencial y Consenso Ético (OE3)",
        "x": -3000, "y": 2150, "scale": 0.90, "rot": -2.5, "cluster": "cap4",
        "notes": "Mostrar la Figura 24 y la Figura 25. Enfatizar el 100% de respaldo curricular unánime bajo no prescripción, la demanda de talleres vivenciales (88.9%) y la solicitud de capacitación docente institucional en neurobiología somática (77.8%)."
    },
    {
        "id": "slide-14", "num": "14", "chapter": "Cap. V",
        "category": "Capítulo V • Propuesta de Intervención (OE3)",
        "short": "Manual de Estrategias MTCI", "metric": "8 Módulos • I-CAM-Q",
        "title": "Manual de Estrategias de MTCI para la Formación y Práctica Psicológica",
        "x": -4850, "y": 1150, "scale": 0.96, "rot": 2, "cluster": "cap5",
        "notes": "Presentar formalmente el Manual de 18 páginas (Anexo 16.2), sus 8 módulos temáticos, el algoritmo clínico de derivación y la adaptación transcultural del inventario I-CAM-Q para tamizaje en Nicaragua."
    },
    {
        "id": "slide-15", "num": "15", "chapter": "Cap. VI",
        "category": "Capítulo VI • Conclusiones y Recomendaciones",
        "short": "Conclusiones Trianguladas", "metric": "5 Conclusiones",
        "title": "Conclusiones Centrales de la Investigación (Triangulación de Objetivos)",
        "x": -2900, "y": 900, "scale": 0.88, "rot": 0, "cluster": "cap6",
        "notes": "Sintetizar las 5 conclusiones centrales: cumplimiento del Objetivo General, caracterización de la brecha estudiantil, resiliencia y alivio somático en facilitadores, consenso curricular docente y materialización del manual."
    },
    {
        "id": "slide-16", "num": "16", "chapter": "Cap. VI",
        "category": "Capítulo VI • Conclusiones y Recomendaciones",
        "short": "Recomendaciones Estratégicas", "metric": "4 Estamentos",
        "title": "Recomendaciones Estratégicas para la Formación, Práctica e Intersectorialidad",
        "x": -1550, "y": 900, "scale": 0.88, "rot": -1.5, "cluster": "cap6",
        "notes": "Detallar las directrices operativas para estudiantes, claustro docente, gestión del CUR-Estelí (adopción formal y comité de bioética) y el sistema de salud / MINSA."
    },
    {
        "id": "slide-17", "num": "17", "chapter": "Cierre",
        "category": "Cierre Institucional",
        "short": "Cierre y Defensa Oral", "metric": "UNAN-Managua",
        "title": "«¡A la libertad por la Universidad!» — Muchas Gracias por su Atención",
        "x": 0, "y": 1050, "scale": 1.05, "rot": 0, "cluster": "hub",
        "notes": "Agradecer al tribunal examinador, a los participantes y a la comunidad universitaria. Declarar formalmente abierto el espacio para preguntas y defensa oral."
    }
]

CSS_STYLES = """
    :root {
      --bg-cosmos: #030811;
      --slide-ivory: #FAF8F5;
      --slide-dark: #06101E;

      --text-main: #0F172A;
      --text-body: #334155;
      --text-muted: #64748B;
      --text-light: #F8FAFC;
      --text-light-muted: #94A3B8;

      --teal-deep: #064E3B;
      --teal-primary: #0D9488;
      --teal-bright: #14B8A6;
      --emerald: #10B981;
      --gold-deep: #92400E;
      --gold-primary: #D97706;
      --gold-bright: #F59E0B;
      --crimson: #DC2626;
      --crimson-soft: #FEE2E2;
      --royal: #1D4ED8;
      --royal-bright: #3B82F6;
      --violet: #6D28D9;

      --font-serif: 'Playfair Display', Georgia, Cambria, serif;
      --font-sans: 'Plus Jakarta Sans', Calibri, system-ui, -apple-system, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    html, body {
      width: 100vw; height: 100vh; overflow: hidden;
      background: radial-gradient(ellipse at 50% 45%, #0A192F 0%, #040B16 65%, #02050A 100%);
      font-family: var(--font-sans); color: var(--text-main);
      user-select: none; -webkit-font-smoothing: antialiased;
    }
    body.editing-active { user-select: text; }

    #viewport {
      position: relative; width: 100vw; height: 100vh;
      overflow: hidden; cursor: grab;
    }
    #viewport.dragging { cursor: grabbing; }

    .cosmos-grid {
      position: absolute; inset: 0;
      background-image:
        radial-gradient(rgba(20, 184, 166, 0.14) 1px, transparent 1px),
        radial-gradient(rgba(245, 158, 11, 0.08) 1px, transparent 1px);
      background-size: 56px 56px, 168px 168px;
      background-position: 0 0, 28px 28px;
      pointer-events: none; z-index: 0;
    }

    #camera {
      position: absolute; top: 50%; left: 50%; width: 0; height: 0; z-index: 2;
      transition: transform 1.15s cubic-bezier(0.22, 1, 0.36, 1); will-change: transform;
    }
    #world {
      position: absolute; top: 0; left: 0; transform-origin: 0 0;
      transition: transform 1.15s cubic-bezier(0.22, 1, 0.36, 1); will-change: transform;
    }
    #viewport.no-transition #camera,
    #viewport.no-transition #world { transition: none !important; }

    #world-connections {
      position: absolute; top: -6000px; left: -8000px; width: 16000px; height: 12000px;
      pointer-events: none; z-index: 1; overflow: visible;
    }
    .conn-path {
      fill: none; stroke-width: 8; stroke-linecap: round;
      stroke-dasharray: 22 18; opacity: 0.55; animation: dashFlow 35s linear infinite;
    }
    .conn-glow { fill: none; stroke-width: 24; stroke-linecap: round; opacity: 0.14; }
    @keyframes dashFlow { to { stroke-dashoffset: -1000; } }

    .cluster-banner {
      position: absolute; transform: translate(-50%, -50%);
      padding: 26px 58px; border-radius: 999px;
      font-size: 46px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;
      white-space: nowrap; z-index: 3; pointer-events: none;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7);
      border: 3px solid rgba(255, 255, 255, 0.25); backdrop-filter: blur(12px);
      transition: opacity 0.5s ease;
    }
    body:not(.in-overview) .cluster-banner { opacity: 0.15; }
    .cluster-cap1 { background: rgba(13, 148, 136, 0.92); color: #FFF; border-color: #5EEAD4; }
    .cluster-cap2 { background: rgba(217, 119, 6, 0.92); color: #FFF; border-color: #FCD34D; }
    .cluster-cap3 { background: rgba(29, 78, 216, 0.92); color: #FFF; border-color: #93C5FD; }
    .cluster-cap4 { background: rgba(185, 28, 28, 0.92); color: #FFF; border-color: #FCA5A5; }
    .cluster-cap5 { background: rgba(5, 150, 105, 0.92); color: #FFF; border-color: #6EE7B7; }
    .cluster-cap6 { background: rgba(109, 40, 217, 0.92); color: #FFF; border-color: #C4B5FD; }

    /* =========================================================================
       BESPOKE EDITORIAL SLIDE ARCHITECTURE (1600x900)
       ========================================================================= */
    .slide {
      position: absolute; top: 0; left: 0;
      width: 1600px; height: 900px;
      margin-left: -800px; margin-top: -450px;
      padding: 46px 64px 52px 64px;
      background:
        radial-gradient(circle at 96% 6%, rgba(13, 148, 136, 0.09) 0%, transparent 42%),
        radial-gradient(circle at 4% 94%, rgba(217, 119, 6, 0.08) 0%, transparent 42%),
        linear-gradient(180deg, #FFFFFF 0%, #F7F5F0 100%);
      border-radius: 28px;
      box-shadow: 0 40px 100px rgba(0, 0, 0, 0.7), inset 0 0 0 1px rgba(255,255,255,0.9);
      display: flex; flex-direction: column;
      transform-origin: 50% 50%;
      transition: box-shadow 0.45s ease, opacity 0.45s ease, filter 0.45s ease;
      z-index: 5; overflow: hidden; cursor: pointer;
    }

    /* Decorative watermark number in top-right background of each slide */
    .bg-watermark-num {
      position: absolute; top: -28px; right: 110px;
      font-family: var(--font-serif); font-size: 210px; font-weight: 800;
      color: rgba(15, 23, 42, 0.032); line-height: 1;
      pointer-events: none; z-index: 0; letter-spacing: -0.04em;
    }
    .slide.theme-dark .bg-watermark-num { color: rgba(255, 255, 255, 0.04); }

    /* Botanical SVG Corner Ornament */
    .botanical-corner {
      position: absolute; bottom: -30px; right: -30px;
      width: 320px; height: 320px; opacity: 0.055;
      pointer-events: none; z-index: 0;
    }

    .slide.theme-dark {
      background:
        radial-gradient(circle at 85% 18%, rgba(16, 185, 129, 0.18) 0%, transparent 45%),
        radial-gradient(circle at 12% 85%, rgba(245, 158, 11, 0.15) 0%, transparent 45%),
        linear-gradient(135deg, #040D1A 0%, #091E36 55%, #051322 100%);
      color: var(--text-light);
      box-shadow: 0 45px 120px rgba(0, 0, 0, 0.88), inset 0 0 0 2px rgba(45, 212, 191, 0.28);
    }

    body:not(.in-overview) .slide:not(.active) {
      opacity: 0.24; filter: blur(1.5px) brightness(0.7);
    }
    body:not(.in-overview) .slide.active {
      opacity: 1; filter: none; cursor: default;
      box-shadow: 0 55px 150px rgba(0, 0, 0, 0.85), 0 0 0 4px rgba(20, 184, 166, 0.65);
      z-index: 15;
    }
    body.in-overview .slide:hover {
      box-shadow: 0 50px 130px rgba(20, 184, 166, 0.55), 0 0 0 12px #2DD4BF;
      z-index: 20;
    }

    /* Overview Macro-Badge */
    .overview-badge {
      position: absolute; inset: 0;
      background: linear-gradient(135deg, rgba(6, 16, 32, 0.90), rgba(11, 31, 54, 0.88));
      backdrop-filter: blur(8px);
      display: flex; flex-direction: column; justify-content: center; align-items: center;
      text-align: center; padding: 60px; opacity: 0; pointer-events: none;
      transition: opacity 0.4s ease; z-index: 40; border-radius: 26px;
    }
    body.in-overview .overview-badge { opacity: 1; }
    body.in-overview .slide:hover .overview-badge {
      background: linear-gradient(135deg, rgba(13, 148, 136, 0.94), rgba(6, 78, 59, 0.94));
    }
    .ov-num {
      font-family: var(--font-serif); font-size: 135px; font-weight: 800;
      line-height: 1; color: var(--gold-bright); margin-bottom: 18px;
      text-shadow: 0 10px 28px rgba(0,0,0,0.5);
    }
    .ov-short {
      font-size: 56px; font-weight: 800; color: #FFFFFF;
      line-height: 1.16; margin-bottom: 24px; max-width: 92%;
    }
    .ov-metric {
      display: inline-block; padding: 14px 38px; border-radius: 999px;
      background: rgba(255, 255, 255, 0.14); border: 2px solid rgba(255, 255, 255, 0.38);
      font-size: 38px; font-weight: 700; color: #5EEAD4;
    }

    /* =========================================================================
       SLIDE HEADER & EDITORIAL COMPONENTS
       ========================================================================= */
    .slide-header {
      position: relative; z-index: 2;
      margin-bottom: 24px; padding-bottom: 14px;
      border-bottom: 2px solid rgba(15, 23, 42, 0.08);
      display: flex; justify-content: space-between; align-items: center;
    }
    .header-left { display: flex; align-items: center; gap: 18px; max-width: 86%; }
    .station-pill {
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      width: 56px; height: 56px; border-radius: 16px;
      background: linear-gradient(135deg, var(--teal-deep), var(--teal-primary));
      color: #FFFFFF; font-family: var(--font-serif); font-size: 22px; font-weight: 800;
      box-shadow: 0 8px 20px rgba(13, 148, 136, 0.3); flex-shrink: 0;
    }
    .station-pill.gold { background: linear-gradient(135deg, #92400E, var(--gold-primary)); box-shadow: 0 8px 20px rgba(217, 119, 6, 0.3); }
    .station-pill.royal { background: linear-gradient(135deg, #1E3A8A, var(--royal)); box-shadow: 0 8px 20px rgba(29, 78, 216, 0.3); }
    .station-pill.crimson { background: linear-gradient(135deg, #7F1D1D, var(--crimson)); box-shadow: 0 8px 20px rgba(220, 38, 38, 0.3); }

    .eyebrow {
      font-size: 12.5px; font-weight: 800; letter-spacing: 0.14em;
      text-transform: uppercase; color: var(--teal-primary); margin-bottom: 4px;
    }
    .slide-title {
      font-family: var(--font-serif); font-size: 30px; font-weight: 800;
      line-height: 1.18; color: var(--text-main);
    }
    .shield-badge img {
      height: 58px; object-fit: contain;
      filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.12));
    }

    .slide-content {
      flex: 1; display: flex; position: relative; z-index: 2; min-height: 0;
    }

    /* Staggered Reveal */
    .reveal-item {
      opacity: 0; transform: translateY(20px);
      transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .slide.active .reveal-item:nth-child(1) { transition-delay: 0.10s; opacity: 1; transform: translateY(0); }
    .slide.active .reveal-item:nth-child(2) { transition-delay: 0.20s; opacity: 1; transform: translateY(0); }
    .slide.active .reveal-item:nth-child(3) { transition-delay: 0.30s; opacity: 1; transform: translateY(0); }
    .slide.active .reveal-item:nth-child(4) { transition-delay: 0.40s; opacity: 1; transform: translateY(0); }
    .slide.active .reveal-item:nth-child(5) { transition-delay: 0.50s; opacity: 1; transform: translateY(0); }
    .slide.active .reveal-item:nth-child(6) { transition-delay: 0.58s; opacity: 1; transform: translateY(0); }
    body.in-overview .reveal-item { opacity: 1; transform: none; }

    /* =========================================================================
       RICH INFOGRAPHIC & BENTO DESIGN SYSTEM
       ========================================================================= */
    .bento-card {
      background: rgba(255, 255, 255, 0.92);
      border-radius: 20px;
      padding: 24px 28px;
      border: 1px solid rgba(203, 213, 225, 0.75);
      box-shadow: 0 14px 35px rgba(15, 23, 42, 0.055);
      position: relative; overflow: hidden;
    }
    .bento-dark {
      background: linear-gradient(135deg, #07162C 0%, #0D2544 100%);
      color: #FFFFFF; border: 1px solid rgba(45, 212, 191, 0.3);
      box-shadow: 0 18px 40px rgba(7, 22, 44, 0.25);
    }
    .bento-emerald {
      background: linear-gradient(135deg, #064E3B 0%, #047857 100%);
      color: #FFFFFF; border: 1px solid rgba(110, 231, 183, 0.35);
    }
    .bento-gold {
      background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
      border: 1px solid #FCD34D;
    }
    .bento-crimson {
      background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
      border: 1px solid #FCA5A5;
    }

    .icon-circle {
      width: 48px; height: 48px; border-radius: 14px;
      display: inline-flex; align-items: center; justify-content: center;
      font-size: 22px; flex-shrink: 0;
      background: rgba(13, 148, 136, 0.12); color: var(--teal-primary);
    }
    .icon-circle.gold { background: rgba(217, 119, 6, 0.14); color: var(--gold-primary); }
    .icon-circle.royal { background: rgba(29, 78, 216, 0.12); color: var(--royal); }
    .icon-circle.crimson { background: rgba(220, 38, 38, 0.12); color: var(--crimson); }

    .tag-pill {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 4px 12px; border-radius: 999px;
      font-size: 11.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em;
    }
    .tag-teal { background: #CCFBF1; color: #0F766E; }
    .tag-gold { background: #FEF3C7; color: #B45309; }
    .tag-crimson { background: #FEE2E2; color: #B91C1C; }
    .tag-royal { background: #DBEAFE; color: #1D4ED8; }

    /* SVG Radial Donut Gauges */
    .gauge-ring {
      position: relative; width: 108px; height: 108px; flex-shrink: 0;
      display: flex; align-items: center; justify-content: center;
    }
    .gauge-ring svg {
      width: 100%; height: 100%; transform: rotate(-90deg);
    }
    .gauge-bg { fill: none; stroke: #E2E8F0; stroke-width: 10; }
    .gauge-val {
      fill: none; stroke-width: 10; stroke-linecap: round;
      stroke-dasharray: 283;
      stroke-dashoffset: 283;
      transition: stroke-dashoffset 1.4s cubic-bezier(0.22, 1, 0.36, 1) 0.3s;
    }
    .slide.active .gauge-val {
      stroke-dashoffset: calc(283 - (283 * var(--pct)) / 100);
    }
    body.in-overview .gauge-val {
      stroke-dashoffset: calc(283 - (283 * var(--pct)) / 100);
    }
    .gauge-label {
      position: absolute; font-family: var(--font-serif);
      font-size: 22px; font-weight: 800; color: var(--text-main);
    }

    /* Animated Progress Bars */
    .bar-track {
      width: 100%; height: 10px; background: rgba(203, 213, 225, 0.55);
      border-radius: 999px; margin-top: 8px; overflow: hidden;
    }
    .bar-fill {
      height: 100%; width: 0%; border-radius: 999px;
      transition: width 1.3s cubic-bezier(0.22, 1, 0.36, 1) 0.35s;
    }
    .slide.active .bar-fill, body.in-overview .bar-fill { width: var(--target-w, 100%); }

    /* Interactive Gallery Frame for Empirical Figures */
    .fig-showcase {
      background: #FFFFFF; border-radius: 20px; padding: 16px;
      border: 1px solid #E2E8F0;
      box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      position: relative; overflow: hidden;
    }
    .fig-showcase img {
      max-width: 100%; max-height: 380px; object-fit: contain;
      border-radius: 8px; cursor: zoom-in;
      transition: transform 0.3s ease;
    }
    .fig-showcase img:hover { transform: scale(1.025); }
    .fig-caption-bar {
      width: 100%; margin-top: 10px; padding-top: 8px;
      border-top: 1px solid #F1F5F9;
      display: flex; justify-content: space-between; align-items: center;
      font-size: 12px; font-weight: 700; color: var(--text-muted);
    }

    /* Editable mode outline */
    body.editing-active [contenteditable="true"] {
      outline: 2px dashed rgba(13, 148, 136, 0.6); outline-offset: 3px; border-radius: 4px; cursor: text;
    }
    body.editing-active [contenteditable="true"]:focus {
      outline: 2px solid var(--gold-bright); background: rgba(254, 243, 199, 0.25);
    }

    /* =========================================================================
       TOP NAV & BOTTOM HUD
       ========================================================================= */
    .top-nav {
      position: fixed; top: 14px; left: 50%; transform: translateX(-50%);
      z-index: 120; display: flex; align-items: center; gap: 6px;
      padding: 6px 12px; background: rgba(7, 14, 28, 0.86);
      backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 999px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
    }
    .nav-pill {
      background: transparent; border: none; color: #CBD5E1;
      font-family: var(--font-sans); font-size: 12px; font-weight: 700;
      padding: 6px 13px; border-radius: 999px; cursor: pointer;
      transition: all 0.2s ease; white-space: nowrap;
    }
    .nav-pill:hover { color: #FFFFFF; background: rgba(255, 255, 255, 0.1); }
    .nav-pill.active {
      background: linear-gradient(135deg, var(--teal-primary), #0F766E);
      color: #FFFFFF; box-shadow: 0 4px 12px rgba(13, 148, 136, 0.4);
    }
    .nav-pill.overview-btn { color: var(--gold-bright); border: 1px solid rgba(245, 158, 11, 0.4); }
    .nav-pill.overview-btn.active {
      background: linear-gradient(135deg, var(--gold-primary), #B45309); color: #FFFFFF;
    }

    .deck-hud {
      position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%);
      width: min(94vw, 1280px); height: 52px; padding: 0 24px;
      display: flex; justify-content: space-between; align-items: center;
      z-index: 120; border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      background: rgba(7, 14, 28, 0.88); backdrop-filter: blur(16px);
      color: #E2E8F0; box-shadow: 0 15px 40px rgba(0, 0, 0, 0.55);
    }
    .hud-left {
      font-size: 12.5px; color: #94A3B8; font-weight: 600;
      display: flex; align-items: center; gap: 10px;
    }
    .status-dot {
      width: 8px; height: 8px; border-radius: 50%;
      background: var(--emerald); box-shadow: 0 0 10px var(--emerald);
    }
    .hud-controls { display: flex; align-items: center; gap: 8px; }
    .btn-hud {
      background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1);
      color: #F8FAFC; cursor: pointer; font-family: var(--font-sans);
      font-size: 12.5px; font-weight: 600; display: flex; align-items: center; gap: 6px;
      padding: 6px 13px; border-radius: 999px; transition: all 0.2s ease;
    }
    .btn-hud:hover {
      background: rgba(20, 184, 166, 0.22); border-color: var(--teal-bright); color: #FFFFFF;
    }
    .btn-hud.active-toggle {
      background: var(--gold-primary); border-color: var(--gold-bright); color: #FFFFFF;
    }
    .slide-counter {
      font-size: 13px; font-weight: 800; letter-spacing: 0.06em;
      min-width: 68px; text-align: center; color: var(--gold-bright);
    }

    #notes-drawer {
      position: fixed; bottom: 80px; left: 50%;
      transform: translateX(-50%) translateY(150%);
      width: min(88vw, 980px); background: rgba(10, 18, 36, 0.96);
      color: #F8FAFC; border-radius: 16px; padding: 20px 28px;
      z-index: 150; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.75);
      border: 1px solid rgba(45, 212, 191, 0.35); backdrop-filter: blur(16px);
      transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }
    #notes-drawer.open { transform: translateX(-50%) translateY(0); }
    .notes-header {
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 8px; font-size: 12px; text-transform: uppercase;
      letter-spacing: 0.1em; color: var(--gold-bright); font-weight: 800;
    }
    .notes-content { font-size: 15px; line-height: 1.55; color: #E2E8F0; }

    #figure-lightbox {
      position: fixed; inset: 0; background: rgba(4, 9, 20, 0.94);
      backdrop-filter: blur(14px); z-index: 300; display: none;
      flex-direction: column; align-items: center; justify-content: center;
      padding: 40px; cursor: zoom-out;
    }
    #figure-lightbox.open { display: flex; }
    #figure-lightbox img {
      max-width: 92vw; max-height: 82vh; object-fit: contain;
      background: #FFFFFF; padding: 18px; border-radius: 14px;
      box-shadow: 0 30px 90px rgba(0, 0, 0, 0.8);
    }
    #figure-lightbox .lb-caption {
      margin-top: 16px; color: #F8FAFC; font-size: 16px; font-weight: 600;
    }
"""

SLIDES_HTML_PART1 = """
        <!-- SLIDE 1: PORTADA EDITORIAL DE ALTO IMPACTO -->
        <section class="slide theme-dark" id="slide-01" data-index="0">
          <div class="bg-watermark-num">01</div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.14); padding-bottom: 18px; position: relative; z-index: 2;">
            <div style="display: flex; align-items: center; gap: 22px;">
              <img src="assets/extracted/unan_logo_clean.png" alt="UNAN Managua" style="height: 76px; filter: drop-shadow(0 6px 14px rgba(0,0,0,0.65));">
              <div>
                <div style="font-size: 17px; font-weight: 800; letter-spacing: 0.05em; color: #FFFFFF;">UNIVERSIDAD NACIONAL AUTÓNOMA DE NICARAGUA, MANAGUA</div>
                <div style="font-size: 13.5px; font-weight: 700; color: var(--gold-bright); margin-top: 3px;">CENTRO UNIVERSITARIO REGIONAL DE ESTELÍ • RECINTO LEONEL RUGAMA RUGAMA</div>
                <div style="font-size: 12.5px; color: #94A3B8; margin-top: 2px;">Departamento de Educación y Humanidades • Carrera de Licenciatura en Psicología</div>
              </div>
            </div>
            <div style="display: flex; gap: 12px; align-items: center;">
              <div style="padding: 8px 18px; border-radius: 999px; background: rgba(16, 185, 129, 0.16); border: 1px solid rgba(52, 211, 153, 0.4); color: #6EE7B7; font-size: 12px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase;">🌿 Línea SAL-3 • Salud e Interculturalidad</div>
              <div style="padding: 8px 18px; border-radius: 999px; background: rgba(245, 158, 11, 0.16); border: 1px solid rgba(251, 191, 36, 0.4); color: #FCD34D; font-size: 12px; font-weight: 800;">Defensa Oral • 2026</div>
            </div>
          </div>

          <div style="flex: 1; display: grid; grid-template-columns: 1.32fr 0.68fr; gap: 40px; align-items: center; position: relative; z-index: 2;">
            <div>
              <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 8px; background: rgba(45, 212, 191, 0.12); color: #2DD4BF; font-size: 12px; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 16px;">
                ✦ Tesis para optar al título de Licenciados en Psicología
              </div>
              <h1 class="editable" style="font-family: var(--font-serif); font-size: 42px; line-height: 1.15; color: #FFFFFF; margin-bottom: 18px; text-shadow: 0 4px 20px rgba(0,0,0,0.4);">
                La Medicina Tradicional, Complementaria e Integrativa (<span style="color: #5EEAD4;">MTCI</span>) como Complemento en la Atención Psicológica
              </h1>
              <p class="editable" style="font-size: 18px; color: #CBD5E1; line-height: 1.5; margin-bottom: 26px;">
                Estudio Mixto Secuencial con Estudiantes y Docentes del CUR-Estelí y Facilitadores Locales del Municipio de Estelí
              </p>

              <!-- 3 Pill KPIs on Cover -->
              <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
                <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-left: 4px solid #2DD4BF; padding: 12px 16px; border-radius: 12px;">
                  <div style="font-family: var(--font-serif); font-size: 26px; font-weight: 800; color: #FFFFFF;">N = 86</div>
                  <div style="font-size: 12px; color: #94A3B8; font-weight: 600;">Muestra Triangulada</div>
                </div>
                <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-left: 4px solid #F59E0B; padding: 12px 16px; border-radius: 12px;">
                  <div style="font-family: var(--font-serif); font-size: 26px; font-weight: 800; color: #FCD34D;">DEXPLIS</div>
                  <div style="font-size: 12px; color: #94A3B8; font-weight: 600;">Diseño Mixto 3 Fases</div>
                </div>
                <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-left: 4px solid #60A5FA; padding: 12px 16px; border-radius: 12px;">
                  <div style="font-family: var(--font-serif); font-size: 26px; font-weight: 800; color: #93C5FD;">8 Módulos</div>
                  <div style="font-size: 12px; color: #94A3B8; font-weight: 600;">Manual Clínico MTCI</div>
                </div>
              </div>
            </div>

            <!-- Right Visual Showcase Card -->
            <div style="background: linear-gradient(145deg, rgba(15, 35, 62, 0.9), rgba(7, 20, 38, 0.95)); border: 1px solid rgba(45, 212, 191, 0.3); border-radius: 22px; padding: 24px; box-shadow: 0 25px 60px rgba(0,0,0,0.5);">
              <div style="font-size: 11.5px; font-weight: 800; letter-spacing: 0.12em; color: var(--gold-bright); text-transform: uppercase; margin-bottom: 12px;">👥 Equipo Investigador Sustentante</div>
              <div class="editable" style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 12px; background: rgba(255,255,255,0.05); padding: 10px 14px; border-radius: 10px;">
                  <span style="width: 32px; height: 32px; border-radius: 50%; background: #0D9488; color: #FFF; display: inline-flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px;">DF</span>
                  <span style="font-size: 15px; font-weight: 700; color: #FFFFFF;">Br. Dina Fabiola García Torres</span>
                </div>
                <div style="display: flex; align-items: center; gap: 12px; background: rgba(255,255,255,0.05); padding: 10px 14px; border-radius: 10px;">
                  <span style="width: 32px; height: 32px; border-radius: 50%; background: #D97706; color: #FFF; display: inline-flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px;">TP</span>
                  <span style="font-size: 15px; font-weight: 700; color: #FFFFFF;">Br. Tatiana Paola López Ramos</span>
                </div>
                <div style="display: flex; align-items: center; gap: 12px; background: rgba(255,255,255,0.05); padding: 10px 14px; border-radius: 10px;">
                  <span style="width: 32px; height: 32px; border-radius: 50%; background: #2563EB; color: #FFF; display: inline-flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px;">EE</span>
                  <span style="font-size: 15px; font-weight: 700; color: #FFFFFF;">Br. Engel Enoc Zamora Velásquez</span>
                </div>
              </div>
              <div style="border-top: 1px solid rgba(255,255,255,0.12); padding-top: 14px;">
                <div style="font-size: 11px; font-weight: 800; letter-spacing: 0.1em; color: #2DD4BF; text-transform: uppercase;">Tutora Académica y Metodológica</div>
                <div class="editable" style="font-size: 16px; font-weight: 800; color: #FFFFFF; margin-top: 4px;">Dra. Tania Libertad Pérez Guevara</div>
                <div style="font-size: 12.5px; color: #94A3B8; margin-top: 2px;">Docente titular • UNAN-Managua CUR-Estelí</div>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 2: PLANTEAMIENTO (BALANZA JURÍDICA Y BENTO DE JUSTIFICACIÓN) -->
        <section class="slide" id="slide-02" data-index="1">
          <div class="bg-watermark-num">02</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill">02</div>
              <div>
                <div class="eyebrow">Capítulo I • Introducción y Delimitación del Problema</div>
                <h2 class="slide-title editable">Asimetría Normativa, Ocultamiento Clínico y Justificación</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="display: grid; grid-template-columns: 1.08fr 0.92fr; gap: 32px;">
            <!-- Left: Visual Tension Diagram -->
            <div class="reveal-item" style="display: flex; flex-direction: column; justify-content: space-between; gap: 14px;">
              <!-- Contrast Scale: Ley 774 vs Ley 292 -->
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                <div class="bento-card" style="background: linear-gradient(135deg, #ECFDF5, #D1FAE5); border-color: #6EE7B7; padding: 18px 20px;">
                  <div class="tag-pill tag-teal" style="margin-bottom: 8px;">⚖ Apertura Sanitaria</div>
                  <div style="font-family: var(--font-serif); font-size: 20px; font-weight: 800; color: #065F46; margin-bottom: 6px;">Ley No. 774 (2012)</div>
                  <p class="editable" style="font-size: 13.5px; color: #064E3B; line-height: 1.45;">Garantiza el derecho ciudadano a la medicina natural y terapias complementarias en el Sistema Nacional de Salud.</p>
                </div>
                <div class="bento-card bento-crimson" style="padding: 18px 20px;">
                  <div class="tag-pill tag-crimson" style="margin-bottom: 8px;">🚫 Límite Prescriptivo</div>
                  <div style="font-family: var(--font-serif); font-size: 20px; font-weight: 800; color: #991B1B; margin-bottom: 6px;">Ley No. 292 (1998)</div>
                  <p class="editable" style="font-size: 13.5px; color: #7F1D1D; line-height: 1.45;">Inhabilita taxativamente al psicólogo para recetar fármacos o prescribir dosis de preparados fitoterapéuticos.</p>
                </div>
              </div>

              <!-- Consequence: Ocultamiento Terapéutico -->
              <div class="bento-card" style="display: flex; gap: 18px; align-items: center; padding: 18px 22px; border-left: 6px solid var(--crimson);">
                <div class="icon-circle crimson" style="width: 54px; height: 54px; font-size: 26px;">🔇</div>
                <div class="editable">
                  <div style="font-size: 16px; font-weight: 800; color: var(--text-main); margin-bottom: 4px;">Fenómeno Clínico: El «Ocultamiento Terapéutico»</div>
                  <p style="font-size: 13.8px; color: var(--text-body); line-height: 1.45;">Los consultantes consumen fitoterapia y acuden a sobadores, pero lo silencian en psicoterapia por temor al juicio clínico, impidiendo detectar interacciones con psicofármacos.</p>
                </div>
              </div>

              <!-- Central Research Question Banner -->
              <div class="bento-dark" style="padding: 20px 24px; border-radius: 18px;">
                <div style="font-size: 11.5px; font-weight: 800; color: var(--gold-bright); letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 6px;">❓ Pregunta Central de Investigación</div>
                <p class="editable" style="font-family: var(--font-serif); font-size: 17.5px; font-style: italic; color: #FFFFFF; line-height: 1.4;">
                  «¿Cómo fundamenta el diagnóstico sobre la integración de las MTCI en estudiantes, docentes y facilitadores locales el diseño de un manual ético y pedagógico en el CUR-Estelí?»
                </p>
              </div>
            </div>

            <!-- Right: 2x2 Bento Matrix for Justification -->
            <div class="reveal-item" style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 14px;">
              <div class="bento-card" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div class="icon-circle">🛡️</div>
                <div class="editable">
                  <div style="font-size: 16px; font-weight: 800; color: var(--text-main); margin-bottom: 6px;">Seguridad y No Maleficencia</div>
                  <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.45;">Previene interacciones fitofarmacológicas adversas mediante el tamizaje clínico sistemático en la entrevista inicial.</p>
                </div>
              </div>
              <div class="bento-card" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div class="icon-circle gold">🌿</div>
                <div class="editable">
                  <div style="font-size: 16px; font-weight: 800; color: var(--text-main); margin-bottom: 6px;">Pertinencia Intercultural</div>
                  <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.45;">Reconoce la tradición etnobotánica segoviana y promueve el respeto a la cosmovisión del usuario en Estelí.</p>
                </div>
              </div>
              <div class="bento-card" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div class="icon-circle royal">🏥</div>
                <div class="editable">
                  <div style="font-size: 16px; font-weight: 800; color: var(--text-main); margin-bottom: 6px;">Clínica Psicosocial CUR-Estelí</div>
                  <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.45;">Fortalece las competencias de discernimiento ético y derivación segura en practicantes de 4.º y 5.º año.</p>
                </div>
              </div>
              <div class="bento-card bento-gold" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div class="icon-circle gold" style="background: rgba(180,83,9,0.18);">📘</div>
                <div class="editable">
                  <div style="font-size: 16px; font-weight: 800; color: #78350F; margin-bottom: 6px;">Aporte Instrumental Inédito</div>
                  <p style="font-size: 13.5px; color: #92400E; line-height: 1.45;">Formaliza el Manual de Estrategias MTCI (18 págs., Anexo 16.2) con algoritmos clínicos e inventario I-CAM-Q.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 3: ANTECEDENTES (LÍNEA DE TIEMPO ARQUITECTÓNICA) -->
        <section class="slide" id="slide-03" data-index="2">
          <div class="bg-watermark-num">03</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill">03</div>
              <div>
                <div class="eyebrow">Capítulo I • Estado del Arte y Evolución Científica</div>
                <h2 class="slide-title editable">Antecedentes de la Investigación: Escala Global, Regional y Nacional</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="flex-direction: column; justify-content: space-between;">
            <!-- Connecting Timeline Track -->
            <div style="position: relative; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 28px; flex: 1;">
              <!-- Stage 1 -->
              <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between; border-top: 6px solid var(--teal-primary);">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <span class="tag-pill tag-teal">🌍 Escala Internacional</span>
                    <span style="font-family: var(--font-serif); font-size: 28px; font-weight: 800; color: var(--teal-primary);">2014–2019</span>
                  </div>
                  <h3 style="font-family: var(--font-serif); font-size: 21px; color: var(--text-main); margin-bottom: 12px;">Directrices OMS y Evidencia Clínica</h3>
                  <div class="editable" style="font-size: 14px; color: var(--text-body); line-height: 1.55;">
                    <p style="margin-bottom: 10px;">• <b>Estrategia OMS MTCI (2014–2025):</b> Exhorta a los Estados a articular saberes tradicionales con medicina basada en evidencia.</p>
                    <p style="margin-bottom: 10px;">• <b>Furlan et al. (2012) y Guo et al. (2024):</b> Metanálisis confirman eficacia de masoterapia en dolor miofascial y reducción de cortisol.</p>
                    <p>• <b>Sotiropoulos et al. (2025):</b> Validan técnicas somáticas <i>Bottom-Up</i> como coadyuvantes en ansiedad y depresión.</p>
                  </div>
                </div>
                <div style="padding: 10px 14px; border-radius: 10px; background: #F0FDF4; border: 1px solid #BBF7D0; font-size: 12.5px; font-weight: 700; color: #166534;">
                  ✓ Consenso: Eficacia psicofisiológica comprobada
                </div>
              </div>

              <!-- Stage 2 -->
              <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between; border-top: 6px solid var(--gold-primary);">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <span class="tag-pill tag-gold">🌎 Escala Latinoamericana</span>
                    <span style="font-family: var(--font-serif); font-size: 28px; font-weight: 800; color: var(--gold-primary);">2020–2023</span>
                  </div>
                  <h3 style="font-family: var(--font-serif); font-size: 21px; color: var(--text-main); margin-bottom: 12px;">Educación Superior en Iberoamérica</h3>
                  <div class="editable" style="font-size: 14px; color: var(--text-body); line-height: 1.55;">
                    <p style="margin-bottom: 10px;">• <b>Papalini (2022) y estudios en Chile/Colombia:</b> Documentan alta receptividad hacia las MTCI en facultades de Psicología y Salud.</p>
                    <p style="margin-bottom: 10px;">• <b>Asimetría Formativa:</b> Más del 80% del alumnado emplea MTCI en su autocuidado, pero reporta ausencia de formación universitaria.</p>
                    <p>• <b>Riesgo Clínico:</b> Inexistencia de protocolos de interconsulta entre psicólogos y terapeutas tradicionales.</p>
                  </div>
                </div>
                <div style="padding: 10px 14px; border-radius: 10px; background: #FFFBEB; border: 1px solid #FDE68A; font-size: 12.5px; font-weight: 700; color: #92400E;">
                  ⚠ Hallazgo: Alta apertura vs. orfandad curricular
                </div>
              </div>

              <!-- Stage 3 -->
              <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between; border-top: 6px solid var(--royal);">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <span class="tag-pill tag-royal">🇳🇮 Escala Nacional y Local</span>
                    <span style="font-family: var(--font-serif); font-size: 28px; font-weight: 800; color: var(--royal);">2024–2026</span>
                  </div>
                  <h3 style="font-family: var(--font-serif); font-size: 21px; color: var(--text-main); margin-bottom: 12px;">Nicaragua y UNAN-Managua CUR-Estelí</h3>
                  <div class="editable" style="font-size: 14px; color: var(--text-body); line-height: 1.55;">
                    <p style="margin-bottom: 10px;">• <b>Vanguardia Jurídica:</b> Nicaragua lidera en la región con las Leyes No. 774 y 759 y las clínicas de Medicina Natural del MINSA.</p>
                    <p style="margin-bottom: 10px;">• <b>Vacío en Psicología:</b> La malla curricular aún no incorpora pautas deontológicas para articular psicología y medicina tradicional.</p>
                    <p>• <b>Aporte Pionero (2026):</b> Primer estudio mixto en Estelí que une academia y territorio en un manual operativo.</p>
                  </div>
                </div>
                <div style="padding: 10px 14px; border-radius: 10px; background: #EFF6FF; border: 1px solid #BFDBFE; font-size: 12.5px; font-weight: 700; color: #1E40AF;">
                  ★ Hito: Primer estudio triangulado en el CUR-Estelí
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 4: CONTEXTO TERRITORIAL (PUENTE ECOSISTÉMICO ESTELÍ - UNAN) -->
        <section class="slide" id="slide-04" data-index="3">
          <div class="bg-watermark-num">04</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill">04</div>
              <div>
                <div class="eyebrow">Capítulo I • Delimitación Espacial y Sociocultural</div>
                <h2 class="slide-title editable">Contexto del Estudio: Ecosistema Territorial de Estelí y CUR-Estelí</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="display: grid; grid-template-columns: 1fr 160px 1fr; gap: 20px; align-items: stretch;">
            <!-- Left: Territorio de Estelí -->
            <div class="reveal-item bento-card" style="background: linear-gradient(160deg, #FFFFFF 0%, #F0FDF4 100%); border-color: #86EFAC; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div class="tag-pill tag-teal" style="margin-bottom: 10px;">🌿 Territorio Comunitario • Las Segovias</div>
                <h3 style="font-family: var(--font-serif); font-size: 24px; color: #064E3B; margin-bottom: 16px;">Municipio de Estelí</h3>
                <div class="editable" style="display: flex; flex-direction: column; gap: 14px;">
                  <div style="background: #FFFFFF; padding: 14px 16px; border-radius: 14px; border-left: 4px solid var(--teal-primary); box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                    <div style="font-size: 15px; font-weight: 800; color: var(--text-main);">Acervo Etnobotánico Vivo</div>
                    <p style="font-size: 13.5px; color: var(--text-body); margin-top: 3px;">Uso arraigado de infusiones calmantes (manzanilla, valeriana, tilo), sobandería y bálsamos naturales en el entorno familiar.</p>
                  </div>
                  <div style="background: #FFFFFF; padding: 14px 16px; border-radius: 14px; border-left: 4px solid var(--teal-primary); box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                    <div style="font-size: 15px; font-weight: 800; color: var(--text-main);">Facilitadores con Arraigo Local</div>
                    <p style="font-size: 13.5px; color: var(--text-body); margin-top: 3px;">Terapeutas comunitarios que reciben diariamente pacientes con somatizaciones, contracturas crónicas, insomnio y duelos.</p>
                  </div>
                </div>
              </div>
              <div style="font-size: 13px; font-weight: 700; color: #047857; padding-top: 10px; border-top: 1px dashed #6EE7B7;">
                📍 Primer eslabón de contención somática comunitaria
              </div>
            </div>

            <!-- Center Bridge: El Puente Intercultural -->
            <div class="reveal-item" style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 12px;">
              <div style="width: 100%; padding: 18px 10px; border-radius: 20px; background: linear-gradient(180deg, #07162C, #0F2942); color: #FFFFFF; box-shadow: 0 14px 30px rgba(0,0,0,0.2); border: 2px solid var(--gold-bright);">
                <div style="font-size: 32px; margin-bottom: 6px;">🌉</div>
                <div style="font-size: 12px; font-weight: 800; color: var(--gold-bright); text-transform: uppercase; letter-spacing: 0.08em;">Puente de Articulación</div>
                <div style="font-size: 11.5px; color: #CBD5E1; margin-top: 6px; line-height: 1.35;">Supera el aislamiento entre clínica y comunidad mediante el <b>Manual MTCI</b></div>
              </div>
            </div>

            <!-- Right: UNAN-Managua CUR-Estelí -->
            <div class="reveal-item bento-card" style="background: linear-gradient(160deg, #FFFFFF 0%, #EFF6FF 100%); border-color: #93C5FD; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div class="tag-pill tag-royal" style="margin-bottom: 10px;">🎓 Espacio Académico y Clínico</div>
                <h3 style="font-family: var(--font-serif); font-size: 24px; color: #1E3A8A; margin-bottom: 16px;">UNAN-Managua • CUR-Estelí</h3>
                <div class="editable" style="display: flex; flex-direction: column; gap: 14px;">
                  <div style="background: #FFFFFF; padding: 14px 16px; border-radius: 14px; border-left: 4px solid var(--royal); box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                    <div style="font-size: 15px; font-weight: 800; color: var(--text-main);">Clínica Psicosocial Universitaria</div>
                    <p style="font-size: 13.5px; color: var(--text-body); margin-top: 3px;">Escenario real de atención donde estudiantes de 4.º y 5.º año conducen procesos psicoterapéuticos supervisados.</p>
                  </div>
                  <div style="background: #FFFFFF; padding: 14px 16px; border-radius: 14px; border-left: 4px solid var(--gold-primary); box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                    <div style="font-size: 15px; font-weight: 800; color: var(--text-main);">Reto Curricular y Deontológico</div>
                    <p style="font-size: 13.5px; color: var(--text-body); margin-top: 3px;">Dotar a futuros psicólogos de herramientas de tamizaje (I-CAM-Q), psicoeducación y derivación interprofesional segura.</p>
                  </div>
                </div>
              </div>
              <div style="font-size: 13px; font-weight: 700; color: #1D4ED8; padding-top: 10px; border-top: 1px dashed #93C5FD;">
                🏛️ Recinto Universitario «Leonel Rugama Rugama»
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 5: OBJETIVOS (ARQUITECTURA JERÁRQUICA CON INDICADORES) -->
        <section class="slide" id="slide-05" data-index="4">
          <div class="bg-watermark-num">05</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill">05</div>
              <div>
                <div class="eyebrow">Capítulo I • Direccionamiento Científico del Estudio</div>
                <h2 class="slide-title editable">Sistema de Objetivos: General y Específicos</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="flex-direction: column; justify-content: space-between; gap: 22px;">
            <!-- Monumental General Objective Banner -->
            <div class="reveal-item bento-dark" style="padding: 24px 32px; display: flex; align-items: center; gap: 26px; border-left: 8px solid var(--gold-bright);">
              <div style="width: 72px; height: 72px; border-radius: 20px; background: rgba(245, 158, 11, 0.18); border: 2px solid var(--gold-bright); display: flex; align-items: center; justify-content: center; font-family: var(--font-serif); font-size: 28px; font-weight: 800; color: var(--gold-bright); flex-shrink: 0;">OG</div>
              <div>
                <div style="font-size: 12px; font-weight: 800; color: var(--gold-bright); text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 6px;">Objetivo General de la Investigación</div>
                <p class="editable" style="font-family: var(--font-serif); font-size: 21px; font-weight: 600; line-height: 1.38; color: #FFFFFF;">
                  Analizar la integración de la Medicina Tradicional, Complementaria e Integrativa (MTCI) como recurso complementario en la atención psicológica, a partir de las percepciones, conocimientos y prácticas de estudiantes, docentes y facilitadores locales, formulando un manual de estrategias bioéticas y formativas en el CUR-Estelí.
                </p>
              </div>
            </div>

            <!-- 3 Specific Objectives Sculptural Cards -->
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; flex: 1;">
              <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between; border-bottom: 6px solid var(--teal-primary);">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <span class="tag-pill tag-teal">Objetivo Específico 1</span>
                    <span style="font-family: var(--font-serif); font-size: 22px; font-weight: 800; color: var(--teal-primary);">n = 68</span>
                  </div>
                  <h3 style="font-family: var(--font-serif); font-size: 20px; color: var(--text-main); margin-bottom: 10px;">Diagnóstico en Estudiantes</h3>
                  <p class="editable" style="font-size: 14.5px; color: var(--text-body); line-height: 1.52;">Caracterizar la percepción, nivel de conocimiento conceptual y normativo, frecuencia de uso y barreras autopercibidas en los estudiantes de 4.º y 5.º año de Psicología.</p>
                </div>
                <div style="font-size: 12px; font-weight: 800; color: var(--teal-primary); text-transform: uppercase; letter-spacing: 0.06em;">📊 Instrumento I1 • Censo Estudiantil</div>
              </div>

              <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between; border-bottom: 6px solid var(--gold-primary);">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <span class="tag-pill tag-gold">Objetivo Específico 2</span>
                    <span style="font-family: var(--font-serif); font-size: 22px; font-weight: 800; color: var(--gold-primary);">n = 9</span>
                  </div>
                  <h3 style="font-family: var(--font-serif); font-size: 20px; color: var(--text-main); margin-bottom: 10px;">Facilitadores Locales (Estelí)</h3>
                  <p class="editable" style="font-size: 14.5px; color: var(--text-body); line-height: 1.52;">Explorar las experiencias terapéuticas, modalidades aplicadas, efectos somáticos/afectivos y barreras socioculturales que enfrentan los facilitadores tradicionales.</p>
                </div>
                <div style="font-size: 12px; font-weight: 800; color: var(--gold-primary); text-transform: uppercase; letter-spacing: 0.06em;">🌿 Instrumento I2 • Muestreo Intencional</div>
              </div>

              <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between; border-bottom: 6px solid var(--royal);">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <span class="tag-pill tag-royal">Objetivo Específico 3</span>
                    <span style="font-family: var(--font-serif); font-size: 22px; font-weight: 800; color: var(--royal);">n = 9 + Manual</span>
                  </div>
                  <h3 style="font-family: var(--font-serif); font-size: 20px; color: var(--text-main); margin-bottom: 10px;">Claustro Docente y Propuesta</h3>
                  <p class="editable" style="font-size: 14.5px; color: var(--text-body); line-height: 1.52;">Diseñar un Manual de Estrategias de MTCI para la formación y práctica psicológica, sustentado en los criterios del claustro docente y los hallazgos empíricos.</p>
                </div>
                <div style="font-size: 12px; font-weight: 800; color: var(--royal); text-transform: uppercase; letter-spacing: 0.06em;">📘 Instrumento I3 + Anexo 16.2 (18 págs.)</div>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 6: MARCO TEÓRICO 1 (TRÍADA EPISTEMOLÓGICA VISUAL) -->
        <section class="slide" id="slide-06" data-index="5">
          <div class="bg-watermark-num">06</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill gold">06</div>
              <div>
                <div class="eyebrow">Capítulo II • Fundamentación Epistemológica (1/2)</div>
                <h2 class="slide-title editable">Tríada Teórica: Biopsicosocial, Pluralismo Médico y Bioética</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px;">
            <!-- Pillar 1 -->
            <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 16px;">
                  <div class="icon-circle" style="width: 56px; height: 56px; font-size: 26px;">🧠</div>
                  <div>
                    <div class="tag-pill tag-teal">Pilar 01 • Psicofisiología</div>
                    <div style="font-size: 13px; font-weight: 800; color: var(--text-muted); margin-top: 3px;">Engel (1977) • Babic et al. (2024)</div>
                  </div>
                </div>
                <h3 style="font-family: var(--font-serif); font-size: 22px; color: var(--text-main); margin-bottom: 12px;">Modelo Biopsicosocial y Vía Bottom-Up</h3>
                <div class="editable" style="font-size: 14px; color: var(--text-body); line-height: 1.55;">
                  <p style="margin-bottom: 10px;">• Supera el dualismo cartesiano integrando cuerpo, psique y entorno sociocultural.</p>
                  <p style="margin-bottom: 10px;">• <b>Regulación Bottom-Up:</b> Las aferencias periféricas (relajación miofascial, respiración vagal) calman la hiperreactividad amigdalina antes de la reestructuración cognitiva.</p>
                </div>
              </div>
              <div style="padding: 12px 16px; border-radius: 12px; background: #F0FDFA; border-left: 4px solid var(--teal-primary); font-size: 13px; font-weight: 700; color: #0F766E;">
                Cuerpo calmado → Mente receptiva al diálogo clínico
              </div>
            </div>

            <!-- Pillar 2 -->
            <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 16px;">
                  <div class="icon-circle gold" style="width: 56px; height: 56px; font-size: 26px;">🤝</div>
                  <div>
                    <div class="tag-pill tag-gold">Pilar 02 • Antropología</div>
                    <div style="font-size: 13px; font-weight: 800; color: var(--text-muted); margin-top: 3px;">Menéndez (2020) • OMS (2025)</div>
                  </div>
                </div>
                <h3 style="font-family: var(--font-serif); font-size: 22px; color: var(--text-main); margin-bottom: 12px;">Pluralismo Médico e Interculturalidad</h3>
                <div class="editable" style="font-size: 14px; color: var(--text-body); line-height: 1.55;">
                  <p style="margin-bottom: 10px;">• En Latinoamérica coexisten el Modelo Médico Hegemónico, la medicina tradicional comunitaria y la autoatención familiar.</p>
                  <p style="margin-bottom: 10px;">• <b>Alianza Terapéutica Cultural:</b> Validar los itinerarios terapéuticos del usuario disuelve el ocultamiento y fortalece la adherencia.</p>
                </div>
              </div>
              <div style="padding: 12px 16px; border-radius: 12px; background: #FFFBEB; border-left: 4px solid var(--gold-primary); font-size: 13px; font-weight: 700; color: #B45309;">
                Articulación respetuosa sin asimilación acrítica
              </div>
            </div>

            <!-- Pillar 3 -->
            <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 16px;">
                  <div class="icon-circle royal" style="width: 56px; height: 56px; font-size: 26px;">⚖️</div>
                  <div>
                    <div class="tag-pill tag-royal">Pilar 03 • Deontología</div>
                    <div style="font-size: 13px; font-weight: 800; color: var(--text-muted); margin-top: 3px;">Beauchamp & Childress (2019)</div>
                  </div>
                </div>
                <h3 style="font-family: var(--font-serif); font-size: 22px; color: var(--text-main); margin-bottom: 12px;">Principios Bioéticos y Frontera Legal</h3>
                <div class="editable" style="font-size: 14px; color: var(--text-body); line-height: 1.55;">
                  <p style="margin-bottom: 10px;">• <b>No Maleficencia:</b> Detectar posibles efectos hepatotóxicos o interacciones planta-psicofármaco.</p>
                  <p style="margin-bottom: 10px;">• <b>Autonomía y Beneficencia:</b> Consentimiento informado y respeto a los valores del paciente.</p>
                  <p>• <b>Delimitación:</b> Psicoeducar y derivar, nunca recetar.</p>
                </div>
              </div>
              <div style="padding: 12px 16px; border-radius: 12px; background: #EFF6FF; border-left: 4px solid var(--royal); font-size: 13px; font-weight: 700; color: #1D4ED8;">
                Rigor deontológico contra el intrusismo profesional
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 7: MARCO TEÓRICO 2 (SEMÁFORO LEGAL Y RUTA NEUROBIOLÓGICA) -->
        <section class="slide" id="slide-07" data-index="6">
          <div class="bg-watermark-num">07</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill gold">07</div>
              <div>
                <div class="eyebrow">Capítulo II • Marco Jurídico y Evidencia Clínica (2/2)</div>
                <h2 class="slide-title editable">Legislación Sanitaria Nicaragüense y Mecanismos Neurobiológicos</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="display: grid; grid-template-columns: 1fr 1fr; gap: 32px;">
            <!-- Left: Legal Architecture -->
            <div class="reveal-item" style="display: flex; flex-direction: column; justify-content: space-between; gap: 14px;">
              <div style="font-size: 13px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em;">🏛️ Ordenamiento Jurídico en Nicaragua</div>
              <div class="bento-card" style="border-left: 6px solid var(--teal-primary); padding: 18px 22px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                  <span style="font-family: var(--font-serif); font-size: 19px; font-weight: 800; color: var(--teal-deep);">Ley No. 774 (2012)</span>
                  <span class="tag-pill tag-teal">Habilitación Institucional</span>
                </div>
                <p class="editable" style="font-size: 13.8px; color: var(--text-body); line-height: 1.45;">Ley de Medicina Natural, Terapias Complementarias y Productos Naturales: integra las MTCI al modelo de salud familiar y comunitario (MOSAFC-MINSA).</p>
              </div>

              <div class="bento-card bento-crimson" style="border-left: 6px solid var(--crimson); padding: 18px 22px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                  <span style="font-family: var(--font-serif); font-size: 19px; font-weight: 800; color: #991B1B;">Ley No. 292 (1998)</span>
                  <span class="tag-pill tag-crimson">Frontera Deontológica</span>
                </div>
                <p class="editable" style="font-size: 13.8px; color: #7F1D1D; line-height: 1.45;">Ley de Medicamentos y Farmacias: circunscribe la facultad de prescribir exclusivamente a profesionales médicos, odontólogos y veterinarios.</p>
              </div>

              <div class="bento-card" style="border-left: 6px solid var(--gold-primary); padding: 18px 22px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                  <span style="font-family: var(--font-serif); font-size: 19px; font-weight: 800; color: var(--gold-deep);">Ley No. 759 (2011)</span>
                  <span class="tag-pill tag-gold">Patrimonio Cultural</span>
                </div>
                <p class="editable" style="font-size: 13.8px; color: var(--text-body); line-height: 1.45;">Ley de Medicina Tradicional Ancestral: protege los saberes terapéuticos comunitarios y promueve la articulación intercultural con el sistema público.</p>
              </div>
            </div>

            <!-- Right: Clinical & Neurobiological Evidence -->
            <div class="reveal-item" style="display: flex; flex-direction: column; justify-content: space-between; gap: 14px;">
              <div style="font-size: 13px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em;">🧬 Mecanismos de Acción Psicofisiológica</div>
              <div class="bento-card" style="display: flex; gap: 16px; align-items: center; padding: 18px 22px;">
                <div class="icon-circle" style="width: 52px; height: 52px; font-size: 24px;">🍵</div>
                <div class="editable">
                  <div style="font-size: 16px; font-weight: 800; color: var(--text-main);">Fitoterapia y Modulación GABAérgica</div>
                  <p style="font-size: 13.5px; color: var(--text-body); margin-top: 3px; line-height: 1.45;">Flavonoides de <i>Matricaria chamomilla</i> (manzanilla) y <i>Passiflora incarnata</i> actúan como moduladores alostéricos de receptores GABA-A, reduciendo ansiedad leve.</p>
                </div>
              </div>

              <div class="bento-card" style="display: flex; gap: 16px; align-items: center; padding: 18px 22px;">
                <div class="icon-circle royal" style="width: 52px; height: 52px; font-size: 24px;">🫁</div>
                <div class="editable">
                  <div style="font-size: 16px; font-weight: 800; color: var(--text-main);">Técnicas Mente-Cuerpo y Tono Vagal</div>
                  <p style="font-size: 13.5px; color: var(--text-body); margin-top: 3px; line-height: 1.45;">La respiración diafragmática lenta y la relajación progresiva activan el freno vagal parasimpático, elevando la variabilidad cardíaca (HRV) y bajando el cortisol.</p>
                </div>
              </div>

              <div class="bento-card" style="display: flex; gap: 16px; align-items: center; padding: 18px 22px;">
                <div class="icon-circle gold" style="width: 52px; height: 52px; font-size: 24px;">👐</div>
                <div class="editable">
                  <div style="font-size: 16px; font-weight: 800; color: var(--text-main);">Masoterapia y Desbloqueo Afectivo</div>
                  <p style="font-size: 13.5px; color: var(--text-body); margin-top: 3px; line-height: 1.45;">La estimulación de mecanorreceptores cutáneos libera oxitocina endógena, reduce la coraza muscular somática y facilita la catarsis verbal en terapia.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 8: METODOLOGÍA 1 (PIPELINE SECUENCIAL DEXPLIS) -->
        <section class="slide" id="slide-08" data-index="7">
          <div class="bg-watermark-num">08</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill royal">08</div>
              <div>
                <div class="eyebrow">Capítulo III • Diseño Metodológico (1/2)</div>
                <h2 class="slide-title editable">Paradigma Pragmático y Ruta Mixta Secuencial (DEXPLIS)</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="flex-direction: column; justify-content: space-between; gap: 22px;">
            <!-- Top 4 Methodological Attributes -->
            <div class="reveal-item" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px;">
              <div class="bento-card" style="padding: 18px 20px; border-top: 4px solid var(--teal-primary);">
                <div style="font-size: 11.5px; font-weight: 800; color: var(--teal-primary); text-transform: uppercase;">🧭 Paradigma</div>
                <div style="font-family: var(--font-serif); font-size: 22px; font-weight: 800; color: var(--text-main); margin: 4px 0;">Pragmático</div>
                <p class="editable" style="font-size: 13px; color: var(--text-body);">Orientado a soluciones clínicas y pedagógicas reales en el CUR-Estelí.</p>
              </div>
              <div class="bento-card" style="padding: 18px 20px; border-top: 4px solid var(--gold-primary);">
                <div style="font-size: 11.5px; font-weight: 800; color: var(--gold-primary); text-transform: uppercase;">🔄 Enfoque y Diseño</div>
                <div style="font-family: var(--font-serif); font-size: 22px; font-weight: 800; color: var(--text-main); margin: 4px 0;">Mixto DEXPLIS</div>
                <p class="editable" style="font-size: 13px; color: var(--text-body);">Secuencial (CUAN → CUAL → Propuesta) de Hernández-Sampieri.</p>
              </div>
              <div class="bento-card" style="padding: 18px 20px; border-top: 4px solid var(--royal);">
                <div style="font-size: 11.5px; font-weight: 800; color: var(--royal); text-transform: uppercase;">⏱️ Alcance y Corte</div>
                <div style="font-family: var(--font-serif); font-size: 22px; font-weight: 800; color: var(--text-main); margin: 4px 0;">Transversal</div>
                <p class="editable" style="font-size: 13px; color: var(--text-body);">Descriptivo-propositivo ejecutado en el II Semestre de 2026.</p>
              </div>
              <div class="bento-card" style="padding: 18px 20px; border-top: 4px solid var(--emerald);">
                <div style="font-size: 11.5px; font-weight: 800; color: var(--emerald); text-transform: uppercase;">📐 Validación</div>
                <div style="font-family: var(--font-serif); font-size: 22px; font-weight: 800; color: var(--text-main); margin: 4px 0;">Triangulación</div>
                <p class="editable" style="font-size: 13px; color: var(--text-body);">Cruce convergente de 3 fuentes actorales e instrumentos I1, I2, I3.</p>
              </div>
            </div>

            <!-- Visual 3-Phase Pipeline -->
            <div class="reveal-item" style="display: grid; grid-template-columns: 1fr 40px 1fr 40px 1fr; align-items: stretch; flex: 1;">
              <div class="bento-card" style="background: linear-gradient(145deg, #FFFFFF, #F0FDFA); border-color: #5EEAD4; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <span class="tag-pill tag-teal">Fase 01 • Etapa Cuantitativa</span>
                  <h3 style="font-family: var(--font-serif); font-size: 21px; color: #064E3B; margin: 10px 0 8px 0;">Diagnóstico Censal Estudiantil</h3>
                  <p class="editable" style="font-size: 13.8px; color: var(--text-body); line-height: 1.5;">Aplicación del cuestionario estructurado con escalas Likert (<b>Instrumento I1</b>) al censo de <b>n = 68 estudiantes</b> de 4.º y 5.º año de Psicología.</p>
                </div>
                <div style="font-size: 12.5px; font-weight: 800; color: var(--teal-primary);">Salida: Perfil estadístico de brechas (OE1)</div>
              </div>

              <div style="display: flex; align-items: center; justify-content: center; font-size: 28px; color: var(--teal-primary); font-weight: 800;">➔</div>

              <div class="bento-card" style="background: linear-gradient(145deg, #FFFFFF, #FFFBEB); border-color: #FCD34D; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <span class="tag-pill tag-gold">Fase 02 • Etapa Cualitativa</span>
                  <h3 style="font-family: var(--font-serif); font-size: 21px; color: #78350F; margin: 10px 0 8px 0;">Inmersión en Actores Clave</h3>
                  <p class="editable" style="font-size: 13.8px; color: var(--text-body); line-height: 1.5;">Profundización mediante entrevistas y cuestionarios mixtos a <b>n = 9 facilitadores locales (I2)</b> y <b>n = 9 docentes-psicólogos del claustro (I3)</b>.</p>
                </div>
                <div style="font-size: 12.5px; font-weight: 800; color: var(--gold-primary);">Salida: Criterios clínicos y pedagógicos (OE2, OE3)</div>
              </div>

              <div style="display: flex; align-items: center; justify-content: center; font-size: 28px; color: var(--gold-primary); font-weight: 800;">➔</div>

              <div class="bento-dark" style="border-radius: 20px; padding: 24px 26px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <span class="tag-pill" style="background: rgba(45,212,191,0.2); color: #5EEAD4;">Fase 03 • Etapa Propositiva</span>
                  <h3 style="font-family: var(--font-serif); font-size: 21px; color: #FFFFFF; margin: 10px 0 8px 0;">Construcción del Manual MTCI</h3>
                  <p class="editable" style="font-size: 13.8px; color: #CBD5E1; line-height: 1.5;">Integración de la evidencia empírica en los <b>8 módulos operativos</b>, árbol de derivación clínica y adaptación del <b>I-CAM-Q</b> (Anexo 16.2).</p>
                </div>
                <div style="font-size: 12.5px; font-weight: 800; color: var(--gold-bright);">★ Producto Final: Manual de 18 páginas</div>
              </div>
            </div>
          </div>
        </section>
"""

SLIDES_HTML_PART2 = """
        <!-- SLIDE 9: METODOLOGÍA 2 (ARQUITECTURA MUESTRAL N = 86 CON DONUTS SVG) -->
        <section class="slide" id="slide-09" data-index="8">
          <div class="bg-watermark-num">09</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill royal">09</div>
              <div>
                <div class="eyebrow">Capítulo III • Universo, Muestra y Criterios (2/2)</div>
                <h2 class="slide-title editable">Delimitación Muestral Consolidada (N = 86) y Criterios de Selección</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px;">
            <!-- Cohort 1: Estudiantes -->
            <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between; border-top: 6px solid var(--teal-primary);">
              <div>
                <div style="display: flex; align-items: center; gap: 18px; margin-bottom: 16px;">
                  <div class="gauge-ring" style="--pct: 79.1;">
                    <svg viewBox="0 0 100 100">
                      <circle class="gauge-bg" cx="50" cy="50" r="45"></circle>
                      <circle class="gauge-val" cx="50" cy="50" r="45" stroke="#0D9488"></circle>
                    </svg>
                    <div class="gauge-label" style="color: #0D9488;">n=68</div>
                  </div>
                  <div>
                    <span class="tag-pill tag-teal">79.1% del Total</span>
                    <h3 style="font-family: var(--font-serif); font-size: 20px; color: var(--text-main); margin-top: 4px;">Estudiantes de Psicología</h3>
                    <div style="font-size: 12.5px; color: var(--text-muted); font-weight: 700;">4.º año (77.9%) • 5.º año (22.1%)</div>
                  </div>
                </div>
                <div class="editable" style="display: flex; flex-direction: column; gap: 10px;">
                  <div style="padding: 10px 14px; border-radius: 10px; background: #F0FDF4; border-left: 3px solid #16A34A; font-size: 13px; color: var(--text-body);">
                    <b style="color: #15803D;">✓ Inclusión:</b> Matrícula activa en II Semestre 2026; cursando asignaturas de clínica y prácticas.
                  </div>
                  <div style="padding: 10px 14px; border-radius: 10px; background: #FEF2F2; border-left: 3px solid #DC2626; font-size: 13px; color: var(--text-body);">
                    <b style="color: #B91C1C;">✕ Exclusión:</b> Estudiantes de 1.º a 3.er año o en retiro académico temporal.
                  </div>
                </div>
              </div>
              <div style="font-size: 12px; font-weight: 800; color: var(--teal-primary);">Muestreo: Censo Poblacional (100% de 4.º y 5.º)</div>
            </div>

            <!-- Cohort 2: Facilitadores -->
            <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between; border-top: 6px solid var(--gold-primary);">
              <div>
                <div style="display: flex; align-items: center; gap: 18px; margin-bottom: 16px;">
                  <div class="gauge-ring" style="--pct: 100;">
                    <svg viewBox="0 0 100 100">
                      <circle class="gauge-bg" cx="50" cy="50" r="45"></circle>
                      <circle class="gauge-val" cx="50" cy="50" r="45" stroke="#D97706"></circle>
                    </svg>
                    <div class="gauge-label" style="color: #D97706;">n=9</div>
                  </div>
                  <div>
                    <span class="tag-pill tag-gold">Actores Territoriales</span>
                    <h3 style="font-family: var(--font-serif); font-size: 20px; color: var(--text-main); margin-top: 4px;">Facilitadores Locales</h3>
                    <div style="font-size: 12.5px; color: var(--text-muted); font-weight: 700;">Municipio de Estelí</div>
                  </div>
                </div>
                <div class="editable" style="display: flex; flex-direction: column; gap: 10px;">
                  <div style="padding: 10px 14px; border-radius: 10px; background: #F0FDF4; border-left: 3px solid #16A34A; font-size: 13px; color: var(--text-body);">
                    <b style="color: #15803D;">✓ Inclusión:</b> Masoterapeutas, fitoterapeutas y sobadores con &gt;5 años de práctica reconocida en Estelí.
                  </div>
                  <div style="padding: 10px 14px; border-radius: 10px; background: #FEF2F2; border-left: 3px solid #DC2626; font-size: 13px; color: var(--text-body);">
                    <b style="color: #B91C1C;">✕ Exclusión:</b> Vendedores ambulantes sin arraigo ni consulta terapéutica establecida.
                  </div>
                </div>
              </div>
              <div style="font-size: 12px; font-weight: 800; color: var(--gold-primary);">Muestreo: No Probabilístico Intencional</div>
            </div>

            <!-- Cohort 3: Docentes -->
            <div class="reveal-item bento-card" style="display: flex; flex-direction: column; justify-content: space-between; border-top: 6px solid var(--royal);">
              <div>
                <div style="display: flex; align-items: center; gap: 18px; margin-bottom: 16px;">
                  <div class="gauge-ring" style="--pct: 100;">
                    <svg viewBox="0 0 100 100">
                      <circle class="gauge-bg" cx="50" cy="50" r="45"></circle>
                      <circle class="gauge-val" cx="50" cy="50" r="45" stroke="#1D4ED8"></circle>
                    </svg>
                    <div class="gauge-label" style="color: #1D4ED8;">n=9</div>
                  </div>
                  <div>
                    <span class="tag-pill tag-royal">Expertos Académicos</span>
                    <h3 style="font-family: var(--font-serif); font-size: 20px; color: var(--text-main); margin-top: 4px;">Claustro Docente</h3>
                    <div style="font-size: 12.5px; color: var(--text-muted); font-weight: 700;">Psicólogos • CUR-Estelí</div>
                  </div>
                </div>
                <div class="editable" style="display: flex; flex-direction: column; gap: 10px;">
                  <div style="padding: 10px 14px; border-radius: 10px; background: #F0FDF4; border-left: 3px solid #16A34A; font-size: 13px; color: var(--text-body);">
                    <b style="color: #15803D;">✓ Inclusión:</b> Docentes-psicólogos activos en la carrera con experiencia en supervisión clínica y curricular.
                  </div>
                  <div style="padding: 10px 14px; border-radius: 10px; background: #FEF2F2; border-left: 3px solid #DC2626; font-size: 13px; color: var(--text-body);">
                    <b style="color: #B91C1C;">✕ Exclusión:</b> Docentes de otras carreras sin vinculación clínica en Psicología.
                  </div>
                </div>
              </div>
              <div style="font-size: 12px; font-weight: 800; color: var(--royal);">Muestreo: Criterio de Expertos Institucionales</div>
            </div>
          </div>
        </section>

        <!-- SLIDE 10: RESULTADOS ESTUDIANTES 1 (DASHBOARD RADIAL + FIGURA 4) -->
        <section class="slide" id="slide-10" data-index="9">
          <div class="bg-watermark-num">10</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill crimson">10</div>
              <div>
                <div class="eyebrow">Capítulo IV • Resultados Empíricos en Estudiantes (1/2)</div>
                <h2 class="slide-title editable">Dominio Conceptual vs. Vacío Normativo en Pregrado (n = 68)</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="display: grid; grid-template-columns: 0.96fr 1.04fr; gap: 30px; align-items: stretch;">
            <!-- Left: Gallery Frame Figure 4 -->
            <div class="reveal-item fig-showcase">
              <img src="assets/figuras_apa7/figura_04_dominio_conceptual_normativo_estudiantes.png" alt="Figura 4: Dominio Conceptual y Normativo en Estudiantes" onclick="openLightbox(this)">
              <div class="fig-caption-bar">
                <span>Figura 4. Dominio conceptual (OMS) y normativo (Leyes 774 y 292)</span>
                <span style="color: var(--teal-primary); cursor: pointer;">🔍 Clic para Ampliar</span>
              </div>
            </div>

            <!-- Right: 2x2 Radial Gauge Dashboard -->
            <div class="reveal-item" style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 14px;">
              <div class="bento-card" style="padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 14px;">
                  <div class="gauge-ring" style="width: 82px; height: 82px; --pct: 82.4;">
                    <svg viewBox="0 0 100 100"><circle class="gauge-bg" cx="50" cy="50" r="45"></circle><circle class="gauge-val" cx="50" cy="50" r="45" stroke="#0D9488"></circle></svg>
                    <div class="gauge-label" style="font-size: 17px; color: #0D9488;">82.4%</div>
                  </div>
                  <div style="font-size: 15px; font-weight: 800; color: var(--text-main);">Perfil Femenino y Joven</div>
                </div>
                <p class="editable" style="font-size: 13px; color: var(--text-body); line-height: 1.42;">56 mujeres; 61.8% entre 20–22 años; 77.9% cursa 4.º año al iniciar prácticas en Clínica Psicosocial.</p>
              </div>

              <div class="bento-card" style="padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 14px;">
                  <div class="gauge-ring" style="width: 82px; height: 82px; --pct: 67.6;">
                    <svg viewBox="0 0 100 100"><circle class="gauge-bg" cx="50" cy="50" r="45"></circle><circle class="gauge-val" cx="50" cy="50" r="45" stroke="#2563EB"></circle></svg>
                    <div class="gauge-label" style="font-size: 17px; color: #2563EB;">67.6%</div>
                  </div>
                  <div style="font-size: 15px; font-weight: 800; color: var(--text-main);">Acierto Conceptual OMS</div>
                </div>
                <p class="editable" style="font-size: 13px; color: var(--text-body); line-height: 1.42;">Identifica la definición oficial de MTCI, aunque el 75.0% declara nula familiaridad con protocolos clínicos.</p>
              </div>

              <div class="bento-card bento-gold" style="padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 14px;">
                  <div class="gauge-ring" style="width: 82px; height: 82px; --pct: 58.8;">
                    <svg viewBox="0 0 100 100"><circle class="gauge-bg" cx="50" cy="50" r="45"></circle><circle class="gauge-val" cx="50" cy="50" r="45" stroke="#D97706"></circle></svg>
                    <div class="gauge-label" style="font-size: 17px; color: #B45309;">58.8%</div>
                  </div>
                  <div style="font-size: 15px; font-weight: 800; color: #78350F;">Desconoce Ley No. 774</div>
                </div>
                <p class="editable" style="font-size: 13px; color: #92400E; line-height: 1.42;">Ignora el objeto regulador de la Ley de Medicina Natural o confunde su alcance dentro del MINSA.</p>
              </div>

              <div class="bento-card bento-crimson" style="padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 14px;">
                  <div class="gauge-ring" style="width: 82px; height: 82px; --pct: 64.7;">
                    <svg viewBox="0 0 100 100"><circle class="gauge-bg" cx="50" cy="50" r="45"></circle><circle class="gauge-val" cx="50" cy="50" r="45" stroke="#DC2626"></circle></svg>
                    <div class="gauge-label" style="font-size: 17px; color: #B91C1C;">64.7%</div>
                  </div>
                  <div style="font-size: 15px; font-weight: 800; color: #991B1B;">Vacío Crítico Ley No. 292</div>
                </div>
                <p class="editable" style="font-size: 13px; color: #7F1D1D; line-height: 1.42;">Desconoce la prohibición legal para prescribir fármacos, exponiendo a riesgos de intrusismo involuntario.</p>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 11: RESULTADOS ESTUDIANTES 2 (PARADOJA FORMATIVA ANIMADA + FIGURA 7) -->
        <section class="slide" id="slide-11" data-index="10">
          <div class="bg-watermark-num">11</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill crimson">11</div>
              <div>
                <div class="eyebrow">Capítulo IV • Resultados Empíricos en Estudiantes (2/2)</div>
                <h2 class="slide-title editable">La Paradoja Formativa: Alta Pertinencia vs. Inseguridad Clínica (OE1)</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 30px; align-items: stretch;">
            <!-- Left: Animated KPI Bars -->
            <div class="reveal-item" style="display: flex; flex-direction: column; justify-content: space-between; gap: 14px;">
              <div class="bento-card" style="padding: 18px 22px; border-left: 6px solid var(--teal-primary);">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                  <span style="font-size: 15.5px; font-weight: 800; color: var(--text-main);">Pertinencia Clínica Asistencial</span>
                  <span class="number" data-target="89.7" style="font-family: var(--font-serif); font-size: 40px; font-weight: 800; color: var(--teal-primary);">0.0%</span>
                </div>
                <p class="editable" style="font-size: 13.5px; color: var(--text-body); margin-top: 2px;">Valora necesario e importante integrar las MTCI como complemento en la atención psicológica.</p>
                <div class="bar-track"><div class="bar-fill" style="--target-w: 89.7%; background: linear-gradient(90deg, #0D9488, #10B981);"></div></div>
              </div>

              <div class="bento-card bento-crimson" style="padding: 18px 22px; border-left: 6px solid var(--crimson);">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                  <span style="font-size: 15.5px; font-weight: 800; color: #991B1B;">Preparación Insuficiente para Derivar</span>
                  <span class="number" data-target="88.2" style="font-family: var(--font-serif); font-size: 40px; font-weight: 800; color: var(--crimson);">0.0%</span>
                </div>
                <p class="editable" style="font-size: 13.5px; color: #7F1D1D; margin-top: 2px;">Reconoce preparación nula o insuficiente para derivar pacientes hacia facilitadores acreditados.</p>
                <div class="bar-track"><div class="bar-fill" style="--target-w: 88.2%; background: linear-gradient(90deg, #DC2626, #F87171);"></div></div>
              </div>

              <div class="bento-card bento-gold" style="padding: 18px 22px; border-left: 6px solid var(--gold-primary);">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                  <span style="font-size: 15.5px; font-weight: 800; color: #78350F;">Brecha en Competencia de Psicoeducación</span>
                  <span class="number" data-target="86.8" style="font-family: var(--font-serif); font-size: 40px; font-weight: 800; color: var(--gold-primary);">0.0%</span>
                </div>
                <p class="editable" style="font-size: 13.5px; color: #92400E; margin-top: 2px;">Carece de herramientas académicas para orientar éticamente a los usuarios sobre terapias tradicionales.</p>
                <div class="bar-track"><div class="bar-fill" style="--target-w: 86.8%; background: linear-gradient(90deg, #D97706, #FBBF24);"></div></div>
              </div>
            </div>

            <!-- Right: Figure 7 + Safety Seal -->
            <div class="reveal-item" style="display: flex; flex-direction: column; justify-content: space-between; gap: 14px;">
              <div class="fig-showcase" style="flex: 1;">
                <img src="assets/figuras_apa7/figura_07_frecuencia_uso_estudiantes.png" alt="Figura 7: Frecuencia de Uso en Estudiantes" style="max-height: 270px;" onclick="openLightbox(this)">
                <div class="fig-caption-bar">
                  <span>Figura 7. Frecuencia de uso personal en estudiantes</span>
                  <span style="color: var(--teal-primary);">🔍 Ampliar</span>
                </div>
              </div>

              <div class="bento-emerald" style="border-radius: 18px; padding: 16px 22px; display: flex; align-items: center; justify-content: space-between; gap: 18px;">
                <div class="editable">
                  <div style="font-size: 12px; font-weight: 800; color: #A7F3D0; text-transform: uppercase;">Efectos en Usuarios Activos (n = 30)</div>
                  <div style="font-size: 14px; color: #FFFFFF; margin-top: 3px;"><b>86.7%</b> reporta alivio muscular y serenidad; <b>0.0%</b> efectos adversos.</div>
                </div>
                <div style="font-family: var(--font-serif); font-size: 34px; font-weight: 800; color: #6EE7B7; flex-shrink: 0;">86.7%</div>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 12: RESULTADOS FACILITADORES LOCALES (RIBBON KPI + FIGURAS 12 Y 14) -->
        <section class="slide" id="slide-12" data-index="11">
          <div class="bg-watermark-num">12</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill crimson">12</div>
              <div>
                <div class="eyebrow">Capítulo IV • Resultados en Facilitadores Locales de Estelí (OE2)</div>
                <h2 class="slide-title editable">Modalidades Terapéuticas, Eficacia Somática y Apertura Afectiva (n = 9)</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="flex-direction: column; justify-content: space-between; gap: 18px;">
            <!-- Top 4 KPI Strip -->
            <div class="reveal-item" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
              <div class="bento-card" style="padding: 14px 18px; border-bottom: 4px solid var(--teal-primary); display: flex; align-items: center; gap: 14px;">
                <div style="font-family: var(--font-serif); font-size: 34px; font-weight: 800; color: var(--teal-primary);">100%</div>
                <div class="editable" style="font-size: 13px; font-weight: 700; color: var(--text-main); line-height: 1.3;">Alivio de Sobrecarga Somática</div>
              </div>
              <div class="bento-card" style="padding: 14px 18px; border-bottom: 4px solid var(--royal); display: flex; align-items: center; gap: 14px;">
                <div style="font-family: var(--font-serif); font-size: 34px; font-weight: 800; color: var(--royal);">88.9%</div>
                <div class="editable" style="font-size: 13px; font-weight: 700; color: var(--text-main); line-height: 1.3;">Mayor Apertura Emocional y Verbal</div>
              </div>
              <div class="bento-card" style="padding: 14px 18px; border-bottom: 4px solid var(--emerald); display: flex; align-items: center; gap: 14px;">
                <div style="font-family: var(--font-serif); font-size: 34px; font-weight: 800; color: var(--emerald);">0.0%</div>
                <div class="editable" style="font-size: 13px; font-weight: 700; color: var(--text-main); line-height: 1.3;">Crisis o Reacciones Adversas</div>
              </div>
              <div class="bento-card" style="padding: 14px 18px; border-bottom: 4px solid var(--gold-primary); display: flex; align-items: center; gap: 14px;">
                <div style="font-family: var(--font-serif); font-size: 34px; font-weight: 800; color: var(--gold-primary);">77.8%</div>
                <div class="editable" style="font-size: 13px; font-weight: 700; color: var(--text-main); line-height: 1.3;">Barreras de Estigma y Económicas</div>
              </div>
            </div>

            <!-- Dual Figure Showcase -->
            <div class="reveal-item" style="display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 24px; flex: 1; min-height: 0;">
              <div class="fig-showcase">
                <img src="assets/figuras_apa7/figura_12_practicas_actores_locales.png" alt="Figura 12: Modalidades Terapéuticas de Facilitadores Locales" style="max-height: 330px;" onclick="openLightbox(this)">
                <div class="fig-caption-bar">
                  <span>Figura 12. Prácticas aplicadas por facilitadores en Estelí</span>
                  <span style="color: var(--teal-primary);">🔍 Ampliar Figura 12</span>
                </div>
              </div>

              <div class="fig-showcase">
                <img src="assets/figuras_apa7/figura_14_apertura_emocional_usuarios_actores.png" alt="Figura 14: Apertura Emocional Observada en Usuarios" style="max-height: 330px;" onclick="openLightbox(this)">
                <div class="fig-caption-bar">
                  <span>Figura 14. Desbloqueo corporal y apertura afectiva</span>
                  <span style="color: var(--teal-primary);">🔍 Ampliar Figura 14</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 13: RESULTADOS CLAUSTRO DOCENTE (CONSENSO + FIGURAS 24 Y 25) -->
        <section class="slide" id="slide-13" data-index="12">
          <div class="bg-watermark-num">13</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill crimson">13</div>
              <div>
                <div class="eyebrow">Capítulo IV • Resultados en el Claustro Docente de Psicología (OE3)</div>
                <h2 class="slide-title editable">Consenso Curricular, Didáctica Vivencial y Respaldo Ético (n = 9)</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="flex-direction: column; justify-content: space-between; gap: 18px;">
            <!-- Top 4 Docente Consensus Cards -->
            <div class="reveal-item" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
              <div class="bento-dark" style="padding: 14px 18px; border-radius: 16px; display: flex; align-items: center; gap: 14px;">
                <div style="font-family: var(--font-serif); font-size: 34px; font-weight: 800; color: #5EEAD4;">100%</div>
                <div class="editable" style="font-size: 12.8px; font-weight: 700; color: #FFFFFF; line-height: 1.3;">Respaldo Unánime a Integración Curricular</div>
              </div>
              <div class="bento-card" style="padding: 14px 18px; border-bottom: 4px solid var(--teal-primary); display: flex; align-items: center; gap: 14px;">
                <div style="font-family: var(--font-serif); font-size: 34px; font-weight: 800; color: var(--teal-primary);">88.9%</div>
                <div class="editable" style="font-size: 12.8px; font-weight: 700; color: var(--text-main); line-height: 1.3;">Prioriza Talleres Prácticos Vivenciales</div>
              </div>
              <div class="bento-card" style="padding: 14px 18px; border-bottom: 4px solid var(--gold-primary); display: flex; align-items: center; gap: 14px;">
                <div style="font-family: var(--font-serif); font-size: 34px; font-weight: 800; color: var(--gold-primary);">77.8%</div>
                <div class="editable" style="font-size: 12.8px; font-weight: 700; color: var(--text-main); line-height: 1.3;">Avala Intercambio con Facilitadores</div>
              </div>
              <div class="bento-card" style="padding: 14px 18px; border-bottom: 4px solid var(--royal); display: flex; align-items: center; gap: 14px;">
                <div style="font-family: var(--font-serif); font-size: 34px; font-weight: 800; color: var(--royal);">77.8%</div>
                <div class="editable" style="font-size: 12.8px; font-weight: 700; color: var(--text-main); line-height: 1.3;">Solicita Formación en Neurobiología</div>
              </div>
            </div>

            <!-- Dual Figure Showcase: Figures 24 & 25 -->
            <div class="reveal-item" style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; flex: 1; min-height: 0;">
              <div class="fig-showcase">
                <img src="assets/figuras_apa7/figura_24_estrategias_academicas_docentes.png" alt="Figura 24: Estrategias Pedagógicas Priorizadas por Docentes" style="max-height: 330px;" onclick="openLightbox(this)">
                <div class="fig-caption-bar">
                  <span>Figura 24. Estrategias pedagógicas sugeridas por el claustro</span>
                  <span style="color: var(--teal-primary);">🔍 Ampliar Figura 24</span>
                </div>
              </div>

              <div class="fig-showcase">
                <img src="assets/figuras_apa7/figura_25_experiencias_favorables_docentes.png" alt="Figura 25: Experiencias Formativas Favorables en Docentes" style="max-height: 330px;" onclick="openLightbox(this)">
                <div class="fig-caption-bar">
                  <span>Figura 25. Experiencias formativas favorables identificadas</span>
                  <span style="color: var(--teal-primary);">🔍 Ampliar Figura 25</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 14: PROPUESTA MANUAL MTCI (SHOWCASE EDITORIAL + 8 MÓDULOS BENTO) -->
        <section class="slide" id="slide-14" data-index="13">
          <div class="bg-watermark-num">14</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill" style="background: linear-gradient(135deg, #047857, #10B981);">14</div>
              <div>
                <div class="eyebrow">Capítulo V • Propuesta de Intervención Aplicada (OE3)</div>
                <h2 class="slide-title editable">Manual de Estrategias de MTCI para la Formación y Práctica Psicológica</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="display: grid; grid-template-columns: 0.72fr 1.28fr; gap: 26px; align-items: stretch;">
            <!-- Left: 3D Book Showcase Card -->
            <div class="reveal-item bento-dark" style="display: flex; flex-direction: column; justify-content: space-between; align-items: center; text-align: center; padding: 24px;">
              <span class="tag-pill" style="background: rgba(16, 185, 129, 0.25); color: #6EE7B7;">📘 Producto Acreditado • Anexo 16.2</span>
              <img src="assets/extracted/portada_manual.jpg" alt="Portada del Manual de Estrategias MTCI" style="height: 320px; border-radius: 12px; box-shadow: 0 20px 45px rgba(0,0,0,0.65); border: 2px solid rgba(255,255,255,0.2); cursor: zoom-in; margin: 12px 0;" onclick="openLightbox(this)">
              <div class="editable" style="font-size: 13px; color: #CBD5E1; line-height: 1.45;">
                <b>18 Páginas In Extenso</b> • Incluye Árbol de Decisión Clínica y Cuestionario Internacional <b>I-CAM-Q</b> adaptado a Nicaragua.
              </div>
            </div>

            <!-- Right: 2x4 Bento Grid of the 8 Modules -->
            <div class="reveal-item" style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(4, 1fr); gap: 12px;">
              <div class="bento-card" style="padding: 12px 16px; display: flex; gap: 12px; align-items: center; border-left: 4px solid var(--teal-primary);">
                <div class="icon-circle" style="width: 40px; height: 40px; font-size: 15px; font-weight: 800;">M1</div>
                <div class="editable"><div style="font-size: 14.5px; font-weight: 800; color: var(--text-main);">Fundamentos y Marco Legal</div><div style="font-size: 12.5px; color: var(--text-body);">Directrices OMS (2025) y Leyes 774, 759 y 292.</div></div>
              </div>
              <div class="bento-card" style="padding: 12px 16px; display: flex; gap: 12px; align-items: center; border-left: 4px solid var(--crimson);">
                <div class="icon-circle crimson" style="width: 40px; height: 40px; font-size: 15px; font-weight: 800;">M2</div>
                <div class="editable"><div style="font-size: 14.5px; font-weight: 800; color: var(--text-main);">Principios Deontológicos</div><div style="font-size: 12.5px; color: var(--text-body);">No maleficencia, consentimiento y no prescripción.</div></div>
              </div>
              <div class="bento-card" style="padding: 12px 16px; display: flex; gap: 12px; align-items: center; border-left: 4px solid var(--teal-primary);">
                <div class="icon-circle" style="width: 40px; height: 40px; font-size: 15px; font-weight: 800;">M3</div>
                <div class="editable"><div style="font-size: 14.5px; font-weight: 800; color: var(--text-main);">Mapa Clínico de Prácticas</div><div style="font-size: 12.5px; color: var(--text-body);">Semáforo de 4 niveles de evidencia y seguridad.</div></div>
              </div>
              <div class="bento-card" style="padding: 12px 16px; display: flex; gap: 12px; align-items: center; border-left: 4px solid var(--gold-primary);">
                <div class="icon-circle gold" style="width: 40px; height: 40px; font-size: 15px; font-weight: 800;">M4</div>
                <div class="editable"><div style="font-size: 14.5px; font-weight: 800; color: var(--text-main);">Algoritmo de Derivación</div><div style="font-size: 12.5px; color: var(--text-body);">Protocolo secuencial de 4 pasos para interconsulta.</div></div>
              </div>
              <div class="bento-card" style="padding: 12px 16px; display: flex; gap: 12px; align-items: center; border-left: 4px solid var(--gold-primary);">
                <div class="icon-circle gold" style="width: 40px; height: 40px; font-size: 15px; font-weight: 800;">M5</div>
                <div class="editable"><div style="font-size: 14.5px; font-weight: 800; color: var(--text-main);">Entrevista Intercultural</div><div style="font-size: 12.5px; color: var(--text-body);">Guía de diálogo clínico para erradicar el ocultamiento.</div></div>
              </div>
              <div class="bento-card" style="padding: 12px 16px; display: flex; gap: 12px; align-items: center; border-left: 4px solid var(--royal);">
                <div class="icon-circle royal" style="width: 40px; height: 40px; font-size: 15px; font-weight: 800;">M6</div>
                <div class="editable"><div style="font-size: 14.5px; font-weight: 800; color: var(--text-main);">Red Intersectorial en Estelí</div><div style="font-size: 12.5px; color: var(--text-body);">Vinculación con facilitadores acreditados e IMNTC.</div></div>
              </div>
              <div class="bento-card" style="padding: 12px 16px; display: flex; gap: 12px; align-items: center; border-left: 4px solid var(--royal);">
                <div class="icon-circle royal" style="width: 40px; height: 40px; font-size: 15px; font-weight: 800;">M7</div>
                <div class="editable"><div style="font-size: 14.5px; font-weight: 800; color: var(--text-main);">Ruta Pedagógica Curricular</div><div style="font-size: 12.5px; color: var(--text-body);">Secuencia formativa en 3 etapas y curso electivo.</div></div>
              </div>
              <div class="bento-card" style="padding: 12px 16px; display: flex; gap: 12px; align-items: center; border-left: 4px solid var(--emerald);">
                <div class="icon-circle" style="width: 40px; height: 40px; font-size: 15px; font-weight: 800;">M8</div>
                <div class="editable"><div style="font-size: 14.5px; font-weight: 800; color: var(--text-main);">Gobernanza y Bioética</div><div style="font-size: 12.5px; color: var(--text-body);">Comité de Bioética y formación docente continua.</div></div>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 15: CONCLUSIONES CENTRALES (MATRIZ BENTO DE 5 NODOS) -->
        <section class="slide" id="slide-15" data-index="14">
          <div class="bg-watermark-num">15</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill" style="background: linear-gradient(135deg, #5B21B6, #7C3AED);">15</div>
              <div>
                <div class="eyebrow">Capítulo VI • Síntesis Conclusiva del Estudio</div>
                <h2 class="slide-title editable">Conclusiones Centrales por Triangulación de Objetivos</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="flex-direction: column; justify-content: space-between; gap: 18px;">
            <!-- Top Row: 2 Major Conclusions -->
            <div class="reveal-item" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
              <div class="bento-dark" style="padding: 20px 24px; border-radius: 18px; border-left: 6px solid #2DD4BF;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                  <span class="tag-pill" style="background: rgba(45,212,191,0.2); color: #5EEAD4;">01 • Objetivo General (N = 86)</span>
                  <span style="font-weight: 800; color: #FCD34D; font-size: 13px;">Convergencia Triangulada</span>
                </div>
                <p class="editable" style="font-size: 14px; color: #F8FAFC; line-height: 1.48;">Los tres colectivos validan a la MTCI como un recurso complementario legítimo y valioso en la atención psicológica en Estelí, siempre que opere bajo rigor científico, respeto intercultural y observancia estricta de los límites legales.</p>
              </div>

              <div class="bento-card bento-gold" style="padding: 20px 24px; border-radius: 18px; border-left: 6px solid var(--gold-primary);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                  <span class="tag-pill tag-gold">05 • Aporte Propositivo (Anexo 16.2)</span>
                  <span style="font-weight: 800; color: #92400E; font-size: 13px;">18 Páginas • I-CAM-Q</span>
                </div>
                <p class="editable" style="font-size: 14px; color: #78350F; line-height: 1.48;">El Manual de Estrategias MTCI traduce el diagnóstico empírico en una herramienta inédita para el CUR-Estelí, articulando el cuestionario I-CAM-Q, pautas contra el ocultamiento y un algoritmo de derivación segura.</p>
              </div>
            </div>

            <!-- Bottom Row: 3 Specific Conclusions -->
            <div class="reveal-item" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; flex: 1;">
              <div class="bento-card" style="border-top: 5px solid var(--teal-primary); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <span class="tag-pill tag-teal" style="margin-bottom: 10px;">02 • Conclusión OE1 (Estudiantes)</span>
                  <h3 style="font-family: var(--font-serif); font-size: 19px; color: var(--text-main); margin-bottom: 8px;">Brecha Formativa y Legal</h3>
                  <p class="editable" style="font-size: 13.5px; color: var(--text-body); line-height: 1.48;">Existe alta aceptación clínica (89.7%) y satisfacción personal (86.7%), pero marcada inseguridad para derivar (88.2%) y desconocimiento de las Leyes 774 (58.8%) y 292 (64.7%).</p>
                </div>
                <div style="font-size: 12px; font-weight: 800; color: var(--crimson);">Urgencia de formación deontológica</div>
              </div>

              <div class="bento-card" style="border-top: 5px solid var(--gold-primary); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <span class="tag-pill tag-gold" style="margin-bottom: 10px;">03 • Conclusión OE2 (Facilitadores)</span>
                  <h3 style="font-family: var(--font-serif); font-size: 19px; color: var(--text-main); margin-bottom: 8px;">Eficacia Somática y Apertura</h3>
                  <p class="editable" style="font-size: 13.5px; color: var(--text-body); line-height: 1.48;">Los terapeutas locales constatan 100% de alivio de tensión muscular y 88.9% de apertura emocional en usuarios, enfrentando estigma sociocultural (77.8%) y barreras económicas (77.8%).</p>
                </div>
                <div style="font-size: 12px; font-weight: 800; color: var(--gold-deep);">Sinergia cuerpo-mente comprobada</div>
              </div>

              <div class="bento-card" style="border-top: 5px solid var(--royal); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <span class="tag-pill tag-royal" style="margin-bottom: 10px;">04 • Conclusión OE3 (Claustro)</span>
                  <h3 style="font-family: var(--font-serif); font-size: 19px; color: var(--text-main); margin-bottom: 8px;">Consenso Curricular Unánime</h3>
                  <p class="editable" style="font-size: 13.5px; color: var(--text-body); line-height: 1.48;">El 100% del claustro respalda transversalizar las MTCI mediante talleres vivenciales (88.9%) y vinculación comunitaria (77.8%), solicitando capacitación en neurobiología somática (77.8%).</p>
                </div>
                <div style="font-size: 12px; font-weight: 800; color: var(--royal);">Viabilidad institucional del Manual</div>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 16: RECOMENDACIONES ESTRATÉGICAS (MATRIZ CUÁDRUPLE) -->
        <section class="slide" id="slide-16" data-index="15">
          <div class="bg-watermark-num">16</div>
          <div class="slide-header">
            <div class="header-left">
              <div class="station-pill" style="background: linear-gradient(135deg, #5B21B6, #7C3AED);">16</div>
              <div>
                <div class="eyebrow">Capítulo VI • Hoja de Ruta y Proyección Institucional</div>
                <h2 class="slide-title editable">Recomendaciones Estratégicas para los Cuatro Estamentos</h2>
              </div>
            </div>
            <div class="shield-badge"><img src="assets/extracted/unan_shield_only.png" alt="UNAN"></div>
          </div>

          <div class="slide-content" style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 20px;">
            <div class="reveal-item bento-card" style="border-left: 6px solid var(--teal-primary); display: flex; gap: 18px; align-items: flex-start;">
              <div class="icon-circle" style="width: 52px; height: 52px; font-size: 24px;">🎓</div>
              <div class="editable">
                <div style="font-size: 15.5px; font-weight: 800; color: var(--teal-deep); text-transform: uppercase; margin-bottom: 8px;">1. Para el Estamento Estudiantil</div>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5; margin-bottom: 5px;">✓ <b>Límites Legales:</b> Respetar estrictamente las Leyes 774 y 292 (cero prescripción o dosificación).</p>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5; margin-bottom: 5px;">✓ <b>Práctica Clínica:</b> Aplicar el tamizaje I-CAM-Q y el árbol de decisión en la Clínica Psicosocial.</p>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5;">✓ <b>Escucha Empática:</b> Indagar sin prejuicios las prácticas del usuario para erradicar el ocultamiento.</p>
              </div>
            </div>

            <div class="reveal-item bento-card" style="border-left: 6px solid var(--royal); display: flex; gap: 18px; align-items: flex-start;">
              <div class="icon-circle royal" style="width: 52px; height: 52px; font-size: 24px;">👩‍🏫</div>
              <div class="editable">
                <div style="font-size: 15.5px; font-weight: 800; color: #1E3A8A; text-transform: uppercase; margin-bottom: 8px;">2. Para el Claustro Docente</div>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5; margin-bottom: 5px;">✓ <b>Transversalización:</b> Incorporar los módulos del manual en Psicología Clínica, Comunitaria y Ética.</p>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5; margin-bottom: 5px;">✓ <b>Didáctica Vivencial:</b> Priorizar talleres de regulación vagal/somática y resolución de casos clínicos.</p>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5;">✓ <b>Actualización:</b> Participar en formación continua sobre neurobiología somática y fitofarmacología.</p>
              </div>
            </div>

            <div class="reveal-item bento-card" style="border-left: 6px solid var(--gold-primary); display: flex; gap: 18px; align-items: flex-start;">
              <div class="icon-circle gold" style="width: 52px; height: 52px; font-size: 24px;">🏛️</div>
              <div class="editable">
                <div style="font-size: 15.5px; font-weight: 800; color: var(--gold-deep); text-transform: uppercase; margin-bottom: 8px;">3. Para UNAN-Managua CUR-Estelí</div>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5; margin-bottom: 5px;">✓ <b>Adopción Oficial:</b> Institucionalizar el Manual de Estrategias MTCI (Anexo 16.2) en la Clínica Psicosocial.</p>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5; margin-bottom: 5px;">✓ <b>Comité de Bioética:</b> Constituir el Comité de Supervisión y Delimitación Profesional.</p>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5;">✓ <b>Convenios MINSA:</b> Articular pasantías e intercambios con las clínicas de Medicina Natural.</p>
              </div>
            </div>

            <div class="reveal-item bento-card" style="border-left: 6px solid var(--emerald); display: flex; gap: 18px; align-items: flex-start;">
              <div class="icon-circle" style="width: 52px; height: 52px; font-size: 24px; background: #D1FAE5; color: #047857;">🌿</div>
              <div class="editable">
                <div style="font-size: 15.5px; font-weight: 800; color: #065F46; text-transform: uppercase; margin-bottom: 8px;">4. Para el Sistema de Salud y Facilitadores</div>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5; margin-bottom: 5px;">✓ <b>Acreditación:</b> Difundir los mecanismos de registro y certificación oficial conforme a la Ley No. 774.</p>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5; margin-bottom: 5px;">✓ <b>Red de Referencia:</b> Habilitar protocolos de interconsulta bidireccional con servicios de psicología.</p>
                <p style="font-size: 13.5px; color: var(--text-body); line-height: 1.5;">✓ <b>Principio de Complementariedad:</b> Garantizar la no sustitución de tratamientos médicos o psiquiátricos.</p>
              </div>
            </div>
          </div>
        </section>

        <!-- SLIDE 17: CIERRE INSTITUCIONAL SOLEMNE -->
        <section class="slide theme-dark" id="slide-17" data-index="16">
          <div class="bg-watermark-num">17</div>
          <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; position: relative; z-index: 2;">
            <img src="assets/extracted/unan_shield_only.png" alt="UNAN" style="height: 112px; margin-bottom: 20px; filter: drop-shadow(0 10px 25px rgba(0,0,0,0.75));">
            <div style="font-family: var(--font-serif); font-size: 26px; font-style: italic; color: var(--gold-bright); margin-bottom: 10px;">
              «¡A la libertad por la Universidad!»
            </div>
            <h1 class="editable" style="font-family: var(--font-serif); font-size: 56px; font-weight: 800; color: #FFFFFF; margin-bottom: 14px;">
              Muchas Gracias por su Atención
            </h1>
            <p class="editable" style="font-size: 19px; color: #CBD5E1; max-width: 74%; margin-bottom: 36px; line-height: 1.5;">
              Queda formalmente abierto el espacio para preguntas, comentarios y deliberación del Honorable Tribunal Examinador
            </p>

            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; width: 92%; border-top: 1px solid rgba(255,255,255,0.15); padding-top: 26px;">
              <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 14px; border-radius: 14px;">
                <div style="font-size: 11px; color: #2DD4BF; font-weight: 800; text-transform: uppercase;">Sustentante</div>
                <div class="editable" style="font-size: 14.5px; color: #FFF; font-weight: 700; margin-top: 4px;">Dina Fabiola García Torres</div>
              </div>
              <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 14px; border-radius: 14px;">
                <div style="font-size: 11px; color: #2DD4BF; font-weight: 800; text-transform: uppercase;">Sustentante</div>
                <div class="editable" style="font-size: 14.5px; color: #FFF; font-weight: 700; margin-top: 4px;">Tatiana Paola López Ramos</div>
              </div>
              <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 14px; border-radius: 14px;">
                <div style="font-size: 11px; color: #2DD4BF; font-weight: 800; text-transform: uppercase;">Sustentante</div>
                <div class="editable" style="font-size: 14.5px; color: #FFF; font-weight: 700; margin-top: 4px;">Engel Enoc Zamora Velásquez</div>
              </div>
              <div style="background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.35); padding: 14px; border-radius: 14px;">
                <div style="font-size: 11px; color: var(--gold-bright); font-weight: 800; text-transform: uppercase;">Tutora de Tesis</div>
                <div class="editable" style="font-size: 14.5px; color: #FFF; font-weight: 700; margin-top: 4px;">Dra. Tania Libertad Pérez Guevara</div>
              </div>
            </div>
          </div>
        </section>
"""

def build_html() -> str:
    slides_json = json.dumps(SLIDES_METADATA, ensure_ascii=False)

    head_and_shell = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lienzo Espacial MTCI en Psicología · UNAN-Managua CUR-Estelí</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,400;1,600&display=swap" rel="stylesheet">
  <style>""" + CSS_STYLES + """</style>
</head>
<body class="in-overview">

  <!-- TOP CHAPTER QUICK-JUMP RIBBON -->
  <nav class="top-nav" id="top-nav">
    <button class="nav-pill overview-btn active" onclick="enterOverview()" title="Mapa General Espacial (Tecla O)">🌍 Mapa General [O]</button>
    <button class="nav-pill" data-jump="0" onclick="goToSlide(0)">Portada</button>
    <button class="nav-pill" data-jump="1" onclick="goToSlide(1)">Cap. I • Problema</button>
    <button class="nav-pill" data-jump="5" onclick="goToSlide(5)">Cap. II • Marco Teórico</button>
    <button class="nav-pill" data-jump="7" onclick="goToSlide(7)">Cap. III • Metodología</button>
    <button class="nav-pill" data-jump="9" onclick="goToSlide(9)">Cap. IV • Resultados</button>
    <button class="nav-pill" data-jump="13" onclick="goToSlide(13)">Cap. V • Manual MTCI</button>
    <button class="nav-pill" data-jump="14" onclick="goToSlide(14)">Cap. VI • Conclusiones</button>
    <button class="nav-pill" data-jump="16" onclick="goToSlide(16)">Cierre</button>
  </nav>

  <!-- INFINITE SPATIAL VIEWPORT -->
  <div id="viewport">
    <div class="cosmos-grid"></div>

    <div id="camera">
      <div id="world">

        <!-- SVG SYNAPTIC & BOTANICAL CONNECTION LINES -->
        <svg id="world-connections" viewBox="-8000 -6000 16000 12000">
          <defs>
            <linearGradient id="gradPath" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#14B8A6" />
              <stop offset="50%" stop-color="#F59E0B" />
              <stop offset="100%" stop-color="#38BDF8" />
            </linearGradient>
          </defs>
          <circle cx="0" cy="300" r="1950" fill="none" stroke="rgba(20, 184, 166, 0.14)" stroke-width="6" stroke-dasharray="30 25" />
          <circle cx="0" cy="300" r="3950" fill="none" stroke="rgba(245, 158, 11, 0.11)" stroke-width="6" stroke-dasharray="40 30" />
          <circle cx="0" cy="300" r="5600" fill="none" stroke="rgba(56, 189, 248, 0.08)" stroke-width="4" />
          <g id="dynamic-paths"></g>
        </svg>

        <!-- ORBITAL CHAPTER BANNERS FOR OVERVIEW MAP -->
        <div class="cluster-banner cluster-cap1" style="left: -4025px; top: -2680px;">I. Introducción y Planteamiento</div>
        <div class="cluster-banner cluster-cap2" style="left: 3850px; top: -2680px;">II. Marco Teórico y Normativo</div>
        <div class="cluster-banner cluster-cap3" style="left: 4100px; top: -820px;">III. Diseño Metodológico Mixto (N = 86)</div>
        <div class="cluster-banner cluster-cap4" style="left: 100px; top: 3120px;">IV. Resultados Empíricos: Estudiantes • Facilitadores • Docentes</div>
        <div class="cluster-banner cluster-cap5" style="left: -4850px; top: 450px;">V. Propuesta: Manual MTCI</div>
        <div class="cluster-banner cluster-cap6" style="left: -2250px; top: 280px;">VI. Conclusiones y Recomendaciones</div>
"""

    footer_and_js = """
      </div>
    </div>
  </div>

  <!-- BOTTOM HUD CONTROLS -->
  <footer class="deck-hud">
    <div class="hud-left">
      <span class="status-dot"></span>
      <span id="hud-status-text">Vista Panorámica Global • Haz clic en cualquier estación o presiona [Siguiente ›]</span>
    </div>

    <div class="hud-controls">
      <button class="btn-hud" id="btn-overview" onclick="toggleOverview()" title="Alternar Mapa General (Tecla O)">🌍 Mapa [O]</button>
      <button class="btn-hud" id="btn-prev" onclick="prevStep()" title="Estación Anterior (Flecha Izq)">‹ Anterior</button>
      <span class="slide-counter" id="counter">MAPA</span>
      <button class="btn-hud" id="btn-next" onclick="nextStep()" title="Siguiente Estación (Flecha Der / Espacio)">Siguiente ›</button>
      <span style="opacity: 0.25;">|</span>
      <button class="btn-hud" id="btn-notes" onclick="toggleNotes()" title="Notas de Oratoria (Tecla N)">🎙️ Notas [N]</button>
      <button class="btn-hud" id="btn-edit" onclick="toggleEditMode()" title="Activar edición directa de textos para compañeras">✏️ Editar</button>
      <button class="btn-hud" id="btn-save" onclick="exportEditedHTML()" style="display: none; background: #10B981; border-color: #34D399;" title="Descargar presentación con los cambios guardados">💾 Guardar HTML</button>
      <button class="btn-hud" id="btn-fs" onclick="toggleFullscreen()" title="Pantalla Completa (Tecla F)">⛶ [F]</button>
    </div>
  </footer>

  <!-- SPEAKER NOTES DRAWER -->
  <div id="notes-drawer">
    <div class="notes-header">
      <span id="notes-slide-label">Guía de Oratoria y Defensa Oral</span>
      <span style="cursor: pointer; opacity: 0.8;" onclick="toggleNotes()">✕ Cerrar [N]</span>
    </div>
    <div class="notes-content editable" id="notes-body">
      Vista general del ecosistema de la investigación. Desde este mapa espacial podemos apreciar los 6 capítulos articulados: desde la tensión legal entre la Ley 774 y la Ley 292 hasta los hallazgos empíricos en los 86 actores y el Manual de Estrategias MTCI.
    </div>
  </div>

  <!-- HIGH-RES FIGURE LIGHTBOX -->
  <div id="figure-lightbox" onclick="closeLightbox()">
    <img id="lb-img" src="" alt="Figura Ampliada">
    <div class="lb-caption" id="lb-caption">Clic en cualquier lugar o presiona [ESC] para regresar a la estación</div>
  </div>

  <script>
    const SLIDES_DATA = """ + slides_json + """;
    const slides = Array.from(document.querySelectorAll('.slide'));
    const totalSlides = slides.length;

    const viewport = document.getElementById('viewport');
    const camera = document.getElementById('camera');
    const world = document.getElementById('world');
    const counterEl = document.getElementById('counter');
    const statusTextEl = document.getElementById('hud-status-text');
    const notesDrawer = document.getElementById('notes-drawer');
    const notesBody = document.getElementById('notes-body');
    const notesLabel = document.getElementById('notes-slide-label');

    let currentIndex = -1;
    let isOverview = true;
    let isEditMode = false;

    let camX = -100;
    let camY = 220;
    let camScale = 0.11;
    let camRot = 0;

    function initSpatialWorld() {
      const pathsGroup = document.getElementById('dynamic-paths');
      let svgHtml = '';

      SLIDES_DATA.forEach((meta, idx) => {
        const el = slides[idx];
        el.style.transform = `translate3d(${meta.x}px, ${meta.y}px, 0) rotate(${meta.rot}deg) scale(${meta.scale})`;

        const badge = document.createElement('div');
        badge.className = 'overview-badge';
        badge.innerHTML = `
          <div class="ov-num">${meta.num}</div>
          <div class="ov-short">${meta.short}</div>
          <div class="ov-metric">${meta.metric}</div>
        `;
        el.appendChild(badge);

        el.addEventListener('click', (e) => {
          if (isEditMode) return;
          if (isOverview || currentIndex !== idx) {
            e.stopPropagation();
            goToSlide(idx);
          }
        });

        if (idx < SLIDES_DATA.length - 1) {
          const next = SLIDES_DATA[idx + 1];
          const midX = (meta.x + next.x) / 2;
          const midY = (meta.y + next.y) / 2 - 220;
          const d = `M ${meta.x} ${meta.y} Q ${midX} ${midY} ${next.x} ${next.y}`;
          svgHtml += `<path class="conn-glow" d="${d}" stroke="url(#gradPath)" />`;
          svgHtml += `<path class="conn-path" d="${d}" stroke="url(#gradPath)" />`;
        }
      });

      pathsGroup.innerHTML = svgHtml;
    }

    function updateCameraTransform() {
      camera.style.transform = `scale(${camScale})`;
      world.style.transform = `rotate(${-camRot}deg) translate3d(${-camX}px, ${-camY}px, 0)`;
    }

    function enterOverview() {
      isOverview = true;
      document.body.classList.add('in-overview');
      slides.forEach(s => s.classList.remove('active'));

      const vw = window.innerWidth;
      const vh = window.innerHeight;
      camScale = Math.min(vw / 12200, vh / 6800) * 0.92;
      camX = -100;
      camY = 220;
      camRot = 0;

      updateCameraTransform();
      counterEl.textContent = 'MAPA';
      statusTextEl.textContent = 'Mapa Panorámico Global (17 Estaciones) • Clic en cualquier estación para hacer Zoom';
      notesLabel.textContent = 'Vista Panorámica Global del Estudio';
      notesBody.textContent = 'Desde este lienzo integral observamos la arquitectura completa de la investigación: Capítulo I (Introducción), Capítulo II (Marco Teórico y Legal), Capítulo III (Metodología Mixta N=86), Capítulo IV (Resultados Empíricos en los 3 colectivos), Capítulo V (Manual de Estrategias MTCI) y Capítulo VI (Conclusiones y Recomendaciones).';
      updateTopNavHighlight(-1);
    }

    function toggleOverview() {
      if (isOverview) {
        goToSlide(currentIndex >= 0 ? currentIndex : 0);
      } else {
        enterOverview();
      }
    }

    function goToSlide(index) {
      if (index < 0 || index >= totalSlides) return;

      isOverview = false;
      document.body.classList.remove('in-overview');

      slides.forEach(s => s.classList.remove('active'));
      currentIndex = index;
      const targetEl = slides[currentIndex];
      const meta = SLIDES_DATA[currentIndex];
      targetEl.classList.add('active');

      const vw = window.innerWidth;
      const vh = window.innerHeight - 90;
      const fitScale = Math.min(vw / 1600, vh / 900) * 0.91;

      camX = meta.x;
      camY = meta.y;
      camRot = meta.rot;
      camScale = fitScale / meta.scale;

      updateCameraTransform();
      animateCounters(targetEl);

      counterEl.textContent = `${meta.num} / 17`;
      statusTextEl.textContent = `${meta.category} — ${meta.short}`;
      notesLabel.textContent = `Estación ${meta.num}: ${meta.short}`;
      notesBody.textContent = meta.notes;
      updateTopNavHighlight(currentIndex);
    }

    function nextStep() {
      if (isOverview) {
        goToSlide(currentIndex >= 0 ? currentIndex : 0);
      } else if (currentIndex < totalSlides - 1) {
        goToSlide(currentIndex + 1);
      } else {
        enterOverview();
      }
    }

    function prevStep() {
      if (isOverview) {
        goToSlide(currentIndex >= 0 ? currentIndex : 0);
      } else if (currentIndex > 0) {
        goToSlide(currentIndex - 1);
      } else {
        enterOverview();
      }
    }

    function updateTopNavHighlight(idx) {
      const pills = document.querySelectorAll('.nav-pill');
      pills.forEach(p => p.classList.remove('active'));
      if (idx === -1) {
        document.querySelector('.overview-btn').classList.add('active');
        return;
      }
      let activeJump = 0;
      if (idx >= 1 && idx <= 4) activeJump = 1;
      else if (idx >= 5 && idx <= 6) activeJump = 5;
      else if (idx >= 7 && idx <= 8) activeJump = 7;
      else if (idx >= 9 && idx <= 12) activeJump = 9;
      else if (idx === 13) activeJump = 13;
      else if (idx >= 14 && idx <= 15) activeJump = 14;
      else if (idx === 16) activeJump = 16;

      const match = document.querySelector(`.nav-pill[data-jump="${activeJump}"]`);
      if (match) match.classList.add('active');
    }

    function animateCounters(slideEl) {
      const counters = slideEl.querySelectorAll('[data-target]');
      counters.forEach(el => {
        const target = parseFloat(el.getAttribute('data-target'));
        const isDecimal = target % 1 !== 0;
        const duration = 1200;
        const startTime = performance.now();

        function update(now) {
          const elapsed = now - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const easeOut = 1 - Math.pow(1 - progress, 3);
          const val = target * easeOut;
          el.textContent = (isDecimal ? val.toFixed(1) : Math.round(val)) + '%';
          if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
      });
    }

    let isDragging = false;
    let dragStartX = 0;
    let dragStartY = 0;
    let startCamX = 0;
    let startCamY = 0;

    viewport.addEventListener('mousedown', (e) => {
      if (isEditMode) return;
      if (e.target.closest('.fig-showcase img')) return;
      isDragging = true;
      dragStartX = e.clientX;
      dragStartY = e.clientY;
      startCamX = camX;
      startCamY = camY;
      viewport.classList.add('dragging', 'no-transition');
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      const dx = (e.clientX - dragStartX) / camScale;
      const dy = (e.clientY - dragStartY) / camScale;
      const rad = (camRot * Math.PI) / 180;
      camX = startCamX - (dx * Math.cos(rad) + dy * Math.sin(rad));
      camY = startCamY - (-dx * Math.sin(rad) + dy * Math.cos(rad));
      updateCameraTransform();
    });

    window.addEventListener('mouseup', () => {
      if (!isDragging) return;
      isDragging = false;
      viewport.classList.remove('dragging', 'no-transition');
    });

    viewport.addEventListener('wheel', (e) => {
      if (isEditMode) return;
      e.preventDefault();
      viewport.classList.add('no-transition');
      const zoomFactor = e.deltaY < 0 ? 1.12 : 0.89;
      camScale = Math.max(0.06, Math.min(2.2, camScale * zoomFactor));
      if (camScale < 0.22 && !isOverview) {
        isOverview = true;
        document.body.classList.add('in-overview');
      } else if (camScale >= 0.28 && isOverview) {
        isOverview = false;
        document.body.classList.remove('in-overview');
      }
      updateCameraTransform();
      clearTimeout(window._wheelTimer);
      window._wheelTimer = setTimeout(() => viewport.classList.remove('no-transition'), 150);
    }, { passive: false });

    function openLightbox(imgEl) {
      if (isEditMode) return;
      const lb = document.getElementById('figure-lightbox');
      const lbImg = document.getElementById('lb-img');
      const lbCap = document.getElementById('lb-caption');
      lbImg.src = imgEl.src;
      lbCap.textContent = imgEl.alt + ' • Clic o [ESC] para cerrar';
      lb.classList.add('open');
    }

    function closeLightbox() {
      document.getElementById('figure-lightbox').classList.remove('open');
    }

    function toggleNotes() {
      notesDrawer.classList.toggle('open');
    }

    function toggleEditMode() {
      isEditMode = !isEditMode;
      document.body.classList.toggle('editing-active', isEditMode);
      const editBtn = document.getElementById('btn-edit');
      const saveBtn = document.getElementById('btn-save');
      const editables = document.querySelectorAll('.editable');

      editables.forEach(el => {
        el.setAttribute('contenteditable', isEditMode ? 'true' : 'false');
      });

      if (isEditMode) {
        if (isOverview) goToSlide(0);
        editBtn.classList.add('active-toggle');
        editBtn.textContent = '✓ Editando';
        saveBtn.style.display = 'inline-flex';
        statusTextEl.textContent = 'Modo Edición Activo: Haz clic sobre cualquier texto para modificarlo y luego pulsa [💾 Guardar HTML]';
      } else {
        editBtn.classList.remove('active-toggle');
        editBtn.textContent = '✏️ Editar';
        saveBtn.style.display = 'none';
      }
    }

    function exportEditedHTML() {
      if (currentIndex >= 0) {
        SLIDES_DATA[currentIndex].notes = notesBody.innerText;
      }
      const editables = document.querySelectorAll('.editable');
      editables.forEach(el => el.removeAttribute('contenteditable'));
      document.body.classList.remove('editing-active');

      const fullHtml = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;
      const blob = new Blob([fullHtml], { type: 'text/html;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'presentacion_tesis_mtci_animated.html';
      a.click();
      URL.revokeObjectURL(url);

      if (isEditMode) {
        editables.forEach(el => el.setAttribute('contenteditable', 'true'));
        document.body.classList.add('editing-active');
      }
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen();
      }
    }

    window.addEventListener('keydown', (e) => {
      if (isEditMode) {
        if (e.key === 'Escape') toggleEditMode();
        return;
      }
      if (document.getElementById('figure-lightbox').classList.contains('open')) {
        if (e.key === 'Escape' || e.key === ' ') closeLightbox();
        return;
      }
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextStep();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevStep();
      } else if (e.key === 'o' || e.key === 'O' || e.key === 'Escape') {
        e.preventDefault();
        toggleOverview();
      } else if (e.key === 'n' || e.key === 'N') {
        e.preventDefault();
        toggleNotes();
      } else if (e.key === 'f' || e.key === 'F') {
        e.preventDefault();
        toggleFullscreen();
      }
    });

    window.addEventListener('resize', () => {
      if (isOverview) enterOverview();
      else goToSlide(currentIndex);
    });

    initSpatialWorld();
    goToSlide(0);
  </script>
</body>
</html>
"""
    return head_and_shell + SLIDES_HTML_PART1 + SLIDES_HTML_PART2 + footer_and_js


def main() -> None:
    content = build_html()
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Lienzo espacial con diseño infográfico editorial generado en: {HTML_OUTPUT} ({len(content):,} bytes)")


if __name__ == "__main__":
    main()
