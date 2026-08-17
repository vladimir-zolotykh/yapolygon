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


if __name__ == "__main__":
    m1 = Module("functools")
    m2 = Module("functools")
    g1 = Logger("stream")
    g2 = Logger("stream")
    assert m1 is m2
    assert g1 is g2
