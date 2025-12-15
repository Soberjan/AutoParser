from typing import Callable, List, Any, Dict, NamedTuple

import pytest


BasicTestCase = NamedTuple(
    "BasicTestCase",
    [("value", Any), ("result", Any), ("exception", Exception | None), ("name", str)],
)


def case_names(cases: List[Any]) -> List[str]:
    """Получить названия всех кейсов.

    Args:
        cases (List[BasicTestCase]): Список кейсов.add()

    Returns:
        List[str]: Список имён.
    """
    return [case.name for case in cases]


def change_data(source: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """Изменить данные для тестов, модифицируя имеющиеся данные.

    Args:
        source (Dict[str, Any]): Исходные данные.

    Kwargs:
        "Новые данные. в формате <название_раздела=новое_значение_раздела>."

    Returns:
        Dict[str, Any]: Созданные данные.
    """
    res = source.copy()
    for k, v in kwargs.items():
        res[k] = v
    return res


def create_object(tc: BasicTestCase, object_class: Callable) -> Any:
    """Простая проверка создания объекта.

    Args:
        tc (BasicTestCase): Данные для проверки.
        object_class (Callable): Класс, из которого надо создать объект.

    Returns:
        Callable: Созданный объект
    """
    instance = None
    if tc.exception is not None:
        with pytest.raises(tc.exception):
            object_class(**tc.value)
    else:
        if tc.result is None:
            assert object_class(**tc.value)
        else:
            instance = object_class(**tc.value)

    return instance


def str_to_bool(val: str | None, default: bool = False) -> bool:
    """
    Проверка значения строки на истину.

    Args:
        val (str|None): строка для проверки
        default (bool): значение по умолчанию
    Returns:
        bool: true если значение строки [1|true|yes].
    Raises:
        AttributeError: Если ошибка при получении значений.

    """
    try:
        if isinstance(val, str):
            return val.lower() in ["1", "true", "yes"]
        else:
            return default
    except AttributeError:
        return default
