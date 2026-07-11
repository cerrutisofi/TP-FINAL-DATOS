"""
Script de entrenamiento del modelo de Presupuesto Participativo.

Reproduce el flujo desarrollado en la notebook
`Presupuesto_Participativo_Random_Forest.ipynb` (TP Final - DS4PS / Vicente López)
de forma productiva: carga los datos, preprocesa, entrena un RandomForest con
GridSearchCV y exporta el pipeline final entrenado como .pkl para ser
consumido por la API (main.py).

Uso:
    python -m ml.entrenar_modelo
"""

import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

import warnings
warnings.filterwarnings("ignore")

# Definimos las rutas
DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIR_DATA = os.path.join(DIR_BASE, "DATOS", "Datos procesados")
DIR_MODELOS = os.path.join(DIR_BASE, "MACHINE_LEARNING")

RUTA_DATASET_PROYECTOS = os.path.join(
    DIR_DATA,
    "dataset_final_vilo.csv"
)

RUTA_CENSO = os.path.join(
    DIR_DATA,
    "Censo_2022_final.xlsx"
)

RUTA_MODELO_SALIDA = os.path.join(
    DIR_MODELOS,
    "modelo_presupuesto_participativo.pkl"
)

os.makedirs(DIR_MODELOS, exist_ok=True)


def cargar_datos():
    """Carga el dataset de proyectos y el censo 2022 desde /data."""
    df = pd.read_csv(RUTA_DATASET_PROYECTOS, sep=";", header=0)
    df_censo_2022 = pd.read_excel(RUTA_CENSO)

    print(f"Proyectos cargados: {df.shape[0]} filas x {df.shape[1]} columnas")
    print(f"Censo cargado:      {df_censo_2022.shape[0]} filas x {df_censo_2022.shape[1]} columnas")
    return df, df_censo_2022


def preprocesar(df, df_censo_2022):
    """Aplica el mismo preprocesamiento que la notebook original."""

    # Corrección de columnas con valores mixtos en el censo
    columnas_a_limpiar = ["Perforación con bomba manual", "Pozo sin bomba"]
    for col in columnas_a_limpiar:
        df_censo_2022[col] = (
            pd.to_numeric(df_censo_2022[col], errors="coerce").fillna(0).astype("int64")
        )

    # Join entre proyectos y censo por localidad
    df_definitivo = pd.merge(df, df_censo_2022, on="Localidades", how="inner")
    print(f"Dataset unificado: {df_definitivo.shape[0]} filas x {df_definitivo.shape[1]} columnas")

    # Agrupación de rangos etarios en 3 franjas
    df_definitivo["0-14"] = df_definitivo[["0-4", "5-9", "10-14"]].sum(axis=1)
    df_definitivo["15-64"] = df_definitivo[[
        "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64",
    ]].sum(axis=1)
    df_definitivo["65-100 y mas"] = df_definitivo[[
        "65-69", "70-74", "75-79", "80-84", "85-89",
        "90-94", "95-99", "100 y más",
    ]].sum(axis=1)

    cols_etarias = [
        "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79",
        "80-84", "85-89", "90-94", "95-99", "100 y más",
    ]
    df_definitivo.drop(columns=cols_etarias, inplace=True)

    # Eliminación de columnas no relevantes para el modelado
    cols_a_eliminar = [
        "Proyecto", "Municipios", "Geolocalización", "Límites",
        "Perforación con bomba a motor", "Perforación con bomba manual",
        "Pozo sin bomba",
        "Transporte por cisterna, agua de lluvia, río, canal, arroyo o acequia",
        "Otra\nprocedencia", "Tiene internet en la vivienda", "No tiene internet en la vivienda",
        "Obra social o\nprepaga\n(incluye PAMI)", "Programas o\nplanes estatales\nde salud",
        "No tiene obra\nsocial, prepaga ni\nplan estatal",
        "Población\nsin asistencia escolar\npero que si asistió",
        "Población\nque nunca\ntuvo asistencia escolar",
        "Población económicamente activa desocupada", "Población no económicamente activa",
    ]
    df_definitivo.drop(columns=cols_a_eliminar, inplace=True, errors="ignore")

    # Cálculo de tasas sobre la población total
    pop = df_definitivo["Total poblacional"]
    df_definitivo["tasa_mujer"] = df_definitivo["Mujer/Femenino"] / pop
    df_definitivo["tasa_varon"] = df_definitivo["Varón/Masculino"] / pop
    df_definitivo["tasa_agua_red"] = df_definitivo["Red pública\n(agua corriente)"] / pop
    df_definitivo["tasa_escolaridad"] = df_definitivo["Población\ncon asistencia escolar"] / pop
    df_definitivo["tasa_pea_ocupada"] = df_definitivo["Población económicamente activa ocupada"] / pop
    df_definitivo["tasa_0_14"] = df_definitivo["0-14"] / pop
    df_definitivo["tasa_15_64"] = df_definitivo["15-64"] / pop
    df_definitivo["tasa_65_mas"] = df_definitivo["65-100 y mas"] / pop

    cols_originales_tasas = [
        "Mujer/Femenino", "Varón/Masculino",
        "Red pública\n(agua corriente)",
        "Población\ncon asistencia escolar",
        "Población económicamente activa ocupada",
        "0-14", "15-64", "65-100 y mas",
        "Total poblacional",
    ]
    df_definitivo.drop(columns=cols_originales_tasas, inplace=True, errors="ignore")

    print(f"Dataset final para entrenamiento: {df_definitivo.shape[0]} filas x {df_definitivo.shape[1]} columnas")
    return df_definitivo


def entrenar(df_definitivo):
    """Entrena el pipeline (preprocesador + RandomForest) con GridSearchCV."""

    X = df_definitivo.drop(columns=["Ganador_bin", "Votos", "Año"])
    y = df_definitivo["Ganador_bin"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train: {X_train.shape[0]} muestras | Test: {X_test.shape[0]} muestras")

    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()
    print(f"Features numéricas ({len(numeric_features)}): {numeric_features}")
    print(f"Features categóricas ({len(categorical_features)}): {categorical_features}")

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ])

    pipeline_rf = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("estimator", RandomForestClassifier(random_state=42, class_weight="balanced")),
    ])

    param_grid = {
        "preprocessor__num__imputer__strategy": ["mean", "median"],
        "estimator__n_estimators": [100, 300, 500],
        "estimator__max_depth": [10, 15, 20],
        "estimator__min_samples_leaf": [1, 2, 5],
    }

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    gs = GridSearchCV(
        estimator=pipeline_rf,
        param_grid=param_grid,
        cv=skf,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=1,
    )
    gs.fit(X_train, y_train)

    print("\nGridSearch finalizado")
    print(f"Mejores parámetros: {gs.best_params_}")
    print(f"Mejor AUC (CV):     {gs.best_score_:.4f}")

    modelo_final = gs.best_estimator_

    y_pred = modelo_final.predict(X_test)
    y_pred_prob = modelo_final.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_prob)

    print(f"\nAccuracy en test: {accuracy:.4f}")
    print(f"AUC en test:      {auc:.4f}\n")
    print("Reporte de clasificación:")
    print(classification_report(y_test, y_pred, target_names=["No Ganador", "Ganador"]))

    return modelo_final


def main():
    df, df_censo_2022 = cargar_datos()
    df_definitivo = preprocesar(df, df_censo_2022)
    modelo_final = entrenar(df_definitivo)

    joblib.dump(modelo_final, RUTA_MODELO_SALIDA)
    print(f"\nModelo exportado en: {RUTA_MODELO_SALIDA}")


if __name__ == "__main__":
    main()

