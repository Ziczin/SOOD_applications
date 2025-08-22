from .login import login

class authenticate:
    def __init__(self, storage: 'ErrorStorage'): # type: ignore
        self.login = login(storage)