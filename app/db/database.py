from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Session

from app.settings import settings

engine = create_engine(settings.DB_URL, echo=True)


# MappedAsDataclass to init the mapped types for autocomplete
class Base(MappedAsDataclass, DeclarativeBase):
    pass


# automatically create session and close on done
def get_db():
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session
