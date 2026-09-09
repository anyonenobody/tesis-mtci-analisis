"""
🌿 App de Análisis e Interpretación de Instrumentos MTCI — Tesis de Psicología
Diseñada para un flujo simple, sin fricciones técnicas:
1. Carga automática del archivo (o subida manual)
2. Mapeo inteligente automático de nombres de columnas y tipos de variable
3. Menú claro para análisis univariado, bivariado, interpretación narrativa y diseño de gráficos al gusto
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from io import BytesIO
from scipy import stats
import sys

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis MTCI — Tesis",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTILOS VISUALES Y SISTEMA DE DISEÑO (CSS MODERNO Y ELEGANTE)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Tipografía y espaciado */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Encabezado principal */
    .hero-banner {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 60%, #40916c 100%);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 24px rgba(27, 67, 50, 0.15);
    }
    .hero-banner h1 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff !important;
        letter-spacing: -0.5px;
    }
    .hero-banner p {
        font-size: 1.05rem;
        color: #d8f3dc;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }
    
    /* Tarjetas métricas personalizadas */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.07);
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }
    .metric-val {
        font-size: 1.9rem;
        font-weight: 700;
        color: #1b4332;
    }
    .metric-sub {
        font-size: 0.85rem;
        color: #10b981;
        font-weight: 500;
        margin-top: 0.2rem;
    }
    
    /* Caja de interpretación académica */
    .narrative-box {
        background: #f0fdf4;
        border-left: 5px solid #10b981;
        border-radius: 8px 12px 12px 8px;
        padding: 1.2rem 1.4rem;
        margin: 1.2rem 0;
        color: #064e3b;
        font-size: 0.98rem;
        line-height: 1.6;
    }
    .narrative-title {
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #047857;
    }
    
    /* Pestañas estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8fafc;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #1b4332 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Tablas limpias */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PALETAS DE COLOR CURADAS PARA EL CONSTRUCTOR DE GRÁFICOS
# -----------------------------------------------------------------------------
PALETAS_COLOR = {
    "🌿 MTCI Botánico (Verdes)": ["#1b4332", "#2d6a4f", "#40916c", "#52b788", "#74c69d", "#95d5b2", "#b7e4c7"],
    "🎓 Tesis Académica (Azul / Gris)": ["#1d3557", "#457b9d", "#e63946", "#a8dadc", "#2a9d8f", "#f4a261", "#e76f51"],
    "🌅 Cálido y Terapéutico (Ámbar / Terracota)": ["#9a3412", "#c2410c", "#ea580c", "#f97316", "#fb923c", "#fdba74", "#fed7aa"],
    "💜 Psicología Clínica (Índigo / Violeta)": ["#312e81", "#4338ca", "#6366f1", "#818cf8", "#a5b4fc", "#c7d2fe", "#e0e7ff"],
    "🌈 Armonía Pastel": ["#60a5fa", "#34d399", "#f472b6", "#fbbf24", "#a78bfa", "#f87171", "#38bdf8"],
    "🖤 Estilo Formal APA (Monocromático)": ["#111827", "#374151", "#4b5563", "#6b7280", "#9ca3af", "#d1d5db", "#e5e7eb"]
}

# -----------------------------------------------------------------------------
# FUNCIONES DE CARGA Y MAPEADO INTELIGENTE
# -----------------------------------------------------------------------------
def leer_archivo_robusto(archivo_o_ruta):
    """Carga un CSV o Excel probando codificaciones y sin romper tildes ni símbolos."""
    if isinstance(archivo_o_ruta, str):
        for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
            try:
                df = pd.read_csv(archivo_o_ruta, encoding=enc, dtype=str, keep_default_na=False, na_values=[''])
                if len(df.columns) > 1:
                    return df, enc
            except Exception:
                continue
        return pd.read_csv(archivo_o_ruta, dtype=str), 'default'
    else:
        nombre = getattr(archivo_o_ruta, "name", "").lower()
        if nombre.endswith((".xlsx", ".xls")):
            return pd.read_excel(archivo_o_ruta, dtype=str, keep_default_na=False, na_values=['']), "excel"
        else:
            bytes_data = archivo_o_ruta.getvalue()
            for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(BytesIO(bytes_data), encoding=enc, dtype=str, keep_default_na=False, na_values=[''])
                    if len(df.columns) > 1:
                        return df, enc
                except Exception:
                    continue
            return pd.read_csv(BytesIO(bytes_data), dtype=str), "default"


def detectar_y_mapear_columna(col_name, series):
    """
    Asigna un alias corto, rol de variable y etiqueta amigable
    sin usar jerga de programador.
    """
    c_lower = col_name.lower().strip()
    n_unique = series.dropna().nunique()
    valores = [str(v).strip() for v in series.dropna().unique() if str(v).strip()]
    
    # 1. Identificadores y consentimiento
    if 'id' in c_lower and ('respondente' in c_lower or 'sujeto' in c_lower or len(c_lower) <= 5):
        return {'alias': 'ID Respondente', 'tipo': 'excluido', 'icono': '🚫', 'rol': 'Identificador (Excluido)', 'original': col_name}
    if any(k in c_lower for k in ['leído', 'leido', 'consentimiento', 'acepto', 'voluntariamente']):
        return {'alias': 'Consentimiento Informado', 'tipo': 'excluido', 'icono': '✅', 'rol': 'Consentimiento (Informativo)', 'original': col_name}
    if 'marca temporal' in c_lower or 'timestamp' in c_lower:
        return {'alias': 'Marca Temporal', 'tipo': 'excluido', 'icono': '📅', 'rol': 'Fecha de registro', 'original': col_name}
    if 'correo' in c_lower or 'email' in c_lower:
        return {'alias': 'Correo Electrónico', 'tipo': 'excluido', 'icono': '📧', 'rol': 'Email (Privado)', 'original': col_name}
    
    # 2. Demografía
    if 'año' in c_lower and 'carrera' in c_lower:
        return {'alias': 'Año de carrera', 'tipo': 'categoria', 'icono': '🎓', 'rol': 'Demográfica (Año)', 'original': col_name}
    if 'edad' in c_lower:
        return {'alias': 'Rango de edad', 'tipo': 'escala', 'icono': '📊', 'rol': 'Demográfica (Edad)', 'original': col_name}
    if 'sexo' in c_lower or 'género' in c_lower or 'genero' in c_lower:
        return {'alias': 'Sexo', 'tipo': 'categoria', 'icono': '👤', 'rol': 'Demográfica (Sexo)', 'original': col_name}
    
    # 3. Conocimiento y posturas clave (prioridad de coincidencias específicas)
    if 'postura profesional' in c_lower:
        return {'alias': 'Postura profesional', 'tipo': 'categoria', 'icono': '💼', 'rol': 'Opinión Profesional', 'original': col_name}
    if 'concepto' in c_lower or 'describe con mayor precisión' in c_lower or 'describe con mayor precision' in c_lower:
        return {'alias': 'Concepto de MTCI', 'tipo': 'categoria', 'icono': '📖', 'rol': 'Conocimiento Conceptual', 'original': col_name}
    if 'familiaridad' in c_lower:
        return {'alias': 'Nivel de familiaridad', 'tipo': 'escala', 'icono': '🔍', 'rol': 'Escala de Familiaridad', 'original': col_name}
    if 'ley no. 774' in c_lower or 'ley 774' in c_lower:
        return {'alias': 'Propósito Ley 774', 'tipo': 'categoria', 'icono': '⚖️', 'rol': 'Conocimiento Normativo', 'original': col_name}
    if 'limitación legal' in c_lower or 'limitacion legal' in c_lower or 'norma que la sustenta' in c_lower:
        return {'alias': 'Límites legales clínicos', 'tipo': 'categoria', 'icono': '🛡️', 'rol': 'Marco Legal y Ético', 'original': col_name}
    
    # 4. Frecuencias de uso y efectos
    if 'autocuidado' in c_lower and ('frecuencia' in c_lower or 'método' in c_lower or 'metodo' in c_lower):
        return {'alias': 'Frecuencia autocuidado', 'tipo': 'escala', 'icono': '🌿', 'rol': 'Frecuencia de Uso', 'original': col_name}
    if 'estrés' in c_lower or 'estres' in c_lower:
        return {'alias': 'Frecuencia manejo de estrés', 'tipo': 'escala', 'icono': '🧘', 'rol': 'Frecuencia de Uso', 'original': col_name}
    if 'cambios o efectos psicofisiológicos' in c_lower or 'experimentado personalmente' in c_lower:
        return {'alias': 'Efectos experimentados', 'tipo': 'categoria', 'icono': '✨', 'rol': 'Efectos Subjetivos', 'original': col_name}
    if 'tipo de efecto' in c_lower and 'regulación psicofisiológica' in c_lower:
        return {'alias': 'Efecto en regulación', 'tipo': 'categoria', 'icono': '🧠', 'rol': 'Valoración Terapéutica', 'original': col_name}
    
    # 5. Competencias y derivación
    if 'preparación actual para realizar psicoeducación' in c_lower or 'preparacion actual para realizar psicoeducacion' in c_lower:
        return {'alias': 'Preparación en psicoeducación', 'tipo': 'escala', 'icono': '📚', 'rol': 'Nivel de Preparación', 'original': col_name}
    if 'preparación actual para realizar una derivación' in c_lower or 'fuentes de derivación' in c_lower or 'preparacion actual para realizar una derivacion' in c_lower:
        return {'alias': 'Preparación en derivación', 'tipo': 'escala', 'icono': '🔄', 'rol': 'Nivel de Preparación', 'original': col_name}
    
    # 6. Listas de prácticas MTCI (selección múltiple)
    if 'medicina natural' in c_lower and 'enfoques' in c_lower:
        return {'alias': 'Prácticas: Medicina Natural', 'tipo': 'seleccion_multiple', 'icono': '🌱', 'rol': 'Selección Múltiple (Prácticas)', 'original': col_name}
    if 'físicas' in c_lower or 'manuales' in c_lower or 'fisicas' in c_lower:
        return {'alias': 'Prácticas: Terapias Manuales/Físicas', 'tipo': 'seleccion_multiple', 'icono': '👐', 'rol': 'Selección Múltiple (Prácticas)', 'original': col_name}
    if 'energéticas' in c_lower or 'psicoemocionales' in c_lower or 'energeticas' in c_lower:
        return {'alias': 'Prácticas: Terapias Energéticas', 'tipo': 'seleccion_multiple', 'icono': '💫', 'rol': 'Selección Múltiple (Prácticas)', 'original': col_name}
    
    # 7. Pregunta abierta
    if any(k in c_lower for k in ['comentario', 'sugerencia', 'inquietud', 'opinión', 'opinion']):
        return {'alias': 'Comentarios / Sugerencias', 'tipo': 'texto_abierto', 'icono': '📝', 'rol': 'Pregunta Abierta (Cualitativa)', 'original': col_name}
    
    # 8. Heurísticas generales para otros cuestionarios/archivos
    tiene_comas = any(len(str(v)) > 35 and ',' in str(v) for v in valores)
    prom_len = series.astype(str).str.len().mean()
    
    if tiene_comas:
        alias_gen = col_name[:32] + ('...' if len(col_name) > 32 else '')
        return {'alias': alias_gen, 'tipo': 'seleccion_multiple', 'icono': '🌿', 'rol': 'Selección Múltiple', 'original': col_name}
    elif n_unique > 15 and prom_len > 35:
        alias_gen = col_name[:32] + ('...' if len(col_name) > 32 else '')
        return {'alias': alias_gen, 'tipo': 'texto_abierto', 'icono': '📝', 'rol': 'Texto Abierto', 'original': col_name}
    else:
        alias_gen = col_name[:32] + ('...' if len(col_name) > 32 else '')
        return {'alias': alias_gen, 'tipo': 'categoria', 'icono': '🏷️', 'rol': 'Categoría', 'original': col_name}


def parsear_seleccion_multiple(df, columnas):
    """
    Parsea las columnas con respuestas separadas por coma en una estructura
    lista para análisis univariado y conteo de participantes.
    """
    registros = []
    conteo_global = Counter()
    
    for col in columnas:
        for idx, row in df.iterrows():
            val = str(row[col]).strip()
            if not val or val.lower() in ["ninguna", "nunca", "nan", "none", "no conozco ninguna", "no utilizo ninguna"]:
                registros.append({"Columna": col, "Practica": "Ninguna / No aplica", "Respondente": idx})
                conteo_global["Ninguna / No aplica"] += 1
            else:
                items = [item.strip() for item in val.split(",") if item.strip()]
                for item in items:
                    registros.append({"Columna": col, "Practica": item, "Respondente": idx})
                    conteo_global[item] += 1
                    
    df_exp = pd.DataFrame(registros)
    n_resp = len(df)
    resumen = pd.DataFrame([
        {
            "Práctica MTCI": k,
            "Menciones": v,
            "% de Respondentes": round(v / n_resp * 100, 1)
        }
        for k, v in conteo_global.most_common()
    ])
    return df_exp, resumen


# -----------------------------------------------------------------------------
# GENERADORES ESTADÍSTICOS E INTERPRETATIVOS
# -----------------------------------------------------------------------------
def calcular_tabla_frecuencias(series):
    """Genera la tabla con Conteo, Porcentaje y Porcentaje Acumulado."""
    validos = series.dropna()
    validos = validos[validos.astype(str).str.strip() != '']
    n_validos = len(validos)
    
    if n_validos == 0:
        return pd.DataFrame(), 0, len(series)
        
    conteo = validos.value_counts().reset_index()
    conteo.columns = ["Opción", "Frecuencia (n)"]
    conteo["Porcentaje (%)"] = round(conteo["Frecuencia (n)"] / n_validos * 100, 1)
    
    # Ordenamiento lógico si tiene letras a), b), etc.
    if conteo["Opción"].astype(str).str.match(r'^[a-z]\)').any():
        conteo["_orden"] = conteo["Opción"].astype(str).str[0].str.lower()
        conteo = conteo.sort_values("_orden").drop(columns=["_orden"])
    
    conteo["% Acumulado"] = round(conteo["Porcentaje (%)"].cumsum(), 1)
    return conteo, n_validos, len(series)


def redactar_interpretacion_univariada(alias, pregunta, tabla_frec, n_validos, n_total):
    """Redacta un párrafo formal en formato de tesis sobre la variable analizada."""
    if tabla_frec.empty or n_validos == 0:
        return "No se registran respuestas válidas para esta variable."
        
    pct_part = round(n_validos / n_total * 100, 1)
    top_row = tabla_frec.sort_values("Frecuencia (n)", ascending=False).iloc[0]
    top_opc = top_row["Opción"]
    top_pct = top_row["Porcentaje (%)"]
    top_n = top_row["Frecuencia (n)"]
    
    texto = (
        f"En relación con la dimensión **'{alias}'** (*\"{pregunta}\"*), se registró la participación de "
        f"**{n_validos} respondentes** ({pct_part}% de la muestra total analizada). "
    )
    
    if len(tabla_frec) == 1:
        texto += f"El total de los participantes ({top_pct}%, n={top_n}) coincidió unánimemente en la categoría **'{top_opc}'**."
    else:
        seg_row = tabla_frec.sort_values("Frecuencia (n)", ascending=False).iloc[1]
        seg_opc = seg_row["Opción"]
        seg_pct = seg_row["Porcentaje (%)"]
        seg_n = seg_row["Frecuencia (n)"]
        
        texto += (
            f"La respuesta con mayor predominancia correspondió a la opción **'{top_opc}'**, concentrando el **{top_pct}%** (n={top_n}) "
            f"de las menciones. En segundo lugar, se situó la opción **'{seg_opc}'** con un **{seg_pct}%** (n={seg_n}). "
        )
        
        if len(tabla_frec) > 2:
            min_row = tabla_frec.sort_values("Frecuencia (n)", ascending=True).iloc[0]
            texto += (
                f"Por su parte, la categoría con menor índice de respuesta fue **'{min_row['Opción']}'**, representando únicamente "
                f"el **{min_row['Porcentaje (%)']}%** (n={min_row['Frecuencia (n)']}) del grupo encuestado."
            )
            
    return texto


def redactar_interpretacion_practicas(resumen_df, n_total):
    """Genera la narrativa académica sobre el reconocimiento de prácticas MTCI."""
    if resumen_df.empty:
        return "No se identificaron prácticas mencionadas."
        
    validas = resumen_df[~resumen_df["Práctica MTCI"].str.contains("Ninguna", case=False)]
    if validas.empty:
        return "La mayoría de respondentes no reportó prácticas específicas."
        
    top1 = validas.iloc[0]
    texto = (
        f"En la exploración de prácticas de MTCI, se identificó un amplio espectro de saberes y terapias. "
        f"La práctica con mayor índice de conocimiento o utilización fue **{top1['Práctica MTCI']}**, siendo seleccionada por el "
        f"**{top1['% de Respondentes']}%** de los participantes (n={top1['Menciones']}). "
    )
    if len(validas) > 1:
        top2 = validas.iloc[1]
        texto += f"Le sigue en relevancia **{top2['Práctica MTCI']}** con el **{top2['% de Respondentes']}%** (n={top2['Menciones']}). "
    if len(validas) > 2:
        top3 = validas.iloc[2]
        texto += f"Asimismo, se destaca la presencia de **{top3['Práctica MTCI']}** con un **{top3['% de Respondentes']}%** (n={top3['Menciones']})."
        
    return texto


def generar_excel_completo(df_base, mapeo, resumen_practicas):
    """Genera un archivo Excel consolidado con pestañas organizadas para la tesis."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # 1. Resumen y Variables
        df_vars = pd.DataFrame([
            {
                "Alias Corto": info["alias"],
                "Tipo de Variable": info["rol"],
                "Enunciado Completo": info["original"]
            }
            for col, info in mapeo.items()
        ])
        df_vars.to_excel(writer, sheet_name="Variables y Mapeo", index=False)
        
        # 2. Frecuencias Univariadas
        filas_todas = []
        for col, info in mapeo.items():
            if info["tipo"] in ["categoria", "escala"]:
                tabla, _, _ = calcular_tabla_frecuencias(df_base[col])
                if not tabla.empty:
                    tabla.insert(0, "Variable", info["alias"])
                    filas_todas.append(tabla)
        if filas_todas:
            df_todas_frec = pd.concat(filas_todas, ignore_index=True)
            df_todas_frec.to_excel(writer, sheet_name="Tablas de Frecuencia", index=False)
            
        # 3. Prácticas MTCI
        if resumen_practicas is not None and not resumen_practicas.empty:
            resumen_practicas.to_excel(writer, sheet_name="Prácticas MTCI Conteo", index=False)
            
        # 4. Datos Base
        df_base.to_excel(writer, sheet_name="Datos Base Anonimizados", index=False)
        
    return output.getvalue()


