class A:
    def foo(self):
        print("A foo")


class B:
    def foo(self):
        print("B foo")


class AB(A, B): ...


class BA(B, A): ...


ab = AB()
ba = BA()

ab.foo()
ba.foo()
