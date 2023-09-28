from typing import Optional
from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor



app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                            password='Token@1234', cursor_factory= RealDictCursor)
    cursor= conn.cursor()
    print("Database connection was successfull!")
except Exception as error:
    print("Connecting to database is failed")
    print("Error :", error)


my_post = [{"title": "title odf post 1", "content": "content of post 1", "id": 1},
           {"title": "favorite food", "content": "I like Pizza", "id": 2}]


def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i


# user = {1:{"name":"sourabh","language":"python"}}
#
# @app.get("/{id}")
# def root(id: int):
#     data = user[id]
#     print(data)
#     return data
#
# @app.post("/{id}")
# def root(id: int, data: dict):
#     user[id]=data
#     print(user)
#     return data
#
# @app.put("/{id}")
# def root(id: int, data: dict):
#     user[id]=data
#     print(user)
#     return data

@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title:{payload['title']} content:{payload['content']}"}


@app.post("/createpost2")
def create_post_2(new_post: Post):
    print(new_post.title, new_post.content, new_post.rating, new_post.published)
    print(new_post.dict())
    return {"data": new_post}


@app.post("/post")
def create_post_3(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_post.append(post_dict)
    return {"data": my_post}


@app.get("/post")
def getdata():
    return {"data": my_post}


@app.get("/post/latest")
def get_latest_post():
    post = my_post[len(my_post) - 1]
    return {"Details": post}


@app.get("/post/{id}")
def getdata(id: int, response: Response):
    post = find_post(id)
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return {"post details": post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    my_post.pop(index)
    return {"message": "This post was Successfully Deleted"}
    # return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.put("/post/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {"data": post_dict}
