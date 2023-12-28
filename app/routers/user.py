from app import schemas
from app.db import UserRepository
from sqlalchemy.orm import Session
from app.dependencies import get_db
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return UserRepository(db=db).create(user)


@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = UserRepository(db=db).get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found",
        )
    return user
