from app.db import Base
from typing import TypeVar, Generic, List, Type
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, Field

MT = TypeVar("MT", bound=Base)  # MT -> ModelType
ST = TypeVar("ST", bound=BaseModel)  # ST -> SchemaType


class BaseRepository(BaseModel, Generic[MT, ST]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    db: Session
    Entity: Type[MT]  # model class definition to db queries

    def get_by_id(self, id: int):
        # model = Type[MT]
        return self.db.get(self.Entity, id)

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(self.Entity).offset(skip).limit(limit).all()

    def create(self, item: ST) -> MT:
        db_item = self.Entity(**item.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, db_item: MT, updated_item: ST):
        for attr, value in updated_item.model_dump().items():
            setattr(db_item, attr, value)
        self.db.commit()
        return db_item

    def delete(self, item: MT):
        self.db.delete(item)
        self.db.commit()
