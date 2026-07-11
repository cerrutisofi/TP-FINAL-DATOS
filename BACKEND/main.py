from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Importamos nuestros módulos separados (Arquitectura Limpia)
from database import get_db, ProyectoDB
from esquemas import ProyectoInput, ProyectoResultado, ProyectoHistorico
from MACHINE_LEARNING.modelo import predecir_aprobacion, localidades_disponibles
#Configuramos la API

app = FastAPI(
    title="Sistema de Predicción - Presupuesto Participativo (Vicente López)",
    description=(
        "API para predecir si un proyecto de Presupuesto Participativo será "
        "ganador, en base a un modelo de Random Forest entrenado con datos "
        "históricos (2017+) cruzados con el Censo 2022."
    ),
    version="1.0.0",
)


# Endpoints

@app.get("/")
def leer_raiz():
    return {
        "mensaje": "Bienvenido al sistema de predicción de Presupuesto Participativo"
    }


@app.get("/localidades")
def obtener_localidades():
    """
    Devuelve las localidades disponibles según el Censo 2022
    (para poblar el frontend).
    """
    return {"localidades": localidades_disponibles()}


@app.post("/predecir", response_model=ProyectoResultado)
def predecir_proyecto(
    proyecto: ProyectoInput,
    db: Session = Depends(get_db)
):
    """
    Recibe los datos de un nuevo proyecto (localidad, categoría y presupuesto),
    ejecuta el modelo de Machine Learning y guarda el resultado en la base de datos.
    """
    try:
        resultado = predecir_aprobacion(
            localidad=proyecto.localidad,
            categoria=proyecto.categoria,
            presupuesto=proyecto.presupuesto,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    # Guardamos el resultado en la base de datos
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


@app.get("/historico", response_model=list[ProyectoHistorico])
def obtener_historico(db: Session = Depends(get_db)):
    """
    Devuelve el histórico de todas las predicciones realizadas,
    ordenadas desde la más reciente.
    """
    registros = (
        db.query(ProyectoDB)
        .order_by(ProyectoDB.fecha.desc())
        .all()
    )

    return registros


# Arranque

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
        loop="none"
    )