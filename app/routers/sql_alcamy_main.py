from fastapi import FastAPI,status,Depends,HTTPException, Response,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models,oauth2
from typing import List,Optional
from ..schemas import posts,PostResponseModel,PostOut

router = APIRouter(
    prefix="/posts",
    tags=['UsingSqlalcami']
)

#sqlalcami,response_model = List[PostResponseModel]
@router.get("/",response_model = List[PostOut])
def test_db(db:Session= Depends(get_db), current_user:int = Depends(oauth2.get_current_user),limit:int=10,skip: int = 0,search: Optional[str] = ""):
    # post = db.query(models.posts).filter(models.posts.title.contains(search)).limit(limit).offset(skip).all()#http://127.0.0.1:8000/posts?limit=3&skip=1&search=new
    # post = db.query(models.posts).limit(limit).offset(skip).all()
    # post = db.query(models.posts).all()
    # post = db.query(models.posts).filter(models.posts.owner_id ==current_user.id).all()
    # print(post)
    post = db.query(models.posts, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.posts.id, isouter=True).group_by(models.posts.id).filter(models.posts.title.contains(search)).limit(limit).offset(skip).all()
    # print(post)
    # print(post.all())
    return post


@router.get("/{id}")
def get_data_by_id(id:int, db:Session= Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    check_post = db.query(models.posts).filter(models.posts.id == id).first()
    check_post = db.query(models.posts, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.posts.id, isouter=True).group_by(models.posts.id).filter(models.posts.id == id).id()
    if not check_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return{'post_for_id': check_post}


@router.post("/")
def create_postd(post:posts, db:Session= Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    sheck_post = models.posts(owner_id =current_user.id, **post.dict())
    # sheck_post = models.posts(title=post.title,content=post.content,published=post.published)
    db.add(sheck_post)
    db.commit()
    db.refresh(sheck_post)
    return {"new_post":sheck_post}


@router.delete("/{id}")
def get_delete_post(id:int, db:Session= Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    check_post = db.query(models.posts).filter(models.posts.id == id)
    post = check_post.first()
    if check_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    check_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#returning pydentic model as a response 
@router.put("/{id}",response_model = PostResponseModel)
def data_update(id:int,post:posts, db:Session= Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    
    check_post = db.query(models.posts).filter(models.posts.id == id)
    post = check_post.first()
    if check_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    check_post.update(post.dict(),synchronize_session=False)
    db.commit()

    return check_post.first()
    