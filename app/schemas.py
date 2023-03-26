from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional


#---------------------------------------USER--------------------------------


class BaseUser(BaseModel):
    name:str
    last_name:str
    email:EmailStr
    password:str

#Responce
class OutUser(BaseUser):
    id:int
    created_at:datetime

    class Config():
        orm_mode = True



#---------------------------------------POST---------------------------------


class BasePost(BaseModel):
    post:str



    class Config():
        orm_mode = True

#Responce

class OutPost(BasePost):
    created_at:datetime
    id:int
    owner_id:int
    owner: OutUser
    
    class Config():
        orm_mode = True

class VotePost(BasePost):
    post:OutPost
    votes:int

    class Config():
        orm_mode = True

#---------------------------------------LOGIN------------------------------


class UserLogin(BaseModel):
    email:EmailStr
    password:str


#-------------------------------------TOKEN--------------------------------

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str]=None
    



#-------------------------------------VOTE--------------


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)