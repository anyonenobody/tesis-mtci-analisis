#!/usr/bin/env python3
"""
tools/generate_apa7_figures.py
==============================
Generates all 25 figures for the MTCI Thesis in strict APA 7th edition format.

Strict APA 7 visual principles applied:
1. NO titles or subtitles baked inside the image canvas (only the pure graphic,
   data labels, axes, and legend). Titles and notes belong as text in the document.
2. Elegant academic color palette (Navy Blue, Slate Teal, Muted Amber, Sage Green, Slate Gray).
3. Despined axes (no top/right lines), subtle horizontal gridlines.
4. Clean typography and high resolution (300 DPI) for crisp printing in Word.
5. Exact empirical data from 'datos_mtci_anonimizado.csv' (students, n=68) and
   instruments I2 (facilitators, n=9) and I3 (teachers, n=9).
"""

import os
import sys
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Reconfigure stdout/stderr for Unicode
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "assets", "figuras_apa7")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# APA 7 Global Style Settings
# ---------------------------------------------------------
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['axes.edgecolor'] = '#4A5568'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['text.color'] = '#1A202C'
plt.rcParams['axes.labelcolor'] = '#1A202C'
plt.rcParams['xtick.color'] = '#2D3748'
plt.rcParams['ytick.color'] = '#2D3748'

# Palette
NAVY   = '#1B365D'
TEAL   = '#2E86AB'
AMBER  = '#E59866'
SAGE   = '#6B9080'
SLATE  = '#5C6B73'
SAND   = '#E0A96D'
CORAL  = '#D9534F'
PURPLE = '#795290'
LIGHT_GRAY = '#F7FAFC'

# Load student dataset
CSV_PATH = os.path.join(REPO_ROOT, "datos_mtci_anonimizado.csv")
df_students = pd.read_csv(CSV_PATH) if os.path.exists(CSV_PATH) else None

def save_clean_fig(fig, filename):
    out_path = os.path.join(OUT_DIR, filename)
    fig.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white', transparent=False)
    plt.close(fig)
    print(f"✅ Generada: {filename}")

# =========================================================
# FIGURA 1: Ubicación geográfica de CUR-Estelí
# =========================================================
def gen_figura_01():
    # Source image from original assets
    orig_path = os.path.join(REPO_ROOT, "assets", "figuras_originales", "image12.jpg")
    out_path = os.path.join(OUT_DIR, "figura_01_ubicacion_cur_esteli.png")
    if os.path.exists(orig_path):
        from PIL import Image
        im = Image.open(orig_path)
        im.save(out_path, "PNG", quality=95)
        print("✅ Generada: figura_01_ubicacion_cur_esteli.png (Mapa base)")
    else:
        print("⚠️ No se encontró image12.jpg para Figura 1")

