# router for user authentication for the user
from fastapi import FastAPI , Depends , status , HTTPException , APIRouter , Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas , models , utils , oauth2

router = APIRouter(
    tags=['Authentication']
)

# user login
@router.post('/login', response_model = schemas.Token)
async def login( user_credential : OAuth2PasswordRequestForm = Depends() ,db : Session = Depends(get_db)):
    # accessing the database
    """
    This endpoint allows users to login by providing their username and password.

    - **username**: The registered email address of the user.
    - **password**: The associated password for the account.

    Returns an access token that can be used to authenticate further API requests.
    """
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    
    # if user does not exist raise an error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid credentials')
    # checking password
    if not utils.check(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credential.")
        
    # at this point user is valid then request the token will create then return the token
    access_token = oauth2.create_access_token(data={'user_id': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}
    
        
    
