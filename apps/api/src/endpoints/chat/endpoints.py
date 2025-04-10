from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.endpoints import dependencies
from apps.api.src.endpoints.chat.responses import ChatModel

router = APIRouter()

@router.get("/history/{chat_id}", response_model=..., status_code=status.HTTP_200_OK, description="Get message history for the chat")
async def get_chat_history(session: AsyncSession = Depends(dependencies.get_session)) -> ChatModel:
    ...
