import plotly.express as px


def grafico_probabilidad(df):
    fig = px.bar(
        df,
        x="localidad",
        y="probabilidad",
        color="etiqueta",
        title="Probabilidad de éxito por proyecto",
        labels={
            "localidad": "Localidad",
            "probabilidad": "Probabilidad"
        }
    )

    fig.update_layout(
        xaxis_title="Localidad",
        yaxis_title="Probabilidad"
    )

    return fig


def grafico_categoria(df):
    resumen = (
        df.groupby("categoria")
        ["probabilidad"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        resumen,
        x="categoria",
        y="probabilidad",
        title="Probabilidad promedio por categoría",
        color="probabilidad"
    )

    return fig