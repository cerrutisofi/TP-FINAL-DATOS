# 🏛️ Análisis de Presupuesto Participativo

---

### 👥 Información General
* **Integrantes:** Cerruti Romero Sofía, Ferriz Claudio, Ozorio Florencia, Seibane Merlina

* **Nombre del proyecto:** ……

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
| **NOMBRE DEL PROYECTO** | ... |
| **EL PROBLEMA** | La opacidad en los criterios de éxito de las propuestas vecinales y la dificultad para identificar cómo interactúan las variables de costo, impacto y alcance en un entorno de recursos limitados. Esto impide entender las prioridades reales de la comunidad y los compromisos financieros asociados |
| **EL USUARIO** | 🔹 **Funcionarios de la Secretaría de Participación Ciudadana** (para evaluación técnica).<br><br>🔹 **Concejales y tomadores de decisiones** (para la asignación presupuestaria estratégica).<br><br>🔹 **Ciudadanía en general** (para co-diseñar propuestas viables y entender los criterios de selección). |
| **ORIGEN DE LOS DATOS** | Portal de Datos Abiertos de Vicente López. Dataset histórico (2017-2025) que incluye año, barrio, categoría, votos, presupuesto y resultados. Enriquecido con variables y datos contextuales de alcance estimado del proyecto y nivel socioeconómico de los barrios (Censo y Redatam) |
| **FUNCIONALIDAD** | Simulador de viabilidad y trade-offs donde el usuario podrá mover variables (ej. aumentar el presupuesto o cambiar el barrio) y visualizar en tiempo real cómo influye cada factor y qué costo implica en la probabilidad de aprobación del proyecto. |

---

### 🛠️ Stack Tecnológico

| **STACK TECNOLÓGICO** | **HERRAMIENTAS Y LIBRERÍAS** |
| :--- | :--- |
| **MANIPULACIÓN DE DATOS** | `pandas`, `numpy` |
| **VISUALIZACIÓN** | `seaborn`, `matplotlib` |
| **MACHINE LEARNING** | `scikit-learn` |
| **EXPLICABILIDAD** | `SHAP (Shapley Additive exPlanations)` |
| **NOTEBOOKS** | `jupyter lab` |
| **API/SERVE** | `fastapi`, `uvicorn` |



| **REQUERIMIENTO** | **DESCRIPCIÓN** |
| :--- |  :---: |
| NOMBRE DEL PROYECTO| ... |
| EL PROBLEMA | La opacidad en los criterios de éxito de las propuestas vecinales y la dificultad para identificar cómo interactúan las variables de costo, impacto y alcance en un entorno de recursos limitados. Esto impide entender las prioridades reales de la comunidad y los compromisos financieros asociados |
| EL USUARIO| • Funcionarios de la Secretaría de Participación Ciudadana (para evaluación técnica).

• Concejales y tomadores de decisiones (para la asignación presupuestaria estratégica).

• Ciudadanía en general (para co-diseñar propuestas viables y entender los criterios de selección).
 |
| ORIGEN DE LOS DATOS | Portal de Datos Abiertos de Vicente López. Dataset histórico (2017-2025) que incluye año, barrio, categoría, votos, presupuesto y resultados. Enriquecido con variables y datos contextuales de alcance estimado del proyecto y nivel socioeconómico de los barrios (Censo y Redatam) |
| FUNCIONALIDAD| Simulador de viabilidad y trade-offs donde el usuario podrá mover variables (ej. aumentar el presupuesto o cambiar el barrio) y visualizar en tiempo real cómo influye cada factor y qué costo implica en la probabilidad de aprobación del proyecto.
 |


| **STACK TECNOLÓGICO** | **HERRAMIENTAS Y LIBRERÍAS** |
| :--- |  :---: |
| MANIPULACIÓN DE DATOS |  pandas, numpy |
| VISUALIZACIÓN | seaborn, matplotlib |
| MACHINE LEARNING |  scikit-learn |
| EXPLICABILIDAD |  SHAP (Shapley Additive exPlanations) |
| NOTEBOOKS |  jupyter lab |
| API/SERVE |  fastapi, uvicorn |
