import psycopg2
from psycopg2.extras import RealDictCursor  # * returns sql operations in a dict format
from app.db.config import Settings

def connect_db():
    try:
        settings = Settings()
        conn = psycopg2.connect(
            host=settings.host,
            database=settings.database,
            user=settings.username,
            password=settings.password,
            cursor_factory=RealDictCursor,
        )

        cursor = conn.cursor()
        print("Database connection was succesfull !", cursor)
        return conn, cursor
    except Exception as error:
        print("Connection failed: ", error, sep="\n")
