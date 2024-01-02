"""
Schemas: Pydantic and custom models
These pydantic models define more or less a "schema" (a valid data shape)
"""

from app.schemas.post import Post, PostCreate
from app.schemas.user import User, UserCreate, UserLogin

__all__ = ["PostCreate", "Post", "User", "UserCreate", "UserLogin"]
