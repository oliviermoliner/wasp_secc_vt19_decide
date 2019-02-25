import pytest
import math

from decide import decide


@pytest.mark.parametrize(
    "point1, point2, point3, expected_area, message",
    [
        ([0, 0], [2, 2], [4, 4], 0, "Area should be 0 when points are collinear"),
        ([0, 0], [2, 0], [4, 0], 0, "Area should be 0 when points are collinear"),
        ([0, 0], [2, 2], [4, 0], 4, "Area of right isoceles triangle"),
        ([10, 0], [0, 0], [5, 8.66], 43.3, "Area of equilateral triangle"),
        ([23, 30], [15, 15], [50, 25], 222.5, "Area of obtuse scalene triangle"),
    ],
)
def test_triangle_area(point1, point2, point3, expected_area, message):
    """
    Verify that the triangle_area function returns expected values
    """
    triangle = decide.Triangle(
        decide.Point(point1), decide.Point(point2), decide.Point(point3)
    )
    assert triangle.area() == pytest.approx(expected_area), message


@pytest.mark.parametrize(
    "point1, point2, point3, expected_radius",
    [
        ([0, 0], [1, 0], [0.5, 0.86602539], 0.5773502645948126),
        ([0, 0], [1, 0], [0.5, 10], 5.0125),
        ([0, 0], [0, 4], [2, 2], 2),
        ([0, 0], [1, 0], [10, 2], 23.50531854708608),
        ([0, 0], [2, 2], [4, 4], math.sqrt(32)),
        ([0, 0], [0, 1], [0, 2], 2),
    ],
)
def test_triangle_circumradius(point1, point2, point3, expected_radius):
    """
    Verify that the circumradius function returns expected values
    """
    triangle = decide.Triangle(
        decide.Point(point1), decide.Point(point2), decide.Point(point3)
    )
    assert triangle.circumradius() == pytest.approx(expected_radius)


@pytest.mark.parametrize(
    "point1, point2, point3, expected_angle",
    [
        ([0, 1], [0, 0], [1, 0], 3 * math.pi / 2),
        ([0, 1], [1, 0], [2, 0], 5 * math.pi / 4),
        ([-1, 0], [0, 0], [1, 0], math.pi),
        ([1, 1], [2, 2], [3, 3], math.pi),
        ([0, 1], [0, 0], [1, 0], 3 * math.pi / 2),
        ([-1, 0], [0, 0], [1, 0], math.pi),
        ([-1, 0], [0, 0], [1, 0], math.pi),
        ([-1, 0], [0, 0], [1, 0], math.pi),
    ],
)
def test_triangle_angle_abc(point1, point2, point3, expected_angle):
    """
    Verify that the angle_abc function returns expected values
    """
    triangle = decide.Triangle(
        decide.Point(point1), decide.Point(point2), decide.Point(point3)
    )
    assert triangle.angle_abc() == pytest.approx(expected_angle)
