from fastapi import FastAPI
from app.routers import user, post, auth

app = FastAPI()


# * path operations
@app.get("/")
def root():
    return {"message": "Hello world"}


# * routers
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
