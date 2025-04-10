import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, Uuid, String
from sqlalchemy.sql.schema import ForeignKey
from domain.repositories.base import Base
from domain.repositories.chat import ChatEntry

class MessagesEntry(Base):
    __tablename__ = "messages"

    message_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4()),
    )
    chat_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), ForeignKey("chats.chat_id"), nullable=False,
    )
    sender_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), ForeignKey("user_accounts.user_id"), nullable=False,
    )
    text: Mapped[str] = mapped_column(
        String(4096), nullable=False,
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean, default=False,
    )
    chat: Mapped["ChatEntry"] = relationship("ChatEntry", back_populates="messages")
