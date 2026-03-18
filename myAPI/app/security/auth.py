#seguridad con HTTP Basic
from fastapi import Depends
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import FastAPI, status, HTTPException, Depends, Request

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