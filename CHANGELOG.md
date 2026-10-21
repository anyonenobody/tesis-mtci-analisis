# Changelog

Todas las modificaciones notables realizadas en este repositorio se documentan en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased] - 2026-10-21

### Added
- **Skill `meta-learning-agent`**: Sistema procedural de auto-aprendizaje, análisis de causa raíz (RCA), resguardo de lecciones aprendidas y registro de bitácora.
- **Suite de Skills Científicas**: Clonadas e integradas desde `prisma-scr` a `.agents/skills/` y sincronizadas en la configuración global de Antigravity:
  - `pandas-data-analysis`
  - `pandas-pro`
  - `prisma-iterative-search`
  - `python-executor`
  - `python-patterns`
  - `python-testing-patterns`
  - `scoping-review-orchestrator`
- **Herramientas metodológicas en `tools/`**:
  - `asset_builder.py`: Generador de activos empíricos y tablas metodológicas.
  - `coherence_audit.py`: Auditor bidireccional de coherencia de flujo PRISMA.
  - `db_cli.py`: Inspección de base de datos SQLite y resúmenes de cribado.
  - `export_snapshot.py`: Versionador de snapshots JSON y matrices CSV.
  - `export_supplementary_docx.py`: Exportador editorial de material suplementario en Word (.docx) bajo normas APA 7.
  - `harvest_search.py`: Motor de búsqueda y cosecha bibliográfica multi-API.
  - `run_screening_and_charting.py`: Protocolo de cribado y vaciado documental.
  - `verify_evidence_links.py`: Auditor y verificador de DOIs, enlaces HTTP y referencias bibliográficas en Crossref.
- **Documento de memoria técnica**: `docs/lecciones_aprendidas.md` para el registro sistemático de diagnósticos, soluciones y reglas preventivas.
- **Dependencia de similitud difusa**: Incorporación de `rapidfuzz` (v3.14.6) en `pyproject.toml` y `uv.lock`.

### Changed
- Configuración de resolución dinámica con fallback multi-proyecto en todas las herramientas de `tools/` para permitir su ejecución tanto dentro de `prisma-scr` como en `tesis-mtci-analisis` y otros proyectos.
- Normalización del identificador en YAML frontmatter de `pandas-data-analysis` para compatibilidad estricta con el agente.

### Fixed
- Resolución de fallo `ModuleNotFoundError: No module named 'rapidfuzz'` en los scripts de verificación documental.
- Prevención de desalineaciones en variables de entorno y codificación de salida UTF-8 en PowerShell.
