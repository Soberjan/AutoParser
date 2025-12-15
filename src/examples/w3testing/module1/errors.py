from typing import Any


class MethodError(Exception):
    def __init__(self, method: Any):
        message = f"Не могу выполнить метод '{method}'."
        super().__init__(message)