# Acá creamos los gráficos que luego serán utilizados en analisis.py
import plotly.express as px
import streamlit as st
import pandas as pd

#Gráfico 1: porcentaje de proyectos aprobados por categoría en cada localidad
def grafico_categoria_localidad(df):
    resumen = (
        df.groupby(
            ["Localidades", "Categoria"]
        )["Ganador_bin"]
        .mean()
        .reset_index()
    )

    resumen["Porcentaje_aprobacion"] = (
        resumen["Ganador_bin"] * 100
    )


    fig = px.bar(
        resumen,
        x="Localidades",
        y="Porcentaje_aprobacion",
        color="Categoria",
        barmode="group",
        title="Porcentaje de  proyectos aprobados localidad y categoría",
        labels={
            "Localidades": "Localidad",
            "Porcentaje_aprobacion": "% de aprobación",
            "Categoria": "Categoría"
        }
    )

    fig.update_layout(
        yaxis_range=[0,100]
    )

    return fig

# Gráfico 2: presupuesto promedio de los proyectos ganadores para cada categoría
def grafico_presupuesto(df):

    # Usamos los proyectos ganadores (esto se repite en los próximos gráficos)
    ganadores = df[df["Ganador_bin"] == 1]

    # Promedio de presupuesto por categoría
    presupuesto_promedio = (
        ganadores.groupby("Categoria")["Presupuesto"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        presupuesto_promedio,
        x="Categoria",
        y="Presupuesto",
        title="Presupuesto promedio de proyectos ganadores por categoría",
        labels={
            "Categoria": "Categoría",
            "Presupuesto": "Presupuesto promedio ($)"
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )
    fig.update_traces(marker_color="#006837")
    return fig

# Gráfico 3: Proyectos aprobados por localidad
def grafico_localidad(df):

    ganadores = df[df["Ganador_bin"] == 1]

    resumen = (
        ganadores.groupby("Localidades")
        .size()
        .reset_index(name="Cantidad")
        .sort_values("Cantidad", ascending=False)
    )

    fig = px.bar(
        resumen,
        x="Localidades",
        y="Cantidad",
        title="Cantidad de proyectos aprobados por localidad",
        labels={
            "Localidades": "Localidad",
            "Cantidad": "Proyectos aprobados"
        }
    )
    fig.update_traces(marker_color="#009ee3")
    return fig

# Gráfico 4: Categorías más aprobadas de mayor a menor
def grafico_categorias(df):
    ganadores = df[df["Ganador_bin"] == 1]

    resumen = (
        ganadores.groupby("Categoria")
        .size()
        .reset_index(name="Cantidad")
        .sort_values("Cantidad", ascending=False)
    )

    fig = px.bar(
        resumen,
        x="Cantidad",
        y="Categoria",
        orientation="h",
        title="Cantidad de proyectos aprobados por categoría",
        labels={
            "Cantidad": "Proyectos aprobados",
            "Categoria": "Categoría"
        },
        category_orders={
        "Categoria": resumen["Categoria"].tolist()
        }
    )
    fig.update_traces(marker_color="#6F2DBD")
    return fig