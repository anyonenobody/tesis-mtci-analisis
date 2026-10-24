# Changelog

Todas las modificaciones notables realizadas en este repositorio se documentan en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased] - 2026-10-22

### Added
- **Presentación Oficial de Defensa de Tesis (`Presentacion_Defensa_Tesis_MTCI_UNAN.pptx`)**: Deck de 17 láminas panorámicas 16:9 alineado a los estándares de la skill `pptx` de Anthropic y diseño editorial contemporáneo sin cajas rectangulares, empleando tipografía de alto contraste (Georgia + Calibri), estructura de contraste oscuro/claro, transiciones nativas de fundido suave OpenXML (`<p:fade/>`), e inserción de gráficos empíricos reales a 300 DPI para las tres poblaciones del estudio (Estudiantes: Figuras 4 y 7; Facilitadores Locales: Figuras 12 y 14; Claustro Docente: Figuras 24 y 25; Propuesta: Portada Manual Anexo 16.2).
- **Presentación Web Interactiva Animada (`presentacion_tesis_mtci_animated.html`)**: Versión interactiva para navegador con animaciones cinéticas de contadores porcentuales (`data-target`), modo orador (`N`), cuadrícula de miniaturas (`T`) y navegación por teclado (flechas / barra espaciadora), con idéntica rigurosidad documental y gráfica que el archivo PowerPoint.

### Changed
- **Depuración Epistemológica y Académica de Títulos**: Erradicación total de frases y subtítulos de corte sensacionalista o dramático (e.g., *"Encrucijada Asistencial"*, *"Paradoja Formativa"*), reemplazándolos por encabezados estrictamente normalizados según la estructura capitular de la tesis de grado (Capítulo I: Introducción, Capítulo II: Marco Teórico, Capítulo III: Marco Metodológico, Capítulo IV: Resultados, Capítulo V: Propuesta, Capítulo VI: Conclusiones y Recomendaciones).
- **Verificación Empírica Integral contra el Documento Maestro**: Alineación del 100% de métricas, citas y hallazgos con `docs/capitulos/04_analisis_y_discusion_resultados.md` y `assets/MTCI_Consolidado_Final_APA7.docx` ($N = 86$: $n = 68$ estudiantes, $n = 9$ facilitadores, $n = 9$ docentes).
- **Instalación de Skills de Presentación y Video**: Incorporación de `pptx` de Anthropic, junto con la suite de `hyperframes` y `remotion` en `.agents/skills/`.
- **Base de Datos Bibliográfica SQLite (`data/bibliografia_mtci.db`)**: Base de datos relacional persistente con 56 referencias completamente tipadas (artículos, libros, informes, leyes, sitios web), metadatos normalizados (autores, año, títulos, volúmenes, páginas, DOIs y URLs) y llaves de citación.
- **Exportación CSL-JSON (`data/bibliografia_mtci.csl.json`)**: Interoperabilidad con gestores bibliográficos (Zotero, Mendeley, PRISMA).
- **Herramienta CLI `tools/bib_cli.py`**: Interfaz de terminal para estadísticas (`stats`), listado categorizado (`list`), búsqueda semántica (`search`) y auditoría HTTP en vivo (`verify`).
- **Script de Consolidación Editorial `tools/consolidate_native_citations_and_bibliography.py`**: Pipeline reproducible para la inyección de fuentes OpenXML, SDTs de citas interactivas y bibliografía dinámica con sangría francesa APA 7.
- **Motor Nativo de Citas en Word (`<b:Sources>`)**: Inyección del esquema XML `http://schemas.openxmlformats.org/officeDocument/2006/bibliography` en `customXml/item1.xml` con las 56 fuentes maestras reconocidas nativamente por Microsoft Word 2016–365.
- **Citas Interactivas Nativas (`<w:sdt><w:citation/>`)**: Integración de campos `{ CITATION Tag \\l 3082 }` en las citas del texto, activando los menús interactivos de Word ("Editar cita", "Editar fuente", "Convertir en texto estático").
- **Bloque Dinámico de Bibliografía (`<w:sdt><w:bibliography/>`)**: Contenedor nativo `{ BIBLIOGRAPHY \\l 3082 }` bajo la sección `15. Referencias` que renderiza las 56 referencias en formato APA 7 con sangría francesa de 1.27 cm y se actualiza dinámicamente con F9.