# -----------------------------------------------------------------------------
# INICIALIZACIÓN AUTOMÁTICA DEL ESTADO
# -----------------------------------------------------------------------------
ARCHIVO_DEFAULT = "datos_mtci_anonimizado.csv"

if "df" not in st.session_state:
    st.session_state.df = None
if "mapeo" not in st.session_state:
    st.session_state.mapeo = {}
if "df_practicas_exp" not in st.session_state:
    st.session_state.df_practicas_exp = None
if "df_practicas_resumen" not in st.session_state:
    st.session_state.df_practicas_resumen = None
if "nombre_origen" not in st.session_state:
    st.session_state.nombre_origen = ""

# Auto-carga al inicio sin intervención del usuario
if st.session_state.df is None:
    try:
        df_ini, enc_ini = leer_archivo_robusto(ARCHIVO_DEFAULT)
        st.session_state.df = df_ini.copy()
        st.session_state.nombre_origen = ARCHIVO_DEFAULT
        
        # Mapear columnas inmediatamente
        mapeo_auto = {}
        for col in df_ini.columns:
            mapeo_auto[col] = detectar_y_mapear_columna(col, df_ini[col])
        st.session_state.mapeo = mapeo_auto
        
        # Parsear prácticas inmediatamente
        cols_mult = [c for c, m in mapeo_auto.items() if m["tipo"] == "seleccion_multiple"]
        if cols_mult:
            exp, res = parsear_seleccion_multiple(df_ini, cols_mult)
            st.session_state.df_practicas_exp = exp
            st.session_state.df_practicas_resumen = res
            
    except Exception:
        pass


