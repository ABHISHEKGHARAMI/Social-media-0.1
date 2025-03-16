from .. import models, schemas , oauth2
from fastapi import FastAPI, status, Response, HTTPException, Depends , APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine , get_db

# router for the vote directory
router = APIRouter(
    prefix = '/votes',
    tags = ['Votes']
)