# with open("./data/.example_html/index.html", "r") as f:
#     data = f.read()
# print(data)

from collections import namedtuple
from typing import NamedTuple


columns = ["id", "name", "index"]
values = [1, "Семён Семёнович Семёнов", 0.99]

s = ",".join(columns)
print(s)

print(values[1].split())

columns_w_values = dict(zip(columns, values))
print(columns_w_values)

# string
print("v1:", end=" ")
for i in range(len(columns)):
    print(columns[i] + "=" + str(values[i]), end="; ")
print()

print(
    "v2: id=%i; name=%s, index=%.2f;"
    % (
        values[0],
        values[1],
        values[2],
    )
)

print("v3: id={}; name={}; index={};".format(*values))

print("v4: id={id}; name={name}; index={index};".format(**columns_w_values))

print(f"v5: id={values[0]}; name={values[1]}; index={values[2]:.2f}; ")

Student = namedtuple("student", columns)
student = Student(**columns_w_values)
print(student)
print(f"{student.name=}")


class Student2(NamedTuple):
    id: int
    name: str
    index: float


student2 = Student2(**columns_w_values)
print(student2)
print(f"{student2.name =}")

print((0, 1, 2) == (0, 1, 2))
print((0, 1, 2) is (0, 1, 2))

print(student == student2)
print(student is student2)

group1_students = {
    student: "Дополнительные данные 1",
    Student(id=2, name="no name", index=0.3): "aaaaaaaaaaa",
}

group2_students = {
    student2: "Дополнительные данные 1",
    Student2(id=2, name="no name", index=0.3): "aaaaaaaaaaa",
}
print(group1_students == group2_students)

print({"a": 1} == {"a": 1})
print({"a": 1} is {"a": 1})


class Foo:
    def __hash__(self) -> int:
        return 1


class Bar:
    def __hash__(self) -> int:
        return 1


foo = Foo()
bar = Bar()

print(hash(foo) == hash(bar))
print(foo == bar)
print(foo is bar)

print("-----------------------")


def log_dec(func):
    def _wrapper(*args, **kwargs):
        print(f"function '{func.__name__}' started")
        res = func(*args, **kwargs)
        print(f"function '{func.__name__}' finished")
        return res

    return _wrapper


def log_param_dec(say_hello=False):
    def log_decorator(func):
        def _wrapper(*args, **kwargs):
            print(f"{'hello ' if say_hello else ''}function '{func.__name__}' started")
            res = func(*args, **kwargs)
            print(f"function '{func.__name__}' finished")
            return res

        return _wrapper

    return log_decorator


@log_param_dec(True)
@log_dec
def my_func(a):
    return a * a


# res = my_func(2)
# print(res)
# res = log_dec(my_func)(2)
# res = log_param_dec(True)(my_func)(2)

# my_func = log_dec(my_func)
res = my_func(2)
print(res)
