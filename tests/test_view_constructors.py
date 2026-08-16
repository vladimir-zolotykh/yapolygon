import re
import pytest
from header import Point


@pytest.mark.parametrize(
    "point_obj, expected",
    (
        (Point(), "Point(x=0.0, y=0.0)"),
        (Point.from_kwargs(x=10, y=20), "Point(x=10.0, y=20.0)"),
        (Point.from_kwargs(x=10), "Point(x=10.0, y=0.0)"),
    ),
)
def test_point(point_obj, expected):
    assert str(point_obj) == expected


def test_point_no_attribute():
    with pytest.raises(TypeError, match=re.escape("'Point' has no attribute(s) for z")):
        Point.from_kwargs(x=10, z=30)
