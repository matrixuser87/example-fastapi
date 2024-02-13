import time

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQL_CONNECTION_STRING = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQL_CONNECTION_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='pwd', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connection to database failed!")
        print("Error: ", error)
        time.sleep(2)
