from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Session

DB_URL = "postgresql://postgres:admin@localhost:5432/pyfastapi"

engine = create_engine(DB_URL, echo=True)


# MappedAsDataclass to init the mapped types for autocomplete
class Base(MappedAsDataclass, DeclarativeBase):
    pass


# automatically create session and close on done
def get_db():
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session
