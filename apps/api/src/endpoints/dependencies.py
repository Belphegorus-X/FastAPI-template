from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.core import database_session
from apps.api.src.core.security.jwt import JWTTokenPayload, verify_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with database_session.get_async_session() as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> JWTTokenPayload:
    token_payload = verify_jwt_token(token)

    return token_payload
