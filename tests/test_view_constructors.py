import re
import pytest
from header import Point, Bbox, Header


@pytest.mark.parametrize(
    "point_obj, expected",
    [
        (Point(), "Point(x=0.0, y=0.0)"),
        (Point.from_kwargs(x=10, y=20), "Point(x=10.0, y=20.0)"),
        (Point.from_kwargs(x=10), "Point(x=10.0, y=0.0)"),
    ],
)
def test_point(point_obj, expected):
    assert str(point_obj) == expected


def test_point_no_attribute():
    with pytest.raises(TypeError, match=re.escape("'Point' has no attribute(s) z")):
        Point.from_kwargs(x=10, z=30)


@pytest.mark.parametrize(
    "bb, expected",
    [
        (Bbox(), "Bbox(xy1=Point(x=0.0, y=0.0), xy2=Point(x=0.0, y=0.0))"),
        (
            Bbox.from_kwargs(xy1=Point.from_kwargs(x=10.0, y=20.0)),
            "Bbox(xy1=Point(x=10.0, y=20.0), xy2=Point(x=0.0, y=0.0))",
        ),
        (
            Bbox.from_kwargs(
                xy1=Point.from_kwargs(x=10.0, y=20.0),
                xy2=Point.from_kwargs(x=100.0, y=200.0),
            ),
            "Bbox(xy1=Point(x=10.0, y=20.0), xy2=Point(x=100.0, y=200.0))",
        ),
    ],
)
def test_bbox(bb, expected):
    assert str(bb) == expected


def test_bbox_no_attribue():
    with pytest.raises(TypeError, match=re.escape("'Bbox' has no attribute(s) xy3")):
        Bbox.from_kwargs(xy3=Point())


@pytest.mark.parametrize(
    "h, expected",
    [
        (
            Header(),
            (
                "Header(magic=0, bbox=Bbox(xy1=Point(x=0.0, y=0.0), "
                "xy2=Point(x=0.0, y=0.0)), num_polygons=0)"
            ),
        ),
        (
            Header.from_kwargs(
                magic=0x1234,
                bbox=Bbox.from_kwargs(
                    xy1=Point.from_kwargs(x=1, y=2), xy2=Point.from_kwargs(x=10, y=20)
                ),
                num_polygons=3,
            ),
            (
                "Header(magic=4660, bbox=Bbox(xy1=Point(x=1.0, y=2.0), "
                "xy2=Point(x=10.0, y=20.0)), num_polygons=3)"
            ),
        ),
    ],
)
def test_header(h, expected):
    assert str(h) == expected


def test_header_no_attribute():
    with pytest.raises(TypeError, match=re.escape("'Header' has no attribute(s) code")):
        Header.from_kwargs(code=0x1234, num_polygons=3)
