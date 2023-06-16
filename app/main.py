from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from . import models
from . database import engine
from .router import posts , users,auth 
from .router import vote
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

my_post = [{"title":"Hello ah jm","content":"BROBRO","id":2},{"title":"BEOEB","content":"jumanji","id":5}]
#First priority 
orgins = ["https://www.google.com/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
#Second priority

