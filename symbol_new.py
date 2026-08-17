#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Symbol:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        name = args[0]
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]

    def __init__(self, name, pat):
        if not hasattr(self, "name"):
            print(f"Initializing {type(self).__name__}({name})")
            self.name = name
            self.pat = pat

    @classmethod
    def masterpat(cls):
        return cls._instances


if __name__ == "__main__":
    NAME = Symbol("NAME", r"[A-Za-z_]\w*")
    WS1 = Symbol("WS", r"\s+")
    WS2 = Symbol("WS", r"\s+")
    assert WS1 is WS2
