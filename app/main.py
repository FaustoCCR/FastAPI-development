from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from app.db import PostRepository
import json

app = FastAPI()

# * repositories
post_repository = PostRepository()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_index(id: int):
    # find the index of the item to delete or update
    return next((index for index, item in enumerate(data) if item["id"] == id), None)


with open("posts.json") as json_file:
    data = json.load(json_file)


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
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000)
    data.append(post_dict)
    return {"data": post_dict}


# * path parameter
@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = next((post for post in data if post["id"] == id), None)
    if not post:
        """response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id {id} was not found"}"""
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)

    if index == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist"
        )
    data.pop(index)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index(id)

    if index == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist"
        )
    post_dict = post.model_dump()
    post_dict["id"] = id
    data[index] = post_dict
    return {"data": post_dict}
