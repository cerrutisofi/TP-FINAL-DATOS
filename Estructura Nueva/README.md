# 🏛️ Presupuesto Participativo - Sistema de Predicción (Vicente López)

Sistema de soporte de decisiones que predice si un proyecto de **Presupuesto
Participativo** será **ganador o no**, usando un modelo de **Random Forest**
entrenado con datos históricos de proyectos (2017 en adelante) cruzados con
el **Censo 2022** de Vicente López.

Este proyecto reutiliza la arquitectura del MVP de fiscalización (FastAPI +
SQLite + Streamlit) y reemplaza el motor de reglas por el modelo de Machine
Learning desarrollado en la notebook
`Presupuesto_Participativo_Random_Forest.ipynb`.

## 🧱 Arquitectura

```
.
├── main.py                 # API FastAPI (endpoints, seguridad)
├── database.py             # Modelo SQLAlchemy + persistencia SQLite
├── esquemas.py              # Schemas Pydantic (entrada / salida)
├── frontend.py              # Tablero Streamlit
├── ml/
│   ├── entrenar_modelo.py   # Script que reproduce la notebook y genera el .pkl
│   └── modelo.py            # Carga el modelo entrenado y expone predecir_aprobacion()
├── modelos/
│   └── modelo_presupuesto_participativo.pkl   # Pipeline entrenado (RandomForest)
├── data/
│   ├── dataset_final_vilo.csv          # Dataset histórico de proyectos
│   └── censo_2022_vicente_lopez.xlsx   # Censo 2022 por localidad
├── requirements.txt
├── .env.example
└── .gitignore
```

## ⚙️ Instalación

```bash
git clone <url-del-repo>
cd <nombre-del-repo>
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🔐 Variables de entorno

Copiá `.env.example` a `.env` y completá el token:

```bash
cp .env.example .env
```

```
TOKEN_MINISTERIAL=tu_token_secreto_aqui
```

## 🤖 Entrenamiento del modelo

El modelo entrenado ya se incluye en `modelos/modelo_presupuesto_participativo.pkl`.
Si querés reentrenarlo (por ejemplo, tras actualizar los datos en `data/`):

```bash
python -m ml.entrenar_modelo
```

Esto reproduce el pipeline completo de la notebook: preprocesamiento,
`GridSearchCV` sobre un `RandomForestClassifier` y exportación con `joblib`.

## 🚀 Levantar el backend (API)

```bash
python main.py
```

La API queda disponible en `http://127.0.0.1:8080`. Documentación interactiva
en `http://127.0.0.1:8080/docs`.

### Endpoints principales

| Método | Endpoint       | Descripción                                            | Seguridad         |
|--------|----------------|---------------------------------------------------------|-------------------|
| GET    | `/`            | Mensaje de bienvenida                                    | Pública           |
| GET    | `/localidades` | Localidades disponibles según el Censo 2022              | `x-api-key`       |
| POST   | `/predecir`    | Predice si un proyecto será ganador y guarda el registro | `x-api-key`       |
| GET    | `/historico`   | Devuelve el histórico de predicciones realizadas         | `x-api-key`       |

Ejemplo de body para `POST /predecir`:

```json
{
  "localidad": "Olivos",
  "categoria": "Seguridad y bomberos",
  "presupuesto": 5000000
}
```

## 🖥️ Levantar el frontend (Streamlit)

En otra terminal (con el backend corriendo):

```bash
streamlit run frontend.py
```

Desde la barra lateral se configura la URL de la API y el API Key
(`TOKEN_MINISTERIAL`).

## 📊 Sobre el modelo

- **Algoritmo:** `RandomForestClassifier` (scikit-learn), optimizado con
  `GridSearchCV` (5-fold `StratifiedKFold`, métrica `roc_auc`).
- **Features:** presupuesto del proyecto, localidad, categoría, y variables
  sociodemográficas derivadas del Censo 2022 (tasas de género, escolaridad,
  actividad económica y franjas etarias).
- **Target:** `Ganador_bin` (1 = proyecto ganador, 0 = no ganador).
- **Fuente de datos original:** [TP-FINAL-DATOS](https://github.com/cerrutisofi/TP-FINAL-DATOS)
  (proyecto académico DS4PS).

## 📌 Notas

- El archivo `presupuesto_participativo.db` (SQLite) se genera automáticamente
  al levantar la API por primera vez, y no se versiona en git.
- Si cambian los datos de origen, basta con reemplazar los archivos en
  `data/` y volver a correr `python -m ml.entrenar_modelo`.
