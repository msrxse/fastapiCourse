from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
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
    return {"data": posts}  # automatically serializes it  - converts it to JSON


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(vars(post))  # converts Pydantic model into dic
    post_dict = vars(post)
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)

    # Send a 201 status code when creating anything!!

    return {"data": post_dict}


@app.get("/posts/{id}")  # id is a path parameter
def get_post(
    id: int,
    response: Response,
):  # automatic extraction happening here
    # type validates is an integer, any string would error
    # print(type(id)) # prints <class 'str'>

    post = find_post(
        id
    )  # I am assured this is an integer - since the type validates it above

    # Use HTTPException to instead return error msg with 404 status id post not found
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} was not found",
        )
    return {"post_detail": post}


@app.delete(
    "/posts/{id}",
    status_code=status.HTTP_204_NO_CONTENT,  # ensure response status is changed to 204
)
def delete_post(
    id: int,
):  # automatic extraction happening here + validation
    # deleting post
    # find the index of the item with that id
    index = find_index_post(id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    my_posts.pop(index)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )  # Dont send any data back on deletes! just the status


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # find the index of the item with that id
    index = find_index_post(id)

    # Use HTTPException to instead return error msg with 404 status id post not found
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} does not exist",
        )

    post_dict = vars(
        post
    )  # takes data received in post and converts it into dictionary
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
