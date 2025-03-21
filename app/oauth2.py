# creating the file for the oauth2 base auth system
from jose import JWTError , jwt
from datetime import datetime , timedelta
from . import schemas , database , models
from fastapi import Depends , status , HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# token validation
# 1 . secret key
# 2 . Algorithm
# 3 . time for automatically signed out
# all this should be moved to the env file
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# creating the token
def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp' : expire})
    encoded_jwt =  jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


# function for the verify the access token
def verify_access_token(token : str , credential_exception):
    # decode for the access token
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id = str(id))
    except JWTError as e: 
        print(e)
        raise credential_exception
    except AssertionError as e:
        print(e)
        
    
    return token_data
    
#  fetches current user
def get_current_user(token : str = Depends(oauth2_schema) , db : Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f'could not validate credential',
                                         headers={'WWW.Authenticate' : 'bearer'})
    token =  verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user
    