#!/usr/bin/env python3
# -*- coding: utf-8 -*- # PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import BinaryIO, Self, Iterator
from functools import singledispatchmethod, partial
import struct
import copy
from typeguard import typechecked, TypeCheckError  # noqa: F401
from beartype import beartype, roar


class Field:
    def __init__(self, name: str, off: int):
        self._name = name
        self.off = off

    def fetch(self, instance):
        raise NotImplementedError

    def drop(self, instance, value):
        raise NotImplementedError

    def __get__(self, instance, owner=None):
        if instance is None:
            return None
        return self.fetch(instance)

    def __set__(self, instance, value):
        self.drop(instance, value)


class FieldStr(Field):
    # @typechecked
    # @beartype
    def __init__(self, name: str, off: int, fmt: str):
        super().__init__(name, off)
        self.strukt = struct.Struct(fmt)

    def fetch(self, instance):
        rng = slice(self.off, self.off + self.strukt.size)
        t = self.strukt.unpack_from(instance._view[rng])
        return t[0] if len(t) == 1 else t

    def drop(self, instance, value):
        self.strukt.pack_into(instance._view, self.off, value)


class FieldType(Field):
    # @typechecked
    # @beartype
    def __init__(self, name: str, off: int, typ: FieldMeta):
        super().__init__(name, off)
        self.typ = typ

    def fetch(self, instance):
        rng = slice(self.off, self.off + self.typ.typ_size)
        return self.typ(instance._view[rng])

    def drop(self, instance, value):
        rng = slice(self.off, self.off + self.typ.typ_size)
        instance._view[rng] = value._view


class FieldMeta(type):
    def __new__(mcls, clsname, bases, ns0):
        ns = dict(ns0)
        off = 0
        fields = []
        for key, val in ns0.items():
            if key[:2] == "__" and key[-2:] == "__":
                continue
            if isinstance(val, (str, FieldMeta)):
                if isinstance(val, str):
                    ns[key] = FieldStr(key, off, val)
                    off += struct.calcsize(val)
                elif isinstance(val, FieldMeta):
                    ns[key] = FieldType(key, off, val)
                    off += val.typ_size
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

    @classmethod
    def zeros(cls) -> Self:
        return cls(bytearray(cls.typ_size))


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


class Polygon(View):
    @classmethod
    def from_file(cls, f: BinaryIO) -> Self:
        (sz,) = struct.unpack("<i", f.read(struct.calcsize("<i")))
        return cls(f.read(sz))

    def iter_type(self, sz, typ: type):
        for off in range(0, len(self._view), sz):
            rng = slice(off, off + sz)
            yield typ(self._view[rng])

    @singledispatchmethod
    def iter_as(self, typ: type):
        raise NotImplementedError(f"Cannot iterate as {typ!r}")

    @iter_as.register
    def _(self, fmt: str = "<dd") -> Iterator[tuple[float, float]]:
        yield from self.iter_type(
            struct.calcsize(fmt), partial(struct.unpack_from, fmt)
        )

    @iter_as.register
    def _(self, typ: FieldMeta) -> Iterator[FieldMeta]:
        yield from self.iter_type(typ.typ_size, typ)


HEADER_DAT = ".headerpolygons.dat"
if __name__ == "__main__":
    import io

    with open(HEADER_DAT, "rb") as f:
        h = Header.from_file(f)
        print(h)
        polygon1 = Polygon.from_file(io.BytesIO(rest := f.read()))
        polygon2 = Polygon.from_file(io.BytesIO(rest))
        for _ in range(h.num_polygons):
            for p in polygon1.iter_as("<dd"):
                print(p)
            for p in polygon2.iter_as(Point):
                print(p)