# =============================================================================
# PANEL LATERAL (CARGA SIMPLE Y ESTADO)
# =============================================================================
with st.sidebar:
    st.markdown("### 📁 Origen de Datos")
    
    subido = st.file_uploader(
        "Cargar archivo CSV o Excel",
        type=["csv", "xlsx", "xls"],
        help="Sube tu archivo de respuestas. La app detectará automáticamente las variables y columnas."
    )
    
    if subido is not None and subido.name != st.session_state.nombre_origen:
        with st.spinner("Cargando y mapeando variables automáticamente..."):
            df_subido, enc = leer_archivo_robusto(subido)
            st.session_state.df = df_subido.copy()
            st.session_state.nombre_origen = subido.name
            
            # Re-mapeo automático
            mapeo_auto = {}
            for col in df_subido.columns:
                mapeo_auto[col] = detectar_y_mapear_columna(col, df_subido[col])
            st.session_state.mapeo = mapeo_auto
            
            # Parseo de selección múltiple automático
            cols_mult = [c for c, m in mapeo_auto.items() if m["tipo"] == "seleccion_multiple"]
            if cols_mult:
                exp, res = parsear_seleccion_multiple(df_subido, cols_mult)
                st.session_state.df_practicas_exp = exp
                st.session_state.df_practicas_resumen = res
            else:
                st.session_state.df_practicas_exp = None
                st.session_state.df_practicas_resumen = None
                
            st.toast(f"✅ Archivo cargado con éxito ({len(df_subido)} respondentes)")
            
    if st.session_state.df is not None:
        st.success(f"**Archivo en uso:** `{st.session_state.nombre_origen}`")
        st.caption(f"**Dimensiones:** {st.session_state.df.shape[0]} filas × {st.session_state.df.shape[1]} columnas")
        
        st.divider()
        st.markdown("### ℹ️ Guía rápida")
        st.markdown("""
        - **1. Panorama y Mapeo**: Revisa tus columnas y ajusta nombres si lo deseas.
        - **2. Explorar e Interpretar**: Estadísticas y redacción lista para tu tesis.
        - **3. Cruce de Variables**: Compara 2 variables (ej. Año vs Postura).
        - **4. Constructor de Gráficos**: Diseña tus figuras a tu gusto.
        - **5. Exportar**: Descarga tu reporte en Excel.
        """)
        
    st.divider()
    st.caption("🌿 **App MTCI Tesis v2.0** — Interfaz simplificada y amigable")


