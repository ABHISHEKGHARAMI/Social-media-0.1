# router for user authentication for the user
from fastapi import FastAPI , Depends , status , HTTPException , APIRouter , Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas , models , utils

router = APIRouter(
    tags=['Authentication']
)

# user login
@router.post('/login')
async def login( user_credential : schemas.UserLogin,db : Session = Depends(get_db)):
    # accessing the database
    user = db.query(models.User).filter(models.User.email == user_credential.email).first()
    
    # if user does not exist raise an error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid credentials')
    # checking password
    if not utils.check(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid credential.")
        
    # at this point user is valid then request the token will create then return the token
    return {'token': 'user_token'}
    
        
    