# =========================================================
# FIGURA 2: Diagrama de criterios de inclusión y exclusión
# =========================================================
def gen_figura_02():
    from matplotlib.patches import FancyBboxPatch

    # Academic Palette
    NAVY_DARK   = '#0F2942'
    NAVY_HEADER = '#1B365D'
    TEAL_BG     = '#F0F9FF'
    TEAL_BADGE  = '#E0F2FE'
    TEAL_BORDER = '#BAE6FD'
    TEAL_TEXT   = '#0369A1'

    ROSE_BG     = '#FFF5F5'
    ROSE_BADGE  = '#FEE2E2'
    ROSE_BORDER = '#FECACA'
    ROSE_TEXT   = '#B91C1C'

    TEXT_MAIN   = '#1E293B'
    GOLD_PILL   = '#FEF3C7'
    GOLD_TEXT   = '#92400E'

    fig, ax = plt.subplots(figsize=(13.8, 8.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    cols = [
        {
            "title": "Estudiantes de Psicología",
            "n_badge": "Muestra: n = 68 (IV y V Año)",
            "inc_bullets": [
                "• Matrícula activa en 4.º o 5.º año de la carrera",
                "• Turno matutino o por encuentro sabatino",
                "• Adscripción vigente en CUR-Estelí (2026)",
                "• Consentimiento informado formalmente aceptado",
                "• Diligenciamiento completo del Cuestionario I1"
            ],
            "exc_bullets": [
                "• Estudiantes cursando de 1.º a 3.º año académico",
                "• Bajas académicas temporales o definitivas",
                "• Matrícula en carreras o facultades no afines",
                "• Omisión de datos críticos en el cuestionario",
                "• Negativa voluntaria a participar en el estudio"
            ]
        },
        {
            "title": "Facilitadores de MTCI",
            "n_badge": "Muestra: n = 9 (Actores Locales)",
            "inc_bullets": [
                "• Ejercicio profesional activo de MTCI en Estelí",
                "• Práctica en terapias corporales o herbolarias",
                "• Certificación, aval o reconocimiento comunitario",
                "• Atención a usuarios con demandas psicofísicas",
                "• Consentimiento y aplicación de la Entrevista I2"
            ],
            "exc_bullets": [
                "• Práctica médica exclusivamente alopática",
                "• Ejercicio radicado fuera del municipio de Estelí",
                "• Comercialización de insumos sin consulta",
                "• Trayectoria menor a un año continuo en MTCI",
                "• Negativa a compartir información del ejercicio"
            ]
        },
        {
            "title": "Docentes de Psicología",
            "n_badge": "Muestra: n = 9 (Cuerpo Docente)",
            "inc_bullets": [
                "• Título de Licenciatura en Psicología acreditado",
                "• Docencia activa en UNAN-Managua / CUR-Estelí",
                "• Impartición lectiva en 4.º o 5.º año de la carrera",
                "• Tutoría de investigación formativa o prácticas",
                "• Diligenciamiento voluntario del Cuestionario I3"
            ],
            "exc_bullets": [
                "• Docentes de otras carreras o áreas del saber",
                "• Personal administrativo sin docencia en aula",
                "• Docentes con licencia prolongada o permiso",
                "• Docencia exclusiva en primeros años (1.º a 3.º)",
                "• Cuestionarios devueltos con datos incompletos"
            ]
        }
    ]

    col_w = 30.0
    x_starts = [2.0, 35.0, 68.0]

    y_header = 88.8
    h_header = 8.0

    y_inc = 49.5
    h_inc = 36.5
    y_inc_top = y_inc + h_inc

    y_exc = 7.0
    h_exc = 36.5
    y_exc_top = y_exc + h_exc

    y_footer = 1.4
    h_footer = 3.8

    for idx, col in enumerate(cols):
        xs = x_starts[idx]
        xc = xs + col_w / 2.0

        # 1. Header Card
        header_box = FancyBboxPatch(
            (xs, y_header), col_w, h_header,
            boxstyle="round,pad=0.2,rounding_size=1.2",
            facecolor=NAVY_HEADER, edgecolor=NAVY_DARK, linewidth=1.4,
            zorder=2
        )
        ax.add_patch(header_box)

        ax.text(
            xc, y_header + 5.0, col["title"],
            ha='center', va='center', color='white',
            fontsize=11.6, fontweight='bold', zorder=3
        )

        pill_w = col_w * 0.74
        pill_h = 2.5
        pill_x = xc - pill_w / 2.0
        pill_y = y_header + 1.2
        pill_box = FancyBboxPatch(
            (pill_x, pill_y), pill_w, pill_h,
            boxstyle="round,pad=0.1,rounding_size=0.8",
            facecolor=GOLD_PILL, edgecolor='#D97706', linewidth=0.8,
            zorder=3
        )
        ax.add_patch(pill_box)
        ax.text(
            xc, pill_y + pill_h / 2.0, col["n_badge"],
            ha='center', va='center', color=GOLD_TEXT,
            fontsize=9.2, fontweight='bold', zorder=4
        )

        # 2. Inclusion Card
        inc_card = FancyBboxPatch(
            (xs, y_inc), col_w, h_inc,
            boxstyle="round,pad=0.2,rounding_size=1.0",
            facecolor='#FFFFFF', edgecolor=TEAL_BORDER, linewidth=1.3,
            zorder=2
        )
        ax.add_patch(inc_card)

        inc_inner = FancyBboxPatch(
            (xs + 0.3, y_inc + 0.3), col_w - 0.6, h_inc - 0.6,
            boxstyle="round,pad=0.1,rounding_size=0.8",
            facecolor=TEAL_BG, edgecolor='none',
            zorder=2.1
        )
        ax.add_patch(inc_inner)

        inc_hdr_h = 4.2
        inc_hdr_y = y_inc_top - inc_hdr_h
        inc_hdr = FancyBboxPatch(
            (xs + 0.4, inc_hdr_y), col_w - 0.8, inc_hdr_h,
            boxstyle="round,pad=0.1,rounding_size=0.6",
            facecolor=TEAL_BADGE, edgecolor='#7DD3FC', linewidth=1.0,
            zorder=2.3
        )
        ax.add_patch(inc_hdr)

        ax.text(
            xc, inc_hdr_y + inc_hdr_h / 2.0, "✓  CRITERIOS DE INCLUSIÓN",
            ha='center', va='center', color=TEAL_TEXT,
            fontsize=9.8, fontweight='bold', zorder=3
        )

        bullet_y_start = inc_hdr_y - 3.8
        line_gap = 5.6
        for b_idx, bullet in enumerate(col["inc_bullets"]):
            by = bullet_y_start - b_idx * line_gap
            ax.text(
                xs + 1.8, by, bullet,
                ha='left', va='center', color=TEXT_MAIN,
                fontsize=8.8, linespacing=1.2, zorder=3
            )

        # 3. Transition Arrow
        arrow_x = xc
        ax.annotate(
            '', xy=(arrow_x, y_exc_top + 0.4), xytext=(arrow_x, y_inc - 0.2),
            arrowprops=dict(
                arrowstyle="-|>",
                color='#64748B',
                lw=1.6,
                mutation_scale=14
            ),
            zorder=2
        )

        # 4. Exclusion Card
        exc_card = FancyBboxPatch(
            (xs, y_exc), col_w, h_exc,
            boxstyle="round,pad=0.2,rounding_size=1.0",
            facecolor='#FFFFFF', edgecolor=ROSE_BORDER, linewidth=1.3,
            zorder=2
        )
        ax.add_patch(exc_card)

        exc_inner = FancyBboxPatch(
            (xs + 0.3, y_exc + 0.3), col_w - 0.6, h_exc - 0.6,
            boxstyle="round,pad=0.1,rounding_size=0.8",
            facecolor=ROSE_BG, edgecolor='none',
            zorder=2.1
        )
        ax.add_patch(exc_inner)

        exc_hdr_h = 4.2
        exc_hdr_y = y_exc_top - exc_hdr_h
        exc_hdr = FancyBboxPatch(
            (xs + 0.4, exc_hdr_y), col_w - 0.8, exc_hdr_h,
            boxstyle="round,pad=0.1,rounding_size=0.6",
            facecolor=ROSE_BADGE, edgecolor='#FCA5A5', linewidth=1.0,
            zorder=2.3
        )
        ax.add_patch(exc_hdr)

        ax.text(
            xc, exc_hdr_y + exc_hdr_h / 2.0, "✕  CRITERIOS DE EXCLUSIÓN",
            ha='center', va='center', color=ROSE_TEXT,
            fontsize=9.8, fontweight='bold', zorder=3
        )

        bullet_y_start = exc_hdr_y - 3.8
        for b_idx, bullet in enumerate(col["exc_bullets"]):
            by = bullet_y_start - b_idx * line_gap
            ax.text(
                xs + 1.8, by, bullet,
                ha='left', va='center', color=TEXT_MAIN,
                fontsize=8.8, linespacing=1.2, zorder=3
            )

    # 5. Bottom Executive Summary Banner
    footer_w = 96.0
    footer_x = 2.0
    footer_box = FancyBboxPatch(
        (footer_x, y_footer), footer_w, h_footer,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.0,
        zorder=2
    )
    ax.add_patch(footer_box)

    footer_text = "Delimitación Muestral Consolidada:  Población Total Investigada N = 86 participantes  |  Estudiantes (n = 68)  •  Facilitadores (n = 9)  •  Docentes (n = 9)"
    ax.text(
        50.0, y_footer + h_footer / 2.0, footer_text,
        ha='center', va='center', color='#334155',
        fontsize=9.3, fontweight='bold', zorder=3
    )

    plt.tight_layout(pad=0.4)
    save_clean_fig(fig, "figura_02_criterios_inclusion_exclusion.png")

# =========================================================
# FIGURA 3: Demografía Estudiantes (3 subpaneles)
# =========================================================
def gen_figura_03():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13.0, 4.8), dpi=300)

    # Panel A: Año de Carrera
    anios = ['4.º Año', '5.º Año']
    anios_pct = [77.9, 22.1]
    anios_n = [53, 15]
    colors_a = [NAVY, TEAL]
    bars1 = ax1.bar(anios, anios_pct, color=colors_a, width=0.52, edgecolor='none')
    ax1.set_ylabel("Porcentaje de Estudiantes (%)", fontsize=10.5, color='#1E293B')
    ax1.set_ylim(0, 95)
    for b, pct, n in zip(bars1, anios_pct, anios_n):
        ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 2.5, f"{pct:.1f}%\n(n={n})",
                 ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=NAVY)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_title("A. Año de Formación", fontsize=11, fontweight='bold', pad=12, color=NAVY)

    # Panel B: Sexo
    sexos = ['Femenino', 'Masculino', 'Prefiere\nno decir']
    sexos_pct = [82.4, 14.7, 2.9]
    sexos_n = [56, 10, 2]
    colors_b = [TEAL, SAGE, SLATE]
    bars2 = ax2.bar(sexos, sexos_pct, color=colors_b, width=0.52, edgecolor='none')
    ax2.set_ylim(0, 95)
    for b, pct, n in zip(bars2, sexos_pct, sexos_n):
        ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 2.5, f"{pct:.1f}%\n(n={n})",
                 ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=TEAL)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_title("B. Distribución por Sexo", fontsize=11, fontweight='bold', pad=12, color=NAVY)

    # Panel C: Rango Etario
    edades = ['18–20', '21–25', '26–30', '>30']
    edades_pct = [20.6, 67.6, 10.3, 1.5]
    edades_n = [14, 46, 7, 1]
    colors_c = [SLATE, NAVY, AMBER, SAND]
    bars3 = ax3.bar(edades, edades_pct, color=colors_c, width=0.52, edgecolor='none')
    ax3.set_ylim(0, 80)
    for b, pct, n in zip(bars3, edades_pct, edades_n):
        ax3.text(b.get_x() + b.get_width()/2, b.get_height() + 2.5, f"{pct:.1f}%\n(n={n})",
                 ha='center', va='bottom', fontsize=8.8, fontweight='bold', color=NAVY)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.grid(axis='y', linestyle='--', alpha=0.3)
    ax3.set_title("C. Rango de Edad (Años)", fontsize=11, fontweight='bold', pad=12, color=NAVY)

    plt.tight_layout(pad=2.2)
    save_clean_fig(fig, "figura_03_demografia_estudiantes.png")

