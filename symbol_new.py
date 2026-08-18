#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Symbol:
    _instances = {}

    def __new__(cls, name, pat):
        if name not in cls._instances:
            sym = cls._instances[name] = super().__new__(cls)
            sym.name = name
            sym.pat = pat
            print(f"Initializing {cls.__name__}({name})")
        return cls._instances[name]

    @classmethod
    def masterpat(cls):
        return cls._instances


if __name__ == "__main__":
    NAME = Symbol("NAME", r"[A-Za-z_]\w*")
    WS1 = Symbol("WS", r"\s+")
    WS2 = Symbol("WS", r"\s+")
    assert WS1 is WS2
