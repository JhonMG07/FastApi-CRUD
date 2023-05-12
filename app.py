from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid
from fastapi.responses import JSONResponse

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
@app.get("/posts")
def get_posts():
    return posts


# Escribir un post/ guardarlo


@app.post("/posts") #usar responsemodel para enviar un codigo especifico
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
    raise HTTPException(status_code=404, detail="Post not found")


# Eliminar post , necesuito encontrar el indice para poder eliminarlo


@app.delete("/posts/{id}")
def delete_post_by_id(id: str):
    for index, post in enumerate(posts):
        if post["id"] == id:
            posts.pop(index)
            return {"message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")


# Editar post


@app.put("/posts/{id}")
def update_post_by_id(id: str, updated_post: Post):
    for index, post in enumerate(posts):
        if post["id"] == id:
            posts[index]["title"] = updated_post.title
            posts[index]["content"] = updated_post.content
            posts[index]["author"] = updated_post.author
            return {"message": "Post updated"}

    raise HTTPException(status_code=404, detail="Post not found")
