from typing import Optional , List
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import models,schemas,utils
from app.database import engine,get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user",
    tags=["Users"]

)


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def postuser(post:schemas.User , db: Session = Depends(get_db)):
    hash_password = utils.hash(post.password)
    post.password = hash_password
    post = models.User(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{id}",response_model=schemas.UserOut)
def getuser(id :int  , db:Session =Depends(get_db)):
    post = db.query(models.User).filter(models.User.id == id ).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry this id {id} was not exist")
    return post


@router.get("/")
def getall( db:Session = Depends(get_db)):
    post = db.query(models.User).all()
    return post
    