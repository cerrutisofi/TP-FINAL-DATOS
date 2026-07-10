import streamlit as st
import requests
import pandas as pd
from graficos import grafico_probabilidad, grafico_categoria
from estilos import cargar_estilos

cargar_estilos()

# Verificamos si el usuario inició sesión
if not st.session_state.get("logueado", False):
    st.error("🚨 Debe iniciar sesión para acceder a esta página.")
    st.switch_page("pages/login.py")
    st.stop()

# Recuperamos los datos guardados durante el login
URL_API_BASE = st.session_state["url_api"]

API_KEY = st.session_state["api_key"]

credenciales = {
    "x-api-key": API_KEY
}

st.sidebar.title("👤 Sesión")

st.sidebar.success("Conectado")

st.sidebar.write("URL de la API")
st.sidebar.code(URL_API_BASE)

st.sidebar.success("API Key verificada")

st.sidebar.divider()

if st.sidebar.button("Cerrar sesión"):
    st.session_state.clear()
    st.switch_page("pages/login.py")

# Visualización de la página principal, donde se hace todo el trabajo
st.set_page_config(
    page_title="ViLo Propone",
    page_icon="logo-mvl.png"
)

col1, col2 = st.columns([2, 6])
with col1:
    st.image("logo_pp.jpg", width=200)
with col2:
    st.title("Predicción de proyectos nuevos")

st.markdown(
    "Sistema de predicción de nuevos proyectos del presupuesto participativo de Vicente López"
)
# 3. Obtenemos las localidades disponibles desde la API (censo 2022)
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
# 5. El Botón de Acción
if st.button("Predecir viabilidad"):
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
                st.success(f"✅ Predicción: **{resultado['etiqueta']}**")
            else:
                st.warning(f"⚠️ Predicción: **{resultado['etiqueta']}**")

            st.metric("Probabilidad de éxito", f"{resultado['probabilidad']:.1%}")
            st.progress(resultado["probabilidad"])

        elif respuesta.status_code == 401:
            st.error("🚨 Acceso Denegado. Verifique su API Key.")
        elif respuesta.status_code == 400:
            st.error(f"🚨 {respuesta.json().get('detail', 'Datos inválidos.')}")
        else:
            st.error(f"🚨 Error en el servidor: {respuesta.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("🚨 No se pudo conectar al Backend. ¿Está encendida la API?")

# 6. Histórico de predicciones
st.subheader("📊 Histórico de proyectos evaluados")
if st.button("Actualizar histórico"):
    try:
        respuesta = requests.get(f"{URL_API_BASE}/historico", headers=credenciales, timeout=10)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if datos:
                df_historico = pd.DataFrame(datos)
                st.dataframe(df_historico, use_container_width=True)

                st.subheader("Probabilidad de éxito por proyecto")
                fig = grafico_probabilidad(df_historico)
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("Todavía no hay proyectos evaluados.")
        elif respuesta.status_code == 401:
            st.error("🚨 Acceso Denegado. Verifique su API Key.")
        else:
            st.error(f"🚨 Error en el servidor: {respuesta.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("🚨 No se pudo conectar al Backend. ¿Está encendida la API?")