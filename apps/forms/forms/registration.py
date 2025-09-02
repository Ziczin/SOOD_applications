from apps.users.models import Department

registration_form_data = {
    'name': 'Registration',
    "action": "/api/auth/register/",
    'title': 'Регистрация',
    'btn_confirm': 'Зарегистрироваться',
    'sub_btn_link': '/users/login',
    'sub_btn_link_text': 'Уже есть аккаунт? Войти',
    'fields': [
        {
            'id': 'username', 'type': 'text',
            'label': 'Имя пользователя',
            'placeholder': 'Например IvanovAV',
        },
        {
            'id': 'fullname', 'type': 'text',
            'label': 'Полное имя',
            'placeholder': 'Например: Иванов Иван Иванович',
        },
        {
            'id': 'password1', 'type': 'password',
            'label': 'Пароль',
            'placeholder': 'Введите пароль',
        },
        {
            'id': 'password2', 'type': 'password',
            'label': 'Повторите пароль',
            'placeholder': 'Введите пароль. Снова',
        },
        {
            'id': 'department', 'type': 'enum',
            'enum': {'model': Department, 'config': {'value': 'name', 'text': 'label'}},
            'label': 'Выберите ваш отдел',
            'placeholder': 'Без отдела',
        },
    ],
}
