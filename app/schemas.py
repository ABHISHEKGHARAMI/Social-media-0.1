# declaring all the database schemas 
from pydantic import BaseModel , EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# declaring the model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool
    # rating : Optional[int] = None
    
# create the post for the base
class PostCreate(PostBase):
    pass

# response schema for the user


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

# designing the response back for the user to restrict the user to get extra information
class Post(PostBase):
    id : int
    # title : str
    # content : str
    # published : bool
    created_at : datetime
    owner_id : int
    owner : UserOut
    
    class Config:
        from_attributes = True  # Replaces `orm_mode = True` in Pydantic v2
        extra = "ignore"
        
# creating the post schema with the vote result
class PostOut(BaseModel):
    Post : Post
    votes : int
    
    class Config:
        from_attributes = True  # Replaces `orm_mode = True` in Pydantic v2
        extra = "ignore"
        
        
# create the user for the application
class UserCreate(BaseModel):
    email : EmailStr
    password : str
    

    
# schema for the user login
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
    
        
# Schema token for the oauth2
class Token(BaseModel):
    access_token : str
    token_type : str
    
# schema for token data
class TokenData(BaseModel):
    id : Optional[str] = None
    
    
# schema for the vote model
class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)