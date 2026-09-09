"""
Genera dataset de ejemplo realista para probar la app de análisis de instrumentos.
Tema: Medicina tradicional, complementaria e integrativa como recurso de apoyo en psicología.
Poblaciones: estudiantes, docentes, actores locales.
"""
import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

n = 85  # respondentes simulados

# ID del respondente
ids = [f"P{i:03d}" for i in range(1, n+1)]
roles = np.random.choice(
    ["Estudiante", "Docente", "Actor local"],
    size=n,
    p=[0.55, 0.25, 0.20]
)
generos = np.random.choice(
    ["Femenino", "Masculino", "Prefiero no decir"],
    size=n,
    p=[0.60, 0.35, 0.05]
)
edades = np.random.randint(18, 65, size=n)
areas = np.random.choice(
    ["Psicología", "Medicina", "Enfermería", "Salud comunitaria", "Otro"],
    size=n,
    p=[0.30, 0.20, 0.15, 0.20, 0.15]
)

datos = {
    "ID_respondente": ids,
    "rol": roles,
    "genero": generos,
    "edad": edades,
    "area_formacion": areas,
}

# --- Instrumento 1: Conocimiento y percepción sobre MTCI ---
titulos_mtci = [
    "Botánica medicinal", "Acupuntura", "Homeopatía",
    "Medicina tradicional mexicana (MTM)", "Terapias corporales",
    "Mindfulness", "Yoga", "Reiki", "Aromaterapia", "Bach"
]

datos["conocimiento_general_mtci"] = np.random.randint(1, 6, size=n)  # Likert 1-5
datos["utilidad_percepcion_mtci"] = np.random.randint(1, 6, size=n)  # Likert 1-5

# ¿Ha escuchado sobre estas prácticas? (lista de reconocimiento, dicotómica)
for practica in titulos_mtci:
    key = f"conoce_{practica.replace(' ', '_').replace('-', '_')}"
    prob = random.uniform(0.3, 0.95)
    datos[key] = np.random.choice(["Sí", "No"], size=n, p=[prob, 1-prob])

# Nivel de acuerdo con afirmaciones (Likert 1-5)
afirmaciones = [
    "La MTCI es un recurso válido para apoyo psicológico",
    "La MTCI puede complementar tratamientos convencionales",
    "Es importante incluir la MTCI en la formación profesional",
    "La MTCI tiene evidencia científica suficiente",
    "Los usuarios de MTCI reportan mejor bienestar",
]

for i, afirm in enumerate(afirmaciones):
    key = f"acuerdo_{i+1}" + "_" + afirm[:30].replace(" ", "_").replace(",", "")
    datos[key] = np.random.randint(1, 6, size=n)

# Prácticas que ha utilizado personalmente (dicotómica)
datos["ha_utilizado_alguna_mtci"] = np.random.choice(["Sí", "No"], size=n, p=[0.65, 0.35])
datos["practicas_utilizadas_multiple"] = np.random.choice(
    ["Ninguna", "1-2 prácticas", "3-5 prácticas", "Más de 5"],
    size=n,
    p=[0.20, 0.40, 0.30, 0.10]
)

# Pregunta abierta: "¿Qué práctica de MTCI le gustaría conocer más?"
datos["practica_interes_abierta"] = np.random.choice([
    "Acupuntura", "Yoga", "Botánica medicinal",
    "Mindfulness", "Homeopatía", "Meditación",
    "Terapias corporales", "Aromaterapia", None, None, None
], size=n)

# --- Instrumento 2: Barreras y facilitadores ---
datos["barrera_falta_info"] = np.random.randint(1, 6, size=n)  # Likert 1-5 (1=nada importante, 5=muy importante)
datos["barrera_falta_formacion"] = np.random.randint(1, 6, size=n)
datos["barrera_prejuicio"] = np.random.randint(1, 6, size=n)
datos["barrera_costo"] = np.random.randint(1, 6, size=n)
datos["facilitador_interes_personal"] = np.random.randint(1, 6, size=n)
datos["facilitador_recomendacion"] = np.random.randint(1, 6, size=n)

# ¿Conoce centros de MTCI en su localidad? (dicotómica)
datos["conoce_centro_mtci_localidad"] = np.random.choice(["Sí", "No", "No sé"], size=n, p=[0.30, 0.55, 0.15])

# --- Instrumento 3: Actitud e intención de uso ---
datos["actitud_positiva_mtci"] = np.random.randint(1, 6, size=n)
datos["intencion_uso_mtci"] = np.random.randint(1, 6, size=n)
datos["recomendaria_mtci"] = np.random.choice(["Sí", "No", "Depende"], size=n, p=[0.50, 0.20, 0.30])
datos["confianza_mtci"] = np.random.randint(1, 6, size=n)

# Pregunta abierta: sugerencias
datos["sugerencias_mtci"] = np.random.choice([
    "Me gustaría más información sobre técnicas de mindfulness",
    "La acupuntura debería estar más disponible en instituciones de salud",
    "Es importante que los psicólogos conozcan sobre MTCI",
    "Me gustaría practicar yoga regularmente",
    None, None, None, None
], size=n)

# --- Convertir a dataframe y agregar faltantes intencionales ---
df = pd.DataFrame(datos)

# Agregar faltantes intencionales para probar limpieza
for col in df.columns:
    if df[col].dtype in ["int64", "float64", "Int64"]:
        idxs = np.random.choice(n, size=int(n * 0.08), replace=False)
        for i in idxs:
            df.at[i, col] = np.random.choice([99, 888, -9999])
    elif df[col].dtype == "object":
        idxs = np.random.choice(n, size=int(n * 0.05), replace=False)
        for i in idxs:
            df.at[i, col] = "NR"

df.to_csv("datos_ejemplo.csv", index=False, encoding="utf-8")
print(f"✅ Dataset de ejemplo generado: {df.shape[0]} filas × {df.shape[1]} columnas")
print(f"Archivo: C:/Users/angel/tesis_app/datos_ejemplo.csv")
print(f"\nVariables por tipo:")
print(f"  - Nominales: rol, genero, area_formacion, ha_utilizado_alguna_mtci, etc.")
print(f"  - Ordinales/Likert (1-5): conocimiento_general, utilidad_percepcion, acuerdos, barreras, etc.")
print(f"  - Dicotómicas/lista reconocimiento: conoce_*, recomendaria_mtci, etc.")
print(f"  - Numérica: edad")
print(f"  - Abiertas: practica_interes_abierta, sugerencias_mtci")
print(f"  - Lista de reconocimiento: conoce_<practica> (10 prácticas)")
