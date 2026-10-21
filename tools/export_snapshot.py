#!/usr/bin/env python3
"""
CLI Utility to Export and Synchronize Project Snapshot and Data Assets.
Wraps core.storage.export_project_snapshot and verifies filesystem artifacts.
"""

import os
import sys

# Reconfigure stdout/stderr for Unicode/UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
PRISMA_SCR_FALLBACK = r"c:\Users\fungicoder\Documents\Fungicoder\Dev\prisma-scr"
if os.path.exists(PRISMA_SCR_FALLBACK) and PRISMA_SCR_FALLBACK not in sys.path:
    sys.path.append(PRISMA_SCR_FALLBACK)

from core.storage import export_project_snapshot, SNAPSHOT_PATH, CSV_TABLE1_PATH
from tools.coherence_audit import run_full_audit
from tools.asset_builder import build_all_assets


def main():
    print("=" * 60)
    print("📦 EXPORTING AND SYNCHRONIZING PRISMA-ScR REPOSITORY ASSETS")
    print("=" * 60)

    # 1. Run coherence audit with fix
    print("1. Auditing coherence and updating checklist progress...")
    audit_res = run_full_audit(fix=True)

    # 2. Build all empirical manuscript assets
    print("2. Regenerating manuscript assets, tables, and diagrams...")
    manifest = build_all_assets()

    # 3. Export snapshot
    print("3. Exporting SQLite snapshot to JSON and CSV...")
    snap_res = export_project_snapshot()

    print(f"\n✅ Sincronización completa:")
    print(f"  • Snapshot JSON:  {SNAPSHOT_PATH} ({os.path.getsize(SNAPSHOT_PATH)} bytes)")
    print(f"  • Matriz CSV:     {CSV_TABLE1_PATH} ({os.path.getsize(CSV_TABLE1_PATH)} bytes)")
    print(f"  • Diagrama SVG:   assets/prisma_flow_diagram.svg")
    print(f"  • Coherence:      state/coherence_matrix.json")
    print(f"  • Manifest:       state/manuscript_assets.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