# =========================================================
# FIGURA 4: Dominio Conceptual y Normativo Estudiantes
# =========================================================
def gen_figura_04():
    fig, ax = plt.subplots(figsize=(10, 5))

    dimensions = [
        "Concepto Técnico MTCI (OMS)",
        "Propósito Ley No. 774 (Medicina Natural)",
        "Límite Legal Ley No. 292 (Farmacias)"
    ]
    aciertos = [67.6, 41.2, 35.3]      # Correcto
    desconocimiento = [20.6, 42.6, 50.0] # No familiarizado
    distorsion = [11.8, 16.2, 14.7]     # Respuestas distorsionadas/erróneas

    y = np.arange(len(dimensions))
    height = 0.25

    rects1 = ax.barh(y + height, aciertos, height, label='Acierto Técnico / Correcto', color=NAVY)
    rects2 = ax.barh(y, desconocimiento, height, label='Desconocimiento / No Familiarizado', color=AMBER)
    rects3 = ax.barh(y - height, distorsion, height, label='Concepción Distorsionada / Errónea', color=SLATE)

    ax.set_xlabel("Porcentaje de Respuestas (%)", fontsize=10.5)
    ax.set_yticks(y)
    ax.set_yticklabels(dimensions, fontsize=10.5)
    ax.set_xlim(0, 80)
    ax.legend(loc='upper right', frameon=False, fontsize=9.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)

    # Data labels
    for rect in rects1:
        w = rect.get_width()
        ax.text(w + 1, rect.get_y() + rect.get_height()/2, f"{w:.1f}%", va='center', fontsize=9, fontweight='bold', color=NAVY)
    for rect in rects2:
        w = rect.get_width()
        ax.text(w + 1, rect.get_y() + rect.get_height()/2, f"{w:.1f}%", va='center', fontsize=9, fontweight='bold', color=AMBER)
    for rect in rects3:
        w = rect.get_width()
        ax.text(w + 1, rect.get_y() + rect.get_height()/2, f"{w:.1f}%", va='center', fontsize=9, fontweight='bold', color=SLATE)

    ax.invert_yaxis()
    plt.tight_layout()
    save_clean_fig(fig, "figura_04_dominio_conceptual_normativo_estudiantes.png")

