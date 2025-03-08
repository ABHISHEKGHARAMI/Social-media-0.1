# declaring all the database schemas 
from pydantic import BaseModel

# declaring the model
class Post(BaseModel):
    title: str
    content: str
    published: bool
    # rating : Optional[int] = None
