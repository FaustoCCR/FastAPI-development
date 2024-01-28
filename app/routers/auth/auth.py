from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import schemas
from app.db.repository import UserRepository
from app.schemas.exceptions import UserNotFoundException, InvalidPasswordException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        # user_credentials = {"username": "example", "password": "example"}
        return UserRepository(db=db).authenticate(user_credentials)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )
    except InvalidPasswordException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
