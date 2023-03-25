from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import engine,get_db
import models
import schemas
import utils






router = APIRouter()

@router.get('/allusers')
def all_users(db: Session = Depends(get_db)):
    allusers = db.query(models.User).all()
    return allusers


@router.get('/user/{id}',response_model=schemas.OutUser,status_code=status.HTTP_302_FOUND)
def user_id(id:int,db: Session = Depends(get_db)):
    userid = db.query(models.User).filter(models.User.id==id).first()
    if not userid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    return userid


@router.post('/createuser',response_model=schemas.OutUser,status_code=status.HTTP_201_CREATED)
def create_user(User:schemas.BaseUser,db:Session=Depends(get_db)):

    hashed_password = utils.hash(User.password)
    User.password = hashed_password


    createuser = models.User(**User.dict())
    db.add(createuser)
    db.commit()
    db.refresh(createuser)
    return createuser


@router.delete('/deleteuser/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int,db: Session = Depends(get_db)):
    deleteuser = db.query(models.User).filter(models.User.id==id).delete("fetch")
    db.commit()
    return deleteuser


@router.put('/updateuser/{id}',response_model=schemas.OutUser)
def update_user_id(id:int,UpdateUser:schemas.BaseUser,db:Session=Depends(get_db)):
    updateuserid=db.query(models.User).filter(models.User.id==id)
    updateuser = updateuserid.first()
    if updateuser == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f'User with id {id} not found')
    updateuserid.update(UpdateUser.dict(),synchronize_session="fetch")
    db.commit()
    return updateuserid.first()