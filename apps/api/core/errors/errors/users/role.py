from apps.api.core.errors.Error import Error

class role:
    def __init__(self, storage: 'ErrorStorage'): # type: ignore
        self.role_not_found = role.role_not_found(storage, 404)

    class role_not_found(Error):
        text = "Роль не найдена!"
        desc = "Проверьте правильность передаваемых данных. Возможно, роль не существует в системе."
    

