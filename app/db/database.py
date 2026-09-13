from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

DB_URL = "postgresql://postgres:admin@localhost:5432/pyfastapi"

engine = create_engine(DB_URL, echo=True)


class Base(DeclarativeBase):
    pass


# automatically create session and close on done
def get_db():
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session
