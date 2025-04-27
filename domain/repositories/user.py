import uuid
from typing import Self

from sqlalchemy import exists, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Uuid

from domain.repositories.base import Base


class UserEntry(Base):
    __tablename__ = "user_accounts"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(),
        primary_key=True,
        default=lambda _: uuid.uuid4(),
    )
    username: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
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
    refresh_tokens: Mapped[list["RefreshTokenEntry"]] = relationship(back_populates="userentry")

    @classmethod
    async def fetch_user_by_identification(
        cls,
        identification: str,
        session: AsyncSession,
    ) -> Self | None:
        statement = select(cls).where((cls.email == identification) | (cls.username == identification))

        result = await session.execute(statement)
        user_entry = result.scalar_one_or_none()

        return user_entry

    @classmethod
    async def fetch_user_by_id(
        cls,
        user_id: uuid.UUID,
        session: AsyncSession,
    ) -> Self | None:
        statement = select(cls).where(cls.user_id == user_id)

        result = await session.execute(statement)
        user_entry = result.scalar_one_or_none()
        return user_entry

    @classmethod
    async def exists(
        cls,
        username: str,
        email: str,
        session: AsyncSession,
    ) -> bool:
        statement = select(exists().where((cls.username == username) | (cls.email == email)))

        result = await session.execute(statement)
        return bool(result.scalar())

    @classmethod
    async def insert(
        cls,
        username: str,
        email: str,
        hashed_password: str,
        session: AsyncSession,
    ) -> Self:
        statement = (
            insert(cls)
            .values(
                username=username,
                email=email,
                hashed_password=hashed_password,
            )
            .returning(cls)
        )

        result = await session.execute(statement)
        await session.commit()

        return result.scalar_one()


from domain.repositories.refresh_token import RefreshTokenEntry  # noqa: E402
