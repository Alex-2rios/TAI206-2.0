from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, List, Optional

app = FastAPI(
    title="Biblioteca Digital API",
    description="Práctica 5 - UPQ", 
    version="1.0.0"
)

libros_db = []
prestamos_db = []

class Libro(BaseModel):
    id: int = Field(..., gt=0) 
    nombre: str = Field(..., min_length=2, max_length=100) 
    anio: int = Field(..., gt=1450, le=2026) 
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
            raise HTTPException(status_code=400, detail="El ID del libro ya existe")
    
    libros_db.append(libro)
    return {"mensaje": "Libro registrado", "libro": libro}

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
        raise HTTPException(status_code=400, detail="El libro solicitado no existe")
        
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
        raise HTTPException(status_code=409, detail="El registro de préstamo no existe")
        
    for l in libros_db:
        if l.id == prestamo_encontrado.id_libro:
            l.estado = "disponible"
            break
            
    return {"mensaje": "Libro devuelto correctamente"}

@app.delete("/v1/prestamos/{id_prestamo}")
async def eliminar_prestamo(id_prestamo: int):
    global prestamos_db
    existe = any(p.id_prestamo == id_prestamo for p in prestamos_db)
    if not existe:
        raise HTTPException(status_code=409, detail="El registro de préstamo no existe")
        
    prestamos_db = [p for p in prestamos_db if p.id_prestamo != id_prestamo]
    return {"mensaje": "Registro eliminado exitosamente"}