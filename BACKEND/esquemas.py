from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProyectoInput(BaseModel):
    """Datos que ingresa el usuario para evaluar un nuevo proyecto."""
    localidad: str 
    categoria: str 
    presupuesto: float 


class ProyectoResultado(BaseModel):
    """Resultado de la predicción para un proyecto."""
    localidad: str
    categoria: str
    presupuesto: float
    prediccion: int
    etiqueta: str
    probabilidad: float


class ProyectoHistorico(ProyectoResultado):
    """Registro histórico tal como se guarda/lee de la base de datos."""
    id: int
    fecha: Optional[datetime] = None

    class Config:
        from_attributes = True
