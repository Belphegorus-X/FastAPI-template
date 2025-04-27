from typing import Self
from uuid import UUID

from sqlalchemy import BigInteger, Boolean, ForeignKey, String, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.repositories.base import Base


class RefreshTokenEntry(Base):
    __tablename__ = "refresh_tokens"

    refresh_token: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=True,
        index=True,
    )
    used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    expires_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_accounts.user_id", ondelete="CASCADE"),
    )
    user: Mapped["UserEntry"] = relationship(back_populates="refresh_tokens")

    @classmethod
    async def fetch_refresh_token(
        cls,
        refresh_token: str,
        session: AsyncSession,
    ) -> Self | None:
        statement = select(cls).where(cls.refresh_token == refresh_token).with_for_update(skip_locked=True)

        result = await session.execute(statement)
        fetched_token = result.scalar_one_or_none()

        return fetched_token

    @classmethod
    async def mark_used(
        cls,
        refresh_token: str,
        session: AsyncSession,
    ) -> None:
        statement = update(cls).where(cls.refresh_token == refresh_token).values(used=True)

        await session.execute(statement)
        await session.commit()

    @classmethod
    async def insert(
        cls,
        refresh_token: str,
        expires_at: int,
        user_id: UUID,
        session: AsyncSession,
    ) -> Self:
        statement = (
            insert(cls)
            .values(
                refresh_token=refresh_token,
                expires_at=expires_at,
                user_id=user_id,
            )
            .returning(cls)
        )

        result = await session.execute(statement)
        await session.commit()

        return result.scalar_one()


from domain.repositories.user import UserEntry  # noqa: E402
