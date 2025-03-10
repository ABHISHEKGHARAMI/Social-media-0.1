from .. import models, schemas
from fastapi import FastAPI, status, Response, HTTPException, Depends , APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine , get_db


# create the router object for the app
router = APIRouter()
# getting the all the post
@router.get('/post', response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # post = cursor.fetchall()
    post = db.query(models.Post).all()
    # print(post)
    return post


# getting the post using the id
@router.get('/post/{id}', response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    # post = post_by_id(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post of {id} not found!!')
    return post

# create the all the post


@router.post('/post', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # storing the post for the user
    # new_post = post.dict()
    # new_post['id'] = randrange(0,100000000)
    # all_posts.append(new_post)
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s)
    #                RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    # using the orm

    # creating new post
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post = models.Post(**post.dict())
    # saving the instance of the data to the db
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# delete a post from the user
@router.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,  db: Session = Depends(get_db)):
    # post = post_by_id(id)
    # index = post_index(id)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with {id} not found to delete!!!')
    # all_posts.pop(index)
    # delete the post
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# this is put update for the user post
@router.put('/post/{id}', response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # index = post_index(id)
    # cursor.execute(""" UPDATE posts SET title=%s , content=%s , published=%s WHERE id = %s RETURNING * """,
    #                (post.title,post.content,post.published,str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post {id} not found!!')

    # new_post_dict = post.dict()
    # new_post_dict['id'] = id
    # all_posts[index] = new_post_dict
    # return Response(status_code=status.HTTP_205_RESET_CONTENT)
    # print(post)
    # print(updated_data)
    post_query.update(updated_post.dict(),  synchronize_session=False)

    db.commit()

    return post_query.first()
