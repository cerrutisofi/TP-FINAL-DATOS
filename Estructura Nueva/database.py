from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Creamos un archivo local llamado presupuesto_participativo.db
URL_BASE_DATOS = "sqlite:///./presupuesto_participativo.db"

engine = create_engine(URL_BASE_DATOS, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# El modelo exacto de cómo se verá la tabla en SQL
class ProyectoDB(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    localidad = Column(String, index=True)
    categoria = Column(String, index=True)
    presupuesto = Column(Float)
    prediccion = Column(Integer)          # 0 = No ganador, 1 = Ganador
    etiqueta = Column(String)             # "GANADOR" / "NO GANADOR"
    probabilidad = Column(Float)          # probabilidad de éxito (0-1)
    fecha = Column(DateTime, default=datetime.utcnow)


# Crear las tablas físicamente
Base.metadata.create_all(bind=engine)


# Dependencia para abrir y cerrar la conexión en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
