from fastapi import FastAPI
import models
from routers import post,user,auth,vote
from database import engine


app = FastAPI()





app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


models.Base.metadata.create_all(bind=engine)