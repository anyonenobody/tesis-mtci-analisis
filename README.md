# tesis-mtci-analisis

Análisis de cuestionario MTCI — Medicina Tradicional, Complementaria e Integrativa en psicología

App interactiva de Streamlit para el análisis de datos del cuestionario I1 sobre saberes, prácticas y valoración de la Medicina Tradicional, Complementaria e Integrativa (MTCI) como recurso de apoyo en la psicología.

## Archivos

- `app_mtci.py` — App de Streamlit principal (adaptada al CSV real de 68 respondentes)
- `datos_mtci_anonimizado.csv` — Datos del cuestionario I1 (anonimizados, sin correos ni datos identificativos)
- `analyzar_csv_real.py` — Script de análisis profundo del CSV
- `probar_detector.py` — Prueba del detector de tipos de variable
- `generar_ejemplo.py` — Generador de datos de ejemplo para pruebas
- `datos_ejemplo.csv` — Dataset de ejemplo (85 respondentes simulados)
- `app.py` — Versión inicial de la app

## Para ejecutar

```bash
streamlit run app_mtci.py
```

Requiere:
- streamlit
- pandas
- numpy
- plotly
- scipy
- openpyxl