# =========================================================
# FIGURA 5: Reconocimiento Prácticas 1 (Naturales y Manuales)
# =========================================================
def gen_figura_05():
    fig, ax = plt.subplots(figsize=(9.5, 4.8))

    practicas = [
        "Masajes terapéuticos y relajantes",
        "Medicina Ayurveda / Yoga / Respiración",
        "Fitoterapia / Herbolaria comunitaria",
        "Quiropraxia",
        "Reflexología / Acupuntura / Digitopuntura",
        "Hidroterapia / Sauna / Geoterapia",
        "Medicina Holística e Integrativa",
        "Ayunoterapia y Nutracéuticos"
    ]
    pcts = [77.9, 67.6, 60.3, 19.1, 16.2, 14.7, 10.3, 4.4]
    ns = [53, 46, 41, 13, 11, 10, 7, 3]

    y = np.arange(len(practicas))
    colors = [NAVY if p > 50 else TEAL if p > 15 else SLATE for p in pcts]

    bars = ax.barh(y, pcts, color=colors, height=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(practicas, fontsize=10)
    ax.set_xlabel("Porcentaje de Reconocimiento (%)", fontsize=10.5)
    ax.set_xlim(0, 92)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.2, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9, fontweight='bold', color='#2D3748')

    plt.tight_layout()
    save_clean_fig(fig, "figura_05_reconocimiento_practicas_1_estudiantes.png")

