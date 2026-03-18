from typing import Optional
from fastapi import HTTPException, Depends, APIRouter
import asyncio
from app.models.usuario import UsuarioBase
from app.security.auth import verificar_Peticion
from app.data.database import usuarios

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)
    
@router.get("/", tags=['CRUD HTTP']) 
async def consultaUsuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }
    
@router.post("/", tags=['CRUD HTTP']) 
async def agregar_usuarios(usuario: UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El usuario con este ID ya existe"
            )
    usuarios.append(usuario.dict()) 
    return {
        "mensaje": "Usuario agregado correctamente",
        "datos": usuario,
        "status": "200"  
    }

@router.put("/{id}", tags=['CRUD HTTP']) # Tag unificado
async def actualizar_usuario(id: int, usuario: dict):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[idx] = {**usr, **usuario}
            return {
                "mensaje": "Usuario actualizado",
                "datos": usuarios[idx],
                "status": "200"
            }
    raise HTTPException(status_code=400, detail="Usuario no encontrado")

@router.delete("/{id}", tags=['CRUD HTTP']) # Tag unificado
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_Peticion)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[idx]
            return {
                "mensaje": f"Usuario eliminado correctamente por {usuarioAuth}",
                "status": "200"
            }

    raise HTTPException(status_code=400, detail="Usuario no encontrado")