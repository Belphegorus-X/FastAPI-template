import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from domain.handlers.chat.chat_errors import ChatNotFoundException
from domain.repositories.chat import ChatEntry


@dataclass
class GetChatHistoryQuery:
    chat_id: uuid.UUID


class GetChatHistoryQueryHandler:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def handle(self, query: GetChatHistoryQuery) -> ChatEntry:
        result = await ChatEntry.get_chat_history(query.chat_id, self.session)

        if result is None:
            raise ChatNotFoundException(query.chat_id)

        return result
