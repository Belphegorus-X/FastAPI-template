from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from domain.handlers.user.user_errors import UserNotFoundException
from domain.repositories.user import UserEntry


class GetUserQuery(BaseModel):
    user_id: UUID


class GetUserQueryHandler:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def handle(self, query: GetUserQuery) -> UserEntry:
        result = await UserEntry.fetch_user_by_id(query.user_id, self.session)

        if result is None:
            raise UserNotFoundException(query.user_id)

        return result
