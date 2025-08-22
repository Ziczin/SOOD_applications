from .Error import Error
from .errors import authenticate, users

class ErrorStorage:
    def __init__(self):
        self._all_errors: list[Error] = []
        self.authenticate = authenticate(self)
        self.users = users(self)

    def register_error(self, *errors: Error) -> None:
        """Регистрация ошибки при её создании"""
        self._all_errors.extend(errors)

    def as_list(self) -> list[dict]:
        """Простой сбор активных ошибок"""
        return [error.to_dict() for error in self._all_errors if error.is_active()]

