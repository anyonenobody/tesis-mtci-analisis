#!/usr/bin/env python3
"""
CLI Utility for Querying and Managing the PRISMA-ScR SQLite Database.
Allows agent to query flow numbers, list articles, inspect search logs,
and check charting data without running the Streamlit server.
"""

import os
import sys
import json
import argparse

# Reconfigure stdout/stderr for Unicode/UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure repository root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
PRISMA_SCR_FALLBACK = r"c:\Users\fungicoder\Documents\Fungicoder\Dev\prisma-scr"
if os.path.exists(PRISMA_SCR_FALLBACK) and PRISMA_SCR_FALLBACK not in sys.path:
    sys.path.append(PRISMA_SCR_FALLBACK)

from core.storage import (
    get_connection,
    get_prisma_flow_numbers,
    get_articles,
    get_charting_data,
    get_search_logs,
    get_checklist,
    update_screening_status,
    export_project_snapshot,
    reset_database
)


def cmd_stats(args):
    flow = get_prisma_flow_numbers()
    charting = get_charting_data()
    logs = get_search_logs()
    
    if args.json:
        print(json.dumps({
            "flow_numbers": flow,
            "charting_rows": len(charting),
            "search_logs_count": len(logs)
        }, indent=2, ensure_ascii=False))
        return

    print("=" * 60)
    print("📊 PRISMA-ScR DATABASE STATISTICS")
    print("=" * 60)
    print(f"Total Identified:       {flow['total_identified']}")
    print(f"Duplicates Removed:     {flow['duplicates_removed']}")
    print(f"Records Screened (P1):  {flow['records_screened']}")
    print(f"Excluded in Phase 1:    {flow['records_excluded_phase1']}")
    print(f"Full-Text Assessed:     {flow['full_text_assessed']}")
    print(f"Excluded in Phase 2:    {flow['full_text_excluded']}")
    print(f"Studies Included:       {flow['studies_included']}")
    print(f"Charting Records:       {len(charting)}")
    print(f"Search Log Runs:        {len(logs)}")
    print("\nMotivos de Exclusión a Texto Completo:")
    for r, q in flow.get("exclusion_reasons", {}).items():
        print(f"  • {r}: {q}")
    print("=" * 60)


def cmd_articles(args):
    articles = get_articles(include_duplicates=args.all)
    if args.status:
        articles = [a for a in articles if a.get("screening_status") == args.status]
    
    if args.json:
        print(json.dumps([dict(a) for a in articles], indent=2, ensure_ascii=False))
        return

    print(f"Total Articles matching: {len(articles)}")
    for a in articles:
        dup = " [DUPLICADO]" if a.get("is_duplicate") else ""
        reason = f" | Motivo: {a.get('exclusion_reason')}" if a.get("exclusion_reason") else ""
        print(f"[{a['id']}] {a.get('screening_status')}{dup}: {a.get('authors', 'S/A')} ({a.get('year', 'S/F')}) - {a.get('title')}{reason}")


def cmd_charting(args):
    charting = get_charting_data()
    if args.json:
        print(json.dumps(charting, indent=2, ensure_ascii=False))
        return

    print(f"Total Charted Studies: {len(charting)}")
    for c in charting:
        print(f"\n--- Artículo ID {c['article_id']}: {c.get('authors')} ({c.get('year')}) ---")
        print(f"  País:         {c.get('country')}")
        print(f"  Diseño:       {c.get('study_design')}")
        print(f"  Muestra:      {c.get('sample_size')} ({c.get('population_description')})")
        print(f"  MTCI:         {c.get('mtci_modality')} - {c.get('mtci_details')}")
        print(f"  Condición:    {c.get('psych_condition')}")
        print(f"  Enfoque:      {c.get('psych_approach')}")
        print(f"  Hallazgos:    {c.get('effectiveness_findings')}")


def cmd_reset(args):
    if not args.confirm:
        print("⚠️ ADVERTENCIA: Esta acción vaciará la base de datos (artículos, extracciones y logs de búsqueda).")
        print("Para confirmar la ejecución desde terminal, añade la bandera --confirm:")
        print("  python tools/db_cli.py reset --confirm")
        sys.exit(1)

    res = reset_database(preserve_protocol=True, backup=not args.no_backup)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    print("=" * 60)
    print("🧹 PRISMA-ScR DATABASE RESET COMPLETADO")
    print("=" * 60)
    if res.get("backup_path"):
        print(f"📦 Respaldo previo guardado en: {res['backup_path']}")
    print(f"📄 Artículos actuales:         {res['articles_count']}")
    print(f"📑 Extracciones (Tabla 1):     {res['charting_count']}")
    print(f"📜 Logs de Búsqueda:           {res['search_logs_count']}")
    print(f"📋 Checklist PRISMA reseteado: {res['checklist_reset_count']} ítems en 'Pendiente'")
    print(f"💾 Snapshot limpio:            {res['snapshot_path']}")
    print(f"📊 Diagrama SVG:               {res['svg_path']}")
    print("=" * 60)
    print("✨ Base de datos lista para una nueva cosecha sistemática desde cero.")


def main():
    parser = argparse.ArgumentParser(description="PRISMA-ScR SQLite DB CLI")
    subparsers = parser.add_subparsers(dest="command")

    # stats
    p_stats = subparsers.add_parser("stats", help="Mostrar resumen cuantitativo del flujo PRISMA")
    p_stats.add_argument("--json", action="store_true", help="Salida en JSON")

    # articles
    p_art = subparsers.add_parser("articles", help="Listar artículos en la base")
    p_art.add_argument("--all", action="store_true", help="Incluir duplicados")
    p_art.add_argument("--status", type=str, help="Filtrar por screening_status (included_phase2, excluded_phase2, etc.)")
    p_art.add_argument("--json", action="store_true", help="Salida en JSON")

    # charting
    p_chart = subparsers.add_parser("charting", help="Listar datos extraídos (Data Charting)")
    p_chart.add_argument("--json", action="store_true", help="Salida en JSON")

    # reset
    p_reset = subparsers.add_parser("reset", help="Resetear la base de datos a 0 para iniciar de cero")
    p_reset.add_argument("--confirm", action="store_true", help="Confirmar el borrado de registros")
    p_reset.add_argument("--no-backup", action="store_true", help="Omitir respaldo del snapshot previo")
    p_reset.add_argument("--json", action="store_true", help="Salida en JSON")

    args = parser.parse_args()
    if args.command == "stats" or not args.command:
        cmd_stats(args)
    elif args.command == "articles":
        cmd_articles(args)
    elif args.command == "charting":
        cmd_charting(args)
    elif args.command == "reset":
        cmd_reset(args)


if __name__ == "__main__":
    main()

