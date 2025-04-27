import uuid
from typing import Self

from pydantic import BaseModel

from domain.repositories.user import UserEntry


class UserModel(BaseModel):
    user_id: uuid.UUID
    username: str
    email: str

    @classmethod
    def from_entry(cls, entry: UserEntry) -> Self:
        return cls(
            user_id=entry.user_id,
            username=entry.username,
            email=entry.email,
        )
