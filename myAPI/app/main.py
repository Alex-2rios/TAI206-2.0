#importaciones
from fastapi import FastAPI
from app.routers.usuarios import router as usuarios_router
from app.routers.misc import router as misc_router


#Inicializacion 
app = FastAPI(
    title="Mi primera API",
    description="Alex Rios Carballo", 
    version="1.0.0"
)

app.include_router(usuarios_router)
app.include_router(misc_router)