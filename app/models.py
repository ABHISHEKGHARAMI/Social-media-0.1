#  models for the orm models
from sqlalchemy import Column , Integer , String , Boolean , TIMESTAMP
from .database import Base
from sqlalchemy.sql import text , func

# model for the Post
class Post(Base):
    __tablename__='posts'
    
    # creating the column for the tables
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='True',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    