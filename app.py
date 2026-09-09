"""
App de Análisis de Instrumentos de Investigación - tipo SPSS interactivo
Tema: Medicina tradicional, complementaria e integrativa como recurso de apoyo en psicología
"""
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

st.set_page_config(
    page_title="Análisis de Instrumentos - Tesis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Estado de la sesión
# -----------------------------------------------------------------------------
if "df" not in st.session_state:
    st.session_state.df = None
if "var_types" not in st.session_state:
    st.session_state.var_types = {}
if "df_clean" not in st.session_state:
    st.session_state.df_clean = None

# -----------------------------------------------------------------------------
# Funciones de análisis
# -----------------------------------------------------------------------------

def detectar_tipo_variable(series, nombre_var, df_completo=None):
    """
    Detecta el tipo de variable basado en su contenido.
    Retorna un diccionario con: tipo, etiqueta, valores únicos, etc.
    """
    col = series.dropna().reset_index(drop=True)
    n_unique = col.nunique()
    n_total = len(series)
    primer_valor = series.dropna().iloc[0] if len(series.dropna()) > 0 else None

    info = {
        "nombre": nombre_var,
        "tipo": "desconocido",
        "etiqueta": "",
        "n_valores_unicos": n_unique,
        "n_faltantes": int(series.isna().sum()),
        "porcentaje_faltantes": round(series.isna().sum() / len(series) * 100, 2) if len(series) > 0 else 0,
        "valores_unicos": sorted(col.unique().tolist()) if n_unique <= 30 else [],
        "primer_valor": primer_valor,
    }

    nombre_lower = nombre_var.lower()
    es_abierta = any(palabra in nombre_lower for palabra in [
        "respuesta_abierta", "comentario", "opinión", "observación",
        "texto", "descripción", "aporte", "sugeren", "interes", "practica_interes", "practica_que_le_gustaria", "que_pratica"
    ])
    es_lista_recognition = any(palabra in nombre_lower for palabra in [
        "reconoc", "lista", "practica", "conoce", "hay", "utiliza", "ha_sido", "que_pratica", "practicas_que"]
    )

    # --- Respuesta abierta / texto libre ---
    if col.dtype == "object":
        longitud_promedio = col.astype(str).str.len().mean()
        # Respuesta abierta si el nombre lo indica, o si los textos son largos (> 30 caracteres)
        # Pero también: si es nominal con muchos valores únicos (> 15) y texto promedio > 10 → probablemente abierta
        if es_abierta:
            info["tipo"] = "abierta"
            info["etiqueta"] = "Respuesta abierta / texto libre"
            return info
        if longitud_promedio > 30:
            info["tipo"] = "abierta"
            info["etiqueta"] = "Respuesta abierta / texto libre"
            return info
        # Si es nominal pero con muchos valores únicos (> 15) y el texto promedio > 8 caracteres → posiblemente abierta
        if n_unique > 15 and longitud_promedio > 8:
            info["tipo"] = "abierta"
            info["etiqueta"] = "Respuesta abierta / texto libre (detectar manualmente)"
            return info

        valores_str = set(str(v).strip().lower() for v in col.unique())
        dicotomicos = {"sí", "si", "no", "s", "n", "verdadero", "falso", "true", "false", "v", "f", "x", "", "nan"}
        if n_unique <= 2 or (n_unique <= 4 and valores_str.issubset(dicotomicos)):
            info["tipo"] = "dicotomica"
            info["etiqueta"] = "Variable dicotómica (sí/no)"
            return info

    # --- Numérica → chequear si es Likert o numérica continua ---
    if pd.api.types.is_numeric_dtype(col):
        if n_unique <= 10:
            min_v = float(col.min())
            max_v = float(col.max())
            rango = min_v, max_v

            # Escalas Likert típicas: 1-5, 1-7, 0-4, 1-4, 1-6, 0-10, 1-10
            likert_ranges = [(1,5), (1,7), (0,4), (1,4), (1,6), (0,10), (1,10), (0,6), (0,3)]
            es_likert = any(
                min_v == r[0] and max_v == r[1]
                for r in likert_ranges
            )
            if es_likert or n_unique <= 5:
                info["tipo"] = "ordinal"
                info["etiqueta"] = f"Escala ordinal / Likert ({int(min_v)}–{int(max_v)})"
                return info

            # Si es numérica pero pocos valores únicos → ordinal
            if n_unique <= 10:
                info["tipo"] = "ordinal"
                info["etiqueta"] = "Escala ordinal"
                return info

        # Numérica continua
        info["tipo"] = "numerica"
        info["etiqueta"] = "Variable numérica"
        return info

    # --- Object con pocos valores únicos → categórica ---
    if col.dtype == "object" and n_unique <= 20:
        if n_unique <= 2:
            info["tipo"] = "dicotomica"
            info["etiqueta"] = "Variable dicotómica"
        else:
            info["tipo"] = "nominal"
            info["etiqueta"] = "Categoría nominal"
        return info

    # Fallback
    info["tipo"] = "nominal"
    info["etiqueta"] = "Categoría nominal"
    return info


def estadisticas_variable(series, tipo_var):
    """Calcula estadísticas según el tipo de variable."""
    resultado = {}
    col = series.dropna()
    n = len(series)
    n_faltantes = int(series.isna().sum())
    n_respondieron = len(col)

    resultado["n_total"] = n
    resultado["n_respondieron"] = n_respondieron
    resultado["n_faltantes"] = n_faltantes
    resultado["porcentaje_respuestados"] = round(n_respondieron / n * 100, 2) if n > 0 else 0

    if tipo_var == "nominal" or tipo_var == "dicotomica":
        frec = col.value_counts(dropna=False).reset_index()
        frec.columns = ["Valor", "Frecuencia"]
        frec["Porcentaje"] = round(frec["Frecuencia"] / n_respondieron * 100, 2)
        frec["Porcentaje_empleado"] = round(frec["Frecuencia"] / n * 100, 2)
        frec = frec.sort_values("Frecuencia", ascending=False)
        resultado["frecuencias"] = frec

    elif tipo_var == "ordinal":
        frec = col.value_counts(dropna=False).reset_index()
        frec.columns = ["Valor", "Frecuencia"]
        frec["Porcentaje"] = round(frec["Frecuencia"] / n_respondieron * 100, 2)
        frec = frec.sort_values("Valor")
        resultado["frecuencias"] = frec

        # Estadísticas ordinales
        if n_respondieron > 0:
            resultado["mediana"] = float(col.median())
            resultado["moda"] = float(col.mode().iloc[0]) if len(col.mode()) > 0 else None
            resultado["min"] = float(col.min())
            resultado["max"] = float(col.max())
            resultado["rango"] = float(col.max() - col.min())

            # Si es Likert típico (1-5, 1-7), calcular media como referencia
            if col.min() >= 1 and col.max() <= 7:
                resultado["media"] = round(float(col.mean()), 2)
                resultado["desviacion_est"] = round(float(col.std()), 2)

    elif tipo_var == "numerica":
        if n_respondieron > 0:
            resultado["media"] = round(float(col.mean()), 2)
            resultado["mediana"] = round(float(col.median()), 2)
            resultado["moda"] = float(col.mode().iloc[0]) if len(col.mode()) > 0 else None
            resultado["min"] = round(float(col.min()), 2)
            resultado["max"] = round(float(col.max()), 2)
            resultado["rango"] = round(float(col.max() - col.min()), 2)
            resultado["desviacion_est"] = round(float(col.std()), 2)
            resultado["varianza"] = round(float(col.var()), 2)
            resultado["asimetria"] = round(float(col.skew()), 3)
            resultado["curtosis"] = round(float(col.kurtosis()), 3)

            # Intervalos de confianza 95% para la media
            if n_respondieron >= 30:
                ic = stats.norm.interval(0.95, loc=col.mean(), scale=col.std() / np.sqrt(n_respondieron))
                resultado["ic_95"] = (round(float(ic[0]), 2), round(float(ic[1]), 2))
            else:
                ic = stats.t.interval(0.95, df=n_respondieron-1, loc=col.mean(), scale=col.std() / np.sqrt(n_respondieron))
                resultado["ic_95"] = (round(float(ic[0]), 2), round(float(ic[1]), 2))

    elif tipo_var == "abierta":
        resultado["n_respuestas"] = n_respondieron
        # Primera resposta como ejemplo
        if n_respondieron > 0:
            resultado["ejemplo_respuesta_1"] = str(col.iloc[0])
            resultado["longitud_promedio_caracteres"] = round(float(col.astype(str).str.len().mean()), 1)

    return resultado


def graficar_frecuencias(frec_df, tipo_var, color_preferido="#4A90D9"):
    """Genera gráfico de barras para frecuencias."""
    if frec_df is None or len(frec_df) == 0:
        return None

    # Prepara datos
    fig = px.bar(
        frec_df,
        x="Valor",
        y="Frecuencia",
        title=f"Distribución de frecuencias",
        color_discrete_sequence=[color_preferido],
        text="Frecuencia",
    )

    # Añadir porcentajes como texto adicional
    if "Porcentaje" in frec_df.columns:
        fig.update_traces(texttemplate="%{text} ({:.1f}%)".format(0), text=frec_df["Porcentaje"])

    fig.update_layout(
        xaxis_title="Valor / Categoría",
        yaxis_title="Frecuencia",
        showlegend=False,
        hovermode="x",
    )

    return fig


# -----------------------------------------------------------------------------
# Interfaz principal
# -----------------------------------------------------------------------------

st.title("📊 Análisis de Instrumentos de Investigación")
st.caption("App interactiva para caracterización de resultados de encuestas — Medicina tradicional, complementaria e integrativa en psicología")

# SIDEBAR
with st.sidebar:
    st.header("📁 Cargar datos")
    st.info("Arrastra tu archivo CSV o Excel (XLSX) al área de abajo, o usa el botón de explorar.")

    uploaded_file = st.file_uploader(
        "Subir archivo",
        type=["csv", "xlsx"],
        help="Formato: CSV o Excel (.xlsx). La primera fila debe contener los nombres de las variables."
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # Detectar y conservar tipos originales
            # Las columnas que parecen numéricas pero tienen strings mezclados → object
            st.session_state.df = df
            st.success(f"✅ Archivo cargado: **{uploaded_file.name}**")
            st.info(f"{df.shape[0]} filas × {df.shape[1]} columnas")
            st.caption("Tipos de datos detectados automáticamente al leer el archivo.")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

    st.divider()

    if st.session_state.df is not None:
        st.header("⚙️ Opciones")

        # Renombrar columnas
        st.subheader("📋 Columnas")
        cols_info = st.session_state.df.columns.tolist()
        st.write(f"Columnas detectadas: {len(cols_info)}")
        st.caption("Los nombres de columna se usan como etiquetas de variable. Puedes renombrarlos si son genéricos (V1, Preg1, etc.).")

        # Detectar tipos de variable
        if st.button("🔍 Detectar tipos de variable", type="primary"):
            with st.spinner("Analizando variables..."):
                tipos = {}
                for col in st.session_state.df.columns:
                    tipos[col] = detectar_tipo_variable(st.session_state.df[col], col)
                st.session_state.var_types = tipos
                st.success("Tipos detectados. Revisa la tabla de abajo.")

        if st.session_state.var_types:
            st.subheader("🧩 Tipos detectados")
            tipo_counts = {}
            for v, info in st.session_state.var_types.items():
                t = info["tipo"]
                tipo_counts[t] = tipo_counts.get(t, 0) + 1

            for t, count in tipo_counts.items():
                emoji = {"nominal": "🏷️", "ordinal": "📏", "dicotomica": "✅", "numerica": "🔢", "abierta": "📝"}.get(t, "❓")
                st.write(f"{emoji} **{t}**: {count} variables")

            st.divider()
            st.subheader("📋 Resumen de variables")

            # Tabla resumen
            rows = []
            for col, info in st.session_state.var_types.items():
                rows.append({
                    "Variable": col,
                    "Tipo": info["etiqueta"],
                    "Tipo_corto": info["tipo"],
                    "Valores únicos": info["n_valores_unicos"],
                    "Faltantes": info["n_faltantes"],
                    "% Faltantes": info["porcentaje_faltantes"],
                })
            df_tipos = pd.DataFrame(rows)
            st.dataframe(df_tipos, use_container_width=True, hide_index=True)

            # Descarga de codificación
            st.download_button(
                label="⬇️ Descargar codificación de variables (CSV)",
                data=df_tipos.to_csv(index=False).encode("utf-8"),
                file_name="codificacion_variables.csv",
                mime="text/csv",
            )

        st.divider()

        # Limpieza básica
        st.header("🧹 Limpieza de datos")
        st.caption("Opciones para manejar valores faltantes y códigos especiales.")

        col1, col2 = st.columns(2)
        with col1:
            codigo_nan = st.text_input(
                "Códigos como faltante (separados por coma)",
                value="99,999,-9999,888,777,NR,S/N,Sin dato",
                help="Ej: 99, 999, -9999, 'NR' (no responde), 'S/N' (sin respuesta)"
            )
        with col2:
            st.write("")

        if st.button("🧹 Aplicar limpieza de faltantes"):
            with st.spinner("Limpando..."):
                df = st.session_state.df.copy()
                codigos = [c.strip() for c in codigo_nan.split(",")]
                # Reemplazar en todo el dataframe
                for codigo in codigos:
                    df = df.replace(codigo, np.nan)
                    # También reemplazar si es string "nan" o similar
                    if codigo.lower() in ["nan", "na", "n/a", "none", "null", "nr", "s/n", "sin dato", "sinrespuesta"]:
                        df = df.replace(codigo, np.nan)

                st.session_state.df_clean = df
                st.success("Limpieza aplicada. Los valores marcados como faltantes ahora son NaN.")

        if st.session_state.df_clean is not None:
            st.info("Datos limpios disponibles. Usa la opción en el panel principal para trabajar con la versión limpia.")

        st.divider()
        st.caption("App basada en Streamlit + Pandas + SciPy + Plotly")
        st.caption("Versión 1.0 — Análisis descriptivo inicial")


# CONTENIDO PRINCIPAL
st.header("📊 Análisis de datos")

if st.session_state.df is None:
    st.info("👆 Sube un archivo CSV o Excel desde el panel lateral para comenzar.")
    st.divider()

    # Sección de ayuda
    st.subheader("📖 ¿Qué puedo hacer con esta app?")
    st.write("""
    Esta app te permite:

    1. **Cargar tus datos** desde CSV o Excel
    2. **Detectar automáticamente** el tipo de cada variable (nominal, ordinal/Likert, dicotómica, numérica, abierta)
    3. **Ver estadística descriptiva** para cada variable según su tipo
    4. **Descargar codificaciones** para tu reporte
    5. **Limpear faltantes** (valores como 99, NR, etc. se convierten en NaN)

    TODO (próximas versiones):
    - Cruzar variables (tablas de contingencia)
    - Alfa de Cronbach (confiabilidad)
    - Pruebas de normalidad
    - Estadística inferencial
    - Gráficos más avanzados
    """)
else:
    # Usar versión limpia si está disponible
    usar_limpio = st.checkbox("Usar versión limpia (faltantes tratados)", value=False)
    if usar_limpio and st.session_state.df_clean is not None:
        df_trabajar = st.session_state.df_clean.copy()
        st.info("Usando versión limpia de los datos.")
    else:
        df_trabajar = st.session_state.df.copy()
        if st.session_state.df_clean is not None:
            st.warning("La versión limpia existe pero no está seleccionada. Marca la casilla para usarla.")

    # ---------- Pestañas ----------
    pestañas = st.tabs([
        "📋 Vista preliminar de datos",
        "📊 Estadística descriptiva",
        "📈 Gráficos",
        "🔍 Filtros y segmentación",
    ])

    # ===== Pestaña 1: Vista preliminar =====
    with pestañas[0]:
        st.subheader("Vista de los datos cargados")

        filas_a_mostrar = st.slider("Filas a mostrar", 5, 50, 10)
        st.dataframe(df_trabajar.head(filas_a_mostrar), use_container_width=True, height=300)

        st.divider()
        st.subheader("Información general del dataset")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Filas (respondentes)", df_trabajar.shape[0])
        with col2:
            st.metric("Columnas (variables)", df_trabajar.shape[1])
        with col3:
            total_faltantes = df_trabajar.isna().sum().sum()
            st.metric("Celdas faltantes", total_faltantes)
        with col4:
            st.metric("% faltantes global", round(total_faltantes / (df_trabajar.shape[0] * df_trabajar.shape[1]) * 100, 2))

        st.divider()
        st.subheader("Descripción de columnas")
        df_desc = pd.DataFrame({
            "Columna": df_trabajar.columns,
            "Tipo de datos": df_trabajar.dtypes.astype(str),
            "Ejemplo (primera fila)": [df_trabajar[col].iloc[0] if len(df_trabajar) > 0 else "" for col in df_trabajar.columns],
        })
        st.dataframe(df_desc, use_container_width=True, hide_index=True)

    # ===== Pestaña 2: Estadística descriptiva =====
    with pestañas[1]:
        st.subheader("Estadística descriptiva por variable")

        if not st.session_state.var_types:
            st.warning("Primero detecta los tipos de variable desde el panel lateral.")
        else:
            # Selección de variable
            col_sel = st.selectbox(
                "Selecciona una variable para analizar",
                options=df_trabajar.columns.tolist(),
                help="Elige la variable (columna) que quieres analizar."
            )

            if col_sel:
                info_var = st.session_state.var_types.get(col_sel, {})
                tipo = info_var.get("tipo", "desconocido")
                serie = df_trabajar[col_sel]

                st.markdown(f"### {col_sel}")
                st.caption(f"Tipo detectado: **{info_var.get('etiqueta', tipo)}**")

                # Métricas rápidas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Respondieron", info_var.get("n_valores_unicos", "—"))
                with col2:
                    st.metric("Faltantes", info_var.get("n_faltantes", "—"))
                with col3:
                    st.metric("% Faltantes", info_var.get("porcentaje_faltantes", "—"))

                st.divider()

                # Estadísticas
                stats_result = estadisticas_variable(serie, tipo)

                if tipo == "nominal" or tipo == "dicotomica":
                    st.subheader("Frecuencias y porcentajes")
                    if "frecuencias" in stats_result and len(stats_result["frecuencias"]) > 0:
                        frec = stats_result["frecuencias"]
                        st.dataframe(frec, use_container_width=True, hide_index=True)
                    else:
                        st.info("No hay datos suficientes para mostrar frecuencias.")

                elif tipo == "ordinal":
                    st.subheader("Frecuencias (ordenadas)")
                    if "frecuencias" in stats_result and len(stats_result["frecuencias"]) > 0:
                        frec = stats_result["frecuencias"]
                        st.dataframe(frec, use_container_width=True, hide_index=True)

                    st.divider()
                    st.subheader("Estadísticas ordinales")
                    if "mediana" in stats_result:
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.metric("Mediana", stats_result["mediana"])
                        with col2:
                            st.metric("Moda", stats_result["moda"])
                        with col3:
                            st.metric("Mínimo", stats_result["min"])
                        with col4:
                            st.metric("Máximo", stats_result["max"])
                        with col5:
                            st.metric("Rango", stats_result["rango"])

                    if "media" in stats_result:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Media", stats_result["media"])
                        with col2:
                            st.metric("Desviación estándar", stats_result["desviacion_est"])

                elif tipo == "numerica":
                    st.subheader("Estadísticas numéricas")
                    if "media" in stats_result:
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.metric("Media", stats_result["media"])
                        with col2:
                            st.metric("Mediana", stats_result["mediana"])
                        with col3:
                            st.metric("Moda", stats_result["moda"])
                        with col4:
                            st.metric("Mínimo", stats_result["min"])
                        with col5:
                            st.metric("Máximo", stats_result["max"])

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Rango", stats_result["rango"])
                        with col2:
                            st.metric("Desv. Estándar", stats_result["desviacion_est"])
                        with col3:
                            st.metric("Varianza", stats_result["varianza"])

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Asimetría", stats_result["asimetria"])
                        with col2:
                            st.metric("Curtosis", stats_result["curtosis"])

                        if "ic_95" in stats_result:
                            st.info(f"Intervalo de confianza 95% para la media: **[{stats_result['ic_95'][0]}, {stats_result['ic_95'][1]}]**")

                elif tipo == "abierta":
                    st.subheader("Respuestas abiertas")
                    st.write(f"Número de respuestas: **{stats_result.get('n_respuestas', '—')}**")
                    st.write(f"Longitud promedio: **{stats_result.get('longitud_promedio_caracteres', '—')} caracteres**")
                    st.divider()
                    st.subheader("Ejemplo de respuesta")
                    st.write(stats_result.get("ejemplo_respuesta_1", "Sin respuestas"))
                    st.divider()
                    st.caption("Para análisis de contenido cualitativo, usa técnicas de codificación manual o software especializado.")

                # Gráfico de la variable seleccionada
                st.divider()
                if tipo in ["nominal", "dicotomica", "ordinal"]:
                    if "frecuencias" in stats_result and len(stats_result["frecuencias"]) > 0:
                        fig = graficar_frecuencias(stats_result["frecuencias"], tipo)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)

    # ===== Pestaña 3: Gráficos =====
    with pestañas[2]:
        st.subheader("Gráficos de las variables")

        if not st.session_state.var_types:
            st.warning("Primero detecta los tipos de variable desde el panel lateral.")
        else:
            graf_sel = st.selectbox(
                "Selecciona una variable para gráfico",
                options=df_trabajar.columns.tolist(),
            )

            if graf_sel:
                info_var = st.session_state.var_types.get(graf_sel, {})
                tipo = info_var.get("tipo", "desconocido")
                serie = df_trabajar[graf_sel]

                st.caption(f"Variable: **{graf_sel}** — Tipo: {info_var.get('etiqueta', tipo)}")

                # Gráfico por tipo
                if tipo in ["nominal", "dicotomica", "ordinal"]:
                    frec = serie.value_counts(dropna=False).reset_index()
                    frec.columns = ["Valor", "Frecuencia"]
                    if "Porcentaje" not in frec.columns:
                        n_resp = len(serie.dropna())
                        frec["Porcentaje"] = round(frec["Frecuencia"] / n_resp * 100, 2) if n_resp > 0 else 0

                    # Gráfico de barras vertical
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.subheader("Gráfico de barras")
                        fig_bar = px.bar(frec, x="Valor", y="Frecuencia", text="Frecuencia",
                                        color_discrete_sequence=["#4A90D9"])
                        fig_bar.update_traces(texttemplate="%{text}")
                        fig_bar.update_layout(showlegend=False, xaxis_title="Valor", yaxis_title="Frecuencia")
                        st.plotly_chart(fig_bar, use_container_width=True)

                    with col2:
                        st.subheader("Gráfico de pastel")
                        fig_pie = px.pie(frec, values="Frecuencia", names="Valor",
                                        color_discrete_sequence=px.colors.qualitative.Set3)
                        fig_pie.update_traces(textinfo="percent+label")
                        st.plotly_chart(fig_pie, use_container_width=True)

                    # Descargar gráfico
                    st.download_button(
                        label="⬇️ Descargar gráfico de barras (PNG)",
                        data=fig_bar.to_image(format="png", width=800, height=500),
                        file_name=f"grafico_{graf_sel}.png",
                        mime="image/png",
                    )

                elif tipo == "numerica":
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Histograma")
                        fig_hist = px.histogram(serie.dropna(), nbins=20,
                                                color_discrete_sequence=["#E74C3C"])
                        fig_hist.update_layout(xaxis_title=graf_sel, yaxis_title="Frecuencia")
                        st.plotly_chart(fig_hist, use_container_width=True)

                    with col2:
                        st.subheader("Diagrama de caja (boxplot)")
                        fig_box = px.box(serie.dropna(), color_discrete_sequence=["#2ECC71"])
                        fig_box.update_layout(yaxis_title=graf_sel)
                        st.plotly_chart(fig_box, use_container_width=True)

                elif tipo == "abierta":
                    st.info("Las variables de texto libre no se representan con gráficos tradicionales.")
                    st.write("Considera: análisis de contenido, nube de palabras, o codificación temática.")

    # ===== Pestaña 4: Filtros =====
    with pestañas[3]:
        st.subheader("Filtrar y segmentar datos")

        st.write("""
        Permite filtrar los datos por una o más variables categóricas y analizar subgrupos.
        """)

        # Selección de variable para filtrar
        vars_categoricas = [
            col for col in df_trabajar.columns
            if st.session_state.var_types.get(col, {}).get("tipo") in ["nominal", "dicotomica", "ordinal"]
        ]

        if vars_categoricas:
            var_filtro = st.selectbox(
                "Variable para filtrar",
                options=vars_categoricas,
                help="Elige una variable categórica para crear filtros."
            )

            if var_filtro:
                valores = df_trabajar[var_filtro].dropna().unique()
                valores_ordenados = sorted(valores, key=str)
                valores_seleccionados = st.multiselect(
                    f"Valores de '{var_filtro}' para incluir",
                    options=valores_ordenados,
                    default=valores_ordenados[:min(3, len(valores_ordenados))] if len(valores_ordenados) > 0 else [],
                )

                if valores_seleccionados:
                    df_filtrado = df_trabajar[df_trabajar[var_filtro].isin(valores_seleccionados)].copy()
                    st.info(f"Dataset filtrado: {df_filtrado.shape[0]} filas (de {df_trabajar.shape[0]} originales)")
                    st.dataframe(df_filtrado.head(10), use_container_width=True, height=200)

                    st.divider()
                    st.subheader("Comparar con el dataset completo")

                    if st.session_state.var_types:
                        col_comp1, col_comp2 = st.columns(2)
                        with col_comp1:
                            st.markdown("### Dataset completo")
                            st.write(f"Filas: {df_trabajar.shape[0]}, Columnas: {df_trabajar.shape[1]}")
                        with col_comp2:
                            st.markdown("### Dataset filtrado")
                            st.write(f"Filas: {df_filtrado.shape[0]}, Columnas: {df_filtrado.shape[1]}")

    # Pie de página
    st.divider()
    st.caption("App creada para análisis de instrumentos de investigación — Medicina tradicional, complementaria e integrativa en psicología")
    st.caption("Usa la pestaña 'Estadística descriptiva' para caracterizar cada variable por su tipo.")
    st.caption("Próximamente: cruzados, confiabilidad (Alfa de Cronbach), pruebas de normalidad, ANOVA, correlaciones.")
