import streamlit as st

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False
    
login = st.Page("pages/login.py", title="Iniciar sesión")
principal = st.Page("pages/principal.py", title= "Predicción de nuevo proyecto")
analisis = st.Page("pages/analisis.py", title="Análisis histórico")
pg = st.navigation([login, principal, analisis])
pg.run()