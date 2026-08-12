#!/usr/bin/env python3
# -*- coding: utf-8 -*- # PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import BinaryIO, Self
import struct
from typeguard import typechecked, TypeCheckError


class Field:
    def __init__(self, off: int):
        self.off = off

    def fetch(self, instance):
        raise NotImplementedError

    def __get__(self, instance, owner=None):
        if instance is None:
            return None
        return self.fetch(instance)


class FieldStr(Field):
    @typechecked
    def __init__(self, off: int, fmt: str):
        super().__init__(off)
        self.strukt = struct.Struct(fmt)

    def fetch(self, instance):
        rng = slice(self.off, self.off + self.strukt.size)
        t = self.strukt.unpack_from(instance._view[rng])
        return t[0] if len(t) == 1 else t


class FieldType(Field):
    @typechecked
    def __init__(self, off: int, typ: FieldMeta):
        super().__init__(off)
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
            if isinstance(val, (str, FieldMeta)):
                try:
                    ns[key] = FieldStr(off, val)
                    off += struct.calcsize(val)
                except TypeCheckError:
                    ns[key] = FieldType(off, val)
                    off += val.typ_size
                finally:
                    fields.append(key)
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
