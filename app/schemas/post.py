from pydantic import BaseModel
from datetime import datetime

"""
Pydantic models / schemas
"""


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# * reading model


class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        """
        Use pydantic's orm_mode (has been renamed to from_attributes)
        It allows to read the data of this model even if it is not a dict, but
        an ORM model (or any arbitrary object with attributes). And with this,
        the Pydantic model is compatible with ORMs, and you can adjust declare it in the
        __response_model__ argument in the path operations.
        """

        from_attributes = True
