#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in type(cls)._instances:
            type(cls)._instances[cls] = super().__call__(*args, **kwargs)
        return type(cls)._instances[cls]


class Module(metaclass=SingletonMeta):
    def __init__(self):
        print(f"Initializing {type(self).__name__}")


class Logger(metaclass=SingletonMeta):
    pass


if __name__ == "__main__":
    m1 = Module()
    m2 = Module()
    assert m1 is m2
