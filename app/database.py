#  creating the standalone database file for the database connection
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


# database url for the connection
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)


# creating the session
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# declaring the base
Base = declarative_base()

# for the db


def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()
       
       
       
# # build the connection for the database
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',
#                                 user='postgres',password='Abhi1998@',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('database connection success')
#         break
#     except Exception as error:
#         print(f'connection error : {error}')
#         time.sleep(2)

