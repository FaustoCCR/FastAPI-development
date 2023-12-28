from app import schemas
from typing import List
from app.db import PostRepository
from sqlalchemy.orm import Session
from app.dependencies import get_db
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/posts", tags=["posts"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = PostRepository(db=db).get_all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = PostRepository(db=db).get_by_id(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post,
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = PostRepository(db=db).create(post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_repository = PostRepository(db=db)

    post = post_repository.get_by_id(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    post_repository.delete(item=post)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    post_repository = PostRepository(db=db)

    post = post_repository.get_by_id(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    return post_repository.update(db_item=post, updated_item=updated_post)
