#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import BinaryIO, Self
from itertools import chain
import struct
import pytest
from typeguard import typechecked


POLYGONS = [
    [(1.0, 2.5), (3.5, 4.0), (2.5, 1.5)],
    [(7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0)],
    [(3.4, 6.3), (1.2, 0.5), (4.6, 9.2)],
]


class Point:
    @typechecked
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __iter__(self):
        yield from self.__dict__.values()


class Bbox:
    @typechecked
    def __init__(self, xy1: Point, xy2: Point):
        self.xy1 = xy1
        self.xy2 = xy2

    def __iter__(self):
        for pp in self.__dict__.values():
            yield from pp


def get_bbox(polygons=POLYGONS) -> Bbox:
    x1 = min(x for x, _ in chain(*polygons))
    y1 = min(y for _, y in chain(*polygons))
    x2 = max(x for x, _ in chain(*polygons))
    y2 = max(y for _, y in chain(*polygons))
    return Bbox(Point(x1, y1), Point(x2, y2))


class Header:
    def __init__(self, magic, x1, y1, x2, y2, num_polygons):
        self.magic = magic
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.num_polygons = num_polygons

    def __eq__(self, other) -> bool:
        return (
            self.__dict__ == other.__dict__
            if isinstance(other, type(self))
            else NotImplemented
        )

    @classmethod
    def from_file(cls, f: BinaryIO) -> Self:
        magic, x1, y1, x2, y2, num_polygons = struct.unpack("<iddddi", f.read(40))
        return Header(magic, x1, y1, x2, y2, num_polygons)

    @classmethod
    def reference(cls, polygons=POLYGONS) -> Self:
        return cls(0x1234, *get_bbox(polygons), len(polygons))

    def __iter__(self):
        yield from self.__dict__.values()

    def __repr__(self):
        args = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{type(self).__name__}({args})"

    def write_to(self, f: BinaryIO) -> None:
        f.write(
            struct.pack(
                "<iddddi",
                *self,
            )
        )


def test_header_init():
    h: Header = Header.reference()
    assert (
        str(h) == "Header(magic=4660, x1=0.5, y1=0.5, x2=7.0, y2=9.2, num_polygons=3)"
    )


HEADER = "header.dat"


def test_write_read():
    h = Header.reference()
    with open(HEADER, "wb") as f:
        h.write_to(f)
    with open(HEADER, "rb") as f:
        assert Header.from_file(f) == h


if __name__ == "__main__":
    h: Header = Header.reference()
    print(h)