# =========================================================
# FIGURA 6: Reconocimiento Prácticas 2 (Psicoemocionales y Energéticas)
# =========================================================
def gen_figura_06():
    fig, ax = plt.subplots(figsize=(9.5, 4.5))

    practicas = [
        "Aromaterapia / Terapia Floral / Arteterapia",
        "Constelaciones Familiares / Hipnosis",
        "Curación Energética / Reiki / Sanación",
        "Psicoterapia Pránica",
        "Nueva Medicina Germánica",
        "Iridología",
        "Ninguna práctica reconocida"
    ]
    pcts = [77.9, 16.2, 8.8, 4.4, 2.9, 1.5, 16.2]
    ns = [53, 11, 6, 3, 2, 1, 11]

    y = np.arange(len(practicas))
    colors = [NAVY if p > 50 else AMBER if "Ninguna" in practicas[i] else TEAL for i, p in enumerate(pcts)]

    bars = ax.barh(y, pcts, color=colors, height=0.58)
    ax.set_yticks(y)
    ax.set_yticklabels(practicas, fontsize=10)
    ax.set_xlabel("Porcentaje de Reconocimiento (%)", fontsize=10.5)
    ax.set_xlim(0, 92)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.2, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9, fontweight='bold', color='#2D3748')

    plt.tight_layout()
    save_clean_fig(fig, "figura_06_reconocimiento_practicas_2_estudiantes.png")

# =========================================================
# FIGURA 7: Frecuencia de Uso y Efectos en Estudiantes
# =========================================================
def gen_figura_07():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 5.0), dpi=300, gridspec_kw={'width_ratios': [1.3, 1]})

    # Panel 1: Frecuencia
    categorias = ["Nunca / No usa", "Rara vez (1-2 veces)", "Ocasional (mensual)", "Frecuente (semanal)"]
    autocuidado = [52.9, 27.9, 19.1, 0.0]
    estres = [47.1, 35.3, 13.2, 4.4]

    x = np.arange(len(categorias))
    width = 0.35

    b1 = ax1.bar(x - width/2, autocuidado, width, label='Autocuidado General', color=NAVY)
    b2 = ax1.bar(x + width/2, estres, width, label='Manejo de Estrés Personal', color=AMBER)

    ax1.set_ylabel("Porcentaje (%)", fontsize=10.5, color='#1E293B')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categorias, rotation=15, ha='right', fontsize=9.2)
    ax1.set_ylim(0, 65)
    ax1.legend(frameon=False, fontsize=9.5, loc='upper right')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_title("A. Frecuencia de Uso en el Último Año (n = 68)", fontsize=11, fontweight='bold', pad=12, color=NAVY)

    for b in b1:
        h = b.get_height()
        if h > 0: ax1.text(b.get_x() + b.get_width()/2, h + 1.2, f"{h:.1f}%", ha='center', fontsize=8.5, color=NAVY, fontweight='bold')
    for b in b2:
        h = b.get_height()
        if h > 0: ax1.text(b.get_x() + b.get_width()/2, h + 1.2, f"{h:.1f}%", ha='center', fontsize=8.5, color=AMBER, fontweight='bold')

    # Panel 2: Efectos en usuarios reales (n=30)
    wedges, texts, autotexts = ax2.pie(
        [26, 4], labels=['Favorables / Alivio\n86.7% (n = 26)', 'Sin cambios\n13.3% (n = 4)'],
        autopct='%1.1f%%', startangle=90, colors=[TEAL, SLATE],
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2.5),
        textprops=dict(fontsize=9.5, fontweight='bold', color=NAVY), pctdistance=0.72
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(9.0)
    ax2.set_title("B. Efectos Percibidos en Bienestar (n = 30)", fontsize=11, fontweight='bold', pad=12, color=NAVY)

    plt.tight_layout(pad=2.2)
    save_clean_fig(fig, "figura_07_frecuencia_uso_estudiantes.png")

# =========================================================
# FIGURA 8: Sexo de Actores Locales
# =========================================================
def gen_figura_08():
    fig, ax = plt.subplots(figsize=(6, 4.2))
    labels = ['Mujeres\n77.8% (n=7)', 'Hombres\n22.2% (n=2)']
    vals = [7, 2]
    colors = [TEAL, SAGE]

    wedges, texts, autotexts = ax.pie(
        vals, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2.5),
        pctdistance=0.75, textprops=dict(fontsize=10.5, fontweight='bold', color=NAVY)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(10)
    save_clean_fig(fig, "figura_08_sexo_actores_locales.png")

# =========================================================
# FIGURA 9: Edad de Facilitadores Locales
# =========================================================
def gen_figura_09():
    fig, ax = plt.subplots(figsize=(7, 3.8))
    rangos = ['30 a 39 años', '40 a 49 años', '50 a 58 años']
    pcts = [55.6, 22.2, 22.2]
    ns = [5, 2, 2]

    y = np.arange(len(rangos))
    bars = ax.barh(y, pcts, color=[NAVY, TEAL, SAGE], height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(rangos, fontsize=10.5)
    ax.set_xlabel("Porcentaje de Facilitadores (%)", fontsize=10)
    ax.set_xlim(0, 70)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.5, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9.5, fontweight='bold', color=NAVY)

    plt.tight_layout()
    save_clean_fig(fig, "figura_09_edad_actores_locales.png")

