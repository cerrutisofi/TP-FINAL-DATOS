# Acá definimos el estilo de la letra y los colores para el FRONTEND
import streamlit as st

def cargar_estilos():
    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    html, body, p, label, input, select {
        font-family: 'Montserrat', 'Gotham', sans-serif !important;
        font-weight: 400 !important; 
        color: #000000 !important;
    }

    h1, h2, h3, strong, b, th {
        font-family: 'Montserrat', 'Gotham', sans-serif !important;
        font-weight: 700 !important; 
        color: #000000 !important;
    }

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