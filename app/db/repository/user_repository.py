from app import schemas
from typing import Type
from app.db import models
from app.auth import oauth2
from app.db.repository.base import BaseRepository
from app.auth.util import get_password_hash, verify_password
from app.schemas.exceptions import UserNotFoundException, InvalidPasswordException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

class UserRepository(BaseRepository[models.User, schemas.UserCreate]):
    Entity: Type[models.User] = models.User

    # Custom repository methods for user model
    def create(self, item: schemas.UserCreate) -> models.User:
        # hash the password attribute
        item.password = get_password_hash(item.password)
        return super().create(item)

    def authenticate(self, user_credentials: OAuth2PasswordRequestForm):
        user = (
            self.db.query(models.User)
            .filter(models.User.email == user_credentials.username)
            .first()
        )
        if not user:
            raise UserNotFoundException(identifier=user_credentials.username)
        if not verify_password(user_credentials.password, user.password):
            raise InvalidPasswordException()

        # create a token and return it
        access_token = oauth2.create_access_token(data={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
