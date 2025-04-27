import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import Boolean, String, Uuid

from domain.repositories.base import Base


class MessagesEntry(Base):
    __tablename__ = "messages"

    message_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(),
        primary_key=True,
        default=lambda _: str(uuid.uuid4()),
    )
    chat_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(),
        ForeignKey("chats.chat_id"),
        nullable=False,
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(),
        ForeignKey("user_accounts.user_id"),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        String(4096),
        nullable=False,
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    chat: Mapped["ChatEntry"] = relationship("ChatEntry", back_populates="messages")


from domain.repositories.chat import ChatEntry  # noqa: E402
