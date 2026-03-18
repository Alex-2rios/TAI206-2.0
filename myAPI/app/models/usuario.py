#Modelo de validacion Pydantic
from pydantic import BaseModel, Field


class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del usuario", example="1")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example="Juan Perez")
    edad: int = Field(..., ge=0, le=120, description="Edad valida entre 0 y 120 años", example="30")