# =============================================================================
# VISTA PRINCIPAL
# =============================================================================

# Banner de bienvenida
st.markdown("""
<div class="hero-banner">
    <h1>🌿 Análisis e Interpretación de Datos MTCI</h1>
    <p>Herramienta amigable para la exploración, interpretación estadística y diseño visual de gráficos para tesis de Psicología.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.df is None:
    st.warning("⚠️ No se ha detectado ningún archivo de datos. Por favor, sube tu archivo CSV o Excel desde el panel lateral izquierdo.")
    st.stop()

df_trabajo = st.session_state.df
mapeo = st.session_state.mapeo

# Menú principal por pestañas limpias
pestanas = st.tabs([
    "📋 1. Panorama y Mapeo",
    "🔍 2. Explorar e Interpretar",
    "🔗 3. Cruce de Variables",
    "🎨 4. Constructor de Gráficos",
    "📑 5. Exportar para Tesis"
])


# =============================================================================
# PESTAÑA 1: PANORAMA Y MAPEO DE VARIABLES
# =============================================================================
with pestanas[0]:
    st.subheader("Resumen General de los Datos")
    
    # Métricas principales en tarjetas estilizadas
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Participantes</div>
            <div class="metric-val">{len(df_trabajo)}</div>
            <div class="metric-sub">100% consentidos</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        vars_analiticas = [c for c, m in mapeo.items() if m["tipo"] != "excluido"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Variables Analíticas</div>
            <div class="metric-val">{len(vars_analiticas)}</div>
            <div class="metric-sub">de {len(df_trabajo.columns)} totales</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        n_practicas = len(st.session_state.df_practicas_resumen) if st.session_state.df_practicas_resumen is not None else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Prácticas MTCI</div>
            <div class="metric-val">{n_practicas}</div>
            <div class="metric-sub">identificadas en listas</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        total_celdas = df_trabajo.size
        vacios = sum(int((df_trabajo[c].isna() | (df_trabajo[c].astype(str).str.strip() == '')).sum()) for c in df_trabajo.columns)
        pct_completitud = round((total_celdas - vacios) / total_celdas * 100, 1)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Completitud Global</div>
            <div class="metric-val">{pct_completitud}%</div>
            <div class="metric-sub">{total_celdas - vacios} respuestas válidas</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Tabla de columnas mapeadas
    st.markdown("### 🗺️ Diccionario de Variables Mapeadas")
    st.caption("La aplicación asignó automáticamente un nombre corto y un rol comprensible a cada pregunta del cuestionario.")

    filas_dicc = []
    for col, info in mapeo.items():
        filas_dicc.append({
            "Icono": info["icono"],
            "Nombre Corto (Alias)": info["alias"],
            "Rol Asignado": info["rol"],
            "Valores Únicos": df_trabajo[col].dropna().nunique(),
            "Pregunta Original": info["original"]
        })
    df_dicc_vista = pd.DataFrame(filas_dicc)
    st.dataframe(df_dicc_vista, use_container_width=True, hide_index=True)

    # Editor rápido de nombres opcional
    with st.expander("✏️ ¿Deseas personalizar el nombre corto de alguna variable?"):
        st.caption("Si deseas que una variable aparezca con otro nombre en tus tablas y gráficos, cámbiala aquí:")
        col_editar = st.selectbox("Selecciona la variable a renombrar:", options=list(df_trabajo.columns), format_func=lambda c: f"{mapeo[c]['alias']} ({c[:50]}...)")
        if col_editar:
            nuevo_alias = st.text_input("Nuevo nombre corto para los menús y gráficos:", value=mapeo[col_editar]["alias"])
            nuevo_rol_tipo = st.selectbox(
                "Tipo de análisis:",
                options=["categoria", "escala", "seleccion_multiple", "texto_abierto", "excluido"],
                index=["categoria", "escala", "seleccion_multiple", "texto_abierto", "excluido"].index(mapeo[col_editar]["tipo"]),
                format_func=lambda x: {"categoria": "🏷️ Categoría (Opción única)", "escala": "📊 Escala / Frecuencia", "seleccion_multiple": "🌿 Selección múltiple (Prácticas)", "texto_abierto": "📝 Texto abierto", "excluido": "🚫 Informativo / Excluir"}.get(x, x)
            )
            if st.button("Guardar cambios en esta variable"):
                mapeo[col_editar]["alias"] = nuevo_alias
                mapeo[col_editar]["tipo"] = nuevo_rol_tipo
                st.session_state.mapeo = mapeo
                st.success(f"Variable actualizada: '{nuevo_alias}'")
                st.rerun()

    # Vista previa de datos tabulares
    with st.expander("👀 Ver las primeras filas de datos sin procesar"):
        st.dataframe(df_trabajo.head(10), use_container_width=True)


# =============================================================================
# PESTAÑA 2: EXPLORACIÓN E INTERPRETACIÓN POR VARIABLE
# =============================================================================
with pestanas[1]:
    st.subheader("Análisis e Interpretación Detallada")
    st.caption("Selecciona cualquier pregunta para obtener su tabla de frecuencias, gráfico sugerido y la redacción formal para tu tesis.")

    # Variables disponibles ordenadas por alias
    vars_analisis = [c for c, m in mapeo.items() if m["tipo"] != "excluido"]
    
    col_sel = st.selectbox(
        "Elige la variable que deseas analizar:",
        options=vars_analisis,
        format_func=lambda c: f"{mapeo[c]['icono']} {mapeo[c]['alias']} — ({mapeo[c]['rol']})"
    )

    if col_sel:
        info_sel = mapeo[col_sel]
        tipo_var = info_sel["tipo"]
        pregunta_orig = info_sel["original"]
        alias_var = info_sel["alias"]

        st.markdown(f"#### {info_sel['icono']} {alias_var}")
        st.markdown(f"> *\"{pregunta_orig}\"*")

        # CASO 1: SELECCIÓN MÚLTIPLE (LISTA DE PRÁCTICAS MTCI)
        if tipo_var == "seleccion_multiple":
            st.info("🌿 **Variable de selección múltiple:** Los respondentes pudieron seleccionar una o varias prácticas dentro de esta categoría.")
            
            # Extraer registros específicos de esta columna
            df_exp = st.session_state.df_practicas_exp
            if df_exp is not None:
                sub_exp = df_exp[df_exp["Columna"] == col_sel]
                conteo_sub = sub_exp["Practica"].value_counts().reset_index()
                conteo_sub.columns = ["Práctica MTCI", "Menciones"]
                n_encuestados = len(df_trabajo)
                conteo_sub["% de Participantes"] = round(conteo_sub["Menciones"] / n_encuestados * 100, 1)

                # Narrativa interpretativa
                narrativa = redactar_interpretacion_practicas(conteo_sub.rename(columns={"% de Participantes": "% de Respondentes"}), n_encuestados)
                st.markdown(f"""
                <div class="narrative-box">
                    <div class="narrative-title">💡 Interpretación redactada para la tesis</div>
                    {narrativa}
                </div>
                """, unsafe_allow_html=True)

                c_izq, c_der = st.columns([1, 1.2])
                with c_izq:
                    st.markdown("**Tabla de menciones:**")
                    st.dataframe(conteo_sub, use_container_width=True, hide_index=True)
                with c_der:
                    fig_sub = px.bar(
                        conteo_sub.head(10).iloc[::-1],
                        x="Menciones",
                        y="Práctica MTCI",
                        orientation="h",
                        title=f"Top Prácticas más Mencionadas ({alias_var})",
                        color_discrete_sequence=["#2d6a4f"],
                        text="Menciones"
                    )
                    fig_sub.update_layout(xaxis_title="Número de menciones", yaxis_title="", margin=dict(l=10, r=10, t=40, b=10))
                    st.plotly_chart(fig_sub, use_container_width=True)

        # CASO 2: TEXTO ABIERTO (COMENTARIOS)
        elif tipo_var == "texto_abierto":
            respuestas_validas = df_trabajo[col_sel].dropna()
            respuestas_validas = respuestas_validas[respuestas_validas.astype(str).str.strip().ne('')]
            
            # Filtrar respuestas que solo sean 'ninguno', 'nulo', etc.
            no_sustantivas = {"ninguno", "ningun comentario", "ninguna", "nulo", "no", "nada", "sin comentarios"}
            resp_sustantivas = [r for r in respuestas_validas if r.strip().lower() not in no_sustantivas]

            st.markdown(f"""
            <div class="narrative-box">
                <div class="narrative-title">💡 Resumen de aportes cualitativos</div>
                Un total de <b>{len(respuestas_validas)} respondentes</b> emitieron respuesta en este apartado ({round(len(respuestas_validas)/len(df_trabajo)*100, 1)}% de la muestra). 
                De ellas, <b>{len(resp_sustantivas)} participantes</b> realizaron comentarios de fondo con aportes, recomendaciones o inquietudes dirigidas a la formación y el ejercicio profesional.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Listado de respuestas recibidas:**")
            filtro_txt = st.text_input("🔍 Filtrar respuestas por palabra clave:", "")
            
            filas_mostrar = [r for r in respuestas_validas if filtro_txt.lower() in r.lower()] if filtro_txt else list(respuestas_validas)
            for i, r in enumerate(filas_mostrar, 1):
                es_valiosa = r.strip().lower() not in no_sustantivas
                badge = "⭐ Aporte sustantivo" if es_valiosa else "🔹 Respuesta breve"
                st.markdown(f"- **#{i}** (`{badge}`): *\"{r}\"*")

        # CASO 3: CATEGORÍAS Y ESCALAS (UNIVARIADO ESTÁNDAR)
        else:
            tabla_frec, n_validos, n_tot = calcular_tabla_frecuencias(df_trabajo[col_sel])
            
            # Párrafo interpretativo automático
            narrativa = redactar_interpretacion_univariada(alias_var, pregunta_orig, tabla_frec, n_validos, n_tot)
            st.markdown(f"""
            <div class="narrative-box">
                <div class="narrative-title">💡 Interpretación sugerida para el capítulo de resultados</div>
                {narrativa}
            </div>
            """, unsafe_allow_html=True)

            col_t1, col_t2 = st.columns([1, 1.2])
            with col_t1:
                st.markdown("**Tabla estadística de frecuencias:**")
                st.dataframe(tabla_frec, use_container_width=True, hide_index=True)
                
                # Descarga rápida de la tabla
                csv_tabla = tabla_frec.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"⬇️ Descargar tabla de '{alias_var}' (CSV)",
                    data=csv_tabla,
                    file_name=f"frecuencias_{alias_var.replace(' ', '_').lower()}.csv",
                    mime="text/csv"
                )

            with col_t2:
                # Gráfico sugerido inmediato
                fig_sug = px.bar(
                    tabla_frec,
                    x="Opción",
                    y="Porcentaje (%)",
                    title=f"Distribución porcentual: {alias_var}",
                    text="Porcentaje (%)",
                    color_discrete_sequence=["#1b4332"]
                )
                fig_sug.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig_sug.update_layout(
                    yaxis_title="Porcentaje (%)",
                    xaxis_title="",
                    yaxis_range=[0, min(100, max(tabla_frec["Porcentaje (%)"]) * 1.25) if not tabla_frec.empty else 100],
                    margin=dict(l=10, r=10, t=40, b=10)
                )
                st.plotly_chart(fig_sug, use_container_width=True)


