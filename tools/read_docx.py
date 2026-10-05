#!/usr/bin/env python3
"""Convenient workspace entrypoint for docx-reader tool."""
import os
import sys
import runpy

script_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".agents",
        "skills",
        "docx-reader",
        "scripts",
        "read_docx.py"
    )
)

if not os.path.exists(script_path):
    # Fallback to local .agents if script is run from project root
    script_path = os.path.abspath(
        os.path.join(os.getcwd(), ".agents", "skills", "docx-reader", "scripts", "read_docx.py")
    )

if not os.path.exists(script_path):
    sys.stderr.write(f"Error: Could not locate docx reader script at {script_path}\n")
    sys.exit(1)

runpy.run_path(script_path, run_name="__main__")
