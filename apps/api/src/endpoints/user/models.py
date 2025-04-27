import uuid

from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: uuid.UUID
    name: str
    email: str
