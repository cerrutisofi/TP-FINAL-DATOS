import streamlit as st
import requests
from estilos import cargar_estilos

cargar_estilos()


col1, col2 = st.columns([2, 6])
with col1:
    st.image("logo-mvl.png", width=200)
with col2:
    st.title("Iniciar sesión")

st.markdown("Bienvenid@ a ViLo Propone, un sistema de predicción de viabilidad de nuevos proyectos para el presupuesto participativo del municipio.")

URL_API_BASE = st.text_input(
    "URL de la API",
    value="http://127.0.0.1:8080"
)
st.subheader("Clave (API Key)")
API_KEY = st.text_input(
    "Para comenzar necesitamos que ingreses la clave:",
    type="password"
)

if st.button("Ingresar"):

    credenciales = {
        "x-api-key": API_KEY
    }

    try:
        respuesta = requests.post(
            f"{URL_API_BASE}/login",
            headers=credenciales,
            timeout=10
        )

        if respuesta.status_code == 200:

            st.session_state["logueado"] = True
            st.session_state["api_key"] = API_KEY
            st.session_state["url_api"] = URL_API_BASE

            st.success("✅ Login exitoso")
            st.switch_page("pages/principal.py")

        elif respuesta.status_code == 401:
            st.error("🚨 API Key incorrecta.")

        else:
            st.error("🚨 Error del servidor.")

    except requests.exceptions.ConnectionError:
        st.error("🚨 No se pudo conectar con la API.")