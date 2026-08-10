#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from itertools import chain
from beartype import beartype


POLYGONS = [
    [(1.0, 2.5), (3.5, 4.0), (2.5, 1.5)],
    [(7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0)],
    [(3.4, 6.3), (1.2, 0.5), (4.6, 9.2)],
]


class Point:
    @beartype
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Bbox:
    @beartype
    def __init__(self, xy1: Point, xy2: Point):
        self.xy1 = xy1
        self.xy2 = xy2


def get_bbox(polygons=POLYGONS) -> Bbox:
    chained = chain(*polygons)
    x1 = min(x for x, _ in chained)
    y1 = min(y for _, y in chained)
    x2 = max(x for x, _ in chained)
    y2 = max(y for _, y in chained)
    return Bbox(Point(x1, y1), Point(x2, y2))


class Header:
    def __init__(self, polygons=POLYGONS):
        self.magic = 0x1234
        bbox = Bbox(polygons)
        self.x1, self.y1 = bbox.xy1
        self.x2, self.y2 = bbox.xy2
        self.num_polygons = 3


if __name__ == "__main__":
    h: Header = Header()
    print(h)
