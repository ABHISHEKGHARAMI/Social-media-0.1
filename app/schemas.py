# declaring all the database schemas 
from pydantic import BaseModel , EmailStr
from datetime import datetime

# declaring the model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool
    # rating : Optional[int] = None
    
# create the post for the base
class PostCreate(PostBase):
    pass

# designing the response back for the user to restrict the user to get extra information
class Post(PostBase):
    id : int
    # title : str
    # content : str
    # published : bool
    created_at : datetime
    
    class Config:
        from_attributes = True  # Replaces `orm_mode = True` in Pydantic v2
        extra = "ignore"
        
        
# create the user for the application
class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
# response schema for the user
class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
# schema for the user login
class UserLogin(BaseModel):
    email : EmailStr
    password : str
        
