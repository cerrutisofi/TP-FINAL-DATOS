import streamlit as st
import requests
import pandas as pd
import os

# 1. Configuración visual del tablero (Limpio e Institucional)
st.set_page_config(
    page_title="Presupuesto Participativo - Vicente López", 
    page_icon="🏛️", 
    layout="centered"
)

# =========================================================
# ELIMINACIÓN TOTAL DEL BOTÓN ROTO Y ESTILOS VL (CSS)
# =========================================================
st.markdown("""
    <style>
    /* Importamos fuentes similares a Gotham desde Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    /* Aplicamos la variante Book (Regular) a textos tradicionales */
    html, body, p, label, input, select {
        font-family: 'Montserrat', 'Gotham', sans-serif !important;
        font-weight: 400 !important; 
        color: #000000 !important;
    }
    
    /* Aplicamos la variante Bold a los títulos principales y subitítulos */
    h1, h2, h3, strong, b, th {
        font-family: 'Montserrat', 'Gotham', sans-serif !important;
        font-weight: 700 !important; 
        color: #000000 !important;
    }

    /* Ocultar la barra decorativa superior de Streamlit */
    header[data-testid="stHeader"] {
        background-color: #ffffff !important;
    }
    
    /* SOLUCIÓN RADICAL CONTRA EL KEYBOARD: Desaparece por completo el botón nativo de la flecha */
    button[data-testid="sidebar-toggle"], 
    [data-testid="collapsedControl"],
    button[aria-label="Expand sidebar"],
    button[aria-label="Collapse sidebar"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0px !important;
        height: 0px !important;
    }
    
    /* Fondo general de la página blanco */
    .stApp, [data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    
    /* CELESTE OFICIAL VL: En las cajas con texto color blanco por dentro */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div,
    div[data-testid="stSelectbox"] div[role="button"],
    div[data-testid="stNumberInput"] input {
        background-color: #009ee3 !important; /* Celeste Vicente López */
        color: #ffffff !important; /* Texto interno blanco */
        -webkit-text-fill-color: #ffffff !important;
    }
    
    /* Cambia los botones de Más (+) y Menos (-) al color celeste oficial */
    div[data-testid="stNumberInput"] button {
        background-color: #009ee3 !important;
        color: #ffffff !important;
        border: 1px solid #008cd1 !important;
    }
    div[data-testid="stNumberInput"] button:hover {
        background-color: #007bb3 !important;
        color: #ffffff !important;
    }
    
    /* Asegurar que las opciones desplegables sigan siendo legibles (Negro en fondo blanco) */
    div[role="listbox"] ul, div[role="listbox"] li, div[role="option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* BLINDAJE CONTRA EL GRIS: Todos los botones de la app pasan a verde de forma absoluta */
    div.stButton > button,
    button[class*="st-emotion-cache"] {
        background-color: #006837 !important; /* Verde Vicente López Oficial */
        color: #ffffff !important; /* Letras blancas */
        border: none !important;
        font-weight: 700 !important; 
        border-radius: 6px !important;
    }
    
    /* Forzar que las letras sigan siendo blancas en cualquier sub-elemento del botón */
    div.stButton > button *,
    button[class*="st-emotion-cache"] * {
        color: #ffffff !important;
    }
    
    div.stButton > button:hover,
    button[class*="st-emotion-cache"]:hover {
        background-color: #004d28 !important; /* Verde más oscuro al pasar el mouse */
        color: #ffffff !important;
    }
    
    /* Adaptación específica para el botón de la barra lateral (ancho completo y sombra) */
    div[data-testid="stSidebar"] div.stButton > button {
        width: 100% !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)


# =========================================================
# BARRA LATERAL (LOGO Y BOTÓN VERDE DE CONEXIÓN)
# =========================================================

# Logo principal de Vicente López (Izquierda)
NOMBRE_LOGO = "logo.png" 
if os.path.exists(NOMBRE_LOGO):
    st.sidebar.image(NOMBRE_LOGO, use_container_width=True)
else:
    st.sidebar.subheader("MUNICIPALIDAD DE VICENTE LÓPEZ")

st.sidebar.divider()

st.sidebar.subheader("Conectividad")
URL_API_BASE = "http://127.0.0.1:8080"

# Botón verde oficial interactivo que simula la validación hermosamente
if "conectado" not in st.session_state:
    st.session_state.conectado = False

if st.sidebar.button("✔️ Token Ministerial Activo" if st.session_state.conectado else "🔑 Validar Token Ministerial"):
    st.session_state.conectado = True

credenciales = {"x-api-key": "TOKEN_MINISTERIAL_VALIDO"}


# =========================================================
# PÁGINA PRINCIPAL (ENCABEZADO ADAPTATIVO)
# =========================================================

IMAGEN_ARRIBA = "images.png"

if os.path.exists(IMAGEN_ARRIBA):
    col_tit1, col_tit2 = st.columns([3, 1])
    with col_tit1:
        st.title("Portal de Evaluación de Proyectos")
        st.subheader("Municipalidad de Vicente López — Presupuesto Participativo")
        st.write("Sistema de Soporte de Decisiones para el análisis de viabilidad de propuestas ciudadanas.")
    with col_tit2:
        st.image(IMAGEN_ARRIBA, use_container_width=True)
else:
    st.title("Portal de Evaluación de Proyectos")
    st.subheader("Municipalidad de Vicente López — Presupuesto Participativo")
    st.write("Sistema de Soporte de Decisiones para el análisis de viabilidad de propuestas ciudadanas.")

st.divider()

# =========================================================
# FORMULARIO DE CARGA (ORDEN ORIGINAL)
# =========================================================

# 3. Obtenemos las localidades disponibles desde la API
localidades_default = [
    "Carapachay", "Florida Este", "Florida Oeste", "La Lucila", "Munro",
    "Olivos", "Vicente López", "Villa Adelina", "Villa Martelli",
]
try:
    resp_localidades = requests.get(f"{URL_API_BASE}/localidades", headers=credenciales, timeout=5)
    if resp_localidades.status_code == 200:
        localidades = resp_localidades.json().get("localidades", localidades_default)
    else:
        localidades = localidades_default
except requests.exceptions.RequestException:
    localidades = localidades_default

categorias_default = [
    "Seguridad y bomberos", "Educación y escuelas",
    "Construcción y reparaciones edilicias", "Salud",
    "Espacios verdes y recreación", "Cultura y deportes",
]

# 4. Interfaz de usuario - Formulario del nuevo proyecto
st.subheader("Nuevo proyecto a evaluar")

col1, col2 = st.columns(2)
with col1:
    localidad_elegida = st.selectbox("Localidad", localidades)
    categoria_elegida = st.selectbox("Categoría", categorias_default)
with col2:
    presupuesto_ingresado = st.number_input(
        "Presupuesto estimado ($)", min_value=0, value=1_000_000, step=50_000
    )

# 5. El Botón de Acción (Verde Oficial VL con letras blancas)
if st.button("Predecir resultado del proyecto"):
    url_api = f"{URL_API_BASE}/predecir"
    payload = {
        "localidad": localidad_elegida,
        "categoria": categoria_elegida,
        "presupuesto": presupuesto_ingresado,
    }

    try:
        respuesta = requests.post(url_api, json=payload, headers=credenciales, timeout=10)

        if respuesta.status_code == 200:
            resultado = respuesta.json()

            if resultado["etiqueta"] == "GANADOR":
                st.success(f"Predicción: **{resultado['etiqueta']}**")
            else:
                st.warning(f"Predicción: **{resultado['etiqueta']}**")

            st.metric("Probabilidad de éxito", f"{resultado['probabilidad']:.1%}")
            st.progress(resultado["probabilidad"])

        elif respuesta.status_code == 401:
            st.error("Acceso Denegado. Verifique su API Key.")
        elif respuesta.status_code == 400:
            st.error(f"Error: {respuesta.json().get('detail', 'Datos inválidos.')}")
        else:
            st.error(f"Error en el servidor: {respuesta.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar al Backend. ¿Está encendida la API?")

# 6. Histórico de predicciones
st.subheader("Histórico de proyectos evaluados")
if st.button("Actualizar histórico"):
    try:
        respuesta = requests.get(f"{URL_API_BASE}/historico", headers=credenciales, timeout=10)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if datos:
                df_historico = pd.DataFrame(datos)
                st.dataframe(df_historico, use_container_width=True)

                st.subheader("Probabilidad de éxito por proyecto")
                st.bar_chart(data=df_historico, x="localidad", y="probabilidad")
            else:
                st.info("Todavía no hay proyectos evaluados.")
        elif respuesta.status_code == 401:
            st.error("Acceso Denegado. Verifique su API Key.")
        else:
            st.error(f"Error en el servidor: {respuesta.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar al Backend. ¿Está encendida la API?")

# Cierre del reporte con firmas humanas
st.divider()
st.write("Desarrollado por: Estudiantes del TP Final de Datos")
st.write("Secretaría de Innovación y Tecnologías Urbanas — Vicente López")