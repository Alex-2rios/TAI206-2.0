from fastapi import APIRouter, HTTPException, Depends
import asyncio
from typing import Optional
from app.data.database import usuarios

router = APIRouter(tags=["Miscelanous"])

@router.get("/", tags=['Miscelanous'])
async def holamundo():
    return {"mensaje": "Hola mundo FastAPI"}

@router.get("/bienvenidos", tags=['Miscelanous'])
async def bienvenidos():
    return {"mensaje": "Bienvenidos a FastAPI"}

@router.get("/v1/calificaciones", tags=['Miscelanous'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje": "Tu calificacion en TAI es 10"}

@router.get("/v1/parametroO/{id}", tags=['Miscelanous'])
async def consultaUsuarios(id: int):
    await asyncio.sleep(3)
    return {"usuarios encontrado": id}

@router.get("/v1/ParametroOP/", tags=['Miscelanous'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario encontrado": id, "Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}
    else:
        return {"Aviso": "No se ha enviado ningun id"}