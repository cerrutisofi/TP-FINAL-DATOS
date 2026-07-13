# Esta sección es de acceso público. Muestra gráficos hechos a partir de datos históricos. Para facilitar la toma de decisiones
import streamlit as st
import pandas as pd
from graficos import(grafico_categoria_localidad, grafico_presupuesto, grafico_localidad, grafico_categorias)
from estilos import cargar_estilos
from pathlib import Path

st.title("📊 Dashboard de análisis histórico")
st.markdown("Análisis histórico a partir de los proyectos presentados en el presupuesto participativo de Vicente López (2013-2025)")

# Cargamos el CSV histórico
@st.cache_data
def cargar_datos():

    BASE_DIR = Path(__file__).resolve().parents[3]

    ruta_csv = (
        BASE_DIR
        / "DATOS"
        / "Datos procesados"
        / "dataset_final_vilo.csv"
    )

    df = pd.read_csv(ruta_csv, sep =";")
    return df


df = cargar_datos()

# Gráfico 1: porcentaje de aprobación de cada categoría en cada localidad
st.subheader("Aprobación de proyectos por localidad y por categoría")

fig1 = grafico_categoria_localidad(df)

st.plotly_chart(
    fig1,
    use_container_width=True
)

#Grafico 2: Presupuesto promedio por categoría
st.subheader("Presupuesto")

fig2 = grafico_presupuesto(df)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# Gráfico 3: Proyectos aprobados por localidad
st.subheader("Localidades")

fig = grafico_localidad(df)

st.plotly_chart(fig, use_container_width=True)

# Gráfico 4: Categorías más arpobadas, de mayor a menor
st.subheader("Categorías")

fig = grafico_categorias(df)

st.plotly_chart(fig, use_container_width=True)