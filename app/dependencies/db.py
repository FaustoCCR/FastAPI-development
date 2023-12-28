from app.db import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)  # create all the tables and fields automatically

# Dependency


def get_db():
    """We need to have an independent database session/connection per request

    Yields:
        _generator_: This will create the new session and then close it once the request is finished
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
