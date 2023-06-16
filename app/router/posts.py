from typing import Optional , List
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import func
from app import models,schemas,utils,oauth2
from app.database import engine,get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter(
    prefix="/post",
    tags=['Posts']
)
@router.get("/",response_model=List[schemas.PostOut])
def get_post( db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user),limit:int = 10, skip : int = 0,search: Optional[str] = ""):
    
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts



# @router.get("/")
# def test_posts(db:Session = Depends(get_db)):
#     post=db.query(models.Post).all()
    
#     return {"status":post}





# @app.get("/posts")
# def get_posts():
#     cursor.execute("""select * from posts""")
#     posts = cursor.fetchall()
#     return{"messege":posts}

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):
#     cursor.execute("""INSERT INTO posts(title,content,published ) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data":new_post}

# @app.get("/")
# def root():
#     return {"Message":"Hello world"}

# def find_post(id):
#     for p in my_post:
#         if p['id']==id:
#             return p



# @app.post("/post",status_code=status.HTTP_201_CREATED)
# def create(post:Post):
#     post_dict = post.dict()
#     post_dict['id']=randrange(0,100000)
#     my_post.append(post_dict)
#     return{"Messege":post_dict}


# @app.get("/posts/lastest")
# def get_post():
#     post =my_post[len(my_post)-1]
#     return {"Result":post}


# # @app.get("/posts/{id}")
# # def get_post(id:int , response: Response):
# #     post =find_post(id)
# #     if not post:
# #         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"this id {id} was not found ")
# #     return {"messege":post}


# def find_index(id):
#     for i , p in enumerate(my_post):
#         if p['id']==id:
#             return i


# # @app.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
# # def delete_post(id: int):
# #     index = find_index(id)
# #     if index == None:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} does not exist")
# #     my_post.pop(index)
# #     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def update_post(id :int , post:Post):
#     index = find_index(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"This {id} not exist")
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_post[index]=post_dict
#     return {"Text":post_dict}

# @app.get("/post/{id}")
# def get_post(id : str):
#         cursor.execute("""Select * from posts Where id = %s""",(str(id),))
#         post = cursor.fetchone()
#         if not post:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This id {id} was not found")
#         return {"Messge":post}


# @app.post("/post",status_code=status.HTTP_201_CREATED)
# def post_rup(post:Post,db:Session = Depends(get_db)):
#     # cursor.execute("""insert into posts(title,content,published) values(%s,%s,%s)returning * """,(post.title , post.content , post.published))
#     # post = cursor.fetchone()
#     # conn.commit()
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return {"result":post}

# @app.get("/getpost/{id}")
# def retrive_post(id : int , db: Session = Depends(get_db)):
#     # cursor.execute("""Select * from posts where id =%s""",(str(id),))
#     get = db.query(models.Post).filter(models.Post.id == id).first()
#     # get = cursor.fetchone()
#     if get==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"sorry this id {id} was not found ")
#     return{"result":get}



# @app.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)

# def delete(id : int ,db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id)
#     if post.first()==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"sorry this id {id} was not exist")
#     post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
# @app.put("/update/{id}")
# def update(id : int , post:Post , db :Session = Depends(get_db)):
#     post_query=db.query(models.Post).filter(models.Post.id==id)
#     post = post_query.first()
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Sorry this id {id} was not exist")
#     post_query.update({'title':'update post ','content':'update postest'},synchronize_session=False)
#     db.commit()
#     return {"text":"successful"}
@router.post("/",response_model=schemas.Post)
def post_rup(post :schemas.PostCreated,db:Session = Depends(get_db),current_user: int =Depends(oauth2.get_current_user) ):
    print(current_user.id)
    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    
    db.refresh(new_post)
    return new_post





@router.put("/update/{id}")
def get_post(id : int , post:schemas.PostCreated , db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"This id {id} was not exist")
    
    post_query.update({'title':'Hello TG','content':'Hello Chem'},synchronize_session=False)
    db.commit()
    return {"text":"successful update "}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id : int  , db:Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"this id {id} was not found ")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"Not authorization problem ")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"sucess":"Delete"}


