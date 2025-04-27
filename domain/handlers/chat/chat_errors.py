from uuid import UUID

from fastapi import status

from domain.domain_errors import DomainError


class ChatNotFoundException(DomainError):
    def __init__(self, chat_id: UUID):
        super().__init__(
            "Chat not found",
            f"Cannot find chat history with id: {chat_id}",
            1_0001,
            status.HTTP_404_NOT_FOUND,
        )
