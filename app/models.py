#  models for the orm models
from sqlalchemy import Column , Integer , String , Boolean
from .database import Base

# model for the Post
class Post(Base):
    __tablename__='posts'
    
    # creating the column for the tables
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,default=True)
    