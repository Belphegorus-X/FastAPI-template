class DomainError(Exception):
    def __init__(
        self,
        message: str,
        inner_massage: str,
        code: int,
        status_code: int,
    ) -> None:
        self.message = message
        self.inner_message = inner_massage
        self.code = code
        self.status_code = status_code
        super().__init__(message)