### Changed
- Sincronización al 100% de `docs/capitulos/07_referencias_bibliograficas.md` y `docs/referencias_bibliograficas.md` con el catálogo canónico de 56 referencias.
- Normalización estricta de normas APA 7 en español: sustitución de ampersands `&` por "y", erradicación de clichés "y otros" por `et al.` canónico, y títulos en estilo oración (*sentence case*).
- Integración de cita curricular a `(Campusano y Valderrama, 2026)` en el marco de educación superior y de `(UNAN-Managua, 2021)` en líneas de investigación institucional, alcanzando 100% de concordancia entre citas in-text y lista bibliográfica.
- Alineación canónica de 56 tags alfanuméricos ASCII entre `customXml/item1.xml`, la base SQLite y los 101 campos dinámicos `{ CITATION Tag \l 3082 }` en párrafos y celdas de tabla.

### Fixed
- Corrección de 11 DOIs y URLs desactualizados o con error 404 (Guo 2024, Furlan 2012, Papalini 2022, Rák 2025, Salinas-Oñate 2022, Sotiropoulos 2025, Thomson 2023, Babic 2024, UNESCO 2013, OPS/OMS 2025) mediante verificación directa contra Crossref, PubMed y PMC (código HTTP 200).
- Subsanación de errata histórica de año en Engel: corrección de `(1997)` a `(1977)` (*Science*, 196(4286), 129–136).
- Eliminación de referencia duplicada a OMS (2022) en la sección final de Word.
- Corrección tipográfica en citas de autores: `Sáchez` -> `Sánchez-Lozano`, `Ruíz` -> `Ruiz`, y unificación de `Cadena et al.` a `Ortega-Cadena et al.`.
- **Subsanación de Menú Contextual Incompleto ("Editar fuente" ausente)**: Resuelto el fallo donde citas como `Chafloque-Capuñay et al., 2025`, `Hernández-Sampieri y Mendoza, 2023` o `Sánchez-Lozano y Martínez-Pizarro, 2025` ocultaban "Editar fuente" debido a discrepancias ortográficas o guiones tipográficos entre el código de campo y el `<b:Tag>`.
- **Cobertura 100% de Checkmarks (`✓`) en Administrador de Fuentes**: Resuelto el problema de 42 fuentes sin marcar en la "Lista actual" de Word mediante la conversión de todas las menciones estáticas institucionales (OMS 2022, 2023, 2025, MINSA, OPS, SETEC, Duarte, GRUN) y de tablas de evidencia (Furlan, Guo, Sotiropoulos, Yerzhan, Rivera, Rodrigues) en campos SDT nativos. Ahora las 56 fuentes tienen su `✓` verificado por Word COM.
- **Enriquecimiento Integral de Metadatos en "Editar fuente" de Word**: Resuelta la carencia de datos en el formulario de edición de fuentes reportada en la evidencia visual (`Ley774_2012`). Se poblaron todos los campos esenciales y recomendados en el esquema `<b:Sources>`:
  - Casilla `* DOI`: Mapeada explícitamente a `<b:DOI>` y `<b:StandardNumber>` con la cadena limpia de DOI para los 24 artículos de revista científica.
  - Casilla `URL`: Cobertura del 100% (56/56) con enlaces HTTPS legítimos y verificados (repositorio oficial `legislacion.asamblea.gob.ni` para leyes y decretos de Nicaragua, repositorios institucionales de UNAN-Managua, MINSA, OMS, OPS y editoriales reconocidas), sin inventar enlaces ni generar alucinaciones.
  - Metadatos de publicación: Desglose completo de día, mes, año, ciudad (`<b:City>`), país (`<b:CountryRegion>`), entidad editora (`<b:Publisher>`), nombre de la revista (`<b:JournalName>`), volumen, número, páginas, edición y publicación oficial (`<b:PublicationTitle>` para La Gaceta, Diario Oficial).
  - Verificación automatizada vía Word COM confirmando 56/56 con título, año, editorial/revista y URL; 24/24 artículos con DOI reconocido en GUI; y 56/56 fuentes con marca de citación (`s.Cited == True`).


## [0.1.0] - 2026-10-21
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
