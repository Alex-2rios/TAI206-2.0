from fastapi import FastAPI, status, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

app = FastAPI(title="Biblioteca Digital API", version="1.0.0")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "mensaje": "Error 400: Faltan datos o el nombre no es válido",
            "detalles": exc.errors()
        }
    )

libros_db = []
prestamos_db = []

class Libro(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=100)
    año: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2)
    correo: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

class Prestamo(BaseModel):
    id_prestamo: int = Field(..., gt=0)
    id_libro: int = Field(..., gt=0)
    usuario: Usuario

@app.post("/v1/libros/", status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro: Libro):
    for l in libros_db:
        if l.id == libro.id:
            raise HTTPException(status_code=400, detail="El ID ya existe")
    
    libros_db.append(libro)
    return {"mensaje": "Libro registrado exitosamente", "libro": libro}

@app.get("/v1/libros/disponibles")
async def listar_disponibles():
    disponibles = [l for l in libros_db if l.estado == "disponible"]
    return {"libros_disponibles": disponibles}

@app.get("/v1/libros/buscar")
async def buscar_libro(nombre: str):
    encontrados = [l for l in libros_db if nombre.lower() in l.nombre.lower()]
    return {"resultados": encontrados}

@app.post("/v1/prestamos/", status_code=status.HTTP_201_CREATED)
async def registrar_prestamo(prestamo: Prestamo):
    libro_encontrado = None
    for l in libros_db:
        if l.id == prestamo.id_libro:
            libro_encontrado = l
            break
            
    if not libro_encontrado:
        raise HTTPException(status_code=400, detail="El libro no existe")
        
    if libro_encontrado.estado == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya se encuentra prestado")
        
    libro_encontrado.estado = "prestado"
    prestamos_db.append(prestamo)
    return {"mensaje": "Préstamo registrado con éxito"}

@app.put("/v1/prestamos/{id_prestamo}/devolver", status_code=status.HTTP_200_OK)
async def devolver_libro(id_prestamo: int):
    prestamo_encontrado = None
    for p in prestamos_db:
        if p.id_prestamo == id_prestamo:
            prestamo_encontrado = p
            break
            
    if not prestamo_encontrado:
        raise HTTPException(status_code=409, detail="El préstamo no existe")
        
    for l in libros_db:
        if l.id == prestamo_encontrado.id_libro:
            l.estado = "disponible"
            break
            
    return {"mensaje": "Libro devuelto correctamente"}

@app.delete("/v1/prestamos/{id_prestamo}", status_code=status.HTTP_200_OK)
async def eliminar_prestamo(id_prestamo: int):
    global prestamos_db
    existe = any(p.id_prestamo == id_prestamo for p in prestamos_db)
    
    if not existe:
        raise HTTPException(status_code=409, detail="El préstamo no existe")
        
    prestamos_db = [p for p in prestamos_db if p.id_prestamo != id_prestamo]
    return {"mensaje": "Registro eliminado exitosamente"}