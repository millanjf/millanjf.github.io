# source venv/bin/activete
# uvicorn main:app --reload

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    number: Optional[int] = None
    content: str
    published: bool = True

# class UpdatePost():

    
my_posts =[{"tittle":"tittle post 1","content":"content pòst 1", "id":1},
          {"tittle":"tittle post 2","content":"content pòst 2", "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
            
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/login")
async def log_user():
    return {"message": "log user"}

@app.get("/posts")
# async def log_user():
#     return {"message": "this is your post"}
def get_post():
    return {"data": my_posts}

@app.post("/posts")
#def create_post(payload: dict = Body(...)):
    # print(payload)
    # return {"new_post": f"title {payload['title']} content: {payload['content']}"}

# def create_post(post: Post):
#     print (post.published)
#     print(post.model_dump())
#     return {"data": post}
def create_post(post: Post, status_code=status.HTTP_201_CREATED):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_lattest():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/posts/{id}")
# def get_post(id:int, response: Response):
def get_post(id:int):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return{"post detasil":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_post(id:int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"pos with id: {id} does not exists")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"pos with id: {id} does not exists")
    post_dict = post.model_dump()
    post_dict["id"] =id
    my_posts[index] = post_dict
    return{"data":"post_dict"}
