from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from examples.w3testing.module2.unit import Unit


class Files:
    def __init__(self, files: list[str]) -> None:
        self._files = files

    def __len__(self):
        return len(self._files)


files = Files(["f1", "f2", "f3"])
print(len(files))


class Reader:
    def __call__(self, name):
        return "......"


reader = Reader()
print(reader("f1"))


class Foo:
    def __init__(self, name, **kwargs) -> None:
        self.name = name
        for arg, value in kwargs.items():
            setattr(self, arg, value)

    def print_args(self):
        for arg, value in self.__dict__.items():
            print(f"{arg}={value}")


foo = Foo("my name", age=100, percent=23.5)
foo.print_args()


class Reader:
    def __init__(self, file) -> None:
        self.file = file

    def __call__(self) -> str:
        res = "some read"
        return res


# Композиция
class Parser:
    def __init__(self, file_name, param1) -> None:
        self.file_name = file_name
        self.param1 = param1
        self.content = Reader(self.file_name)

    def parse(self):
        return self.content().split()


parser = Parser("f1", "some_param")
print(parser.parse())


# Агрегация
class Parser2:
    def __init__(self, file_name, param1, reader) -> None:
        self.file_name = file_name
        self.param1 = param1
        self.content = None
        self.reader = reader(file_name)

    def parse(self):
        self.content = self.reader()
        return self.content.split()


parser2 = Parser2("f1", "some_param", Reader)
print(parser2.parse())


@dataclass_json
@dataclass
class Experience:
    company: str
    experience: float
    position: str


@dataclass_json
@dataclass
class Candidate:
    name: str
    email: str
    skills: list[str] = field(default_factory=list)
    experience: Optional[list[Experience]] = None


experience = Experience(company="c1", experience=12.5, position="boss")
candidate_data = {
    "name": "my name",
    "email": "aa@aa.com",
    "skills": ["s1", "s2"],
    "experience": [experience],
}

candidate = Candidate(**candidate_data)
print(candidate)
print(candidate.to_json())
print("------------")


material = {"id": "s1", "density": 125, "mass": 50, "volume": 0.4}
unit_type = {"name": "n1", "velocity": 12.4}
unit = {"name": "u1", "content": [material], "type_": unit_type}

unit = Unit(**unit)
print(unit)
print(unit.model_dump_json())
print(unit.model_json_schema())
