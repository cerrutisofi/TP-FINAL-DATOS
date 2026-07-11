"""
Módulo de inferencia del modelo de Presupuesto Participativo.

Carga el pipeline entrenado (RandomForest) generado por `ml/entrenar_modelo.py`
y el Censo 2022 de Vicente López, y expone `predecir_aprobacion(...)`
replicando exactamente el preprocesamiento usado durante el entrenamiento
(ver notebook `Presupuesto_Participativo_Random_Forest.ipynb`).
"""

import os
import joblib
import pandas as pd

DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_MODELO = os.path.join(DIR_BASE,"MACHINE_LEARNING","modelo_presupuesto_participativo.pkl")
RUTA_CENSO = os.path.join(DIR_BASE,"DATOS","Datos procesados","Censo_2022_final.xlsx")

_modelo = None
_df_censo = None


def _cargar_recursos():
    """Carga (una sola vez, en memoria) el modelo entrenado y el censo original."""
    global _modelo, _df_censo

    if _modelo is None:
        if not os.path.exists(RUTA_MODELO):
            raise RuntimeError(
                f"No se encontró el modelo en '{RUTA_MODELO}'. "
                "Ejecutá primero: python -m ml.entrenar_modelo"
            )
        _modelo = joblib.load(RUTA_MODELO)

    if _df_censo is None:
        if not os.path.exists(RUTA_CENSO):
            raise RuntimeError(f"No se encontró el censo en '{RUTA_CENSO}'.")
        _df_censo = pd.read_excel(RUTA_CENSO)

    return _modelo, _df_censo


def localidades_disponibles():
    """Devuelve la lista de localidades presentes en el Censo 2022."""
    _, df_censo = _cargar_recursos()
    return sorted(df_censo["Localidades"].dropna().unique().tolist())


def _agrupar_rangos_etarios(df):
    """Agrupa los rangos etarios del censo en 3 franjas (0-14, 15-64, 65+),
    igual que en el preprocesamiento de entrenamiento."""
    df["0-14"] = df[["0-4", "5-9", "10-14"]].sum(axis=1)

    df["15-64"] = df[[
        "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64",
    ]].sum(axis=1)

    df["65-100 y mas"] = df[[
        "65-69", "70-74", "75-79", "80-84", "85-89",
        "90-94", "95-99", "100 y más",
    ]].sum(axis=1)

    cols_etarias = [
        "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79",
        "80-84", "85-89", "90-94", "95-99", "100 y más",
    ]
    df.drop(columns=cols_etarias, inplace=True)
    return df


def _calcular_tasas(df):
    """Calcula las tasas poblacionales sobre el total y elimina las columnas
    originales, igual que en el preprocesamiento de entrenamiento."""
    pop = df["Total poblacional"]

    df["tasa_mujer"] = df["Mujer/Femenino"] / pop
    df["tasa_varon"] = df["Varón/Masculino"] / pop
    df["tasa_agua_red"] = df["Red pública\n(agua corriente)"] / pop
    df["tasa_escolaridad"] = df["Población\ncon asistencia escolar"] / pop
    df["tasa_pea_ocupada"] = df["Población económicamente activa ocupada"] / pop
    df["tasa_0_14"] = df["0-14"] / pop
    df["tasa_15_64"] = df["15-64"] / pop
    df["tasa_65_mas"] = df["65-100 y mas"] / pop

    cols_originales = [
        "Mujer/Femenino", "Varón/Masculino",
        "Red pública\n(agua corriente)",
        "Población\ncon asistencia escolar",
        "Población económicamente activa ocupada",
        "0-14", "15-64", "65-100 y mas",
        "Total poblacional",
    ]
    df.drop(columns=[c for c in cols_originales if c in df.columns], inplace=True)
    return df


def predecir_aprobacion(localidad: str, categoria: str, presupuesto: float) -> dict:
    """
    Predice si un nuevo proyecto del Presupuesto Participativo será ganador,
    cruzando los datos ingresados con el Censo 2022 de la localidad indicada.

    Retorna un dict con: prediccion (0/1), etiqueta y probabilidad de éxito.
    """
    modelo, df_censo = _cargar_recursos()

    nuevo_proy = pd.DataFrame({
        "Localidades": [localidad],
        "Categoria": [categoria],
        "Presupuesto": [presupuesto],
    })

    # Merge con el censo original (con columnas etarias sin agrupar)
    nuevo_completo = pd.merge(nuevo_proy, df_censo, on="Localidades", how="left")

    if nuevo_completo["Localidades"].isnull().all() or nuevo_completo.iloc[0].isnull().sum() > 2:
        raise ValueError(
            f"La localidad '{localidad}' no se encontró en el censo. "
            f"Localidades válidas: {', '.join(localidades_disponibles())}"
        )

    nuevo_completo = _agrupar_rangos_etarios(nuevo_completo)
    nuevo_completo = _calcular_tasas(nuevo_completo)

    cols_a_eliminar = [
        "Municipios", "Geolocalización", "Límites",
        "Perforación con bomba a motor", "Perforación con bomba manual",
        "Pozo sin bomba",
        "Transporte por cisterna, agua de lluvia, río, canal, arroyo o acequia",
        "Otra procedencia", "Tiene internet en la vivienda", "No tiene internet en la vivienda",
        "Obra social o prepaga (incluye PAMI)", "Programas o planes estatales de salud",
        "No tiene obra social, prepaga ni plan estatal",
        "Población sin asistencia escolar pero que si asistió",
        "Población que nunca tuvo asistencia escolar",
        "Población económicamente activa desocupada", "Población no económicamente activa",
    ]
    nuevo_completo.drop(
        columns=[c for c in cols_a_eliminar if c in nuevo_completo.columns],
        inplace=True,
    )

    prediccion = modelo.predict(nuevo_completo)[0]
    probabilidad = modelo.predict_proba(nuevo_completo)[0][1]
    etiqueta = "GANADOR" if prediccion == 1 else "NO GANADOR"

    return {
        "prediccion": int(prediccion),
        "etiqueta": etiqueta,
        "probabilidad": float(probabilidad),
    }
