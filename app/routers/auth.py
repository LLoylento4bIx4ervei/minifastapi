from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import engine,get_db
import database,schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 




router = APIRouter()



@router.post('/login',response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    get_login = db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not get_login:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials((')
                                            #Hashed password from db
    if not utils.verify(user_credentials.password,get_login.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    

#CREATE A TOKEN
    access_token = oauth2.create_access_token(data = {'user_id':get_login.id})
    return {"access_token":access_token,"token_type":"bearer"}
