"""
Análisis profundo del CSV real de respuestas MTCI.
Extrae: todos los headers, tipos de pandas, valores únicos, patrones, conteos.
"""
import os
import pandas as pd
import numpy as np
import re
from collections import Counter

ruta = os.path.join(os.path.dirname(__file__), "datos_mtci_anonimizado.csv")

df = pd.read_csv(ruta, dtype=str, keep_default_na=False, na_values=[''])
print(f"Filas (respondentes): {df.shape[0]}")
print(f"Columnas (variables): {df.shape[1]}")
print(f"\n{'='*80}")
print("LISTA COMPLETA DE VARIABLES (headers)")
print(f"{'='*80}")

for i, col in enumerate(df.columns):
    n_unique = df[col].nunique()
    n_blank = (df[col].str.strip() == '').sum()
    n_na = df[col].isna().sum()
    n_faltantes = n_blank + n_na
    pct_faltantes = round(n_faltantes / len(df) * 100, 1)

    print(f"\n[{i+1}] {col}")
    print(f"    Valores únicos: {n_unique} | Faltantes: {n_faltantes} ({pct_faltantes}%)")

    # Valores más comunes (top 5)
    top = df[col].value_counts().head(5)
    if len(top) > 0:
        print(f"    Top 5 respuestas:")
        for val, cnt in top.items():
            pct = round(cnt / len(df) * 100, 1)
            # Truncar valor largo para visualización
            val_display = str(val)[:80] + "..." if len(str(val)) > 80 else str(val)
            print(f"      [{cnt} ({pct}%)] {val_display}")

print(f"\n{'='*80}")
print("ANÁLISIS DE PATRONES POR TIPO DE VARIABLE")
print(f"{'='*80}")

# Patrones a detectar:
# 1. Variables de consentimiento (Sí/No acepto)
# 2. Variables de año de carrera (ordinal: 1ro, 2do, 3ro, 4to, 5to)
# 3. Variables de edad (ordinal: rangos)
# 4. Variables de sexo (nominal)
# 5. Variables de opción múltiple con letras (a, b, c, d, e) → nominal/ordinal
# 6. Variables de reconocimiento (varias prácticas en una celda, separadas por comas)
# 7. Preguntas abiertas (texto libre largo)
# 8. Likert (escala 1-5, 1-7, etc.)

def detectar_patron(col_name, series):
    """Detecta el patrón de respuesta de una variable."""
    nombre = col_name.lower()

    # Consentimiento
    if "acepto" in nombre or "acept" in nombre or "participar" in nombre or "información anterior" in nombre:
        return "consentimiento (dicotómica)"

    # Año de carrera
    if "año" in nombre and "carrera" in nombre:
        return "ordinal (año de carrera)"

    # Edad
    if nombre == "edad" or "edad" in nombre:
        valores = set(str(v) for v in series.unique())
        if any("-" in str(v) for v in series.unique()):
            return "ordinal (rango de edad)"
        return "numérica (edad)"

    # Sexo
    if nombre == "sexo" or "sexo" in nombre or "género" in nombre or "genero" in nombre:
        return "nominal (sexo/genero)"

    # Email / timestamp → no analíticas
    if "correo" in nombre or "email" in nombre or "marca temporal" in nombre or "timestamp" in nombre:
        return "no analítica (identificador/fecha)"

    # Detectar si es opción múltiple con letras (a, b, c, d, e)
    valores = [str(v).strip() for v in series.unique() if str(v).strip() != '']
    if len(valores) > 0:
        primeros_chars = set(v[0].lower() for v in valores if len(v) > 0)
        if primeros_chars.issubset({'a', 'b', 'c', 'd', 'e', 'f', 'g'}):
            # Es probablemente opción múltiple con letras
            # Verificar si hay texto después de la letra
            tiene_texto = any(len(v) > 1 and v[1] == ')' for v in valores)
            if tiene_texto:
                return "opción múltiple con letras (a-e) — nominal"
            else:
                return "opción con letras (a-e) — verificar"

    # Detectar listas de prácticas (varias prácticas separadas por comas)
    for v in valores:
        if ',' in v and len(v) > 50:
            return "lista de prácticas (múltiple) — parsear"

    # Detectar texto libre (abierta)
    longitud_promedio = series.astype(str).str.len().mean()
    if longitud_promedio > 40:
        return "abierta (texto libre)"

    # Si no detectamos nada específico
    return "por determinar"

print("\n=== Clasificación automática por patrón ===\n")
for col in df.columns:
    patron = detectar_patron(col, df[col])
    print(f"  {col[:90]}")
    print(f"    -> {patron}")
    print()

print(f"\n{'='*80}")
print("LISTA DE PRÁCTICAS MTCI (variables de selección múltiple)")
print(f"{'='*80}")

# Identificar columnas que son listas de prácticas
for col in df.columns:
    valores = df[col].dropna().unique()
    for v in valores:
        if ',' in str(v) and len(str(v)) > 50:
            print(f"\n[{col[:80]}]")
            # Extraer prácticas individuales
            practicas = [p.strip() for p in str(v).split(',')]
            for i, p in enumerate(practicas, 1):
                print(f"  {i}. {p}")
            break  # Solo mostrar el primer valor con lista

print(f"\n{'='*80}")
print("RESUMEN EJECUTIVO")
print(f"{'='*80}")
print(f"Total de respuestas: {len(df)}")
print(f"Total de variables: {len(df.columns)}")
print(f"\nVariables por categoría (estimado):")

categorias = {
    "no analíticas (fecha/email/consentimiento)": 0,
    "nominales (sexo, opciones múltiples con letras)": 0,
    "ordinales (año, edad, escalas)": 0,
    "listas de prácticas MTCI (múltiple)": 0,
    "abiertas (texto libre)": 0,
    "por determinar": 0,
}

for col in df.columns:
    patron = detectar_patron(col, df[col])
    if "no analítica" in patron:
        categorias["no analíticas (fecha/email/consentimiento)"] += 1
    elif "nominal" in patron:
        categorias["nominales (sexo, opciones múltiples con letras)"] += 1
    elif "ordinal" in patron:
        categorias["ordinales (año, edad, escalas)"] += 1
    elif "lista" in patron:
        categorias["listas de prácticas MTCI (múltiple)"] += 1
    elif "abierta" in patron:
        categorias["abiertas (texto libre)"] += 1
    else:
        categorias["por determinar"] += 1

for cat, count in categorias.items():
    print(f"  {cat}: {count}")
