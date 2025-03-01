from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# declaring the model
class Post(BaseModel):
    title : str 
    content : str 
    published : bool
    rating : Optional[int] = None
    
# at the moment i am storing the posts in the memory but after that we will store the posts in the postgresql
#  data base
all_posts = []


app = FastAPI()


@app.get('/')
async def root():
    return {
        'message' : 'hello world!!'
    }
    

# getting the all the post
@app.get('/posts')
async def get_post():
    return {
        "data" : all_posts
    }
    
    
# create the all the post 
@app.post('/posts')
async def create_post(post : Post):
    print(post)
    print(post.dict())
    # storing the post for the user
    new_post = post.dict()
    all_posts.append(new_post)
    return {
        "data" : new_post
    }