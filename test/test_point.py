import pytest
import math

from decide import decide


@pytest.mark.parametrize(
    "coordinates, expected_quadrant",
    [([0, 0], 1), ([-1, 0], 2), ([0, -1], 3), ([0, 1], 1), ([1, 0], 1), ([1, -1], 4)],
)
def test_quadrant(coordinates, expected_quadrant):
    """
    Verify that the quadrant function returns expected values
    """
    point = decide.Point(coordinates)
    assert point.quadrant() == expected_quadrant


@pytest.mark.parametrize(
    "point1, point2, expected_distance",
    [([0, 0], [0, 0], 0), ([-1, 0], [0, 0], 1), ([-1, -1], [1, 1], math.sqrt(8))],
)
def test_distance(point1, point2, expected_distance):
    """
    Verify that the distance function returns expected values
    """
    assert decide.Point(point1).distance(decide.Point(point2)) == pytest.approx(
        expected_distance
    )
