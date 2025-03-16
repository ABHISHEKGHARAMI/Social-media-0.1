from .. import models, schemas , oauth2
from fastapi import FastAPI, status, Response, HTTPException, Depends , APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine , get_db

# router for the vote directory
router = APIRouter(
    prefix = '/vote',
    tags = ['Votes']
)


# here we will go for different route for vote for post



# route for the vote
@router.post('/',status_code=status.HTTP_201_CREATED)
async def vote(vote : schemas.Vote,db : Session = Depends(get_db) , 
               current_user : int = Depends(oauth2.get_current_user)):
    """
    Endpoint for the add vote or delete vote for the user on the specific post.
    To use the endpoint user should be authorize
    """
    
    # checking the post exist or not
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {vote.post_id} does not exist')
    # logic for the voting
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    # checking the post exist and user voted on this specific post
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='user already voted on this posts..')
        new_vote = models.Vote(user_id=current_user.id,post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {'message':'successfully added vote.'}
    else:
        # user want to delete the vote 
        # check the post not in there raise exception
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="post not found to delete.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message':'successfully deleted post..'}
    