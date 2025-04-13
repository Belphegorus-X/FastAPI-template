
from fastapi import status

from domain.domain_errors import DomainError


class ChatNotFoundException(DomainError):
    def __init__(self, chat_id: str):
        message = f"Cannot find chat history with id: {chat_id}"

        super().__init__(
            message,
            message,
            1000_0001,
            status.HTTP_404_NOT_FOUND,
        )
