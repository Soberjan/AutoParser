from dataclasses import dataclass, field
from typing import Any, Dict, List


class Foo:
    _bar: int = 0

    def __init__(self, bar: int = 2) -> None:
        self.bar = bar


@dataclass
class Bookshelf:
    books: list = field(default_factory=list)
    # books = []


def bad_dict(new_item: Any, a_dict=None) -> Dict[Any, Any]:
    if not a_dict:
        a_dict = {}
    a_dict[new_item] = new_item
    return a_dict


def main():
    b = Bookshelf()
    b.books.append("11")
    b2 = Bookshelf()
    print(f"{b2.books=}")

    print(bad_dict("one"))
    print(bad_dict("two"))

    # print("Тут только тесты")
    # f1 = Foo()
    # f1.bar = 1
    # f2 = Foo()
    # f2.bar = 2

    # print(f1.bar, f2.bar)


if __name__ == "__main__":
    main()
