from typing import Any
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.endpoints.chat.responses import ChatModel
from domain.handlers.chat.chat_errors import ChatNotFoundException
from domain.repositories.chat import ChatEntry

@dataclass
class GetChatHistoryQuery:
    chat_id: str
    session: AsyncSession

class GetChatHistoryQueryHandler:
    async def __call__(self, query: GetChatHistoryQuery) -> ChatEntry:
        result = await ChatEntry.get_chat_history(query.chat_id, query.session)

        if result is None:
            raise ChatNotFoundException

        return result
