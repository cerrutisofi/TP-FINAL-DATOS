# 🏛️ ViLo Propone – Sistema de Predicción para Presupuesto Participativo

---

### 👥 Información General
* **Integrantes:** Cerruti Romero Sofía, Ferriz Claudio, Ozorio Florencia, Seibane Merlina

* **Nombre del proyecto:** ViLo Propone

---

## 🎯 Planteo del proyecto

El objetivo del programa es proporcionar a los ciudadanos y gestores públicos una herramienta analítica basada en machine learning que no solo prediga la viabilidad de los proyectos vecinales, sino que haga explícitas las variables relevantes para la aprobación o no.

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
│   ├── Datos crudos/          # Excel de los resultados de las votaciones, barrios y delegaciones
│   ├── Datos procesados/
│   ├── Info adicional/
|   └── prueba_datos.ipynb     # Limpieza y normalización de datos
|
├── FRONT END
│   ├── pages/
|         ├── analisis.py      # Muestra gráficos con datos históricos. Acceso público
|         ├── login.py         # Primera pág de la web. Verifica APIKey
|         └── principal.py     # Pág principal, aquí se presenta la predicción
│   ├── estilos.py             # Diseño de la web
│   ├── frontend.py            # Inicio de app, control de inicio de sesión, preguntas de la web y navegación
│   ├── graficos.py            # Construcción de gráficos a usar 
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
---
## 📊 Sobre el modelo

- **Algoritmo:** `RandomForestClassifier` (scikit-learn), optimizado mediante `GridSearchCV` utilizando validación cruzada `StratifiedKFold` de 5 particiones y la métrica **ROC AUC**.

- **Variables de entrada (features):**
  - Presupuesto del proyecto.
  - Localidad.
  - Categoría.
  - Variables sociodemográficas derivadas del **Censo Nacional 2022** de Vicente López, incluyendo tasas de género, escolaridad, actividad económica y distribución por franjas etarias.

- **Variable objetivo (target):**
  - `Ganador_bin`, donde:
    - `1` = Proyecto ganador.
    - `0` = Proyecto no ganador.
---
### 🚀 Levantar el backend (API)
```text
python -m BACKEND.main
```
La API queda disponible en http://127.0.0.1:8080. Documentación interactiva en http://127.0.0.1:8080/docs.

Endpoints principales
| Método | Endpoint     | Descripción          |
| ------ | ------------ | -------------------- |
| GET    | /leer_raiz   | Bienvenida           |
| GET    | /localidades | Lista de localidades |
| POST   | /predecir    | Predicción           |
| GET    | /historico   | Historial            |

---
## 🖥️ Levantar el frontend (Streamlit) En otra terminal (con el backend corriendo):
En otra terminal (con el backend corriendo):
```text
streamlit run frontend.py
```

