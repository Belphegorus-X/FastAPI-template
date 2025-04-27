from uuid import UUID

from fastapi import status

from domain.domain_errors import DomainError


class UserNotFoundException(DomainError):
    def __init__(self, user_id: UUID):
        super().__init__(
            "User not found",
            f"Cannot find user with id: {user_id}",
            2_0001,
            status.HTTP_404_NOT_FOUND,
        )
