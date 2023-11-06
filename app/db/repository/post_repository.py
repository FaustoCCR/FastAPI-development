from app.db.connection import connect_db
from app.db.models import Post


class PostRepository:
    def __init__(self) -> None:
        self.conn, self.cursor = connect_db()

    def find_all(self):
        # this just send the SQL statement to our db
        self.cursor.execute(query="SELECT * FROM posts")
        # run the statement
        return self.cursor.fetchall()

    def create(self, post: Post):
        # * We avoid string interpolation to protect us of SQL Injection
        # * We insert the VALUES as parameters using the %s operator
        self.cursor.execute(
            query="""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
            vars=(post.title, post.content, post.published),
        )

        new_post = self.cursor.fetchone()
        # * commit the changes
        self.conn.commit()
        return new_post

    def find_by_id(self, id: int):
        self.cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
        return self.cursor.fetchone()

    def delete(self, id: int):
        self.cursor.execute(
            """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id))
        )
        deleted_post = self.cursor.fetchone()
        self.conn.commit()
        return deleted_post

    def update(self, id: int, post: Post):
        self.cursor.execute(
            """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
            vars=(post.title, post.content, post.published, str(id)),
        )
        updated_post = self.cursor.fetchone()
        self.conn.commit()
        return updated_post
