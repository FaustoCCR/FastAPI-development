from app import schemas
from app.db import models
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

"""
By creating functions that are only dedicated to interacting with 
the database (get a user or an item) independent of your path operation 
function, you can more easily reuse them in multiple parts and also 
add unit tests for them.
"""


class PostRepository(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: Session

    def get_by_id(self, id: int):
        return self.db.get(models.Post, id)

    def get_all(self, skip: int = 0, limit: int = 100):
        # sql_statement = db.query(Post)
        # print(sql_statement)
        # posts = sql_statement.all() => applies the query
        return self.db.query(models.Post).offset(skip).limit(limit).all()

    def create(self, item: schemas.PostCreate):
        db_item = models.Post(**item.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(
            db_item
        )  # reload the attributes in the given instance with new data from the db
        return db_item

    def update(self, db_item: models.Post, updated_item: schemas.PostCreate):
        for attr, value in updated_item.model_dump().items():
            setattr(db_item, attr, value)
        self.db.commit()
        return db_item

    def delete(self, item: models.Post):
        self.db.delete(item)
        self.db.commit()
