from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# Creamos un archivo local llamado proyectos.db
URL_BASE_DATOS = "sqlite:///./proyectos.db"

engine = create_engine(URL_BASE_DATOS, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# El modelo exacto de cómo se verá la tabla en SQL
class ProyectoDB(Base):
    __tablename__ = "proyectos"
    
    id = Column(Integer, primary_key=True, index=True)
    año = Column(Integer)
    localidad = Column(String)
    categoria = Column(String)
    presupuesto = Column(Float)
    ganador_bin = Column(Integer)

# Crear las tablas físicamente
Base.metadata.create_all(bind=engine)

# Dependencia para abrir y cerrar la conexión en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()