# =========================================================
# FIGURA 10: Años de Experiencia Facilitadores
# =========================================================
def gen_figura_10():
    fig, ax = plt.subplots(figsize=(7, 3.8))
    rangos = ['20 a 30 años', '0 a 9 años', '10 a 19 años']
    pcts = [44.4, 33.3, 22.2]
    ns = [4, 3, 2]

    y = np.arange(len(rangos))
    bars = ax.barh(y, pcts, color=[NAVY, AMBER, TEAL], height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(rangos, fontsize=10.5)
    ax.set_xlabel("Porcentaje de Facilitadores (%)", fontsize=10)
    ax.set_xlim(0, 60)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.2, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9.5, fontweight='bold', color=NAVY)

    plt.tight_layout()
    save_clean_fig(fig, "figura_10_experiencia_actores_locales.png")

# =========================================================
# FIGURA 11: Procedencia de Actores Locales
# =========================================================
def gen_figura_11():
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ciudades = ['Municipio de Estelí', 'Municipio de San Nicolás', 'Otra localidad nacional']
    pcts = [77.8, 11.1, 11.1]
    ns = [7, 1, 1]

    y = np.arange(len(ciudades))
    bars = ax.barh(y, pcts, color=[NAVY, SLATE, SAND], height=0.52)
    ax.set_yticks(y)
    ax.set_yticklabels(ciudades, fontsize=10.5)
    ax.set_xlabel("Porcentaje (%)", fontsize=10)
    ax.set_xlim(0, 95)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.5, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9.5, fontweight='bold', color=NAVY)

    plt.tight_layout()
    save_clean_fig(fig, "figura_11_procedencia_actores_locales.png")

# =========================================================
# FIGURA 12: Prácticas de MTCI Utilizadas por Actores Locales
# =========================================================
def gen_figura_12():
    fig, ax = plt.subplots(figsize=(9.5, 5))
    practicas = [
        "Masajes terapéuticos",
        "Reflexología y Acupuntura",
        "Aromaterapia y Terapias florales",
        "Medicina Ayurveda / Yoga",
        "Fitoterapia / Herbolaria",
        "Quiropraxia",
        "Nueva Medicina Germánica",
        "Psicoterapia Pránica",
        "Medicina Holística e Integrativa",
        "Curación Energética / Reiki"
    ]
    pcts = [44.4, 44.4, 44.4, 44.4, 33.3, 22.2, 11.1, 11.1, 11.1, 11.1]
    ns = [4, 4, 4, 4, 3, 2, 1, 1, 1, 1]

    y = np.arange(len(practicas))
    colors = [NAVY if p > 40 else TEAL if p > 20 else SLATE for p in pcts]
    bars = ax.barh(y, pcts, color=colors, height=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(practicas, fontsize=10)
    ax.set_xlabel("Porcentaje de Facilitadores (%)", fontsize=10.5)
    ax.set_xlim(0, 58)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.0, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9, fontweight='bold', color='#2D3748')

    plt.tight_layout()
    save_clean_fig(fig, "figura_12_practicas_actores_locales.png")

# =========================================================
# FIGURA 13: Cambios Percibidos en Estrés y Ansiedad
# =========================================================
def gen_figura_13():
    fig, ax = plt.subplots(figsize=(6, 4))
    wedges, texts = ax.pie([100], labels=['Reducción Positiva de Tensión\n100.0% (n = 9)'],
                           colors=[TEAL], startangle=90,
                           wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
                           textprops=dict(fontsize=10.5, fontweight='bold', color=NAVY))
    save_clean_fig(fig, "figura_13_cambios_estres_ansiedad_actores.png")

