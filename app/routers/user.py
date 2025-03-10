from .. import models, schemas, utils
from fastapi import FastAPI, status, Response, HTTPException, Depends , APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine, get_db


# creating the router instance
router = APIRouter()
# creating new user
@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hashed the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    # creating new user
    new_user = models.User(**user.dict())
    # saving it to database
    db.add(new_user)
    # commit the db
    db.commit()
    # refresh the database
    db.refresh(new_user)
    return new_user


# get the specific user data using the id
@router.get('/users/{id}', response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    # query the db model for the specific user
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user of {id} does not exist in the db.')
    # else return the user
    return user
