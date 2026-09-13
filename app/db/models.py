from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    # id = Column(Integer, primary_key=True, nullable=False)
    # title = Column(String, nullable=False)
    # content = Column(String, nullable=False)
    # published = Column(Boolean, default=True)\
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    # need to place server default as we need to maintain it from server
    published: Mapped[bool] = mapped_column(Boolean, server_default="true")