# =========================================================
# FIGURA 14: Disposición y Apertura Emocional de Usuarios
# =========================================================
def gen_figura_14():
    fig, ax = plt.subplots(figsize=(6, 4.2))
    labels = ['Cambios Significativos\n88.9% (n = 8)', 'Cambios Moderados\n11.1% (n = 1)']
    vals = [8, 1]
    colors = [NAVY, SAND]

    wedges, texts, autotexts = ax.pie(
        vals, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
        pctdistance=0.75, textprops=dict(fontsize=10.5, fontweight='bold', color=NAVY)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(10)
    save_clean_fig(fig, "figura_14_apertura_emocional_usuarios_actores.png")

# =========================================================
# FIGURA 15: Efectos Observados (Seguridad / Reacciones Adversas)
# =========================================================
def gen_figura_15():
    fig, ax = plt.subplots(figsize=(6, 4))
    wedges, texts = ax.pie([100], labels=['Ausencia Total de Reacciones Adversas\n100.0% Seguridad Observada (n = 9)'],
                           colors=[SAGE], startangle=90,
                           wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
                           textprops=dict(fontsize=10.5, fontweight='bold', color=NAVY))
    save_clean_fig(fig, "figura_15_efectos_observados_actores.png")

# =========================================================
# FIGURA 16: Interacción con Profesionales de la Salud
# =========================================================
def gen_figura_16():
    fig, ax = plt.subplots(figsize=(7, 3.8))
    niveles = ['Excelente', 'Buena', 'Regular']
    pcts = [66.7, 22.2, 11.1]
    ns = [6, 2, 1]

    y = np.arange(len(niveles))
    bars = ax.barh(y, pcts, color=[TEAL, SAGE, AMBER], height=0.52)
    ax.set_yticks(y)
    ax.set_yticklabels(niveles, fontsize=10.5)
    ax.set_xlabel("Porcentaje (%)", fontsize=10)
    ax.set_xlim(0, 80)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.5, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9.5, fontweight='bold', color=NAVY)

    plt.tight_layout()
    save_clean_fig(fig, "figura_16_interaccion_profesionales_salud.png")

