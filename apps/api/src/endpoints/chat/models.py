import enum
from typing import Self

from pydantic.main import BaseModel

from domain.repositories.chat import ChatEntry, ChatTypeEntry
from domain.repositories.messages import MessagesEntry


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


class MessagesModel(BaseModel):
    message_id: str
    chat_id: str
    sender_id: str
    text: str
    is_read: bool

    class Config:
        orm_mode = True

    @classmethod
    def from_entry(cls, entry: MessagesEntry) -> Self:
        return MessagesModel(
            message_id=entry.message_id,
            chat_id=entry.chat_id,
            sender_id=entry.sender_id,
            text=entry.text,
            is_read=entry.is_read
        )


class ChatModel(BaseModel):
    chat_id: str
    name: str
    chat_type: ChatTypeModel
    messages: list[MessagesModel]

    class Config:
        orm_mode = True

    @classmethod
    def from_entry(cls, entry: ChatEntry) -> Self:
        return ChatModel(
            chat_id=entry.chat_id,
            name=entry.name,
            chat_type=ChatTypeModel.from_entry(entry.chat_type),
            messages=[MessagesModel.from_entry(message) for message in entry.messages]
        )
