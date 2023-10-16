from typing import Optional, List
from random import randrange
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.main import BaseModel
# from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models, schemas, utils
from .database import engine
from .routers import post, user, auth

# pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='Token@1234', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connecting to database is failed")
#         print("Error :", error)
#         time.sleep(3)

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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

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
