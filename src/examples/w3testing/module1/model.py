from examples.w3testing.module1.errors import MethodError


class Model:
    """Псевдо модель для тестов."""

    def __init__(self, a: int):
        """Инициализировать модель с первым параметром.

        Args:
            a (int): Первый параметр.
        """
        self._a = a
        self._b = None

    def set_b(self, b: int) -> bool:
        """Установить второй параметр.

        Args:
            b (int): Второй параметр модели.
        Returns:
            bool: Результат установки.
        """

        if not isinstance(b, int):  # type: ignore
            return False

        self._b = b
        return True

    def calculate(self, method: str) -> int | str:
        """Посчитать значения.

        Args:
            method (str): Каким методом считать.

        Raises:
            ValueError: Если нет второго параметра.
            MethodError: Если неизвестный метод.

        Returns:
            int|str: Результат операции.
        """

        if self._b is None:
            raise ValueError("Не установлен b")

        match method:
            case "m1":
                return self._a + self._b + 1
            case "m2":
                return str(self._a - self._b)
            case _:
                raise MethodError(method)
