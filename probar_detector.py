"""
Prueba rápida del detector de tipos con los datos de ejemplo.
"""
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, "C:/Users/angel/tesis_app")

# Leer datos
df = pd.read_csv("C:/Users/angel/tesis_app/datos_ejemplo.csv")
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
print(f"\nTipos de datos por columna:")
print(df.dtypes)
print(f"\nPrimeros 3 valores de cada columna:")
for col in df.columns:
    print(f"  {col}: {df[col].head(3).tolist()}")

# Importar función de detección desde app.py
from app import detectar_tipo_variable

print(f"\n\n=== Resultado de detección de tipos ===")
for col in df.columns:
    info = detectar_tipo_variable(df[col], col)
    print(f"  {col}: {info['etiqueta']} (tipo={info['tipo']}, únicos={info['n_valores_unicos']}, faltantes={info['n_faltantes']})")

print(f"\n\n=== Resumen por tipo ===")
tipos = {}
for col in df.columns:
    info = detectar_tipo_variable(df[col], col)
    t = info['tipo']
    tipos[t] = tipos.get(t, 0) + 1

for t, count in sorted(tipos.items()):
    print(f"  {t}: {count} variables")
