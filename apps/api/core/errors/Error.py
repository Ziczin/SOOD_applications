class Error:
    text = ''
    desc = ''
    """Конкретная ошибка с авто-регистрацией в хранилище"""
    def __init__(self, storage: 'ErrorStorage', code: int=418): # type: ignore
        storage.register_error(self)
        self.code = code
        self.enabled = False
        self.suppressed = False

    def include(self) -> int:
        if not self.suppressed:
            self.enabled = True
        return self.code

    def exclude(self):
        self.enabled = False

    def suppress(self):
        self.suppressed = True

    def is_active(self) -> bool:
        return self.enabled and not self.suppressed

    def to_dict(self) -> dict:
        return {"text": self.text, "desc": self.desc}
