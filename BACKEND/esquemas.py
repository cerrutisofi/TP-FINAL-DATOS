from pydantic import BaseModel

class ProyectoBase(BaseModel):
    localidad: str
    categoria: str
    presupuesto: float
