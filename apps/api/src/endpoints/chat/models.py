import enum
from typing import Self

from pydantic import UUID4
from pydantic.main import BaseModel

from domain.repositories.chat import ChatEntry, ChatTypeEntry
from domain.repositories.messages import MessagesEntry


class MessagesModel(BaseModel):
    message_id: UUID4
    chat_id: UUID4
    sender_id: UUID4
    text: str
    is_read: bool

    class Config:
        orm_mode = True

    @classmethod
    def from_entry(cls, entry: MessagesEntry) -> Self:
        return cls(
            message_id=entry.message_id,
            chat_id=entry.chat_id,
            sender_id=entry.sender_id,
            text=entry.text,
            is_read=entry.is_read,
        )


class ChatTypeModel(enum.Enum):
    group = "group"
    personal = "personal"

    class Config:
        orm_mode = True

    @classmethod
    def from_entry(cls, entry: ChatTypeEntry) -> Self:
        match entry:
            case entry.personal:
                return ChatTypeModel.personal
            case entry.group:
                return ChatTypeModel.group
            case _:
                raise ValueError(f"Unknown ChatTypeEntry: {entry}")


class ChatModel(BaseModel):
    chat_id: UUID4
    name: str
    chat_type: ChatTypeModel
    messages: list[MessagesModel]

    class Config:
        orm_mode = True

    @classmethod
    def from_entry(cls, entry: ChatEntry) -> Self:
        return cls(
            chat_id=entry.chat_id,
            name=entry.name,
            chat_type=ChatTypeModel.from_entry(entry.chat_type),
            messages=[MessagesModel.from_entry(message) for message in entry.messages],
        )
