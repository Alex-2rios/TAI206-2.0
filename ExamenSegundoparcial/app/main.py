
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from datetime import date

app = FastAPI(
    title="API de Sistema de Citas Medicas",
    description="Examen Segundo Parcial", 
    version="1.0.0"
)

citas_db = []


class CitaBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de la cita", example=1)
    nombre_paciente: str = Field(..., min_length=5, description="Nombre del paciente", example="Juan Perez")
    fecha: date = Field(..., description="Fecha de la cita (YYYY-MM-DD)", example="2026-03-15")
    motivo: str = Field(..., max_length=100, description="Motivo de la cita", example="Consulta general")
    confirmacion: bool = Field(False, description="Estado de confirmación")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "mensaje": "Error 400: Datos incompletos o no cumplen con los requisitos",
            "detalles": exc.errors()
        }
    )

security = HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "root")
    contraAuth = secrets.compare_digest(credentials.password, "1234")
    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    return credentials.username


@app.post("/v1/citas/", tags=['CRUD Citas'])
async def crear_cita(cita: CitaBase):
    if cita.fecha < date.today():
        raise HTTPException(
            status_code=400, 
            detail="La fecha de la cita no puede ser menor a la fecha actual"
        )
        
    citas_mismo_dia = sum(1 for c in citas_db if c["nombre_paciente"] == cita.nombre_paciente and c["fecha"] == cita.fecha)
    if citas_mismo_dia >= 3:
        raise HTTPException(
            status_code=400, 
            detail="El paciente ya alcanzó el límite de 3 citas para este día"
        )

  