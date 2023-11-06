from app.db.connection import connect_db


class PostRepository:
  def __init__(self) -> None:
    self.cursor = connect_db()
  
  def find_all(self):
    # this just send the SQL statement to our db
    self.cursor.execute(query="SELECT * FROM posts")
    # run the statement
    posts = self.cursor.fetchall()
    return posts
    