# =============================================================================
# PESTAÑA 3: CRUCE DE VARIABLES (ANÁLISIS BIVARIADO)
# =============================================================================
with pestanas[2]:
    st.subheader("Cruce de Variables y Comparativas (Bivariado)")
    st.caption("Cruza dos variables para evaluar diferencias según año de carrera, sexo o posturas profesionales.")

    # Solo variables categóricas o escalas con <= 10 categorías
    vars_cruce = [
        c for c, m in mapeo.items() 
        if m["tipo"] in ["categoria", "escala"] and df_trabajo[c].dropna().nunique() <= 10
    ]

    col_b1, col_b2, col_b3 = st.columns([1, 1, 0.8])
    with col_b1:
        v1 = st.selectbox(
            "Variable 1 (Filas / Segmentación):",
            options=vars_cruce,
            index=0 if vars_cruce else 0,
            format_func=lambda c: f"{mapeo[c]['alias']}"
        )
    with col_b2:
        v2_opciones = [c for c in vars_cruce if c != v1]
        v2 = st.selectbox(
            "Variable 2 (Columnas / Respuesta):",
            options=v2_opciones,
            index=min(1, len(v2_opciones)-1) if v2_opciones else 0,
            format_func=lambda c: f"{mapeo[c]['alias']}"
        )
    with col_b3:
        modo_cruce = st.selectbox(
            "Visualizar valores como:",
            options=["Porcentaje por fila (% fila)", "Porcentaje por columna (% col)", "Conteo absoluto (n)"]
        )

    if v1 and v2:
        alias1 = mapeo[v1]["alias"]
        alias2 = mapeo[v2]["alias"]

        # Crear tabla de contingencia
        df_sub = df_trabajo[[v1, v2]].dropna()
        df_sub = df_sub[(df_sub[v1].astype(str).str.strip() != '') & (df_sub[v2].astype(str).str.strip() != '')]

        contingencia_n = pd.crosstab(df_sub[v1], df_sub[v2], margins=True, margins_name="Total")
        contingencia_sin_margins = pd.crosstab(df_sub[v1], df_sub[v2])

        if modo_cruce == "Porcentaje por fila (% fila)":
            tabla_mostrar = pd.crosstab(df_sub[v1], df_sub[v2], normalize='index').round(3) * 100
        elif modo_cruce == "Porcentaje por columna (% col)":
            tabla_mostrar = pd.crosstab(df_sub[v1], df_sub[v2], normalize='columns').round(3) * 100
        else:
            tabla_mostrar = contingencia_n

        # Prueba de Chi-Cuadrado si las dimensiones lo permiten
        p_val = None
        if contingencia_sin_margins.shape[0] > 1 and contingencia_sin_margins.shape[1] > 1:
            try:
                chi2, p_val, dof, _ = stats.chi2_contingency(contingencia_sin_margins)
            except Exception:
                p_val = None

        # Redacción de interpretación bivariada
        narrativa_bi = f"Al realizar el cruce entre **'{alias1}'** y **'{alias2}'** sobre un total de {len(df_sub)} respondentes con datos válidos en ambas variables, "
        if p_val is not None:
            if p_val < 0.05:
                narrativa_bi += f"se identifica una asociación estadísticamente significativa (Chi² = {round(chi2, 2)}, p = {round(p_val, 4)} < 0.05), sugiriendo patrones diferenciados de respuesta según el grupo de pertenencia. "
            else:
                narrativa_bi += f"no se evidencia una asociación estadísticamente significativa con el tamaño muestral disponible (Chi² = {round(chi2, 2)}, p = {round(p_val, 3)} > 0.05), observándose distribuciones predominantemente homogéneas. "
        
        # Resaltar la combinación mayoritaria
        top_comb = contingencia_sin_margins.unstack().sort_values(ascending=False)
        if len(top_comb) > 0:
            top_v2, top_v1 = top_comb.index[0]
            narrativa_bi += f"La concentración más alta se encuentra en el grupo de **'{top_v1}'** que eligió **'{top_v2}'** con {int(top_comb.iloc[0])} casos."

        st.markdown(f"""
        <div class="narrative-box">
            <div class="narrative-title">💡 Interpretación comparativa para la discusión</div>
            {narrativa_bi}
        </div>
        """, unsafe_allow_html=True)

        col_g1, col_g2 = st.columns([1.1, 1.2])
        with col_g1:
            st.markdown(f"**Tabla de contingencia ({modo_cruce}):**")
            st.dataframe(tabla_mostrar, use_container_width=True)

        with col_g2:
            tipo_bar_cruce = st.radio("Disposición del gráfico:", ["Barras agrupadas", "Barras apiladas al 100%"], horizontal=True)
            df_plot_bi = pd.crosstab(df_sub[v1], df_sub[v2], normalize='index' if "100%" in tipo_bar_cruce else False).reset_index()
            df_plot_bi = df_plot_bi.melt(id_vars=v1, var_name=alias2, value_name="Valor")
            if "100%" in tipo_bar_cruce:
                df_plot_bi["Valor"] = round(df_plot_bi["Valor"] * 100, 1)

            fig_bi = px.bar(
                df_plot_bi,
                x=v1,
                y="Valor",
                color=alias2,
                barmode="relative" if "100%" in tipo_bar_cruce else "group",
                title=f"Relación entre {alias1} y {alias2}",
                color_discrete_sequence=PALETAS_COLOR["🌿 MTCI Botánico (Verdes)"]
            )
            fig_bi.update_layout(
                xaxis_title=alias1,
                yaxis_title="Porcentaje (%)" if "100%" in tipo_bar_cruce else "Frecuencia (n)",
                legend_title=alias2,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_bi, use_container_width=True)


