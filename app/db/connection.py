from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db.config import Settings

settings = Settings()

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    settings.username, settings.password, settings.host, settings.database
)
# * stablish connection
# we will use this engine in other places
engine = create_engine(SQLALCHEMY_DATABASE_URL)

"""
Each instance of the SessionLocal class will be a database session.
To create a session class, use the function sessionmaker 
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


"""
We will use the function declarative_base() that returns a class.
Later we will inherit from this class to create each of the database models or classes ( the ORM models)
"""

Base = declarative_base()
