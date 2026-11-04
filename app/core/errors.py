class InstagramError(Exception):
    code = "InstagramError"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UserAlreadyExistsError(InstagramError):
    code = "user_already_exists"


class UserNotFoundError(InstagramError):
    code = "user_not_found"
