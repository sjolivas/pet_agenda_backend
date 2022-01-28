from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DB_PASSWORD = os.getenv("DB_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql://myuser:{DB_PASSWORD}@localhost/pet_agenda_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
