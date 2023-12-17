from app.db import PostRepository, UserRepository
from app import schemas
from typing import List
from app.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, status, HTTPException, Depends


app = FastAPI()


# * path operations
@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = PostRepository(db=db).get_all()
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = PostRepository(db=db).get_by_id(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return post


@app.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post,
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = PostRepository(db=db).create(post)
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_repository = PostRepository(db=db)

    post = post_repository.get_by_id(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    post_repository.delete(item=post)


@app.put("/posts/{id}", response_model=schemas.Post)
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


# * ---------- User route ----------
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return UserRepository(db=db).create(user)
    