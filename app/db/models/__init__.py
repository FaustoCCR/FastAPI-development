from app.db.models.post import Post
from app.db.models.user import User

"""
Create models from the Base class
SQLAlchemy uses the term "model" to refer to these classes and instances
that interact with the database.
"""
__all__ = ["Post", "User"]
