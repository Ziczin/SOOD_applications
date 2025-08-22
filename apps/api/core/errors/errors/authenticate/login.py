from apps.api.core.errors.Error import Error

class login:
    def __init__(self, storage: 'ErrorStorage'): # type: ignore
        self.unauthorized = login.unauthorized(storage, 401)
        self.invalid_data = login.invalid_data(storage, 400)
        
    class unauthorized(Error):
        text = "Неправильный логин или пароль!",
        desc = "Если вы забыли пароль, то обратитесь в отдел программирования."

    class invalid_data(Error):
        text = "Данные в поле ввода невозможно прочитать!",
        desc = "Возможно, в поле ввода находится недопустимый символ или что-то что не является символом. " +\
            "Проверьте ввод на корректность, если ошибка сохранится - обратитесь в отдел программирования."