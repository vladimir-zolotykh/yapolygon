#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter
import pytest


class TupleMeta(type):
    def __init__(cls, clsname, bases, ns):
        super().__init__(clsname, bases, ns)
        fields = ns.get("_fields", [])
        for n, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(n)))


class Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args, **kwargs):
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"{cls.__name__!r} gets exactly {n} arguments")
        return super().__new__(cls, args)


class Person(Tuple):
    _fields = ["name", "age", "salary"]


def test_person():
    bob = Person("Bob", 37, 12000)
    assert bob.name == "Bob" and bob.age == 37 and bob.salary == 12000
    assert str(bob) == "('Bob', 37, 12000)"
    with pytest.raises(TypeError, match="'Person' gets exactly 3 arguments"):
        Person("Bob", 37, 12000, "Senior engineer")


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob.name, bob.age, bob.salary)
