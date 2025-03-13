#  models for the orm models
from sqlalchemy import Column , Integer , String , Boolean , TIMESTAMP , ForeignKey
from .database import Base
from sqlalchemy.sql import text , func
from sqlalchemy.orm import relationship

# model for the Post
class Post(Base):
    __tablename__='posts'
    
    # creating the column for the tables
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='True',nullable=False)
    created_at = Column(TIMESTAMP,nullable=False,server_default=func.now())
    
    
    # setting up the foreign  key for the user
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    
    # fetching some information about the user for who created the post
    owner  = relationship("User")
    
    
    
# model for the user
class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False,unique=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    