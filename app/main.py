from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from app.db.database import Base, engine
from app.db.models import Post
from app.db.schemas import PostCreate
from app.dependencies import DbSession

app = FastAPI()

# To create the tables/ models from code
Base.metadata.create_all(engine)


@app.get("/posts")
# Need to pass db session as param
def get_all_post(db: DbSession):
    statement = select(Post)
    data = db.scalars(statement).all()
    return {"data": data}


@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: DbSession):
    # spreading the model data, spreading
    new_post = Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
def root():
    return "Hello World"


@app.get("/path_params/{path_name}")
def path_by_name(path_name: str):
    return {"path": path_name}


# auto parse and convert string to int
@app.get("/items/{item_id}")
def path_by_item(item_id: int):
    return fake_items_db[item_id]


# query params with optional and default values
@app.get("/query")
def with_query(skip: int = 0, limit: int = 10, q: str | None = None):
    data = fake_items_db[skip : skip + limit]

    if q:
        data.append({"q": q})

    return data


# post req with body
# body only available in post type req
class Item(BaseModel):
    id: int
    name: str
    verified: bool | None = False


@app.post("/with_body", status_code=status.HTTP_201_CREATED)
def return_with_body(item: Item):
    return item


# updated error handling
@app.get("/error")
def get_error(error: bool):
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hell yeah")
    return "Nopes"
