#importaciones
from typing import Optional
from fastapi import FastAPI 
import asyncio

#Inicializacion 
app = FastAPI(
    title="Mi primera API",
    description="Alex Rios Carballo", 
    version="1.0.0"
)


usuarios=[
    {"id":1, "nombre":"Ivan","edad":38},
    {"id":2, "nombre":"Tommy","edad":21},
    {"id":3, "nombre":"Santy","edad":18},
]

#Endpoint 
@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje": "Hola mundo FastAPI"}

@app.get("/bienvenidos", tags=['Inicio'])
async def bienvenidos():
    return {"mensaje": "Bienvenidos a FastAPI"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje": "Tu calificacion en TAI es 10"}

@app.get("/v1/usuarios/", tags=['Parametro obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"usuarios encontrado": id}

@app.get("/v1/usuarios_op/", tags=['Parametro opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return {"usuario encontrado":id , "Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}
    else:
        return {"Aviso": "No se ha enviado ningun id"}