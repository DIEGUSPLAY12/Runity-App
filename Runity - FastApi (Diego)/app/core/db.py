import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

# Recuperamos la URL de conexión desde las variables de entorno para mayor seguridad
DATABASE_URL = os.getenv("DATABASE_URL")

# Motor de conexión de SQLAlchemy. 
# Gestiona el Pool de conexiones hacia la base de datos PostgreSQL.
engine = create_engine(DATABASE_URL)

# Fábrica de sesiones (Session Factory). 
# Configuramos autocommit y autoflush en False para tener un control manual de las transacciones.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base declarativa para el Mapeo Objeto-Relacional (ORM) usando SQLAlchemy 2.0.
# Todos los modelos de dominio (Profile, Session) heredarán de esta clase.
class Base(DeclarativeBase):
    pass

# Generador de sesiones para Inyección de Dependencias en los endpoints de FastAPI.
def get_db():
    """
    Provee una sesión de base de datos por cada petición y garantiza 
    su cierre al finalizar, incluso si ocurre una excepción durante la ejecución.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Garantiza la liberación de la conexión al pool de SQLAlchemy
        db.close()