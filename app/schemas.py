# declaring all the database schemas 
from pydantic import BaseModel

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
class Post(BaseModel):
    title : str
    content : str
    published : bool
