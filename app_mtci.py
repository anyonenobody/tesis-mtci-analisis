"""
🌿 App de Análisis del Cuestionario MTCI
Adaptada específicamente a tu CSV real:
I1-Cuestionario sobre Saberes, prácticas y valoración de la MTCI (68 respondentes, 21 variables)

Corre con: streamlit run app_mtci.py
"""
import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(
    page_title="Análisis MTCI - Tesis",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Carga automática del CSV si existe
# -----------------------------------------------------------------------------

CSV_AUTOMATICO = "datos_mtci_anonimizado.csv"

if "df" not in st.session_state:
    st.session_state.df = None
if "df_practicas" not in st.session_state:
    st.session_state.df_practicas = None
if "var_types" not in st.session_state:
    st.session_state.var_types = {}
if "df_expanded" not in st.session_state:
    st.session_state.df_expanded = None

# Intentar cargar automáticamente
try:
    df_auto = pd.read_csv(CSV_AUTOMATICO, dtype=str, keep_default_na=False, na_values=[''])
    st.session_state.df = df_auto.copy()
    st.session_state.df_original_name = CSV_AUTOMATICO

    # Detectar tipos automáticamente
    tipos = {}
    for col in df_auto.columns:
        tipos[col] = detectar_tipo_columna(df_auto[col], col)
    st.session_state.var_types = tipos

    st.toast(f"✅ CSV precargado: {CSV_AUTOMATICO} ({df_auto.shape[0]} respondentes)")
except Exception:
    pass  # No está disponible, el usuario subirá manualmente


# -----------------------------------------------------------------------------
# Detección de tipos específica para tu CSV
# -----------------------------------------------------------------------------

def detectar_tipo_columna(series, nombre):
    """Detecta el tipo específico de cada columna de tu CSV."""
    col = series.dropna()
    n_unique = col.nunique()
    n_total = len(series)
    n_faltantes = int(series.isna().sum()) + (series.astype(str).str.strip() == '').sum()

    info = {
        "nombre": nombre,
        "tipo": "por_determinar",
        "etiqueta": "",
        "n_uniques": n_unique,
        "n_faltantes": n_faltantes,
        "pct_faltantes": round(n_faltantes / len(series) * 100, 1),
        "values": sorted([str(v) for v in col.unique()]) if n_unique <= 50 else [],
    }

    nombre_lower = nombre.lower().strip()

    # 1. Identificadores / no analíticos
    if "marca temporal" in nombre_lower or "timestamp" in nombre_lower:
        info["tipo"] = "no_analitico"
        info["etiqueta"] = "Fecha (no analítico)"
        return info
    if "correo" in nombre_lower or "email" in nombre_lower or "dirección" in nombre_lower:
        info["tipo"] = "no_analitico"
        info["etiqueta"] = "Email (identificador)"
        return info
    if "id" in nombre_lower or "sujeto" in nombre_lower or "participante" in nombre_lower:
        info["tipo"] = "no_analitico"
        info["etiqueta"] = "ID (identificador)"
        return info

    # 2. Consentimiento
    if "acepto" in nombre_lower or "participar" in nombre_lower or "información" in nombre_lower:
        info["tipo"] = "consentimiento"
        info["etiqueta"] = "Consentimiento informado"
        return info

    # 3. Año de carrera (ordinal)
    if "año" in nombre_lower:
        info["tipo"] = "ordinal"
        info["etiqueta"] = "Año de carrera (ordinal)"
        return info

    # 4. Edad (ordinal por rangos)
    if "edad" == nombre_lower or "edad" in nombre_lower:
        info["tipo"] = "ordinal"
        info["etiqueta"] = "Edad en rangos (ordinal)"
        return info

    # 5. Sexo (nominal)
    if "sexo" == nombre_lower or "sexo" in nombre_lower:
        info["tipo"] = "nominal"
        info["etiqueta"] = "Sexo (nominal)"
        return info

    # 6. Detectar si es opción con letra (a,b,c,d,e) o texto libre con letra
    if n_unique <= 10:
        valores_str = [str(v).strip() for v in col.unique()]
        primeros_caracteres = [v[0].lower() for v in valores_str if len(v) > 0]
        if set(primeros_caracteres).issubset({'a', 'b', 'c', 'd', 'e', 'f'}):
            info["tipo"] = "opcion_letra"
            info["etiqueta"] = "Opción con letra (a-e) — nominal"
            # Si el texto después de la letra es largo, es una opción larga
            if any(len(v) > 20 for v in valores_str):
                info["etiqueta"] = "Opción múltiple con texto (a-e) — nominal"
            return info

    # 7. Detectar frecuencias ordinales (Nunca, Rara vez, etc.)
    if n_unique <= 6:
        valores_lower = set(str(v).strip().lower() for v in col.unique())
        palabras_frecuencia = {"nunca", "rara vez", "ocasionalmente", "a veces", "muchas veces",
                               "frecuentemente", "siempre", "casi siempre", "casi nunca", "poco",
                               "diariamente", "semanal", "mensual", "anual"}
        if valores_lower & palabras_frecuencia:
            info["tipo"] = "ordinal_frecuencia"
            info["etiqueta"] = "Frecuencia de uso (ordinal: Nunca → Siempre)"
            return info

    # 8. Detectar listas de prácticas MTCI (varias prácticas separadas por coma)
    #    Indicios: texto largo, contiene comas, menciona prácticas conocidas
    practicas_palabras = ["fitoterapia", "herbolaria", "ayurveda", "yoga", "meditación", "masajes",
                          "quiropraxia", "reflexología", "acupuntura", "aromaterapia", "terapia floral",
                          "arte terapia", "reiki", "sanación", "pránica", "constelaciones", "hipnosis",
                          "homeopatía", "limpias", "sopladas", "naturopatía", "hidroterapia", "hieloterapia",
                          "geoterapia", "barro", "digtopuntura", "digitopuntura", "shiatzu", "tui na"]
    for v in col.unique():
        str_v = str(v).strip()
        if len(str_v) > 40 and ',' in str_v:
            if any(p in str_v.lower() for p in practicas_palabras):
                info["tipo"] = "lista_practicas"
                info["etiqueta"] = "Lista de prácticas MTCI (múltiple) — parsear"
                return info

    # 9. Pregunta abierta (texto largo)
    if n_unique > 10 or (n_unique <= 30 and n_unique > 5):
        longitud_prom = series.astype(str).str.len().mean()
        if longitud_prom > 30:
            info["tipo"] = "abierta"
            info["etiqueta"] = "Pregunta abierta / comentario"
            return info

    # 10. Caer a nominal si tiene pocos valores únicos
    if n_unique <= 10:
        info["tipo"] = "nominal"
        info["etiqueta"] = "Categoría nominal"
        return info

    # 11. Fallback
    info["tipo"] = "por_determinar"
    info["etiqueta"] = "Por determinar"
    return info


# -----------------------------------------------------------------------------
# Parseo de listas de prácticas
# -----------------------------------------------------------------------------

def parsear_practicas(df, columnas):
    """Parsea las columnas de listas de prácticas en formato largo."""
    registros = []
    conteo_global = Counter()

    for col in columnas:
        for idx, row in df.iterrows():
            valor = str(row[col]).strip()
            if valor.lower() in ["ninguna", "nunca", ""] or valor == "NaN":
                registros.append({"Columna": col, "Practica": "Ninguna", "Respondente": idx})
                conteo_global["Ninguna"] += 1
            else:
                partes = [p.strip() for p in valor.split(",")]
                for parte in partes:
                    if parte:
                        registros.append({"Columna": col, "Practica": parte, "Respondente": idx})
                        conteo_global[parte] += 1

    df_exp = pd.DataFrame(registros)
    df_resumen = pd.DataFrame([
        {"Practica MTCI": k, "Menciones": v, "% de respondentes": round(v / len(df) * 100, 1)}
        for k, v in conteo_global.most_common()
    ])
    return df_exp, df_resumen


# -----------------------------------------------------------------------------
# Estadísticas por tipo
# -----------------------------------------------------------------------------

def stats_por_tipo(series, tipo):
    """Devuelve estadísticas según el tipo de variable."""
    resultado = {}
    col = series.dropna()
    n = len(series)
    n_faltantes = int(series.isna().sum()) + (series.astype(str).str.strip() == '').sum()
    n_respondieron = len(col)

    resultado["n_total"] = n
    resultado["n_respondidos"] = n_respondidos
    resultado["n_faltantes"] = n_faltantes

    if tipo == "no_analitico" or tipo == "consentimiento":
        resultado["conteo"] = series.value_counts().to_dict()

    elif tipo == "ordinal" or tipo == "ordinal_frecuencia":
        frec = col.value_counts().reset_index()
        frec.columns = ["Valor", "Frecuencia"]
        frec["Porcentaje"] = round(frec["Frecuencia"] / n_respondidos * 100, 1)

        # Orden lógico para rangos
        if tipo == "ordinal" and "edad" in series.name.lower():
            orden = ["18-20", "21-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", "56-60", "60+"]
            frec["_orden"] = frec["Valor"].apply(lambda x: next((i for i, o in enumerate(orden) if o in str(x)), 99))
            frec = frec.sort_values("_orden").drop(columns="_orden")
        elif tipo == "ordinal_frecuencia":
            orden_frec = ["nunca", "rara vez", "poco", "ocasionalmente", "a veces", "muchas veces",
                          "frecuentemente", "siempre", "casi siempre", "casi nunca", "diariamente",
                          "semanal", "mensual", "anual"]
            frec["_orden"] = frec["Valor"].str.lower().apply(
                lambda x: next((i for i, o in enumerate(orden_frec) if o in x), 99))
            frec = frec.sort_values("_orden").drop(columns="_orden")
        else:
            frec = frec.sort_values("Valor")

        resultado["frecuencias"] = frec

    elif tipo == "opcion_letra":
        frec = col.value_counts().reset_index()
        frec.columns = ["Opción", "Frecuencia"]
        frec["Porcentaje"] = round(frec["Frecuencia"] / n_respondidos * 100, 1)
        frec["_orden"] = frec["Opción"].str[0].apply(lambda x: ord(x.lower()) - ord('a') if x else 99)
        frec = frec.sort_values("_orden").drop(columns="_orden")
        resultado["frecuencias"] = frec

    elif tipo == "nominal":
        frec = col.value_counts().reset_index()
        frec.columns = ["Valor", "Frecuencia"]
        frec["Porcentaje"] = round(frec["Frecuencia"] / n_respondidos * 100, 1)
        frec = frec.sort_values("Frecuencia", ascending=False)
        resultado["frecuencias"] = frec

    elif tipo == "lista_practicas":
        resultado["nota"] = "Variable con lista de prácticas. Usa la pestaña '🌿 Prácticas MTCI'."

    elif tipo == "abierta":
        resultado["n_respuestas"] = n_respondidos
        resultado["longitud_prom"] = round(float(col.astype(str).str.len().mean()), 1)
        resultado["ejemplo"] = str(col.iloc[0]) if len(col) > 0 else "—"

    return resultado


# -----------------------------------------------------------------------------
# INICIO DE LA APP
# -----------------------------------------------------------------------------

st.title("🌿 Análisis del Cuestionario MTCI")
st.caption("Medicina Tradicional, Complementaria e Integrativa como recurso de apoyo en psicología")

with st.sidebar:
    st.header("📁 Datos")

    uploaded_file = st.file_uploader(
        "O sube tu propio archivo CSV/Excel",
        type=["csv", "xlsx"],
        help="Si el CSV automático no carga, sube tu archivo manualmente."
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, dtype=str, keep_default_na=False, na_values=[''])
            else:
                df = pd.read_excel(uploaded_file, dtype=str, keep_default_na=False, na_values=[''])

            st.session_state.df = df.copy()
            st.session_state.df_original_name = uploaded_file.name
            st.success(f"✅ Archivo: **{uploaded_file.name}**")
            st.info(f"{df.shape[0]} respondentes × {df.shape[1]} variables")

            # Detectar tipos automáticamente al cargar
            with st.spinner("Detectando tipos de variables..."):
                tipos = {}
                for col in df.columns:
                    tipos[col] = detectar_tipo_columna(df[col], col)
                st.session_state.var_types = tipos

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

    st.divider()

    if st.session_state.df is not None:
        st.header("⚙️ Configuración")

        if st.button("🔍 Detectar tipos de todas las variables", type="primary"):
            with st.spinner("Analizando las 21 variables..."):
                tipos = {}
                for col in st.session_state.df.columns:
                    tipos[col] = detectar_tipo_columna(st.session_state.df[col], col)
                st.session_state.var_types = tipos
                st.success("Tipos detectados.")

        st.divider()

        if st.session_state.var_types:
            st.header("🧩 Resumen de tipos")
            tipo_counts = {}
            for info in st.session_state.var_types.values():
                t = info["tipo"]
                tipo_counts[t] = tipo_counts.get(t, 0) + 1

            emoji_map = {
                "no_analitico": "📅", "consentimiento": "✅", "ordinal": "📊",
                "nominal": "🏷️", "opcion_letra": "🔤", "ordinal_frecuencia": "📈",
                "lista_practicas": "🌿", "abierta": "📝", "por_determinar": "❓"
            }

            for t, count in tipo_counts.items():
                emoji = emoji_map.get(t, "❓")
                st.write(f"{emoji} **{t}**: {count} variables")

            st.divider()

            st.header("🌿 Parsear prácticas MTCI")
            cols_practicas = [
                col for col, info in st.session_state.var_types.items()
                if info["tipo"] == "lista_practicas"
            ]
            if cols_practicas:
                st.info(f"Columnas a parsear: {len(cols_practicas)}")
                for c in cols_practicas:
                    st.write(f"- {c[:60]}")

                if st.button("🌿 Parsear y expandir prácticas MTCI"):
                    with st.spinner("Parseando listas de prácticas..."):
                        df_exp, resumen = parsear_practicas(st.session_state.df, cols_practicas)
                        st.session_state.df_expanded = df_exp
                        st.session_state.df_practicas = resumen
                        st.success(f"✅ Expandido: {len(df_exp)} registros de prácticas individuales")
            else:
                st.caption("No se detectaron columnas de listas de prácticas.")

        st.divider()
        st.caption("Versión 1.2 — Adaptada a tu I1 MTCI")


# =============================================================================
# CONTENIDO PRINCIPAL
# =============================================================================

st.header("📊 Análisis de resultados")

if st.session_state.df is None:
    st.info("👆 Sube tu archivo CSV desde el panel lateral o espera que el CSV automático cargue.")
    st.divider()
    st.subheader("📖 Guía rápida del cuestionario I1")
    st.write(f"""
    **Estructura del cuestionario (21 variables, 68 respondentes):**

    | # | Variable | Tipo detectado |
    |---|----------|----------------|
    | 1 | Marca temporal | 📅 Fecha (excluir análisis) |
    | 2 | Correo electrónico | 📅 Identificador (excluir) |
    | 3 | Consentimiento | ✅ Sí, acepto (100%) |
    | 4 | Año de carrera | 📊 Ordinal (4to / 5to) |
    | 5 | Edad | 📊 Ordinal (rangos 18-20 a 42+) |
    | 6 | Sexo | 🏷️ Nominal (F/M/Prefiero no decir) |
    | 7-17 | Preguntas de opción múltiple (con letras a-e) | 🔤 Nominal con opciones |
    | 11-13 | Frecuencia de uso MTCI | 📈 Ordinal (Nunca → Siempre) |
    | 18-20 | Listas de prácticas MTCI | 🌿 Múltiple (parsear) |
    | 21 | Comentarios / sugerencias | 📝 Abierta (34 sin respuesta) |

    **Lo que la app hace automáticamente:**
    - Detecta el tipo de cada variable al presionar "🔍 Detectar tipos"
    - Parsea las 3 columnas de prácticas MTCI cuando presionas "🌿 Parsear"
    - Calcula frecuencias, porcentajes y gráficos por variable
    - Permite descargar resultados para tu tesis
    """)
else:
    df_trabajar = st.session_state.df
    usar_limpio = st.checkbox("Usar datos sin modificar (si aplica)", value=True)

    pestañas = st.tabs([
        "📋 Resumen general",
        "📊 Estadística por variable",
        "🌿 Prácticas MTCI (parseadas)",
        "📈 Gráficos",
        "📤 Exportar para tesis",
    ])

    # -------------------------------------------------------------------------
    # Pestaña 1: Resumen general
    # -------------------------------------------------------------------------
    with pestañas[0]:
        st.subheader("Resumen general del cuestionario")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Respondentes", len(df_trabajar))
        with c2:
            st.metric("Variables totales", df_trabajar.shape[1])
        with c3:
            n_falt_total = sum(info["n_faltantes"] for info in st.session_state.var_types.values())
            st.metric("Celdas sin respuesta", n_falt_total)
        with c4:
            vars_analiticas = [info for info in st.session_state.var_types.values()
                              if info["tipo"] not in ["no_analitico", "consentimiento"]]
            st.metric("Variables analíticas", len(vars_analiticas))

        st.divider()

        st.subheader("Tabla de variables y tipos detectados")
        if st.session_state.var_types:
            filas = []
            for col, info in st.session_state.var_types.items():
                filas.append({
                    "Variable": col[:70],
                    "Tipo": info["etiqueta"],
                    "Tipo interno": info["tipo"],
                    "Valores únicos": info["n_uniques"],
                    "Faltantes": info["n_faltantes"],
                    "% sin respuesta": info["pct_faltantes"],
                })
            df_tipos = pd.DataFrame(filas)
            st.dataframe(df_tipos, use_container_width=True, hide_index=True)

            st.download_button(
                "⬇️ Descargar tabla de tipos (CSV)",
                data=df_tipos.to_csv(index=False).encode("utf-8"),
                file_name="tabla_tipos_variables.csv",
                mime="text/csv",
            )

        st.divider()

        st.subheader("📋 Variables excluidas del análisis")
        vars_excluidas = [
            (col, info) for col, info in st.session_state.var_types.items()
            if info["tipo"] in ["no_analitico", "consentimiento"]
        ]
        if vars_excluidas:
            for col, info in vars_excluidas:
                st.write(f"- **{col}** → {info['etiqueta']}")
                if info["tipo"] == "consentimiento":
                    st.success(f"Todos los {len(df_trabajar)} respondentes aceptaron participar.")
        else:
            st.info("Todas las variables están incluidas en el análisis.")

        st.divider()

        st.subheader("📊 Variables por tipo de análisis")
        st.write("""
        **Variables demográficas (3):**
        - Año de carrera, Edad, Sexo → permiten segmentar los resultados

        **Variables de conocimiento y opinión (8):**
        - Concepto MTCI, familiaridad, conocimiento Ley 774, limitaciones legales
        - Postura profesional, preparación, tipo de efecto

        **Variables de uso de MTCI (3):**
        - Frecuencia de autocuidado, manejo de estrés, efectos experimentados
        - Escalas ordinales: Nunca → Siempre (con opción 'No he utilizado')

        **Listas de prácticas MTCI (3):**
        - Medicina Natural, Terapias Físicas/Manuales, Terapias Energéticas
        - Varias prácticas por celda → parseadas para análisis individual

        **Pregunta abierta (1):**
        - Comentarios y sugerencias (34 sin respuesta — 50%)
        """)

    # -------------------------------------------------------------------------
    # Pestaña 2: Estadística por variable
    # -------------------------------------------------------------------------
    with pestañas[1]:
        st.subheader("Estadística descriptiva por variable")

        vars_para_analizar = [
            col for col, info in st.session_state.var_types.items()
            if info["tipo"] not in ["no_analitico", "consentimiento", "lista_practicas"]
        ]

        if not st.session_state.var_types:
            st.warning("Primero detecta los tipos desde el panel lateral.")
        else:
            col_sel = st.selectbox(
                "Seleccionar variable para analizar",
                options=[c for c in df_trabajar.columns if c in vars_para_analizar],
                help="Elige la variable que quieres analizar.",
            )

            if col_sel:
                info_var = st.session_state.var_types.get(col_sel, {})
                tipo = info_var.get("tipo", "por_determinar")
                stats = stats_por_tipo(df_trabajar[col_sel], tipo)

                st.markdown(f"### {col_sel}")
                st.caption(f"Tipo: **{info_var.get('etiqueta', tipo)}** | Valores únicos: {info_var.get('n_uniques', '—')} | Faltantes: {info_var.get('n_faltantes', '—')} ({info_var.get('pct_faltantes', '—')}%)")

                if tipo in ["ordinal", "ordinal_frecuencia", "opcion_letra", "nominal"]:
                    if "frecuencias" in stats:
                        st.subheader("Frecuencias y porcentajes")
                        st.dataframe(stats["frecuencias"], use_container_width=True, hide_index=True)

                elif tipo == "abierta":
                    st.divider()
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.metric("Respondieron", stats.get("n_respuestas", "—"))
                    with c2:
                        st.metric("Longitud promedio", f"{stats.get('longitud_prom', '—')} caracteres")
                    st.divider()
                    with st.expander("Ejemplo de respuesta"):
                        st.info(stats.get("ejemplo", "—"))

                elif tipo == "lista_practicas":
                    st.info(stats.get("nota", "—"))
                    st.markdown("""
                    **Para analizar esta variable:**
                    1. Ve a la pestaña **"🌿 Prácticas MTCI (parseadas)"**
                    2. Obtendrás el conteo individual por práctica
                    3. Puedes ver qué prácticas son más mencionadas
                    """)

                st.divider()

                # Botón de descarga de esta variable específica
                st.download_button(
                    f"⬇️ Descargar frecuencias de '{col_sel[:30]}' (CSV)",
                    data=stats.get("frecuencias", pd.DataFrame()).to_csv(index=False).encode("utf-8"),
                    file_name=f"frecuencias_{col_sel[:20].replace(' ', '_')}.csv",
                    mime="text/csv",
                )

    # -------------------------------------------------------------------------
    # Pestaña 3: Prácticas MTCI parseadas
    # -------------------------------------------------------------------------
    with pestañas[2]:
        st.subheader("🌿 Análisis de prácticas MTCI")

        if st.session_state.df_expanded is None:
            st.info("👆 Presiona el botón **'🌿 Parsear y expandir prácticas MTCI'** en el panel lateral para analizar las prácticas.")
        else:
            df_exp = st.session_state.df_expanded
            df_resumen = st.session_state.df_practicas

            st.success(f"{len(df_exp)} menciones de prácticas individuales (de {len(df_trabajar)} respondentes)")
            st.caption("Cada mención de práctica se convierte en una fila para análisis independiente.")

            # Mostrar resumen
            st.divider()
            st.subheader("Conteo de prácticas MTCI mencionadas")

            cols_show = st.columns([2, 1])
            with cols_show[0]:
                st.dataframe(df_resumen.head(20), use_container_width=True, hide_index=True)
            with cols_show[1]:
                st.subheader("Top 10 prácticas más mencionadas")
                top10 = df_resumen.head(10).iloc[::-1]
                if len(top10) > 0:
                    fig = px.bar(top10, x="Menciones", y="Practica MTCI",
                                orientation="h", color_discrete_sequence=["#27AE60"])
                    fig.update_layout(showlegend=False, xaxis_title="N° de menciones")
                    st.plotly_chart(fig, use_container_width=True)

            # Por grupo de prácticas
            st.divider()
            st.subheader("Prácticas por categoría")
            cols_grupo = df_exp["Columna"].unique()
            for col_grupo in cols_grupo:
                st.markdown(f"#### {col_grupo[:70]}")
                sub = df_exp[df_exp["Columna"] == col_grupo]
                conteo = sub["Practica"].value_counts().reset_index()
                conteo.columns = ["Practica", "Menciones"]
                st.dataframe(conteo, use_container_width=True, hide_index=True)

            st.divider()

            st.download_button(
                "⬇️ Descargar conteo completo de prácticas MTCI (CSV)",
                data=df_resumen.to_csv(index=False).encode("utf-8"),
                file_name="practicas_mtci_cocuentos.csv",
                mime="text/csv",
            )

    # -------------------------------------------------------------------------
    # Pestaña 4: Gráficos
    # -------------------------------------------------------------------------
    with pestañas[3]:
        st.subheader("Gráficos de variables")

        vars_graficables = [
            col for col, info in st.session_state.var_types.items()
            if info["tipo"] in ["nominal", "opcion_letra", "ordinal", "ordinal_frecuencia"]
        ]

        if not vars_graficables:
            st.warning("No hay variables para graficar (detecta primero los tipos).")
        else:
            graf_sel = st.selectbox(
                "Seleccionar variable para gráfico",
                options=vars_graficables,
            )

            if graf_sel:
                frec = df_trabajar[graf_sel].value_counts().reset_index()
                frec.columns = ["Valor", "Frecuencia"]

                # Gráfico de barras
                fig_bar = px.bar(frec, x="Valor", y="Frecuencia",
                                color_discrete_sequence=["#2980B9"])
                fig_bar.update_layout(showlegend=False, yaxis_title="Frecuencia")
                st.plotly_chart(fig_bar, use_container_width=True)

                # Gráfico de pastel
                fig_pie = px.pie(frec, values="Frecuencia", names="Valor",
                                color_discrete_sequence=px.colors.qualitative.Set2)
                fig_pie.update_traces(textinfo="percent+label")
                st.plotly_chart(fig_pie, use_container_width=True)

                # Descargar gráfico
                try:
                    img_bytes = fig_bar.to_image(format="png", width=800, height=400)
                    st.download_button(
                        f"⬇️ Descargar gráfico de '{graf_sel[:30]}' (PNG)",
                        data=img_bytes,
                        file_name=f"grafico_{graf_sel[:20].replace(' ', '_')}.png",
                        mime="image/png",
                    )
                except Exception:
                    st.caption("(No se pudo generar la imagen descargable)")

    # -------------------------------------------------------------------------
    # Pestaña 5: Exportar para tesis
    # -------------------------------------------------------------------------
    with pestañas[4]:
        st.subheader("📤 Exportar resultados para tu memoria de tesis")

        st.write("""
        Exporta los resultados del análisis en formatos listos para incluir en tu memoria:

        1. **Tabla de tipos de variables** — lista completa con tipos detectados
        2. **Conteo de prácticas MTCI** — prácticas más mencionadas por categoría
        3. **Datos originales** — tu CSV/Excel original (para respaldo)
        """)

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Tabla de tipos de variables")
            if st.session_state.var_types:
                df_tipos = pd.DataFrame([
                    {"Variable": col, "Tipo_detectado": info["etiqueta"],
                     "Tipo_interno": info["tipo"], "Valores_únicos": info["n_uniques"],
                     "Faltantes": info["n_faltantes"], "%_sin_respuesta": info["pct_faltantes"]}
                    for col, info in st.session_state.var_types.items()
                ])
                st.download_button(
                    "📥 Descargar tabla de tipos (CSV)",
                    data=df_tipos.to_csv(index=False).encode("utf-8"),
                    file_name="tabla_tipos_mtci.csv",
                    mime="text/csv",
                )

        with col2:
            st.subheader("Conteo de prácticas MTCI")
            if st.session_state.df_practicas is not None:
                st.download_button(
                    "📥 Descargar conteo de prácticas (CSV)",
                    data=st.session_state.df_practicas.to_csv(index=False).encode("utf-8"),
                    file_name="practicas_mtci.csv",
                    mime="text/csv",
                )
            else:
                st.info("Primero parsea las prácticas desde el panel lateral.")

        with col3:
            st.subheader("Datos originales")
            if st.session_state.df_original_name:
                st.download_button(
                    "📥 Descargar CSV original",
                    data=df_trabajar.to_csv(index=False).encode("utf-8"),
                    file_name="datos_mtci_original.csv",
                    mime="text/csv",
                )

        st.divider()

        st.subheader("📋 Texto sugerido para tu memoria")

        st.write("""
        Puedes copiar y pegar estos textos directamente en tu memoria de tesis:

        **Descripción del instrumento:**
        > El instrumento I1 (Cuestionario sobre Saberes, prácticas y valoración de la Medicina Tradicional, Complementaria e Integrativa - MTCI) fue aplicado a 68 participantes (estudiantes de Psicología en 4to y 5to año, profesionales y actores locales). El cuestionario consta de 21 variables que incluyen: datos demográficos (año de carrera, edad, sexo), conocimiento sobre MTCI, familiaridad con prácticas, conocimiento de la Ley No. 774, limitaciones legales para la psicología clínica, frecuencia de uso de prácticas MTCI como autocuidado y para manejo de estrés, efectos psicofisiológicos percibidos, postura profesional frente a la pertinencia de abordar MTCI en el espacio psicoterapéutico, tipos de efecto sobre la regulación psicofisiológica del consultante, nivel de preparación para psicoeducación y derivación, listado de prácticas MTCI conocidas y utilizadas, y pregunta abierta de comentarios.

        **Tipo de diseño:**
        > El estudio tiene un enfoque mixto con predominio cuantitativo. Las variables cuantitativas incluyen escalas ordinales (frecuencia de uso), variables nominales (sexo, opciones múltiples de selección única) y listas de reconocimiento múltiple (prácticas MTCI). Se incluyó una pregunta abierta para capturar cualitativamente las percepciones y sugerencias de los participantes.

        **Variables excluidas del análisis:**
        > Se excluyeron del análisis estadístico la marca temporal de respuesta y el correo electrónico, por ser datos identificativos sin valor analítico para los objetivos del estudio.
        """)
