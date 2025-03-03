from fastapi import FastAPI , status , Response , HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# declaring the model
class Post(BaseModel):
    title : str 
    content : str 
    published : bool
    # rating : Optional[int] = None
    
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


# function for the getting the post index id
def post_by_id(id):
    for p in all_posts:
        if p.id == id:
            return p

#  function for the getting the index of a specific post
def post_index(id):
    for i , p in enumerate(all_posts):
        if p['id'] == id:
            return i
            


app = FastAPI()


@app.get('/')
async def root():
    return {
        'message' : 'hello world!!'
    }
    

# getting the all the post
@app.get('/post')
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    post = cursor.fetchall()
    # print(post)
    return {
        "data" : post
    }
    
    
# getting the post using the id
@app.get('/post/{id}')
async def get_post(id: int ,response : Response):
    # post = post_by_id(id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    post = cursor.fetchone()
    if post is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post of {id} not found!!')
    return {
        'data' : post
    }
    
    
# create the all the post 
@app.post('/post',status_code=status.HTTP_201_CREATED)
async def create_post(post : Post):
    # storing the post for the user
    # new_post = post.dict()
    # new_post['id'] = randrange(0,100000000)
    # all_posts.append(new_post)
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) 
                   RETURNING * """,
                   (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    
    conn.commit()
    
    return {
        "data" : new_post
    }
    
    
# delete a post from the user
@app.delete('/post/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int ):
    # post = post_by_id(id)
    # index = post_index(id)
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with {id} not found to delete!!!')
    # all_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# this is put update for the user post
@app.put('/post/{id}')
async def update_post(id: int, post : Post):
    # index = post_index(id)
    cursor.execute(""" UPDATE posts SET title=%s , content=%s , published=%s WHERE id = %s RETURNING * """,
                   (post.title,post.content,post.published,str(id)))
    
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f'the post {id} not found!!')
    
    # new_post_dict = post.dict()
    # new_post_dict['id'] = id
    # all_posts[index] = new_post_dict
    # return Response(status_code=status.HTTP_205_RESET_CONTENT)
    return {'post' : updated_post}
    