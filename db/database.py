from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Usar una base de datos temporal en memoria para pruebas unitarias
URL_BD = os.getenv('URL_BASE_DE_DATOS', 'sqlite:///:memory:')

# sqlalchemy engine
# engine = create_engine(URL_BD, connect_args={'client_encoding': 'UTF8'})
engine = create_engine(URL_BD, connect_args={'check_same_thread': False} if "sqlite" in URL_BD else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# sqlalchemy base
Base = declarative_base()

# sqlalchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()