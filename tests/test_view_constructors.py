import re
import pytest
from header import Point, Bbox


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
    with pytest.raises(TypeError, match=re.escape("'Point' has no attribute(s) for z")):
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
    with pytest.raises(
        TypeError, match=re.escape("'Bbox' has no attribute(s) for xy3")
    ):
        Bbox.from_kwargs(xy3=Point())
