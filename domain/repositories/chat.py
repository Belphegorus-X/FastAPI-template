import enum
import uuid
from datetime import datetime
from typing import Self

from sqlalchemy import Enum, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.types import String, Uuid

from domain.repositories.base import Base


class ChatTypeEntry(enum.Enum):
    group = "group"
    personal = "personal"


class ChatEntry(Base):
    __tablename__ = "chats"

    chat_id: Mapped[str] = mapped_column(
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
    chat_type: Mapped[ChatTypeEntry] = mapped_column(
        Enum(ChatTypeEntry, name="chat_type_entry", native_enum=True),
        nullable=False,
        default=ChatTypeEntry.personal,
    )
    messages: Mapped[list["MessagesEntry"]] = relationship(
        "MessagesEntry",
        back_populates="chat",
    )

    @classmethod
    async def get_chat_history(
        cls, chat_id: str, session: AsyncSession
    ) -> Self | None:
        statement = (
            select(cls)
            .options(selectinload(cls.messages))
            .where(cls.chat_id == chat_id)
        )

        result = await session.execute(statement)
        chat_entry = result.scalar_one_or_none()
        return chat_entry

    @classmethod
    async def insert(
        cls,
        name: str,
        chat_type: ChatTypeEntry,
        created_at: datetime,
        updated_at: datetime,
        session: AsyncSession,
    ) -> Self:
        statement = (
            insert(cls)
            .values(
                name=name,
                chat_type=chat_type,
                created_at=created_at,
                updated_at=updated_at,
            )
            .returning(cls)
        )

        result = await session.execute(statement)
        await session.commit()

        return result.scalar_one()


from domain.repositories.messages import MessagesEntry
