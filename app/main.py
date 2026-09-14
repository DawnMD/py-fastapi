from fastapi import FastAPI

from app.db.database import Base, engine
from app.routers import auth, post, user

app = FastAPI()

# To create the tables/ models from code
Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
