from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.core.security.password import get_password_hash
from domain.handlers.auth.auth_errors import EmailAlreadyUsedException
from domain.repositories.user import UserEntry


class RegisterUserCommand(BaseModel):
    username: str
    email: str
    password: str


class RegisterUserCommandHandler:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def handle(self, command: RegisterUserCommand) -> UserEntry:
        exists = await UserEntry.exists(command.username, command.email, self.session)

        if exists:
            raise EmailAlreadyUsedException(command.email, command.username)

        hashed_password = get_password_hash(command.password)
        user = await UserEntry.insert(command.username, command.email, hashed_password, self.session)

        return user