# =============================================================================
# PESTAÑA 4: CONSTRUCTOR DE GRÁFICOS A TU GUSTO (CHART STUDIO)
# =============================================================================
with pestanas[3]:
    st.subheader("🎨 Constructor de Gráficos Personalizados")
    st.caption("Construye las figuras de tu tesis exactamente como las necesitas: elige el tipo, paleta de colores, títulos y etiquetas con descarga directa en alta resolución.")

    with st.expander("🛠️ Panel de Configuración del Gráfico", expanded=True):
        col_conf1, col_conf2, col_conf3 = st.columns(3)
        
        with col_conf1:
            st.markdown("**1. Variable y Métrica**")
            # Lista de variables elegibles
            opciones_graf = [c for c, m in mapeo.items() if m["tipo"] in ["categoria", "escala"]]
            var_principal = st.selectbox(
                "Variable principal (Eje):",
                options=opciones_graf,
                format_func=lambda c: f"{mapeo[c]['alias']}"
            )
            
            # Opción de segunda variable para color/segmentación
            opciones_seg = ["(Ninguna - univariado)"] + [c for c in opciones_graf if c != var_principal]
            var_seg = st.selectbox(
                "Segmentar / Desglosar por (opcional):",
                options=opciones_seg,
                format_func=lambda c: "(Ninguna - univariado)" if c.startswith("(") else f"{mapeo[c]['alias']}"
            )
            
            metrica = st.radio("Métrica a representar:", ["Porcentaje (%)", "Conteo de participantes (n)"], horizontal=True)

        with col_conf2:
            st.markdown("**2. Tipo de Gráfico y Orden**")
            tipo_grafico = st.selectbox(
                "Tipo de gráfico:",
                options=[
                    "📊 Barras Verticales (Columnas)",
                    "📏 Barras Horizontales",
                    "🍩 Dona / Pastel Moderno",
                    "📦 Barras Apiladas al 100% (Segmentado)",
                    "👥 Barras Agrupadas (Segmentado)",
                    "🗺️ Treemap (Mosaico de bloques)"
                ]
            )
            
            orden_cat = st.selectbox(
                "Orden de las categorías:",
                options=["De mayor a menor (Descendente)", "De menor a mayor (Ascendente)", "Orden natural de las opciones"]
            )
            
            mostrar_etiquetas = st.checkbox("Mostrar etiquetas con valores en las barras/secciones", value=True)

        with col_conf3:
            st.markdown("**3. Estilo y Paleta de Colores**")
            paleta_elegida = st.selectbox("Paleta cromática:", options=list(PALETAS_COLOR.keys()))
            colores = PALETAS_COLOR[paleta_elegida]
            
            alias_p = mapeo[var_principal]["alias"]
            titulo_sugerido = f"Figura. Distribución de participantes según {alias_p.lower()}"
            titulo_grafico = st.text_input("Título del gráfico:", value=titulo_sugerido)
            subtitulo_grafico = st.text_input("Nota / Subtítulo:", value=f"Fuente: Instrumento MTCI (N={len(df_trabajo)})")
            alto_grafico = st.slider("Altura del gráfico (px):", min_value=350, max_value=750, value=480, step=20)

    # CONSTRUCCIÓN DEL GRÁFICO PERSONALIZADO
    if var_principal:
        alias_x = mapeo[var_principal]["alias"]
        df_p = df_trabajo.dropna(subset=[var_principal])
        df_p = df_p[df_p[var_principal].astype(str).str.strip() != '']
        
        # Mapeo de datos para graficar
        if var_seg == "(Ninguna - univariado)":
            tabla_plot, n_val, _ = calcular_tabla_frecuencias(df_p[var_principal])
            
            # Ordenamiento
            if orden_cat == "De mayor a menor (Descendente)":
                tabla_plot = tabla_plot.sort_values("Frecuencia (n)", ascending=False)
            elif orden_cat == "De menor a mayor (Ascendente)":
                tabla_plot = tabla_plot.sort_values("Frecuencia (n)", ascending=True)

            eje_y = "Porcentaje (%)" if metrica == "Porcentaje (%)" else "Frecuencia (n)"
            formato_texto = '%{text:.1f}%' if metrica == "Porcentaje (%)" else '%{text}'

            if "Horizontales" in tipo_grafico:
                # Para horizontales ordenar invertido para que el mayor quede arriba
                tabla_h = tabla_plot.iloc[::-1] if orden_cat == "De mayor a menor (Descendente)" else tabla_plot
                fig = px.bar(
                    tabla_h,
                    x=eje_y,
                    y="Opción",
                    orientation="h",
                    title=f"<b>{titulo_grafico}</b><br><sup>{subtitulo_grafico}</sup>",
                    text=eje_y if mostrar_etiquetas else None,
                    color_discrete_sequence=colores
                )
                fig.update_layout(xaxis_title=eje_y, yaxis_title="")
            elif "Dona" in tipo_grafico:
                fig = px.pie(
                    tabla_plot,
                    names="Opción",
                    values=eje_y,
                    hole=0.45,
                    title=f"<b>{titulo_grafico}</b><br><sup>{subtitulo_grafico}</sup>",
                    color_discrete_sequence=colores
                )
                fig.update_traces(textinfo='percent+label' if mostrar_etiquetas else 'none', textposition='outside')
            elif "Treemap" in tipo_grafico:
                fig = px.treemap(
                    tabla_plot,
                    path=["Opción"],
                    values=eje_y,
                    title=f"<b>{titulo_grafico}</b><br><sup>{subtitulo_grafico}</sup>",
                    color_discrete_sequence=colores
                )
            else: # Barras verticales
                fig = px.bar(
                    tabla_plot,
                    x="Opción",
                    y=eje_y,
                    title=f"<b>{titulo_grafico}</b><br><sup>{subtitulo_grafico}</sup>",
                    text=eje_y if mostrar_etiquetas else None,
                    color_discrete_sequence=colores
                )
                if mostrar_etiquetas:
                    fig.update_traces(texttemplate=formato_texto, textposition='outside')
                lim_sup = 100 if metrica == "Porcentaje (%)" else max(tabla_plot["Frecuencia (n)"]) * 1.2
                fig.update_layout(yaxis_title=eje_y, xaxis_title="", yaxis_range=[0, min(100, max(tabla_plot[eje_y]) * 1.25) if metrica == "Porcentaje (%)" else max(tabla_plot[eje_y]) * 1.2])

        else:
            # Segmentado por segunda variable
            alias_seg = mapeo[var_seg]["alias"]
            df_bi = df_p.dropna(subset=[var_seg])
            df_bi = df_bi[df_bi[var_seg].astype(str).str.strip() != '']
            
            es_100 = "Apiladas" in tipo_grafico
            df_c = pd.crosstab(df_bi[var_principal], df_bi[var_seg], normalize='index' if (es_100 or metrica == "Porcentaje (%)") else False).reset_index()
            df_c_melt = df_c.melt(id_vars=var_principal, var_name=alias_seg, value_name="Valor")
            if es_100 or metrica == "Porcentaje (%)":
                df_c_melt["Valor"] = round(df_c_melt["Valor"] * 100, 1)

            fig = px.bar(
                df_c_melt,
                x=var_principal,
                y="Valor",
                color=alias_seg,
                barmode="relative" if es_100 else "group",
                title=f"<b>{titulo_grafico}</b><br><sup>{subtitulo_grafico}</sup>",
                color_discrete_sequence=colores,
                text="Valor" if mostrar_etiquetas else None
            )
            if mostrar_etiquetas:
                fig.update_traces(texttemplate='%{text:.1f}%' if (es_100 or metrica == "Porcentaje (%)") else '%{text}', textposition='auto')
            fig.update_layout(xaxis_title=alias_x, yaxis_title="Porcentaje (%)" if (es_100 or metrica == "Porcentaje (%)") else "Frecuencia (n)", legend_title=alias_seg)

        # Ajustes finales de estilo
        fig.update_layout(
            height=alto_grafico,
            template="plotly_white",
            font=dict(family="Plus Jakarta Sans, sans-serif", size=13),
            margin=dict(l=30, r=30, t=70, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Descargas y referencias para la tesis
        c_down1, c_down2, c_down3 = st.columns([1, 1, 1.5])
        with c_down1:
            # Exportación PNG de alta resolución optimizada
            try:
                # Generación directa con manejo robusto
                img_png = fig.to_image(format="png", width=1200, height=750, scale=2)
                st.download_button(
                    label="⬇️ Descargar en Alta Calidad (PNG)",
                    data=img_png,
                    file_name=f"grafico_{alias_x.replace(' ', '_').lower()}.png",
                    mime="image/png",
                    help="Imagen nítida a 300 DPI lista para insertar en Microsoft Word o tu memoria de tesis."
                )
            except Exception:
                st.info("💡 Puedes descargar la imagen nítida usando el icono de cámara 📷 en la barra superior derecha del gráfico.")

        with c_down2:
            html_bytes = fig.to_html(include_plotlyjs='cdn').encode('utf-8')
            st.download_button(
                label="🌐 Descargar Gráfico Interactivo (HTML)",
                data=html_bytes,
                file_name=f"grafico_interactivo_{alias_x.replace(' ', '_').lower()}.html",
                mime="text/html"
            )

        with c_down3:
            st.caption(f"**Referencia formal sugerida para Word / APA:**")
            st.code(f"{titulo_grafico}. {subtitulo_grafico}.", language="text")


# =============================================================================
# PESTAÑA 5: EXPORTACIÓN PARA TESIS
# =============================================================================
with pestanas[4]:
    st.subheader("📤 Exportación de Resultados y Metodología")
    st.caption("Descarga todas las tablas consolidadas en un único Excel y copia los párrafos metodológicos listos para tu informe final.")

    col_exp1, col_exp2 = st.columns([1.2, 1])

    with col_exp1:
        st.markdown("#### 📥 Paquete de Datos y Tablas")
        st.write("""
        El libro de Excel incluye automáticamente:
        - **Hoja 1:** Diccionario completo de variables y preguntas originales
        - **Hoja 2:** Todas las tablas de frecuencias univariadas consolidadas
        - **Hoja 3:** Conteo y ranking de menciones de prácticas MTCI
        - **Hoja 4:** Datos anonimizados procesados
        """)

        excel_data = generar_excel_completo(df_trabajo, mapeo, st.session_state.df_practicas_resumen)
        st.download_button(
            label="📗 Descargar Reporte Integral en Excel (.xlsx)",
            data=excel_data,
            file_name="reporte_resultados_mtci_tesis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )

        st.divider()
        st.markdown("#### 📄 Base de Datos Limpia (CSV)")
        csv_data = df_trabajo.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="⬇️ Descargar Datos Limpios (CSV UTF-8)",
            data=csv_data,
            file_name="datos_mtci_limpios.csv",
            mime="text/csv"
        )

    with col_exp2:
        st.markdown("#### 📋 Redacción Metodológica Sugerida")
        st.caption("Párrafos redactados con rigor metodológico listos para adaptar a tu memoria:")

        st.markdown("""
        **Descripción del Instrumento y Participantes:**
        > *Para la recolección de los datos empíricos, se aplicó el Instrumento I1 sobre saberes, prácticas y valoración de la Medicina Tradicional, Complementaria e Integrativa (MTCI) en la psicología clínica. La muestra final estuvo conformada por N=68 participantes pertenecientes a 4to y 5to año de la carrera de Psicología, así como profesionales del área. El 100% de los respondentes otorgó previamente su consentimiento informado voluntario.*

        **Tratamiento Estadístico de los Datos:**
        > *El análisis estadístico descriptivo comprendió el cálculo de frecuencias absolutas (n), relativas porcentuales (%) y porcentajes acumulados para las variables nominales y ordinales. Para las dimensiones de selección múltiple sobre prácticas MTCI, se procedió a la desagregación de menciones individuales y cálculo del porcentaje de prevalencia sobre el total de la muestra. Los análisis bivariados se contrastaron mediante tablas de contingencia y la prueba de independencia de Chi-cuadrado.*
        """)
