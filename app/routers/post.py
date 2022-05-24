#from sqlalchemy.sql.functions import user
#from starlette.routing import Router
# from _typeshed import Self
# import re
from .. import models,schemas,oauth2
from fastapi import FastAPI , Response ,status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.sql.expression import null
from sqlalchemy import func
from typing import List, Optional


router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
    )
router_group = APIRouter(
    prefix= "/group",
    tags= ['Posts']
    )

# class RetrunPost():
#     def __init__(self,post,comments):
#         self.post = post
#         self.comments = comments



@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), func.count(models.Comment.post_id).label("comments")).join(models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True).join(models.Comment,models.Comment.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return  posts

@router_group.get("/{group_id}/posts", response_model= List[schemas.PostOut], status_code = status.HTTP_200_OK)
def get_posts_by_group(group_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    if not db.query(models.Groups).filter(models.Groups.groups_id == group_id).first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"group with id {group_id} was not found")
    if not db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).filter(models.UserInGroups.user_id == current_user.id).first():
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action, you are not member in this group")
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), func.count(models.Comment.post_id).label("comments")).join(models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True).join(models.Comment,models.Comment.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.group_id == group_id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    if new_post.title == "" or new_post.content == "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the post must contains context and title")
    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except:
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the post")
    return  new_post

@router_group.post("/{group_id}/post", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post_in_group(post: schemas.PostCreate, group_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if not db.query(models.Groups).filter(models.Groups.groups_id == group_id).first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"group with id {group_id} was not found")
    if not db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).filter(models.UserInGroups.user_id == current_user.id).first():
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action, you are not member in this group")
    if post.title == "" or post.content == "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the post must contains context and title")
    new_post = models.Post(owner_id = current_user.id, group_id = group_id ,**post.dict())
    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except:
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the post")
    return  new_post


@router.get("/{id}",response_model= schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), func.count(models.Comment.post_id).label("comments")).join(models.Vote,
       models.Vote.post_id == models.Post.id,
       isouter=True).join(models.Comment,models.Comment.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    if post["Post"].group_id != 0:
        if not db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == post["Post"].group_id).filter(models.UserInGroups.user_id == current_user.id).first():
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action, not member in this group")
    return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    try:
        post_query.delete(synchronize_session= False)
        db.commit()
    except:
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the post")
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()
    return post_query.first()  