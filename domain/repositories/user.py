import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Uuid

from domain.repositories.base import Base


class UserEntry(Base):
    __tablename__ = "user_accounts"

    user_id: Mapped[str] = mapped_column(
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
    email: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
