from pydantic import BaseModel

class ProyectoBase(BaseModel):
    año: int
    localidad: str
    categoria: str
    presupuesto: float
