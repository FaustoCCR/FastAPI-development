class UserNotFoundException(Exception):
    def __init__(self, identifier: str) -> None:
        super().__init__(f"User not found with identifier: {identifier}")

    """ def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})" """


class InvalidPasswordException(Exception):
    def __init__(self) -> None:
        super().__init__(f"Invalid password")
