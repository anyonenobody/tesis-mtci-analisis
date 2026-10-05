#!/usr/bin/env python3
"""
read_docx.py - Advanced Word Document (.docx) Reader and Inspector
===================================================================
A CLI tool designed for AI agents and developers to inspect Word documents
with full structural and formatting fidelity (headings, styles, runs, fonts,
sizes, colors, alignments, tables, cells, margins, sections, and placeholders).

Usage:
    uv run python read_docx.py <path_to_docx> [options]
    python read_docx.py <path_to_docx> [options]

Modes & Options:
    --overview, -o        Print executive summary, outline/TOC, and tables overview.
    --markdown, -m        Output clean Markdown representation.
    --detailed, -d        Output exhaustive formatting breakdown (runs, fonts, pt sizes, colors).
    --json, -j            Dump complete document model as JSON.
    --styles, -s          List all styles defined and used in the document.
    --search <text>, -q   Search text, regex, or placeholders across paragraphs and tables.
    --range <start> <end> Element index range to output (for large documents).
    --paragraph <idx>     Inspect specific paragraph in deep detail.
    --table <idx>         Inspect specific table in deep detail.
    --output <filepath>   Save the output to a file.
"""

import sys
import os
import re
import json
import argparse
from typing import Dict, List, Any, Optional

try:
    import docx
    from docx.text.paragraph import Paragraph
    from docx.table import Table
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
except ImportError:
    sys.stderr.write(
        "Error: 'python-docx' is required. Run 'uv add python-docx' or 'pip install python-docx'.\n"
    )
    sys.exit(1)


# Helper formatting functions
def pt_to_str(length_obj) -> Optional[str]:
    if length_obj is None:
        return None
    try:
        return f"{length_obj.pt:.1f}pt"
    except Exception:
        return None


def cm_to_str(length_obj) -> Optional[str]:
    if length_obj is None:
        return None
    try:
        return f"{length_obj.cm:.2f}cm"
    except Exception:
        return None


def get_alignment_name(alignment) -> Optional[str]:
    if alignment is None:
        return None
    try:
        # WD_ALIGN_PARAGRAPH enum values
        val_map = {
            WD_ALIGN_PARAGRAPH.LEFT: "LEFT",
            WD_ALIGN_PARAGRAPH.CENTER: "CENTER",
            WD_ALIGN_PARAGRAPH.RIGHT: "RIGHT",
            WD_ALIGN_PARAGRAPH.JUSTIFY: "JUSTIFY",
            WD_ALIGN_PARAGRAPH.DISTRIBUTE: "DISTRIBUTE",
        }
        return val_map.get(alignment, str(alignment))
    except Exception:
        return str(alignment)


def get_cell_shading(cell) -> Optional[str]:
    """Extract cell background fill color from oxml if present."""
    try:
        tcPr = cell._tc.get_or_add_tcPr()
        shd = tcPr.find(qn("w:shd"))
        if shd is not None:
            fill = shd.get(qn("w:fill"))
            if fill and fill.lower() not in ("auto", "none"):
                return f"#{fill}"
    except Exception:
        pass
    return None


