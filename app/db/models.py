from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    # id = Column(Integer, primary_key=True, nullable=False)
    # title = Column(String, nullable=False)
    # content = Column(String, nullable=False)
    # published = Column(Boolean, default=True)

    # init for telling the orm dont provide during initialisation
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    # need to place server default as we need to maintain it from server
    # default=True for making it optional
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped[User] = relationship(
        back_populates="posts",
        init=False,
    )
    likes: Mapped[list[PostLike]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True,
        init=False,
    )
    published: Mapped[bool] = mapped_column(
        Boolean, server_default="true", default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), init=False
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    posts: Mapped[list[Post]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        init=False,
    )
    post_likes: Mapped[list[PostLike]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        init=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), init=False
    )


class PostLike(Base):
    __tablename__ = "post_likes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False,
    )

    user: Mapped[User] = relationship(
        back_populates="post_likes",
        init=False,
    )

    post: Mapped[Post] = relationship(
        back_populates="likes",
        init=False,
    )
