"""Genera los recursos gráficos de la presentación de defensa.

- Fondos con degradado (claro y oscuro) para la plantilla minimalista.
- Nubes de palabras de prácticas y de condiciones/patologías cuya escala
  proviene del conteo REAL de menciones en el cuerpo del manuscrito
  (Introducción → Recomendaciones), sin cifras inventadas.

Uso:
    uv run --with wordcloud python presentacion_defensa/build_assets.py <tesis.md>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
ASSETS.mkdir(exist_ok=True)

NAVY = (27, 54, 93)
TEAL = (46, 134, 171)
SAGE = (107, 143, 122)
ORANGE = (230, 149, 95)
SLATE = (92, 103, 112)


def gradient(path: Path, c1, c2, size=(2400, 1350), diagonal=True) -> None:
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w * 0.55 + y / h * 0.45) if diagonal else y / h
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    img.save(path, optimize=True)


def fast_gradient(path: Path, c1, c2, size=(2400, 1350)) -> None:
    """Degradado diagonal rápido (líneas verticales + vertical blend)."""
    w, h = size
    base = Image.new("RGB", size, c1)
    draw = ImageDraw.Draw(base)
    steps = w + h
    for s in range(0, steps, 2):
        t = s / steps
        col = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        draw.line([(s, 0), (s - h, h)], fill=col, width=3)
    base.save(path, optimize=True)


# --------------------------------------------------------------------------
# Conteo de términos en el manuscrito
# --------------------------------------------------------------------------
PRACTICAS = {
    "Herbolaria / Fitoterapia": r"herbolari\w*|fitoterap\w*",
    "Plantas medicinales": r"plantas medicinales",
    "Masajes": r"masaj\w*",
    "Yoga": r"\byoga\b",
    "Meditación": r"meditaci\w*",
    "Mindfulness": r"mindfulness",
    "Acupuntura": r"acupuntur\w*",
    "Reflexología": r"reflexolog\w*",
    "Aromaterapia": r"aromaterapi\w*",
    "Terapia floral": r"terapia floral|terapias florales",
    "Arteterapia": r"arteterapi\w*",
    "Dramaterapia": r"dramaterapi\w*",
    "Reiki": r"\breiki\b",
    "Quiropraxia": r"quiroprax\w*",
    "Hidroterapia": r"hidroterapi\w*",
    "Ayurveda": r"ayurveda",
    "Respiración": r"respiraci\w*",
    "Relajación": r"relajaci\w*",
    "Hipnosis": r"hipnosis",
    "Constelaciones familiares": r"constelaciones familiares",
    "Parteras": r"parter\w*",
    "Curanderos": r"curander\w*",
    "Sobadores": r"sobador\w*",
    "Imaginería guiada": r"imaginer\w* guiada",
    "Medicina ancestral": r"medicina (?:tradicional )?ancestral",
}

CONDICIONES = {
    "Estrés": r"estr[eé]s",
    "Ansiedad": r"ansiedad\w*|ansios\w*",
    "Tensión": r"tensi[oó]n\w*",
    "Depresión": r"depresi\w*",
    "Burnout": r"burnout|agotamiento",
    "Insomnio / sueño": r"insomnio|trastornos del sueño|el sueño",
    "Dolor": r"\bdolor\b",
    "Trauma": r"trauma\w*|postraum\w*",
    "Somatización": r"somatiz\w*|psicosom\w*",
    "Abuso de sustancias": r"abuso de sustancias",
    "Duelo": r"\bduelo\b",
    "Autoestima": r"autoestima",
    "Sufrimiento emocional": r"sufrimiento emocional",
    "Sobrecarga emocional": r"sobrecarga emocional",
    "Malestar psico-físico": r"malestar psico-f\w+",
}


def body_text(md_path: Path) -> str:
    lines = md_path.read_text(encoding="utf8").splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("# 1. Introducción"))
    end = next(i for i, l in enumerate(lines) if l.startswith("# 15. Referencias"))
    return "\n".join(lines[start:end]).lower()


def count_terms(text: str, terms: dict[str, str]) -> dict[str, int]:
    out = {}
    for label, pat in terms.items():
        n = len(re.findall(pat, text, flags=re.IGNORECASE))
        if n:
            out[label] = n
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def make_cloud(freqs: dict[str, int], path: Path, colors, size=(1600, 1000)) -> None:
    from wordcloud import WordCloud

    def color_func(word, font_size, position, orientation, random_state=None, **kw):
        # color por rango de frecuencia (coherencia gestáltica: similitud)
        rank = list(freqs).index(word) if word in freqs else len(freqs)
        c = colors[min(rank * len(colors) // max(len(freqs), 1), len(colors) - 1)]
        return "rgb(%d,%d,%d)" % c

    wc = WordCloud(
        width=size[0], height=size[1], mode="RGBA", background_color=None,
        prefer_horizontal=1.0, relative_scaling=0.55, min_font_size=22,
        max_font_size=190, margin=14, font_path="C:/Windows/Fonts/calibrib.ttf",
        random_state=7, collocations=False,
    )
    wc.generate_from_frequencies(freqs)
    wc.recolor(color_func=color_func)
    wc.to_file(str(path))


def crop_manual_cover() -> None:
    """Recorta la franja ilustrada de la portada del manual (Anexo 16.2)."""
    src = ASSETS / "portada_manual.jpg"
    if not src.exists():
        return
    im = Image.open(src).convert("RGB")
    w, h = im.size
    # la ilustración ocupa la franja central; se eliminan márgenes blancos
    gray = im.convert("L")
    rows = [y for y in range(h) if min(gray.crop((0, y, w, y + 1)).getdata()) < 235]
    top, bottom = (rows[0], rows[-1]) if rows else (0, h)
    im.crop((0, top, w, bottom + 1)).save(ASSETS / "portada_manual_banda.jpg", quality=92)


def main() -> None:
    md = Path(sys.argv[1])
    crop_manual_cover()
    fast_gradient(ASSETS / "bg_dark.png", (16, 38, 66), (31, 94, 115))
    fast_gradient(ASSETS / "bg_light.png", (255, 255, 255), (232, 241, 243))
    text = body_text(md)
    prac = count_terms(text, PRACTICAS)
    cond = count_terms(text, CONDICIONES)
    (ASSETS / "frecuencias_terminos.json").write_text(
        json.dumps({"practicas": prac, "condiciones": cond}, ensure_ascii=False, indent=2),
        encoding="utf8",
    )
    print("PRACTICAS", prac)
    print("CONDICIONES", cond)
    make_cloud(prac, ASSETS / "nube_practicas.png", [NAVY, TEAL, SAGE, SLATE])
    make_cloud(cond, ASSETS / "nube_condiciones.png", [ORANGE, TEAL, SAGE, SLATE], size=(1400, 1000))


if __name__ == "__main__":
    main()
