import enum
from typing import Literal

from pydantic import UUID4, BaseModel


class ChatEventType(enum.Enum):
    send = "send"
    read = "read"

    class Config:
        orm_mode = True


class SendMessageEvent(BaseModel):
    text: str


class SendEvent(BaseModel):
    event_type: Literal[ChatEventType.send]
    chat_id: UUID4
    data: SendMessageEvent


class ReadMessageEvent(BaseModel):
    message_id: str


class ReadEvent(BaseModel):
    event_type: Literal[ChatEventType.read]
    chat_id: UUID4
    data: ReadMessageEvent


ChatEvents = ReadEvent | SendEvent