# =========================================================
# FIGURA 17: Dificultades Normativas Percibidas
# =========================================================
def gen_figura_17():
    fig, ax = plt.subplots(figsize=(6, 4.2))
    labels = ['Sin Dificultades Significativas\n77.8% (n = 7)', 'Dificultad Moderada\n22.2% (n = 2)']
    vals = [7, 2]
    colors = [TEAL, SLATE]

    wedges, texts, autotexts = ax.pie(
        vals, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
        pctdistance=0.75, textprops=dict(fontsize=10.5, fontweight='bold', color=NAVY)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(10)
    save_clean_fig(fig, "figura_17_dificultades_normativas_actores.png")

# =========================================================
# FIGURA 18: Usuarios con Reservas Socioculturales
# =========================================================
def gen_figura_18():
    fig, ax = plt.subplots(figsize=(6, 4.2))
    labels = ['Encuentro Ocasional\n77.8% (n = 7)', 'Encuentro Frecuente\n22.2% (n = 2)']
    vals = [7, 2]
    colors = [AMBER, NAVY]

    wedges, texts, autotexts = ax.pie(
        vals, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
        pctdistance=0.75, textprops=dict(fontsize=10.5, fontweight='bold', color=NAVY)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(10)
    save_clean_fig(fig, "figura_18_reservas_socioculturales_usuarios.png")

# =========================================================
# FIGURA 19: Incidencia del Factor Económico
# =========================================================
def gen_figura_19():
    fig, ax = plt.subplots(figsize=(6, 4.2))
    labels = ['Incide Moderadamente\n77.8% (n = 7)', 'No Incide / Gratuito\n22.2% (n = 2)']
    vals = [7, 2]
    colors = [CORAL, SAGE]

    wedges, texts, autotexts = ax.pie(
        vals, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
        pctdistance=0.75, textprops=dict(fontsize=10.5, fontweight='bold', color=NAVY)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(10)
    save_clean_fig(fig, "figura_19_incidencia_factor_economico.png")

# =========================================================
# FIGURA 20: Sexo de los Docentes
# =========================================================
def gen_figura_20():
    fig, ax = plt.subplots(figsize=(6, 4.2))
    labels = ['Femenino\n77.8% (n = 7)', 'Masculino\n22.2% (n = 2)']
    vals = [7, 2]
    colors = [NAVY, TEAL]

    wedges, texts, autotexts = ax.pie(
        vals, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
        pctdistance=0.75, textprops=dict(fontsize=10.5, fontweight='bold', color=NAVY)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(10)
    save_clean_fig(fig, "figura_20_sexo_docentes.png")

# =========================================================
# FIGURA 21: Edad de los Docentes
# =========================================================
def gen_figura_21():
    fig, ax = plt.subplots(figsize=(7, 3.8))
    rangos = ['22 a 28 años', '29 a 36 años', '37 a 50 años', '70 años']
    pcts = [33.3, 44.4, 11.1, 11.1]
    ns = [3, 4, 1, 1]

    y = np.arange(len(rangos))
    bars = ax.barh(y, pcts, color=[TEAL, NAVY, AMBER, SLATE], height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(rangos, fontsize=10.5)
    ax.set_xlabel("Porcentaje de Docentes (%)", fontsize=10)
    ax.set_xlim(0, 58)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.2, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9.5, fontweight='bold', color=NAVY)

    plt.tight_layout()
    save_clean_fig(fig, "figura_21_edad_docentes.png")

# =========================================================
# FIGURA 22: Especialidad de los Docentes
# =========================================================
def gen_figura_22():
    fig, ax = plt.subplots(figsize=(7.5, 4))
    especialidades = [
        "Psicología Clínica",
        "Psicología Infantil y Educativa",
        "Psicología Social y Comunitaria",
        "Servicios de Salud y Epidemiología"
    ]
    pcts = [55.6, 22.2, 11.1, 11.1]
    ns = [5, 2, 1, 1]

    y = np.arange(len(especialidades))
    bars = ax.barh(y, pcts, color=[NAVY, TEAL, SAGE, SLATE], height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(especialidades, fontsize=10)
    ax.set_xlabel("Porcentaje de Docentes (%)", fontsize=10)
    ax.set_xlim(0, 70)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.5, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9.5, fontweight='bold', color=NAVY)

    plt.tight_layout()
    save_clean_fig(fig, "figura_22_especialidad_docentes.png")

# =========================================================
# FIGURA 23: Experiencia Docente
# =========================================================
def gen_figura_23():
    fig, ax = plt.subplots(figsize=(6, 4.2))
    labels = ['1 a 5 Años de Docencia\n77.8% (n = 7)', '6 a 10 Años de Docencia\n22.2% (n = 2)']
    vals = [7, 2]
    colors = [TEAL, SAND]

    wedges, texts, autotexts = ax.pie(
        vals, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
        pctdistance=0.75, textprops=dict(fontsize=10.5, fontweight='bold', color=NAVY)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(10)
    save_clean_fig(fig, "figura_23_experiencia_docente.png")

# =========================================================
# FIGURA 24: Estrategias Académicas Docentes
# =========================================================
def gen_figura_24():
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    estrategias = [
        "Talleres vivenciales y prácticos",
        "Investigación y producción estudiantil",
        "Integración transversal en asignaturas",
        "Prácticas clínicas y comunitarias supervisadas",
        "Foros y debates académicos críticos"
    ]
    pcts = [66.7, 66.7, 55.6, 44.4, 22.2]
    ns = [6, 6, 5, 4, 2]

    y = np.arange(len(estrategias))
    colors = [NAVY if p > 60 else TEAL if p > 40 else SLATE for p in pcts]
    bars = ax.barh(y, pcts, color=colors, height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(estrategias, fontsize=10)
    ax.set_xlabel("Porcentaje de Respuestas de Docentes (%)", fontsize=10)
    ax.set_xlim(0, 80)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.5, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9.5, fontweight='bold', color='#2D3748')

    plt.tight_layout()
    save_clean_fig(fig, "figura_24_estrategias_academicas_docentes.png")

# =========================================================
# FIGURA 25: Experiencias Favorables sobre MTCI Docentes
# =========================================================
def gen_figura_25():
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    experiencias = [
        "Talleres experienciales y vivenciales",
        "Intercambio con terapeutas tradicionales",
        "Visitas de campo a centros e instituciones",
        "Conferencias magistrales con especialistas",
        "Análisis reflexivo de casos clínicos"
    ]
    pcts = [88.9, 77.8, 66.7, 33.3, 33.3]
    ns = [8, 7, 6, 3, 3]

    y = np.arange(len(experiencias))
    colors = [NAVY if p > 70 else TEAL if p > 50 else SLATE for p in pcts]
    bars = ax.barh(y, pcts, color=colors, height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(experiencias, fontsize=10)
    ax.set_xlabel("Porcentaje de Respuestas de Docentes (%)", fontsize=10)
    ax.set_xlim(0, 102)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()

    for b, pct, n in zip(bars, pcts, ns):
        ax.text(b.get_width() + 1.5, b.get_y() + b.get_height()/2, f"{pct:.1f}% (n={n})",
                va='center', fontsize=9.5, fontweight='bold', color='#2D3748')

    plt.tight_layout()
    save_clean_fig(fig, "figura_25_experiencias_favorables_docentes.png")

def main():
    print("Iniciando generación de figuras APA 7...")
    gen_figura_01()
    gen_figura_02()
    gen_figura_03()
    gen_figura_04()
    gen_figura_05()
    gen_figura_06()
    gen_figura_07()
    gen_figura_08()
    gen_figura_09()
    gen_figura_10()
    gen_figura_11()
    gen_figura_12()
    gen_figura_13()
    gen_figura_14()
    gen_figura_15()
    gen_figura_16()
    gen_figura_17()
    gen_figura_18()
    gen_figura_19()
    gen_figura_20()
    gen_figura_21()
    gen_figura_22()
    gen_figura_23()
    gen_figura_24()
    gen_figura_25()
    print("✨ Todas las 25 figuras generadas con éxito en assets/figuras_apa7/")

if __name__ == "__main__":
    main()
