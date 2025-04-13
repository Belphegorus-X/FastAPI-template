import enum

from pydantic.main import BaseModel


class ChatTypeModel(enum.Enum):
    group = "group"
    personal = "personal"


class MessagesModel(BaseModel):
    message_id: str
    chat_id: str
    sender_id: str
    text: str
    is_read: bool


class ChatModel(BaseModel):
    chat_id: str
    name: str
    chat_type: ChatTypeModel
    messages: list[MessagesModel]
