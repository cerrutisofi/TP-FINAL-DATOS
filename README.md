# 🏛️ ViLo Propone – Sistema de Predicción para Presupuesto Participativo

---

### 👥 Información General
* **Integrantes:** Cerruti Romero Sofía, Ferriz Claudio, Ozorio Florencia, Seibane Merlina

* **Nombre del proyecto:** ViLo Propone

---

## 🎯 Planteo del proyecto

El objetivo del programa es proporcionar a los ciudadanos y gestores públicos una herramienta analítica basada en machine learning que no solo prediga la viabilidad de los proyectos vecinales, sino que haga explícitos los trade-offs entre el costo (presupuesto requerido), el alcance (población beneficiada) y el impacto del proyecto.

> A través de un enfoque de inteligencia artificial explicable, el sistema permitirá entender cómo las personas priorizan distintas alternativas cuando los recursos son limitados, identificando qué factores específicos (geográficos, económicos o temáticos) influyen realmente en las decisiones y el éxito de una propuesta.

---

## ⚠️ Planteo del problema

El proceso actual de presupuesto participativo sufre de asimetría de información, falta de criterios predictivos y una nula automatización. La desconexión entre las demandas ciudadanas y las restricciones presupuestarias del municipio genera ineficiencias graves: los ciudadanos proponen ideas sin noción real de su viabilidad técnica o económica, y los funcionarios carecen de herramientas basadas en datos históricos para optimizar la asignación de recursos.

Al no transparentar de forma clara por qué ciertos proyectos ganan y otros se descartan, se genera opacidad en los criterios de éxito de las propuestas vecinales.


### 📋 Requerimientos del Proyecto

| **REQUERIMIENTO** | **DESCRIPCIÓN** |
| :--- | :--- |
| **NOMBRE DEL PROYECTO** | ViLo Propone |
| **EL PROBLEMA** | La opacidad en los criterios de éxito de las propuestas vecinales y la dificultad para identificar cómo interactúan las variables de costo, impacto y alcance en un entorno de recursos limitados. Esto impide entender las prioridades reales de la comunidad y los compromisos financieros asociados |
| **EL USUARIO** | 🔹 **Funcionarios de la Secretaría de Participación Ciudadana** (para evaluación técnica).<br><br>🔹 **Concejales y tomadores de decisiones** (para la asignación presupuestaria estratégica).<br><br>🔹 **Ciudadanía en general** (para co-diseñar propuestas viables y entender los criterios de selección). |
| **ORIGEN DE LOS DATOS** | Portal de Datos Abiertos de Vicente López. Dataset histórico (2013-2025) que incluye año, barrio, categoría, votos, presupuesto y resultados. Enriquecido con variables y datos contextuales de alcance estimado del proyecto y nivel socioeconómico de los barrios (Censo y Redatam) |
| **FUNCIONALIDAD** | Simulador de viabilidad y trade-offs donde el usuario podrá mover variables (ej. aumentar el presupuesto o cambiar el barrio) y visualizar en tiempo real cómo influye cada factor y qué costo implica en la probabilidad de aprobación del proyecto. |

---
### 📁 Estructura del proyecto

```text
TP FINAL DATOS
│
├── BACKEND
|   ├── __init__.py
│   ├── database.py            # Base de datos SQLite + SQLAlchemy
│   ├── esquemas.py            # Esquemas Pydantic
|   ├── main.py                # API FastAPI (endpoints)
│   └── proyectos_presup.db    # Base de datos (automáticamente generada)
│
├── DATOS
│   ├── Datos crudos/
│   ├── Datos procesados/
│   ├── Info adicional/
|   └── prueba_datos.ipynb     #Limpieza y normalización de datos
|
├── FRONT END
│   ├── estilos.py
│   ├── frontend.py
│   ├── graficos.py
|   ├── logo-mvl.png
|   └── logo_pp.jpg
|
├── MACHINE_LEARNING
|   ├── Presupuesto_Participativo_Random_Forest.ipynb
|   ├── __init__.py
│   ├── entrenar_modelo.py      # Entrena el modelo y genera el .pkl
│   ├── modelo.py               # Carga el modelo y realiza predicciones
│   └── modelo_presupuesto_participativo.pkl
│
├── requirements.txt
└── README.md
```
---
### 🛠️ Stack Tecnológico

| **STACK TECNOLÓGICO** | **HERRAMIENTAS Y LIBRERÍAS** |
| :--- | :--- |
| **MANIPULACIÓN DE DATOS** | `pandas`, `numpy` |
| **VISUALIZACIÓN** | `seaborn`, `matplotlib` |
| **MACHINE LEARNING** | `scikit-learn` |
| **MODELO** | `Random Forest` |
| **EXPLICABILIDAD** | `SHAP (Shapley Additive exPlanations)` |
| **NOTEBOOKS** | `jupyter lab` |
| **API/SERVE** | `fastapi`, `uvicorn` |
| **BASE DE DATOS** | `SQLite`, `SQLAlchemy` |
| **FRONT END** | `streamlit`|

---
### ⚙️ Instalación
```text
git clone https://github.com/cerrutisofi/TP-FINAL-DATOS
cd TP-FINAL-DATOS

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```
---
### 🤖 Entrenamiento del modelo
El modelo entrenado ya se incluye en modelos/modelo_presupuesto_participativo.pkl. Para reentrenarlo: 
```text
python -m MACHINE_LEARNING.entrenar_modelo
```
📊 Sobre el modelo
. Algoritmo: RandomForestClassifier (scikit-learn), optimizado con GridSearchCV (5-fold StratifiedKFold, métrica roc_auc).
. Features: presupuesto del proyecto, localidad, categoría, y variables sociodemográficas derivadas del Censo 2022 (tasas de género, escolaridad, actividad económica y franjas etarias)
. Target: Ganador_bin (1 = proyecto ganador, 0 = no ganador).
---
### 🚀 Levantar el backend (API)
```text
python -m BACKEND.main
```
La API queda disponible en http://127.0.0.1:8080. Documentación interactiva en http://127.0.0.1:8080/docs.

Endpoints principales
| Método | Endpoint     | Descripción          |
| ------ | ------------ | -------------------- |
| GET    | /            | Bienvenida           |
| GET    | /localidades | Lista de localidades |
| POST   | /predecir    | Predicción           |
| GET    | /historico   | Historial            |

---
###🖥️ Levantar el frontend (Streamlit)
En otra terminal (con el backend corriendo):
```text
streamlit run frontend.py
```

