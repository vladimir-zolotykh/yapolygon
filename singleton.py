#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


class SingletonMeta(type):
    _instances = defaultdict(dict)

    def __call__(cls, *args, **kwargs):
        name = args[0]
        instances = type(cls)._instances
        if cls not in instances or name not in instances[cls]:
            instances[cls][name] = super().__call__(*args, **kwargs)
        return type(cls)._instances[cls]


class Module(metaclass=SingletonMeta):
    def __init__(self, name):
        print(f"Initializing {type(self).__name__}({name})")


class Logger(metaclass=SingletonMeta):
    def __init__(self, name):
        print(f"Initializing {type(self).__name__}({name})")


class Symbol(metaclass=SingletonMeta):
    def __init__(self, name, pat):
        print(f"Initializing {type(self).__name__}({name})")
        self.name = name
        self.pat = pat

    @classmethod
    def masterpat(cls):
        return type(cls)._instances[cls]


if __name__ == "__main__":
    m1 = Module("functools")
    m2 = Module("functools")
    assert m1 is m2
    t1 = Module("types")
    t2 = Module("types")
    assert t1 is t2
    g1 = Logger("stream")
    g2 = Logger("stream")
    assert g1 is g2
    NAME = Symbol("NAME", r"[A-Za-z_]\w*")
    WS1 = Symbol("WS", r"\s+")
    WS2 = Symbol("WS", r"\s+")
    assert WS1 is WS2
    print(Symbol.masterpat())
