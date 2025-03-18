from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from . import models 
from .database import engine 
from .routers import user, post , auth , vote
from .config import settings




# declaring the connection for the alchemy
models.Base.metadata.create_all(bind=engine)

origins = ["*"]


app = FastAPI(
    title = 'Social Media API',
    description="This API allows users to register, login, create posts, and interact with other users.",
    version="1.0.0",
    contact={
        "name": "Abhishek Gharami",
        "email": "abhishekgharami1998@gmail.com",
    },
    license_info={
        "name": "MIT License",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
       
       
       

    
# at the moment i am storing the posts in the memory but after that we will store the posts in the postgresql
#  data base
all_posts = []




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
app.include_router(auth.router)
app.include_router(vote.router)


