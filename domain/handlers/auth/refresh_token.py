import secrets
import time

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.core.config import get_settings
from apps.api.src.core.security.jwt import create_jwt_token
from apps.api.src.endpoints.auth.models import AccessTokenResponse
from domain.handlers.auth.auth_errors import (
    RefreshTokenAlreadyUsedException,
    RefreshTokenExpiredException,
    RefreshTokenNotFoundException,
)
from domain.repositories.refresh_token import RefreshTokenEntry


class RefreshTokenCommand(BaseModel):
    refresh_token: str


class RefreshTokenCommandHandler:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def handle(self, command: RefreshTokenCommand) -> AccessTokenResponse:
        token = await RefreshTokenEntry.fetch_refresh_token(command.refresh_token, self.session)

        if token is None:
            raise RefreshTokenNotFoundException(refresh_token=command.refresh_token)

        if time.time() > token.expires_at:
            raise RefreshTokenExpiredException(refresh_token=command.refresh_token)

        if token.used:
            raise RefreshTokenAlreadyUsedException(refresh_token=command.refresh_token)

        await RefreshTokenEntry.mark_used(token.refresh_token, self.session)

        jwt_token = create_jwt_token(token.user_id)

        refresh_token = await RefreshTokenEntry.insert(
            refresh_token=secrets.token_urlsafe(64),
            expires_at=int(time.time() + get_settings().security.jwt_refresh_token_expire_secs),
            user_id=token.user_id,
            session=self.session,
        )

        return AccessTokenResponse(
            access_token=jwt_token.access_token,
            expires_at=jwt_token.payload.exp,
            refresh_token=refresh_token.refresh_token,
            refresh_token_expires_at=refresh_token.expires_at,
        )
