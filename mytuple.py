#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, bases, ns):
        fields = ns.get("_fields", [])
        for n, name in enumerate(fields):
            setattr(cls, "name", property(itemgetter(n)))


class Tuple(tuple):
    def __new__(cls, *args, **kwargs):
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"{cls!r} gets exactly {n} arguments")
        return super().__new__(cls, *args, **kwargs)


class Person(Tuple):
    _fields = ["name", "age", "salary"]


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob.name, bob.age, bob.salary)
