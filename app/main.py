from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Stored in memory temporarily
my_posts = [
    {"title": "title of post 1", "content": "Content of post 1", "id": 1},
    {"title": "title of post 2", "content": "Content of post 2", "id": 2},
]


# Defo not best practices
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):  # enumerate gets a counter in a loop
        if p["id"] == id:
            return i


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # defaults to true
    rating: Optional[int] = None  # truly optional field with default of None


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="practical_python",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(4)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()

    conn.commit()

    return {"data": posts}  # automatically serializes it  - converts it to JSON


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()

    return {"data": new_post}


@app.get("/posts/{id}")  # id is a path parameter
def get_post(
    id: int,
):  # automatic extraction happening here
    # type validates is an integer, any string would error
    cursor.execute(
        """SELECT * FROM posts WHERE id = %s""", (str(id),)
    )  # the comma 2 chars from the right is important!
    post = cursor.fetchone()

    # Use HTTPException to instead return error msg with 404 status id post not found
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return {"post_detail": post}


@app.delete(
    "/posts/{id}",
    status_code=status.HTTP_204_NO_CONTENT,  # ensure response status is changed to 204
)
def delete_post(
    id: int,
):  # automatic extraction happening here + validation
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()

    conn.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )  # Dont send any data back on deletes! just the status


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (
            post.title,
            post.content,
            post.published,
            str(id),
        ),
    )
    updated_post = cursor.fetchone()

    conn.commit()

    # Use HTTPException to instead return error msg with 404 status id post not found
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    return {"data": updated_post}
