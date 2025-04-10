from typing import Optional, Self
import uuid
import enum

from sqlalchemy import Enum, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.types import Uuid, String

from domain.repositories.base import Base
from domain.repositories.messages import MessagesEntry


class ChatTypeEntry(enum.Enum):
    group = "group"
    personal = "personal"

class ChatEntry(Base):
    __tablename__ = "chats"

    chat_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4()),
    )
    name: Mapped[str] = mapped_column(
        String(256), nullable=False, unique=False, index=True,
    )
    chat_type: Mapped[ChatTypeEntry] = mapped_column(
        Enum(ChatTypeEntry), nullable=False, default=ChatTypeEntry.personal,
    )
    messages: Mapped[list["MessagesEntry"]] = relationship("MessagesEntry", back_populates="chat")

    @classmethod
    async def get_chat_history(cls, chat_id: str, session: AsyncSession) -> Optional[Self]:
        statement = select(cls).options(selectinload(cls.messages)).where(cls.chat_id == chat_id)

        result = await session.execute(statement)
        chat_entry = result.scalar_one_or_none()
        return chat_entry
