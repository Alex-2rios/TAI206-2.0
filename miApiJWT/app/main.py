from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field
import asyncio
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


SECRET_KEY = "mi_clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)
 
app = FastAPI(
    title="Mi primera API JWT",
    description="Alex Rios Carballo", 
    version="1.0.0"
)

usuarios=[
    {"id":1, "nombre":"Ivan","edad":38},
    {"id":2, "nombre":"Tommy","edad":21},
    {"id":3, "nombre":"Santy","edad":18},
]

class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del usuario", example="1")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example="Juan Perez")
    edad: int = Field(..., ge=0, le=120, description="Edad valida entre 0 y 120 años", example="30")

def crear_token_acceso(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/login", tags=['Autenticación'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or form_data.password != "1234":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crear_token_acceso(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def validar_token(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado. No se proporcionó ningún token.",
        )
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo validar las credenciales",
            )
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado" 
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


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
async def consultaUsuario_obligatorio(id:int):
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
    usuarios.append(usuario.model_dump())
    return{
        "mensaje":"Usuario agregado correctamente",
        "datos":usuario,
        "status":"200"  
    }


@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuario(id: int, usuario: dict, usuarioAuth: str = Depends(validar_token)):  
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[idx] = {**usr, **usuario}
            return {
                "mensaje": f"Usuario actualizado por {usuarioAuth}",
                "datos": usuarios[idx],
                "status": "200"
            }
            
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
        )

@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(validar_token)): 
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