import abc


class Shape(abc.ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abc.abstractmethod
    def area(self):
        pass  # абстрактны метод

    def print_point(self):  # неабстрактный метод
        print("X:", self.x, "\tY:", self.y)

    def __repr__(self) -> str:
        return f"Фигура {id(self)}"

    def __str__(self) -> str:
        return f"Фигура {self.x=}, {self.y=}"


# класс прямоугольника
# OCP
class Rectangle(Shape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    # Делаем прямоугольник итерируемым
    # Интерфейсы - Утиная типизация
    # ISP
    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        match self._i:
            case 0:
                self._i += 1
                return self.x
            case 1:
                self._i += 1
                return self.y
            case _:
                raise StopIteration


# LSP
def invert(shape: Shape):
    print(f"Обратная {str(shape)}")


rect = Rectangle(10, 20, 100, 100)
rect.print_point()

invert(rect)

for i in rect:
    print(i)
