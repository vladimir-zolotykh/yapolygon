#!/usr/bin/env python3
# -*- coding: utf-8 -*- # PYTHON_ARGCOMPLETE_OK
from typing import BinaryIO, Self
import struct


class Field:
    def __init__(self, fname: str, off: int):
        self.fname = fname
        self.off = off

    def fetch(self, instance):
        raise NotImplementedError

    def __get__(self, instance, owner=None):
        if instance is None:
            return None
        return self.fetch(instance)


class FieldStr(Field):
    def __init__(self, fname, off, fmt: str):
        super().__init__(fname, off)
        self.strukt = struct.Struct(fmt)

    def fetch(self, instance):
        rng = slice(self.off, self.off + self.strukt.size)
        t = self.strukt.unpack_from(instance._view[rng])
        return t[0] if len(t) == 1 else t


class FieldType(Field):
    def __init__(self, fname, off, typ: type):
        super().__init__(fname, off)
        self.typ = typ

    def fetch(self, instance):
        rng = slice(self.off, self.off + self.typ.typ_size)
        return self.typ(instance._view[rng])


class FieldMeta(type):
    def __new__(mcls, clsname, bases, ns0):
        ns = dict(ns0)
        off = 0
        fields = []
        for key, val in ns0.items():
            if key[:2] == "__" and key[-2:] == "__":
                continue
            if isinstance(val, str):
                ns[key] = FieldStr(key, off, val)
                off += struct.calcsize(val)
                fields.append(key)
            elif isinstance(val, FieldMeta):
                ns[key] = FieldType(key, off, val)
                off += val.typ_size
                fields.append(key)
            else:
                pass
        ns["typ_size"] = off
        ns["_fields"] = fields
        return super().__new__(mcls, clsname, bases, ns)


class View(metaclass=FieldMeta):
    def __init__(self, bytesdata: bytes | memoryview):
        self._view = memoryview(bytesdata)

    def __repr__(self):
        args = ", ".join(f"{k}={getattr(self, k)!r}" for k in self._fields)
        return f"{type(self).__name__}({args})"

    @classmethod
    def from_file(cls, f: BinaryIO) -> Self:
        return cls(f.read(cls.typ_size))


class Point(View):
    x = "<d"
    y = "<d"


class Bbox(View):
    xy1 = Point
    xy2 = Point


class Header(View):
    magic = "<i"
    bbox = Bbox
    num_polygons = "<i"


HEADER_DAT = ".header.dat"
if __name__ == "__main__":
    with open(HEADER_DAT, "rb") as f:
        h = Header.from_file(f)
        print(h)
