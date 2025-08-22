from apps.api.core.errors.Error import Error

from .role import role

class users:
    def __init__(self, storage: 'ErrorStorage'): # type: ignore
        self.role = role(storage)
        self.user_not_found = users.user_not_found(storage, 404)

    class user_not_found(Error):
        text = "Пользователь не найден!",
        desc = "Проверьте правильность вводимого логина. Возможно, пользователя не существует в системе."