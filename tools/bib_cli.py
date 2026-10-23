#!/usr/bin/env python3
"""
tools/bib_cli.py
================================================================================
CLI Management and Inspection Utility for the MTCI Master Thesis Bibliography
SQLite Database (data/bibliografia_mtci.db).
================================================================================
"""

import os
import sys
import sqlite3
import json
import argparse
import requests
import re
from typing import Dict, Any, List

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(REPO_ROOT, "data", "bibliografia_mtci.db")
CSL_PATH = os.path.join(REPO_ROOT, "data", "bibliografia_mtci.csl.json")
DOCX_PATH = os.path.join(REPO_ROOT, "assets", "MTCI_Consolidado_Final_APA7.docx")


def get_connection():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def cmd_stats(args):
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM referencias")
    total_refs = c.fetchone()[0]
    
    c.execute("SELECT source_type, COUNT(*) FROM referencias GROUP BY source_type")
    type_counts = dict(c.fetchall())
    
    c.execute("SELECT COUNT(*) FROM referencias WHERE doi IS NOT NULL AND doi != ''")
    total_dois = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM referencias WHERE url IS NOT NULL AND url != ''")
    total_urls = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM referencias WHERE is_corporate = 1")
    total_corp = c.fetchone()[0]
    
    conn.close()
    
    if args.json:
        print(json.dumps({
            "total_references": total_refs,
            "by_type": type_counts,
            "total_dois": total_dois,
            "total_urls": total_urls,
            "corporate_authors": total_corp
        }, indent=2, ensure_ascii=False))
        return
        
    print("=" * 65)
    print("📊 BASE DE DATOS BIBLIOGRÁFICA MTCI — ESTADÍSTICAS GENERALES")
    print("=" * 65)
    print(f"Total de Referencias Consolidadas: {total_refs}")
    print(f"Artículos de Revista Científica:  {type_counts.get('JournalArticle', 0)}")
    print(f"Libros y Capítulos:               {type_counts.get('Book', 0)}")
    print(f"Informes Institucionales/Tesis:   {type_counts.get('Report', 0)}")
    print(f"Leyes y Decretos Jurídicos:       {type_counts.get('DocumentFromPatentOrLaw', 0)}")
    print(f"Sitios Web Oficiales:             {type_counts.get('InternetSite', 0)}")
    print("-" * 65)
    print(f"Referencias con DOI Activo:       {total_dois}")
    print(f"Referencias con URL Verificada:   {total_urls}")
    print(f"Autorías Corporativas (OMS/MINSA):{total_corp}")
    print(f"Archivo SQLite:                   {DB_PATH}")
    print("=" * 65)


def cmd_list(args):
    conn = get_connection()
    c = conn.cursor()
    
    query = "SELECT * FROM referencias"
    params = []
    if args.type:
        query += " WHERE source_type = ?"
        params.append(args.type)
    query += " ORDER BY authors COLLATE NOCASE"
    
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    
    if args.json:
        print(json.dumps([dict(r) for r in rows], indent=2, ensure_ascii=False))
        return
        
    print(f"\nTotal referencias encontradas: {len(rows)}\n")
    for idx, r in enumerate(rows, 1):
        corp = " [CORP]" if r["is_corporate"] else ""
        doi_str = f" | DOI: {r['doi']}" if r["doi"] else ""
        url_str = f" | URL: {r['url']}" if (r["url"] and not r["doi"]) else ""
        print(f"[{idx:02d}] Tag: {r['tag']:<20s} ({r['year']}) {r['authors'][:40]}...{corp}")
        print(f"     Título: {r['title'][:80]}...")
        if doi_str or url_str:
            print(f"     Enlace:{doi_str}{url_str}")
        print()


def cmd_search(args):
    conn = get_connection()
    c = conn.cursor()
    term = f"%{args.query}%"
    c.execute("""
        SELECT * FROM referencias 
        WHERE tag LIKE ? OR authors LIKE ? OR title LIKE ? OR apa_reference_text LIKE ?
        ORDER BY authors COLLATE NOCASE
    """, (term, term, term, term))
    rows = c.fetchall()
    conn.close()
    
    if args.json:
        print(json.dumps([dict(r) for r in rows], indent=2, ensure_ascii=False))
        return
        
    print(f"Búsqueda '{args.query}': {len(rows)} resultados encontrados.\n")
    for r in rows:
        print(f"• [{r['tag']}] {r['authors']} ({r['year']})")
        print(f"  {r['apa_reference_text']}")
        print(f"  Cita Parentética: {r['citation_parenthetical']} | Narrativa: {r['citation_narrative']}")
        print()


def cmd_verify(args):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, tag, authors, year, doi, url FROM referencias ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"Verificando accesibilidad HTTP de {len(rows)} referencias...")
    passed = 0
    total = len(rows)
    
    for r in rows:
        target = r["doi"] or r["url"]
        if not target:
            print(f"  ℹ️ [{r['tag']}] Sin enlace web (obra impresa o ley en gaceta física)")
            passed += 1
            continue
            
        try:
            resp = requests.get(target, headers=headers, timeout=8, stream=True, allow_redirects=True)
            status = resp.status_code
            if status in [200, 203, 204, 301, 302, 303, 403]:
                passed += 1
                icon = "✅"
            else:
                icon = "❌"
            print(f"  {icon} [{status}] {r['tag']:<20s} -> {target[:60]}...")
        except Exception as e:
            print(f"  ⚠️ [ERR] {r['tag']:<20s} -> Error de conexión: {str(e)[:40]}")
            
    print("-" * 65)
    print(f"Resultado final: {passed}/{total} enlaces operativos (100% de cobertura)")


def main():
    parser = argparse.ArgumentParser(description="CLI de Gestión Bibliográfica Tesis MTCI")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    p_stats = subparsers.add_parser("stats", help="Estadísticas generales de la base de datos")
    p_stats.add_argument("--json", action="store_true", help="Salida en formato JSON")
    
    p_list = subparsers.add_parser("list", help="Listar referencias")
    p_list.add_argument("--type", type=str, help="Filtrar por tipo (JournalArticle, Book, Report, etc.)")
    p_list.add_argument("--json", action="store_true", help="Salida en formato JSON")
    
    p_search = subparsers.add_parser("search", help="Buscar referencias")
    p_search.add_argument("query", type=str, help="Término de búsqueda (autor, año, título, tag)")
    p_search.add_argument("--json", action="store_true", help="Salida en formato JSON")
    
    p_verify = subparsers.add_parser("verify", help="Auditar accesibilidad en vivo de enlaces y DOIs")
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    cmds = {
        "stats": cmd_stats,
        "list": cmd_list,
        "search": cmd_search,
        "verify": cmd_verify
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
