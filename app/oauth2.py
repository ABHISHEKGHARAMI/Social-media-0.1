# creating the file for the oauth2 base auth system
from jose import JWTError , jwt
from datetime import datetime , timedelta
from . import schemas
from fastapi import Depends , status , HTTPException
from fastapi.security import OAuth2PasswordBearer

# token validation
# 1 . secret key
# 2 . Algorithm
# 3 . time for automatically signed out
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
        token_data = schemas.TokenData(id = id)
    except JWTError as e: 
        print(e)
        raise credential_exception
    except AssertionError as e:
        print(e)
        
    
    return token_data
    
#  fetches current user
def get_current_user(token : str = Depends(oauth2_schema)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f'could not validate credential',
                                         headers={'WWW.Authenticate' : 'bearer'})
    return verify_access_token(token, credential_exception)