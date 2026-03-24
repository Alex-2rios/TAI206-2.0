from typing import Optional
from fastapi import HTTPException, Depends, APIRouter, status
import asyncio
from app.models.usuario import UsuarioBase
from app.security.auth import verificar_Peticion
from app.data.database import usuarios

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)
    
@router.get("/") 
async def consultaUsuarios(db: Session = Depends(get_db)):
    consultaUsuarios = db.query(usuarioDB).all()
    
    return {
        "status": "200",
        "total": len(consultaUsuarios),
        "data": consultaUsuarios
    }
    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuarioP: UsuarioBase, db: Session = Depends(get_db)):
    nuevoUsuario=usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)

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