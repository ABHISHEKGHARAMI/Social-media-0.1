from fastapi import FastAPI , status , Response , HTTPException , Depends
from pydantic import BaseModel
from typing import Optional , List
from random import randrange
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models , schemas , utils
from .database import engine , SessionLocal
from .routers import user, post




# declaring the connection for the alchemy
models.Base.metadata.create_all(bind=engine)


app = FastAPI()
       
       
       

    
# at the moment i am storing the posts in the memory but after that we will store the posts in the postgresql
#  data base
all_posts = []


# build the connection for the database
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',
                                user='postgres',password='Abhi1998@',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection success')
        break
    except Exception as error:
        print(f'connection error : {error}')
        time.sleep(2)


# # function for the getting the post index id
# def post_by_id(id):
#     for p in all_posts:
#         if p.id == id:
#             return p

# #  function for the getting the index of a specific post
# def post_index(id):
#     for i , p in enumerate(all_posts):
#         if p['id'] == id:
#             return i
            


    

# include the router path for the user and post
app.include_router(post.router)
app.include_router(user.router)


