import secrets
import time

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.core.config import get_settings
from apps.api.src.core.security.jwt import create_jwt_token
from apps.api.src.core.security.password import verify_password
from apps.api.src.endpoints.auth.models import AccessTokenResponse
from domain.handlers.auth.auth_errors import (
    InvalidPasswordException,
    UserNotFoundException,
)
from domain.repositories.refresh_token import RefreshTokenEntry
from domain.repositories.user import UserEntry


class UserLoginCommand(BaseModel):
    identification: str
    password: str


class UserLoginCommandHandler:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def handle(self, command: UserLoginCommand) -> AccessTokenResponse:
        user = await UserEntry.fetch_user_by_identification(command.identification, self.session)

        if user is None:
            raise UserNotFoundException(command.identification)

        if not verify_password(command.password, user.hashed_password):
            raise InvalidPasswordException(command.identification)

        jwt_token = create_jwt_token(user.user_id)

        refresh_token = await RefreshTokenEntry.insert(
            refresh_token=secrets.token_urlsafe(64),
            expires_at=int(time.time() + get_settings().security.jwt_refresh_token_expire_secs),
            user_id=user.user_id,
            session=self.session,
        )

        return AccessTokenResponse(
            access_token=jwt_token.access_token,
            expires_at=jwt_token.payload.exp,
            refresh_token=refresh_token.refresh_token,
            refresh_token_expires_at=refresh_token.expires_at,
        )
