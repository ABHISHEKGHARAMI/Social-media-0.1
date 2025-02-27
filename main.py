from fastapi import FastAPI
from pydantic import BaseModel

# declaring the model
class Post(BaseModel):
    title : str 
    content : str 


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
        "data" : "all the posts."
    }
    
    
# create the all the post 
@app.post('/posts')
async def create_post(post : Post):
    print(post)
    print(post.dict())
    return {
        "data" : post
    }