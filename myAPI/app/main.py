from fastapi import FastAPI
from app.routers import usuarios, misc
from app.data.db import engine
from app.data import usuario

# Esto crea las tablas en Postgres al iniciar
usuario.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mi primera API",
    description="Alex Rios Carballo", 
    version="1.0.0"
)

# Accedemos al objeto 'router' dentro de cada módulo importado
app.include_router(usuarios.router) 
app.include_router(misc.router)