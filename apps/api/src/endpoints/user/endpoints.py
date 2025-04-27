from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.core.security.jwt import JWTTokenPayload
from apps.api.src.endpoints.dependencies import get_current_user, get_session
from apps.api.src.endpoints.user.models import UserModel
from domain.handlers.user.get_user import GetUserQuery, GetUserQueryHandler

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get(
    "/me/",
    response_model=UserModel,
    description="Get user info",
    status_code=200,
)
async def get_me(
    current_user: JWTTokenPayload = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> UserModel:
    query = GetUserQuery(user_id=UUID(current_user.sub))
    entry = await GetUserQueryHandler(session).handle(query)

    return UserModel.from_entry(entry)
