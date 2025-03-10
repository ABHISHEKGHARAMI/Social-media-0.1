#  creating the standalone database file for the database connection

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# database url for the connection
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Abhi1998@@localhost/fastapi'

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
