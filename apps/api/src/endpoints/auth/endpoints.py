from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from apps.api.src.endpoints import dependencies
from apps.api.src.endpoints.auth.models import (
    AccessTokenResponse,
    RefreshTokenRequest,
    UserCreateRequest,
)
from apps.api.src.endpoints.user.models import UserModel
from domain.handlers.auth.login_user import UserLoginCommand, UserLoginCommandHandler
from domain.handlers.auth.refresh_token import (
    RefreshTokenCommand,
    RefreshTokenCommandHandler,
)
from domain.handlers.auth.register import (
    RegisterUserCommand,
    RegisterUserCommandHandler,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/login/",
    response_model=AccessTokenResponse,
    status_code=status.HTTP_200_OK,
    description="OAuth2 compatible token, get an access token for future requests using username and password",
)
async def access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(dependencies.get_session),
) -> AccessTokenResponse:
    command = UserLoginCommand(identification=form_data.username, password=form_data.password)
    result = await UserLoginCommandHandler(session).handle(command)

    return result


@auth_router.post(
    "/refresh-token/",
    response_model=AccessTokenResponse,
    status_code=status.HTTP_200_OK,
    description="OAuth2 compatible token, get an access token for future requests using refresh token",
)
async def refresh_token(
    request: RefreshTokenRequest,
    session: AsyncSession = Depends(dependencies.get_session),
) -> AccessTokenResponse:
    command = RefreshTokenCommand(refresh_token=request.refresh_token)
    result = await RefreshTokenCommandHandler(session).handle(command)

    return result


@auth_router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserModel,
    description="User registration",
)
async def register(
    request: UserCreateRequest,
    session: AsyncSession = Depends(dependencies.get_session),
) -> UserModel:
    command = RegisterUserCommand(username=request.username, email=str(request.email), password=request.password)
    user = await RegisterUserCommandHandler(session).handle(command)

    return UserModel.from_entry(user)
