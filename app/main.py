from fastapi import FastAPI , status , Response , HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

# declaring the model
class Post(BaseModel):
    title : str 
    content : str 
    published : bool
    rating : Optional[int] = None
    
# at the moment i am storing the posts in the memory but after that we will store the posts in the postgresql
#  data base
all_posts = []


# function for the getting the post index id
def post_by_id(id):
    for p in all_posts:
        if p.id == id:
            return p
            


app = FastAPI()


@app.get('/')
async def root():
    return {
        'message' : 'hello world!!'
    }
    

# getting the all the post
@app.get('/post')
async def get_posts():
    return {
        "data" : all_posts
    }
    
    
# getting the post using the id
@app.get('/post/{id}')
async def get_post(id: int ,response : Response):
    post = post_by_id(id)
    if post is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post of {id} not found!!')
    return {
        'data' : post
    }
    
    
# create the all the post 
@app.post('/post')
async def create_post(post : Post):
    # storing the post for the user
    new_post = post.dict()
    new_post['id'] = randrange(0,100000000)
    all_posts.append(new_post)
    return {
        "data" : new_post
    }