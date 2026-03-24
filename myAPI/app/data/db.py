
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

#1. definiendo la URL de conexion a la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

#2. creando el motor de conexion
engine=create_engine(DATABASE_URL)

#3. agregamos el gestor de sesiones
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

#4. Base declarativa para modelos
Base=declarative_base()

#5. funcion para obtener la sesion en los requests
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
