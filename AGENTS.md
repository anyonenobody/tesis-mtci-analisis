# 🌿 AGENTS.md — Tesis MTCI: Análisis y Directrices del Agente

Este archivo establece las directrices operativas, metodológicas, analíticas y de gobernanza de datos que cualquier agente de IA o colaborador debe seguir estrictamente al interactuar con este repositorio.

---

## 📌 1. Información General y Metadatos del Proyecto

* **Título de la Investigación:**  
  *Integración de la Medicina Tradicional, Complementaria e Integrativa (MTCI) en la Formación y Práctica Psicológica: Estudio Mixto con Estudiantes y Docentes*
* **Institución Académica:** Universidad Nacional Autónoma de Nicaragua, Managua (UNAN-Managua), Centro Universitario Regional Estelí (CUR-Estelí).
* **Marco Metodológico:** Enfoque cuantitativo y descriptivo-transversal con análisis comparativo, correlacional y multivariado sobre percepción, conocimientos, actitudes y barreras institucionales respecto a las MTCI.
* **Normativa de Publicación y Redacción:** Normas **APA 7.ª edición** estricta, redacción académica formal desprovista de clichés de IA (gobernada por la skill `academic-humanizer`) y formateo institucional en Microsoft Word (`test_documento_tesis.docx`).

---

## 🏗️ 2. Arquitectura del Repositorio

```text
tesis-mtci-analisis/
├── AGENTS.md                   # Directrices operativas, contexto de dominio y directivas del agente
├── CHANGELOG.md                # Registro de cambios cronológico y semántico (Keep a Changelog)
├── pyproject.toml / uv.lock    # Gestión determinista de dependencias con uv (pandas, matplotlib, rapidfuzz, python-docx, etc.)
│
├── datos_mtci_anonimizado.csv  # Base de datos empírica anonimizada de encuestas a estudiantes y docentes
├── datos_ejemplo.csv           # Subconjunto de pruebas para validación rápida
│
├── .agents/skills/             # Habilidades operativas del agente
│   ├── meta-learning-agent/    # Auto-aprendizaje, diagnóstico de fallos y bitácora técnica
│   ├── academic-humanizer/     # Calibración de estilo, burstiness y evasión de detectores IA
│   ├── docx-reader/            # Lector e inspector de alta fidelidad de archivos Word (.docx)
│   ├── pandas-data-analysis/   # Análisis EDA y visualizaciones estadísticas
│   ├── pandas-pro/             # Manipulación avanzada de DataFrames y transformaciones vectorizadas
│   ├── prisma-iterative-search/# Motor de búsqueda bibliográfica iterativa multi-API
│   ├── scoping-review-orchestrator/ # Metodología y auditoría de revisiones JBI / PRISMA
│   ├── python-patterns/        # Patrones limpios y tipado en Python
│   └── python-testing-patterns/# Pruebas automatizadas con pytest
│
├── tools/                      # Herramientas de terminal (CLI) multi-proyecto
│   ├── read_docx.py            # Inspector estructural y extractor de estilos Word
│   ├── export_supplementary_docx.py # Generador de anexos formateados en Word APA 7
│   ├── verify_evidence_links.py# Verificador de enlaces DOI y referencias en Crossref
│   ├── harvest_search.py       # Cosechador de literatura multi-API (PubMed, Europe PMC, OpenAlex)
│   ├── asset_builder.py        # Generador de tablas Markdown y figuras analíticas
│   ├── coherence_audit.py      # Verificador de coherencia metodológica y balances empíricos
│   ├── db_cli.py               # Inspección de base de datos bibliográfica SQLite
│   └── export_snapshot.py      # Versionador de snapshots JSON y matrices CSV
│
├── assets/                     # Figuras vectoriales y gráficos estadísticos (Figuras 1 a 5)
│
├── docs/                       # Documentación analítica y manuscrito de tesis
│   ├── analisis_y_discusion_estudiantes.md # Análisis empírico detallado del componente estudiantil
│   ├── memoria_cambios_introduccion.md    # Memoria de ajustes epistemológicos en la introducción
│   ├── referencias_bibliograficas.md      # Corpus de referencias normalizadas en APA 7
│   ├── lecciones_aprendidas.md            # Diagnósticos de fallas técnicas y reglas preventivas
│   └── assets/                            # Insumos compilados (Material Suplementario Completo .docx)
│
└── app_mtci.py / app.py        # Aplicaciones interactivas para exploración y tabulación de datos
```

---

## 🎯 3. Principios Analíticos y Metodológicos Invariables

1. **Cero Métricas Alucinadas:** Toda cifra reportada en los análisis, discusiones o documentos debe provenir de cálculos reproducibles sobre `datos_mtci_anonimizado.csv` o sobre el corpus de literatura verificado.
2. **Coherencia Estadística:** Al citar porcentajes, promedios o correlaciones (e.g. correlación de Pearson o Spearman, diferencias por año académico o género), los valores deben verificarse mediante scripts en Python antes de incorporarse al texto.
3. **Perspectiva Intercultural y Ética:** Abordar las prácticas de medicina tradicional y complementaria reconociendo el marco jurídico nicaragüense (Ley No. 759 y Ley No. 774) y la pertinencia comunitaria, delimitando el rol profesional del psicólogo.
4. **Auto-Corrección y Registro:** Cuando surja un fallo técnico o una observación metodológica, consultar y actualizar `docs/lecciones_aprendidas.md` y `CHANGELOG.md` siguiendo el protocolo de la skill `meta-learning-agent`.
