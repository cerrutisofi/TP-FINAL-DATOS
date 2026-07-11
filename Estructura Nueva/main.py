from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Importamos nuestros módulos separados (Arquitectura Limpia)
from database import get_db, ProyectoDB
from esquemas import ProyectoInput, ProyectoResultado, ProyectoHistorico
from ml.modelo import predecir_aprobacion, localidades_disponibles

# ==========================================
# 1. CONFIGURACIÓN DE LA API
# ==========================================
app = FastAPI(
    title="Sistema de Predicción - Presupuesto Participativo (Vicente López)",
    description=(
        "API para predecir si un proyecto de Presupuesto Participativo será "
        "ganador, en base a un modelo de Random Forest entrenado con datos "
        "históricos (2017+) cruzados con el Censo 2022."
    ),
    version="1.0.0",
)

# ==========================================
# 2. CAPA DE SEGURIDAD
# ==========================================
def verificar_permiso(x_api_key: str = Header(...)):
    if x_api_key != TOKEN_MINISTERIAL:
        raise HTTPException(status_code=401, detail="No autorizado.")

# ==========================================
# 3. ENDPOINTS
# ==========================================
@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido al sistema de predicción de Presupuesto Participativo"}

@app.post("/login", dependencies=[Depends(verificar_permiso)])
def login():
    return {"mensaje": "Login exitoso"}


@app.get("/localidades", dependencies=[Depends(verificar_permiso)])
def obtener_localidades():
    """Devuelve las localidades disponibles según el Censo 2022 (para poblar el frontend)."""
    return {"localidades": localidades_disponibles()}


@app.post("/predecir", response_model=ProyectoResultado, dependencies=[Depends(verificar_permiso)])
def predecir_proyecto(proyecto: ProyectoInput, db: Session = Depends(get_db)):
    """
    Recibe los datos de un nuevo proyecto (localidad, categoría, presupuesto),
    ejecuta el modelo de Machine Learning y persiste el resultado en la BD.
    """
    try:
        resultado = predecir_aprobacion(
            localidad=proyecto.localidad,
            categoria=proyecto.categoria,
            presupuesto=proyecto.presupuesto,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Guardamos el resultado en la base de datos (histórico)
    registro_db = ProyectoDB(
        localidad=proyecto.localidad,
        categoria=proyecto.categoria,
        presupuesto=proyecto.presupuesto,
        prediccion=resultado["prediccion"],
        etiqueta=resultado["etiqueta"],
        probabilidad=resultado["probabilidad"],
    )
    db.add(registro_db)
    db.commit()
    db.refresh(registro_db)

    return ProyectoResultado(
        localidad=proyecto.localidad,
        categoria=proyecto.categoria,
        presupuesto=proyecto.presupuesto,
        prediccion=resultado["prediccion"],
        etiqueta=resultado["etiqueta"],
        probabilidad=resultado["probabilidad"],
    )


@app.get("/historico", response_model=list[ProyectoHistorico], dependencies=[Depends(verificar_permiso)])
def obtener_historico(db: Session = Depends(get_db)):
    """Devuelve el histórico de todas las predicciones realizadas, más recientes primero."""
    registros = db.query(ProyectoDB).order_by(ProyectoDB.fecha.desc()).all()
    return registros


# ==========================================
# 6. ARRANQUE
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080, loop="none")
