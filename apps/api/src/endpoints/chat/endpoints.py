import uuid

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.endpoints import dependencies
from apps.api.src.endpoints.chat.models import ChatModel
from domain.handlers.chat.get_chat_history import (
    GetChatHistoryQuery,
    GetChatHistoryQueryHandler,
)

router = APIRouter()


@router.get(
    "/history/{chat_id}",
    response_model=ChatModel,
    status_code=status.HTTP_200_OK,
    description="Get message history for the chat",
)
async def get_chat_history(
    chat_id: uuid.UUID = Path(..., title="The Uuid of the chat to fetch history"),
    session: AsyncSession = Depends(dependencies.get_session),
) -> ChatModel:
    query = GetChatHistoryQuery(chat_id=str(chat_id), session=session)
    entry = await GetChatHistoryQueryHandler()(query)

    return ChatModel.from_entry(entry)
