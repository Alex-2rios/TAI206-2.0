#importaciones
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends, Request
from fastapi.exceptions import RequestValidationError
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

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

#Modelo de validacion Pydantic
class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del usuario", example="1")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example="Juan Perez")
    edad: int = Field(..., ge=0, le=120, description="Edad valida entre 0 y 120 años", example="30")

#seguridad con HTTP Basic
security = HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials=Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "admin")
    contraAuth = secrets.compare_digest(credentials.password, "1234")
    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    return credentials.username

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

@app.get("/v1/parametroO/{id}", tags=['Parametro obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"usuarios encontrado": id}

@app.get("/v1/ParametroOP/", tags=['Parametro opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return {"usuario encontrado":id , "Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}
    else:
        return {"Aviso": "No se ha enviado ningun id"}
    
    
@app.get("/v1/usuarios/", tags=['CRUD usuarios'])
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
    
@app.post("/v1/usuarios/", tags=['CRUD usuarios'])
async def agregar_usuarios(usuario:UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El usuario con este ID ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado correctamente",
        "datos":usuario,
        "status":"200"  
    }

@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuario(id: int, usuario: dict):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[idx] = {**usr, **usuario}
            return {
                "mensaje": "Usuario actualizado",
                "datos": usuarios[idx],
                "status": "200"
            }
            
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
        )

@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_Peticion)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[idx]
            return {
                "mensaje": f"Usuario eliminado correctamente por {usuarioAuth}",
                "status": "200"
            }
        raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
        )
