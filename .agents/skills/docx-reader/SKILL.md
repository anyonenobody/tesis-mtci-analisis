---
name: docx-reader
description: >-
  Read, inspect, and analyze Microsoft Word (.docx) documents with full formatting
  and structural fidelity (headings, paragraph styles, character runs, fonts,
  sizes, colors, alignments, tables, cells, margins, sections, and placeholders).
  Use whenever the user wants to read or understand a Word document, check its
  formatting, prepare to insert statistical results, or edit document content.
---

# Word Document (.docx) Reader & Inspector Skill

This skill equips the agent with a dedicated, high-fidelity tool to read and inspect Microsoft Word (`.docx`) documents directly from the terminal or scripts. It preserves and exposes layout, typography, headings hierarchy, table matrices, cell properties, and insertion placeholders.

## Tool Script Location
`c:/Users/fungicoder/Documents/Fungicoder/Dev/tesis-mtci-analisis/.agents/skills/docx-reader/scripts/read_docx.py`

Execute via `uv run python`:
```bash
uv run python .agents/skills/docx-reader/scripts/read_docx.py <ruta_al_documento.docx> [opciones]
```

---

## Command Modes & Use Cases

### 1. Executive Overview & Outline (Recommended first step)
Shows metadata, statistics, page margins, paragraph styles in use, full heading hierarchy with indices, tables summary, and detected placeholders.
```bash
uv run python .agents/skills/docx-reader/scripts/read_docx.py documento.docx --overview
```

### 2. Standard View (Overview + Formatted Markdown)
Generates the summary plus a markdown-rendered version of the text, preserving headings, bold/italics, and markdown tables.
```bash
uv run python .agents/skills/docx-reader/scripts/read_docx.py documento.docx
```

### 3. Detailed Structural & Formatting Breakdown
Displays every element in document sequence with run-level tokens (`[BOLD]`, `[ITALIC]`, `[Font: Name, Size: Xpt, Color: #HEX]`), alignments (`CENTER`, `JUSTIFY`), spacing, indents, and table structures.
```bash
uv run python .agents/skills/docx-reader/scripts/read_docx.py documento.docx --detailed
```

### 4. Search for Placeholders, Keywords, or Sections
Quickly locates specific terms, section titles, or placeholders (e.g. `{{TABLA_RESULTADOS}}`, `[INSERTAR]`, `ANCOVA`) in paragraphs and tables, displaying their exact paragraph (`[P#]`) or table (`[T#]`) index.
```bash
uv run python .agents/skills/docx-reader/scripts/read_docx.py documento.docx --search "ANCOVA"
```

### 5. Inspect Styles Catalog
Catalogs all paragraph, character, and table styles available in the document, including fonts, sizes, and colors. Crucial when preparing to insert new paragraphs or tables so they match the exact document styles.
```bash
uv run python .agents/skills/docx-reader/scripts/read_docx.py documento.docx --styles
```

### 6. Inspect Specific Paragraph or Table
Dumps complete JSON structure for a single element.
```bash
uv run python .agents/skills/docx-reader/scripts/read_docx.py documento.docx --paragraph 5
uv run python .agents/skills/docx-reader/scripts/read_docx.py documento.docx --table 0
```

### 7. Range Selection (For large documents / theses)
Extracts only a slice of elements (e.g. from element index 10 to 40) to conserve token context.
```bash
uv run python .agents/skills/docx-reader/scripts/read_docx.py documento.docx --range 10 40 --detailed
```

### 8. Export to File
Saves the output directly to a file (Markdown, text, or JSON).
```bash
uv run python .agents/skills/docx-reader/scripts/read_docx.py documento.docx --markdown --output documento_extraido.md
uv run python .agents/skills/docx-reader/scripts/read_docx.py documento.docx --json --output documento_datos.json
```

---

## Workflow for Inserting Results and Editing .docx

When the user asks to insert results (tables, statistics, charts, paragraphs) into a Word document:

1. **Inspect First**: Run `--overview` and `--search` to locate where results should go (e.g., target headings, placeholders, or after specific tables).
2. **Identify Styles**: Run `--styles` or check the target paragraph's style to replicate the exact formatting (font family, font size, paragraph alignment, line spacing, table style).
3. **Target Element by Index**: Use the element indices (`elem_idx`, `p_idx`, `t_idx`) to know exactly where in `doc.element.body` or `doc.paragraphs` the insertion or replacement will take place.
4. **Insert / Edit**: Use `python-docx` scripts to edit the document, adding styled paragraphs (`doc.add_paragraph(..., style=...)`), inserting tables (`doc.add_table(...)`), or modifying existing runs while preserving original document formatting.
