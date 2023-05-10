from fastapi import FastAPI
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

posts: list = []

# Post Model


class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False


# Ruta inicial/ home
@app.get("/")
def read_root():
    return {"welcome": "Welcome to my Rest Api"}


# Obtener todos los post
@app.get("/post")
def get_posts():
    return posts


# Escribir un post/ guardarlo


@app.post("/posts")
def save_post(post: Post):
    # genero la id automatica necesito convertiro en str
    post.id = str(uuid())

    # convierte en diccionario y lo añade a la lista
    posts.append(post.dict())

    return posts[-1]  # me devuelve el arrelo del final


# Obtener un solo post


@app.get("/posts/{id}")
def get_post_by_id(id: str):
    for post in posts:
        if post["id"] == id:
            return post
    return "not found"