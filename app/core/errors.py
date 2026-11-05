class InstagramError(Exception):
    code = "InstagramError"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UsernameAlreadyExistsError(InstagramError):
    code = "username_already_exists"


class EmailAlreadyExistsError(InstagramError):
    code = "email_already_exists"


class UserNotFoundError(InstagramError):
    code = "user_not_found"