class DocxInspector:
    def __init__(self, file_path: str):
        self.file_path = os.path.abspath(file_path)
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        self.doc = docx.Document(self.file_path)
        self.data: Dict[str, Any] = {
            "file": {
                "name": os.path.basename(self.file_path),
                "path": self.file_path,
                "size_bytes": os.path.getsize(self.file_path),
            },
            "metadata": self._extract_metadata(),
            "sections": self._extract_sections(),
            "elements": [],
            "headings_outline": [],
            "tables_summary": [],
            "style_usage": {},
            "placeholders": [],
        }
        self._parse_body()

    def _extract_metadata(self) -> Dict[str, Any]:
        meta: Dict[str, Any] = {}
        try:
            cp = self.doc.core_properties
            meta["title"] = cp.title or ""
            meta["author"] = cp.author or ""
            meta["subject"] = cp.subject or ""
            meta["keywords"] = cp.keywords or ""
            meta["comments"] = cp.comments or ""
            meta["last_modified_by"] = cp.last_modified_by or ""
            meta["revision"] = str(cp.revision) if cp.revision is not None else ""
            meta["created"] = str(cp.created) if cp.created else ""
            meta["modified"] = str(cp.modified) if cp.modified else ""
        except Exception as e:
            meta["error"] = str(e)
        return meta

    def _extract_sections(self) -> List[Dict[str, Any]]:
        sections_data = []
        for idx, sec in enumerate(self.doc.sections):
            header_text = ""
            footer_text = ""
            try:
                header_text = "\n".join(p.text for p in sec.header.paragraphs if p.text.strip())
                footer_text = "\n".join(p.text for p in sec.footer.paragraphs if p.text.strip())
            except Exception:
                pass

            sec_info = {
                "index": idx,
                "orientation": "LANDSCAPE" if sec.orientation == 1 else "PORTRAIT",
                "page_width": cm_to_str(sec.page_width),
                "page_height": cm_to_str(sec.page_height),
                "margins": {
                    "top": cm_to_str(sec.top_margin),
                    "bottom": cm_to_str(sec.bottom_margin),
                    "left": cm_to_str(sec.left_margin),
                    "right": cm_to_str(sec.right_margin),
                },
                "header": header_text.strip(),
                "footer": footer_text.strip(),
            }
            sections_data.append(sec_info)
        return sections_data

    def _parse_body(self):
        p_count = 0
        t_count = 0
        elem_idx = 0

        # Pattern for typical placeholders like {{key}}, <<key>>, [INSERTAR...], {TODO}
        placeholder_pattern = re.compile(r"(\{\{[^}]+\}\}|<<[^>]+>>|\[(INSERTAR|TODO|COMPLETAR|TABLA|GRAFICO)[^\]]*\]|\{[a-zA-Z0-9_]+\})", re.IGNORECASE)

        for child in self.doc.element.body:
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag

            if tag == "p":
                p = Paragraph(child, self.doc)
                p_data = self._parse_paragraph(p, p_count, elem_idx)
                self.data["elements"].append(p_data)

                # Record style usage
                st_name = p_data["style"]
                self.data["style_usage"][st_name] = self.data["style_usage"].get(st_name, 0) + 1

                # Record outline if heading
                if p_data["heading_level"] is not None and p_data["text"].strip():
                    self.data["headings_outline"].append({
                        "level": p_data["heading_level"],
                        "style": st_name,
                        "text": p_data["text"].strip(),
                        "elem_idx": elem_idx,
                        "p_idx": p_count,
                    })

                # Check for placeholders
                for match in placeholder_pattern.finditer(p_data["text"]):
                    self.data["placeholders"].append({
                        "placeholder": match.group(0),
                        "elem_idx": elem_idx,
                        "p_idx": p_count,
                        "context": p_data["text"].strip(),
                    })

                p_count += 1
                elem_idx += 1

            elif tag == "tbl":
                tbl = Table(child, self.doc)
                t_data = self._parse_table(tbl, t_count, elem_idx)
                self.data["elements"].append(t_data)

                self.data["tables_summary"].append({
                    "tbl_idx": t_count,
                    "elem_idx": elem_idx,
                    "style": t_data["style"],
                    "rows": t_data["rows_count"],
                    "cols": t_data["cols_count"],
                    "headers": t_data["headers"],
                })

                # Search placeholders in table cells
                for r_idx, row in enumerate(t_data["matrix"]):
                    for c_idx, cell_str in enumerate(row):
                        for match in placeholder_pattern.finditer(cell_str):
                            self.data["placeholders"].append({
                                "placeholder": match.group(0),
                                "elem_idx": elem_idx,
                                "t_idx": t_count,
                                "cell": f"R{r_idx}C{c_idx}",
                                "context": cell_str.strip(),
                            })

                t_count += 1
                elem_idx += 1

        self.data["stats"] = {
            "total_elements": elem_idx,
            "total_paragraphs": p_count,
            "total_tables": t_count,
            "total_sections": len(self.data["sections"]),
            "total_words": sum(len(el.get("text", "").split()) for el in self.data["elements"] if el["type"] == "paragraph"),
        }

    def _parse_paragraph(self, p: Paragraph, p_idx: int, elem_idx: int) -> Dict[str, Any]:
        style_name = p.style.name if (p.style and p.style.name) else "Normal"
        heading_level = None

        if style_name.startswith("Heading"):
            try:
                heading_level = int(style_name.replace("Heading", "").strip())
            except ValueError:
                heading_level = 1
        elif style_name.lower() in ("title", "título"):
            heading_level = 0
        elif style_name.lower() in ("subtitle", "subtítulo"):
            heading_level = 2

        # Check list items
        is_list = False
        pPr = p._element.pPr
        if pPr is not None and pPr.find(qn("w:numPr")) is not None:
            is_list = True
        elif "list" in style_name.lower():
            is_list = True

        # Check image drawings
        drawings = p._element.xpath(".//w:drawing")
        images_count = len(drawings)

        # Runs extraction
        runs_data = []
        for r in p.runs:
            if not r.text:
                continue
            r_info = {
                "text": r.text,
                "bold": bool(r.bold) if r.bold is not None else None,
                "italic": bool(r.italic) if r.italic is not None else None,
                "underline": bool(r.underline) if r.underline is not None else None,
                "font_name": r.font.name if r.font and r.font.name else None,
                "font_size": pt_to_str(r.font.size) if r.font and r.font.size else None,
                "color": f"#{r.font.color.rgb}" if r.font and r.font.color and r.font.color.rgb else None,
            }
            runs_data.append(r_info)

        pf = p.paragraph_format
        return {
            "type": "paragraph",
            "elem_idx": elem_idx,
            "p_idx": p_idx,
            "style": style_name,
            "heading_level": heading_level,
            "is_list": is_list,
            "alignment": get_alignment_name(p.alignment),
            "spacing_before": pt_to_str(pf.space_before),
            "spacing_after": pt_to_str(pf.space_after),
            "line_spacing": pf.line_spacing if pf.line_spacing else None,
            "left_indent": cm_to_str(pf.left_indent),
            "right_indent": cm_to_str(pf.right_indent),
            "first_line_indent": cm_to_str(pf.first_line_indent),
            "images_count": images_count,
            "runs": runs_data,
            "text": p.text,
        }

    def _parse_table(self, tbl: Table, t_idx: int, elem_idx: int) -> Dict[str, Any]:
        style_name = tbl.style.name if (tbl.style and tbl.style.name) else "Table Grid"
        rows_count = len(tbl.rows)
        cols_count = len(tbl.columns) if tbl.columns else (len(tbl.rows[0].cells) if rows_count > 0 else 0)

        matrix = []
        headers = []
        cells_detail = []

        for r_idx, row in enumerate(tbl.rows):
            row_texts = []
            for c_idx, cell in enumerate(row.cells):
                cell_text = cell.text.strip()
                row_texts.append(cell_text)

                shd = get_cell_shading(cell)
                if shd or len(cell.paragraphs) > 1:
                    cells_detail.append({
                        "row": r_idx,
                        "col": c_idx,
                        "text": cell_text,
                        "background": shd,
                        "paragraphs_count": len(cell.paragraphs),
                    })

            matrix.append(row_texts)
            if r_idx == 0:
                headers = row_texts

        return {
            "type": "table",
            "elem_idx": elem_idx,
            "t_idx": t_idx,
            "style": style_name,
            "alignment": get_alignment_name(tbl.alignment),
            "rows_count": rows_count,
            "cols_count": cols_count,
            "headers": headers,
            "matrix": matrix,
            "cells_detail": cells_detail,
        }

    # -------------------------------------------------------------
    # Output formatting methods
    # -------------------------------------------------------------
    def get_overview_str(self) -> str:
        lines: List[str] = []
        lines.append("=" * 70)
        lines.append(f"📄 DOCUMENT OVERVIEW: {self.data['file']['name']}")
        lines.append("=" * 70)
        lines.append(f"• File Path: {self.data['file']['path']}")
        lines.append(f"• File Size: {self.data['file']['size_bytes'] / 1024:.1f} KB")

        # Stats
        st = self.data["stats"]
        lines.append(f"• Statistics: {st['total_paragraphs']} paragraphs, {st['total_tables']} tables, {st['total_sections']} sections, ~{st['total_words']} words")

        # Metadata
        meta = self.data["metadata"]
        lines.append("\n📌 Core Metadata:")
        for k, v in meta.items():
            if v:
                lines.append(f"  - {k.capitalize()}: {v}")

        # Page setup
        lines.append("\n📐 Page Setup & Margins:")
        for sec in self.data["sections"]:
            m = sec["margins"]
            lines.append(f"  - Section {sec['index']}: {sec['orientation']} ({sec['page_width']} x {sec['page_height']}), Margins: [T: {m['top']}, B: {m['bottom']}, L: {m['left']}, R: {m['right']}]")
            if sec["header"]:
                lines.append(f"    Header: {sec['header'][:80]}...")
            if sec["footer"]:
                lines.append(f"    Footer: {sec['footer'][:80]}...")

        # Styles used
        lines.append("\n🎨 Paragraph Styles in Use:")
        for sname, count in sorted(self.data["style_usage"].items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  - {sname}: {count} paragraphs")

        # Headings Outline
        lines.append("\n📑 Document Structure Outline (Table of Contents):")
        if not self.data["headings_outline"]:
            lines.append("  (No standard heading styles detected)")
        else:
            for h in self.data["headings_outline"]:
                indent = "  " * (h["level"] if h["level"] > 0 else 0)
                tag = f"[H{h['level']} | P{h['p_idx']}]" if h["level"] > 0 else f"[TITLE | P{h['p_idx']}]"
                lines.append(f"{indent}{tag} {h['text']}")

        # Tables summary
        lines.append("\n📊 Tables Overview:")
        if not self.data["tables_summary"]:
            lines.append("  (No tables found in document)")
        else:
            for t in self.data["tables_summary"]:
                headers_preview = " | ".join(t["headers"][:4])
                if len(t["headers"]) > 4:
                    headers_preview += "..."
                lines.append(f"  - [T{t['tbl_idx']} | Elem {t['elem_idx']}]: {t['rows']} rows x {t['cols']} cols | Style: '{t['style']}' | Headers: [{headers_preview}]")

        # Placeholders
        if self.data["placeholders"]:
            lines.append("\n🔍 Detected Placeholders / Tags:")
            for p in self.data["placeholders"]:
                target = f"P{p['p_idx']}" if "p_idx" in p else f"T{p['t_idx']} {p.get('cell','')}"
                lines.append(f"  - [{target}] Tag: `{p['placeholder']}` in \"{p['context'][:60]}...\"")

        lines.append("=" * 70)
        return "\n".join(lines)

    def get_markdown_str(self, start_idx: int = 0, end_idx: Optional[int] = None) -> str:
        lines: List[str] = []
        elements = self.data["elements"]
        if end_idx is None:
            end_idx = len(elements)

        for el in elements[start_idx:end_idx]:
            if el["type"] == "paragraph":
                txt = el["text"].strip()
                if not txt:
                    lines.append("")
                    continue

                h_level = el["heading_level"]
                if h_level is not None:
                    if h_level == 0:
                        lines.append(f"\n# {txt} <!-- [P{el['p_idx']} Style: {el['style']}] -->\n")
                    else:
                        prefix = "#" * min(h_level, 6)
                        lines.append(f"\n{prefix} {txt} <!-- [P{el['p_idx']} Style: {el['style']}] -->\n")
                elif el["is_list"]:
                    lines.append(f"- {txt}")
                else:
                    # Format text with runs if bold/italic present
                    formatted_runs = []
                    for r in el["runs"]:
                        r_txt = r["text"]
                        if r["bold"] and r["italic"]:
                            r_txt = f"***{r_txt}***"
                        elif r["bold"]:
                            r_txt = f"**{r_txt}**"
                        elif r["italic"]:
                            r_txt = f"*{r_txt}*"
                        formatted_runs.append(r_txt)
                    p_body = "".join(formatted_runs).strip() or txt
                    lines.append(p_body)

            elif el["type"] == "table":
                lines.append(f"\n<!-- [Table T{el['t_idx']} ({el['rows_count']}x{el['cols_count']}) Style: {el['style']}] -->")
                matrix = el["matrix"]
                if not matrix:
                    continue

                # Header row
                header_row = [c.replace("\n", " ").strip() for c in matrix[0]]
                lines.append("| " + " | ".join(header_row) + " |")
                lines.append("| " + " | ".join(["---"] * len(header_row)) + " |")

                # Data rows
                for row in matrix[1:]:
                    clean_row = [c.replace("\n", " ").strip() for c in row]
                    # Ensure column count matches header
                    while len(clean_row) < len(header_row):
                        clean_row.append("")
                    lines.append("| " + " | ".join(clean_row[:len(header_row)]) + " |")
                lines.append("")

        return "\n".join(lines)

    def get_detailed_str(self, start_idx: int = 0, end_idx: Optional[int] = None) -> str:
        lines: List[str] = []
        elements = self.data["elements"]
        if end_idx is None:
            end_idx = len(elements)

        lines.append(self.get_overview_str())
        lines.append("\n" + "=" * 70)
        lines.append(f"🔍 DETAILED STRUCTURAL CONTENT (Elements {start_idx} to {end_idx - 1}):")
        lines.append("=" * 70 + "\n")

        for el in elements[start_idx:end_idx]:
            if el["type"] == "paragraph":
                prop_tokens = []
                if el["style"] != "Normal":
                    prop_tokens.append(f"Style: '{el['style']}'")
                if el["alignment"]:
                    prop_tokens.append(f"Align: {el['alignment']}")
                if el["spacing_before"]:
                    prop_tokens.append(f"Before: {el['spacing_before']}")
                if el["spacing_after"]:
                    prop_tokens.append(f"After: {el['spacing_after']}")
                if el["left_indent"]:
                    prop_tokens.append(f"Indent: {el['left_indent']}")
                if el["images_count"] > 0:
                    prop_tokens.append(f"Images: {el['images_count']}")

                props_str = f" | {', '.join(prop_tokens)}" if prop_tokens else ""
                lines.append(f"----------------------------------------------------------------------")
                lines.append(f"[P{el['p_idx']:03d} | Elem {el['elem_idx']:03d}{props_str}]")
                
                # Show runs if text exists
                if not el["text"].strip():
                    lines.append("  <Empty paragraph>")
                else:
                    lines.append(f"  Text: {el['text']}")
                    # Runs breakdown if multiple runs or special formatting
                    has_format = any(r["bold"] or r["italic"] or r["font_name"] or r["font_size"] or r["color"] for r in el["runs"])
                    if has_format or len(el["runs"]) > 1:
                        lines.append("  Runs:")
                        for r_i, r in enumerate(el["runs"]):
                            fmt = []
                            if r["bold"]: fmt.append("BOLD")
                            if r["italic"]: fmt.append("ITALIC")
                            if r["underline"]: fmt.append("UNDERLINE")
                            if r["font_name"]: fmt.append(f"Font: {r['font_name']}")
                            if r["font_size"]: fmt.append(f"Size: {r['font_size']}")
                            if r["color"]: fmt.append(f"Color: {r['color']}")
                            fmt_tag = f" [{', '.join(fmt)}]" if fmt else ""
                            lines.append(f"    ({r_i}) {repr(r['text'])}{fmt_tag}")

            elif el["type"] == "table":
                lines.append(f"----------------------------------------------------------------------")
                lines.append(f"[T{el['t_idx']:03d} | Elem {el['elem_idx']:03d}] Table: {el['rows_count']} rows x {el['cols_count']} cols | Style: '{el['style']}' | Align: {el['alignment']}")
                
                # Table markdown representation
                matrix = el["matrix"]
                if matrix:
                    header = [c.replace("\n", " ").strip() for c in matrix[0]]
                    lines.append("  | " + " | ".join(header) + " |")
                    lines.append("  | " + " | ".join(["---"] * len(header)) + " |")
                    for row in matrix[1:]:
                        clean_row = [c.replace("\n", " ").strip() for c in row]
                        while len(clean_row) < len(header):
                            clean_row.append("")
                        lines.append("  | " + " | ".join(clean_row[:len(header)]) + " |")
                
                if el["cells_detail"]:
                    lines.append("  Cell details (shading / multi-paragraph):")
                    for cd in el["cells_detail"][:10]:
                        lines.append(f"    R{cd['row']}C{cd['col']}: BG: {cd['background']}, Paragraphs: {cd['paragraphs_count']}")
                    if len(el["cells_detail"]) > 10:
                        lines.append(f"    ... and {len(el['cells_detail']) - 10} more cells")

        return "\n".join(lines)

    def search(self, query: str) -> str:
        lines: List[str] = []
        lines.append("=" * 70)
        lines.append(f"🔍 SEARCH RESULTS FOR: '{query}' in {self.data['file']['name']}")
        lines.append("=" * 70)

        pattern = re.compile(re.escape(query), re.IGNORECASE)
        matches = 0

        for el in self.data["elements"]:
            if el["type"] == "paragraph":
                if pattern.search(el["text"]):
                    matches += 1
                    lines.append(f"\n• [P{el['p_idx']} | Elem {el['elem_idx']} | Style: '{el['style']}']")
                    highlighted = pattern.sub(lambda m: f"**>>>{m.group(0)}<<<**", el["text"])
                    lines.append(f"  {highlighted.strip()}")

            elif el["type"] == "table":
                t_matches = []
                for r_idx, row in enumerate(el["matrix"]):
                    for c_idx, cell_str in enumerate(row):
                        if pattern.search(cell_str):
                            t_matches.append((r_idx, c_idx, cell_str))
                if t_matches:
                    matches += len(t_matches)
                    lines.append(f"\n• [Table T{el['t_idx']} | Elem {el['elem_idx']} | {el['rows_count']}x{el['cols_count']}]")
                    for r, c, txt in t_matches:
                        hl = pattern.sub(lambda m: f"**>>>{m.group(0)}<<<**", txt)
                        lines.append(f"  - Cell [Row {r}, Col {c}]: {hl}")

        lines.append(f"\nTotal matches found: {matches}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def list_styles(self) -> str:
        lines: List[str] = []
        lines.append("=" * 70)
        lines.append(f"🎨 STYLES CATALOG FOR: {self.data['file']['name']}")
        lines.append("=" * 70)

        paragraph_styles: List[str] = []
        table_styles: List[str] = []
        character_styles: List[str] = []

        for s in self.doc.styles:
            name = s.name or "Unknown"
            stype = str(s.type).split(".")[-1]
            usage = self.data["style_usage"].get(name, 0)

            font_desc = []
            if hasattr(s, "font") and s.font:
                if s.font.name: font_desc.append(f"Font: {s.font.name}")
                if s.font.size: font_desc.append(f"Size: {pt_to_str(s.font.size)}")
                if s.font.bold: font_desc.append("Bold")
                if s.font.italic: font_desc.append("Italic")
                if s.font.color and s.font.color.rgb: font_desc.append(f"Color: #{s.font.color.rgb}")

            desc_str = f" ({', '.join(font_desc)})" if font_desc else ""

            entry = f"• '{name}'{desc_str} - In use: {usage} times"
            if "PARAGRAPH" in stype:
                paragraph_styles.append(entry)
            elif "TABLE" in stype:
                table_styles.append(entry)
            elif "CHARACTER" in stype:
                character_styles.append(entry)

        lines.append("\n[PARAGRAPH STYLES]")
        lines.extend(paragraph_styles)
        lines.append("\n[TABLE STYLES]")
        lines.extend(table_styles)
        lines.append("\n[CHARACTER STYLES]")
        lines.extend(character_styles)
        lines.append("=" * 70)
        return "\n".join(lines)

    def get_paragraph_detail(self, p_idx: int) -> str:
        for el in self.data["elements"]:
            if el["type"] == "paragraph" and el["p_idx"] == p_idx:
                return json.dumps(el, indent=2, ensure_ascii=False)
        return f"Error: Paragraph P{p_idx} not found."

    def get_table_detail(self, t_idx: int) -> str:
        for el in self.data["elements"]:
            if el["type"] == "table" and el["t_idx"] == t_idx:
                return json.dumps(el, indent=2, ensure_ascii=False)
        return f"Error: Table T{t_idx} not found."


def main():
    parser = argparse.ArgumentParser(
        description="Inspect and extract Word (.docx) documents with full formatting and structural fidelity.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("docx_path", help="Path to the .docx file")
    parser.add_argument("--overview", "-o", action="store_true", help="Print executive summary, TOC outline, and tables list")
    parser.add_argument("--markdown", "-m", action="store_true", help="Output document converted to Markdown")
    parser.add_argument("--detailed", "-d", action="store_true", help="Print detailed structural and formatting breakdown")
    parser.add_argument("--json", "-j", action="store_true", help="Export full document data as JSON")
    parser.add_argument("--styles", "-s", action="store_true", help="List all styles defined and used in the document")
    parser.add_argument("--search", "-q", type=str, help="Search for text, regex, or placeholders in the document")
    parser.add_argument("--range", "-r", nargs=2, type=int, metavar=("START", "END"), help="Output only elements within [START, END] index")
    parser.add_argument("--paragraph", type=int, metavar="PIDX", help="Inspect a specific paragraph index in JSON")
    parser.add_argument("--table", type=int, metavar="TIDX", help="Inspect a specific table index in JSON")
    parser.add_argument("--output", "-out", type=str, help="Path to write the output to a file instead of stdout")

    args = parser.parse_args()

    try:
        inspector = DocxInspector(args.docx_path)
    except Exception as e:
        sys.stderr.write(f"Error loading document: {e}\n")
        sys.exit(1)

    output_str = ""

    # Range limits
    start_idx = args.range[0] if args.range else 0
    end_idx = args.range[1] if args.range else None

    if args.json:
        output_str = json.dumps(inspector.data, indent=2, ensure_ascii=False)
    elif args.overview:
        output_str = inspector.get_overview_str()
    elif args.styles:
        output_str = inspector.list_styles()
    elif args.search:
        output_str = inspector.search(args.search)
    elif args.paragraph is not None:
        output_str = inspector.get_paragraph_detail(args.paragraph)
    elif args.table is not None:
        output_str = inspector.get_table_detail(args.table)
    elif args.detailed:
        output_str = inspector.get_detailed_str(start_idx, end_idx)
    elif args.markdown:
        output_str = inspector.get_markdown_str(start_idx, end_idx)
    else:
        # Default mode: Overview + Markdown preview
        output_str = inspector.get_overview_str() + "\n\n" + inspector.get_markdown_str(start_idx, end_idx)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_str)
            print(f"Output successfully written to: {args.output}")
        except Exception as e:
            sys.stderr.write(f"Failed to write output to file: {e}\n")
            sys.exit(1)
    else:
        try:
            # Use sys.stdout.reconfigure for utf-8 on Windows terminal if needed
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
            print(output_str)
        except Exception:
            print(output_str.encode("utf-8", errors="replace").decode("utf-8"))


if __name__ == "__main__":
    main()
