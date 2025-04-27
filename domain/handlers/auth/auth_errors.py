from starlette import status

from domain.domain_errors import DomainError


class UserNotFoundException(DomainError):
    def __init__(self, identification: str):
        super().__init__(
            "Authorization error",
            f"Cannot find user with identification: {identification}",
            3_0001,
            status.HTTP_404_NOT_FOUND,
        )


class InvalidPasswordException(DomainError):
    def __init__(self, identification: str):
        super().__init__(
            "Authorization error",
            f"Incorrect password for user with identification: {identification}",
            3_0002,
            status.HTTP_401_UNAUTHORIZED,
        )


class RefreshTokenNotFoundException(DomainError):
    def __init__(self, refresh_token: str):
        super().__init__(
            "Authorization error",
            f"Cannot find refresh token: {refresh_token}",
            3_0003,
            status.HTTP_404_NOT_FOUND,
        )


class RefreshTokenExpiredException(DomainError):
    def __init__(self, refresh_token: str):
        super().__init__(
            "Authorization error",
            f"Refresh token already expired: {refresh_token}",
            3_0004,
            status.HTTP_400_BAD_REQUEST,
        )


class RefreshTokenAlreadyUsedException(DomainError):
    def __init__(self, refresh_token: str):
        super().__init__(
            "Authorization error",
            f"Refresh token already used: {refresh_token}",
            3_0005,
            status.HTTP_400_BAD_REQUEST,
        )


class EmailAlreadyUsedException(DomainError):
    def __init__(self, email: str, username: str):
        super().__init__(
            "Authorization error",
            f"Email {email} and username {username} already in use",
            3_0006,
            status.HTTP_400_BAD_REQUEST,
        )
