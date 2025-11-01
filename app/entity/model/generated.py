import datetime
import uuid

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        UniqueConstraint("username", name="users_username_key"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    username: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)

    search_logs: Mapped[list["SearchLogs"]] = relationship("SearchLogs", back_populates="user")


class SearchLogs(Base):
    __tablename__ = "search_logs"
    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_search_logs_user_id"),
        PrimaryKeyConstraint("id", name="search_logs_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    query: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text("now()"))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text("now()"))
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid)

    user: Mapped["Users"] = relationship("Users", back_populates="search_logs")
    search_feedbacks: Mapped[list["SearchFeedbacks"]] = relationship("SearchFeedbacks", back_populates="search_log")


class SearchFeedbacks(Base):
    __tablename__ = "search_feedbacks"
    __table_args__ = (
        ForeignKeyConstraint(
            ["search_log_id"],
            ["search_logs.id"],
            name="search_feedbacks_search_log_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="search_feedbacks_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    search_log_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    is_relevant: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text("now()"))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text("now()"))

    search_log: Mapped["SearchLogs"] = relationship("SearchLogs", back_populates="search_feedbacks")
