from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import engine,get_db
import models,oauth2
import schemas
from typing import List,Optional
from sqlalchemy import func

router = APIRouter()

@router.get('/allposts',response_model=List[schemas.OutPost])
def get_all_posts(db:Session = Depends(get_db), limit : int = 10,skip:int = 0,search:Optional[str]="" ):
    
    posts = db.query(models.Post).filter(models.Post.post.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    print(results)
    return posts


@router.get('/post/{id}',response_model=schemas.OutPost,status_code=status.HTTP_302_FOUND)
def get_post_by_id(id:int,db:Session = Depends(get_db)):
    postid = db.query(models.Post).filter(models.Post.id==id).first()
    if not postid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id {id} not found')
    return postid


@router.post('/postcreate',response_model=schemas.OutPost,status_code=status.HTTP_201_CREATED)
def create_post(Post:schemas.BasePost,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    
    createpost = models.Post(owner_id = current_user.id,  **Post.dict())
    db.add(createpost)
    db.commit()
    db.refresh(createpost)
    return createpost


@router.delete('/postdelete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post_dy_id(id:int,db:Session=Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    deletepost_query = db.query(models.Post).filter(models.Post.id==id)
    deletepost = deletepost_query.first()
    if deletepost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Sorry post with id {id} doez not exist')
    if deletepost.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Not authorize))')
    deletepost_query.delete(synchronize_session=False)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/postupdate/{id}',response_model=schemas.OutPost)
def update_post_by_id(id:int,UpdatePost:schemas.BasePost,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    updatepost = db.query(models.Post).filter(models.Post.id==id)
    byidup = updatepost.first()
    if byidup == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id {id} not found')
    if byidup.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Not authorize')
    updatepost.update(UpdatePost.dict(),synchronize_session="fetch")
    db.commit()
    return updatepost.first()