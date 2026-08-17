#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class SymbolMeta(type):
    _instances = {}  # symbol instances

    def __call__(cls, *args, **kwargs):
        name = args[0]
        instances = type(cls)._instances
        if name not in instances:
            instances[name] = super().__call__(*args, **kwargs)
        return instances[name]


class Symbol(metaclass=SymbolMeta):
    def __init__(self, name, pat):
        print(f"Initializing {type(self).__name__}({name})")
        self.name = name
        self.pat = pat

    @classmethod
    def masterpat(cls):
        return type(cls)._instances


if __name__ == "__main__":
    NAME = Symbol("NAME", r"[A-Za-z_]\w*")
    WS1 = Symbol("WS", r"\s+")
    WS2 = Symbol("WS", r"\s+")
    assert WS1 is WS2
    print(Symbol.masterpat())
