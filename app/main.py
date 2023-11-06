from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from app.db import PostRepository
from app.db.models import Post
import json

app = FastAPI()

# * repositories
post_repository = PostRepository()


# * path operations
@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/posts")
def get_posts():
    posts = post_repository.find_all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post = post_repository.create(post)
    return {"data": new_post}


# * path parameter
@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = post_repository.find_by_id(id)
    if not post:
        """response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id {id} was not found"}"""
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deleted_post = post_repository.delete(id)

    if deleted_post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist"
        )


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    updated_post = post_repository.update(id, post)

    if updated_post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist"
        )
    return {"data": updated_post}
