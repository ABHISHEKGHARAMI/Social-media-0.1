from .. import models, schemas , oauth2
from fastapi import FastAPI, status, Response, HTTPException, Depends , APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine , get_db


# create the router object for the app
router = APIRouter(
    prefix="/post",
    tags = ['Post']
)
# getting the all the post
@router.get('/', response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db),limit : int = 10):
    # cursor.execute(""" SELECT * FROM posts """)
    # post = cursor.fetchall()
    """
      This is the endpoint for getting all the post for the user.
    """
    # query parameter for the post
    
    post = db.query(models.Post).limit(limit).all()
    # print(post)
    return post


@router.get('/my_posts', response_model=List[schemas.Post])
async def get_user_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                         limit : int = 10):
    # query parameter for the user to set the limit
    """
    Get all posts created by the authenticated user.
    - Requires authentication.
    - Uses the current user's ID from the OAuth2 token.
    """
    posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id).limit(limit).all()
    return posts


# # this is the endpoint for user specific posts
# @router.get('/userPost',response_model=List[schemas.Post])
# async def get_user_post(db : Session = Depends(get_db), current_user = oauth2.get_current_user):
#     """
#     This is the endpoint for the getting the user written or published so far
#     we collect user from the database using the id.
#     """
#     posts = db.query(models.Post).filter(models.Post.owner_id == int(current_user.id)).all()
#     return posts

# getting the post using the id
@router.get('/{id}', response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    """
    This is the endpoint for getting the post using the id.
    
    
    - **id** : Post id to get the post.
    
    
    Returns all the post.
    """
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


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):
    """
    This is the endpoint for the creating a new post,but for that user have to authorize for that.
    
    
    - All the data should be in the body.
    
    
    Returns the newly created object for the post.
    """
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
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # saving the instance of the data to the db
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# delete a post from the user
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Delete Post endpoint for delete post. For that user should be authorized.
    
    
    - **id** : Post id  for the delete
    
    
    Returns the status code for the delete.
    """
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
    # for deleting the post user must delete its own post 
    # unless superuser or stuff user logic is implemented
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user can delete  own post!!")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# this is put update for the user post
@router.put('/{id}', response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Update Post endpoint for the post . For that user should be authorized.
    
    
    - **id** : Post id for the authorized.
    
    
    Returns for the updated post object.
    """
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
    # logic for checking the user
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user should delete own post!!")
        # we try to implement the different roles for user then
        # can delete the posts according to the roles.
    post_query.update(updated_post.dict(),  synchronize_session=False)

    db.commit()
    
    print(current_user.email)

    return post_query.first()
