from app.db import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text  # allows send string SQL operations


class Post(Base):
    __tablename__ = "posts"  # table name attribute of the database

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String(length=50), nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    # * server_default -> Indicates the that db server will generate a default value for a column field
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
