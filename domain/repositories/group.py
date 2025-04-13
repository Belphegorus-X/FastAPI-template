import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import String, Uuid

from domain.repositories.base import Base


class GroupsEntry(Base):
    __tablename__ = "groups"

    group_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False),
        primary_key=True,
        default=lambda _: str(uuid.uuid4()),
    )
    name: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=False,
        index=True,
    )
    creator_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False),
        ForeignKey("user_accounts.user_id"),
        nullable=False,
    )


class GroupUsers(Base):
    __tablename__ = "group_users"

    group_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False),
        ForeignKey("groups.group_id"),
        nullable=False,
        primary_key=True,
    )
    user_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False),
        ForeignKey("user_accounts.user_id"),
        nullable=False,
        primary_key=True,
    )
