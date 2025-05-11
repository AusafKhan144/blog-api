from sqlalchemy.ext.declarative import declarative_base
from app.config import DATABASE_CONNECTION_STRING
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(DATABASE_CONNECTION_STRING)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
