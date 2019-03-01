import pytest
import math

from decide import decide


@pytest.mark.parametrize(
    "coordinates, expected_quadrant",
    [
        # Point belongs to all quadrants and should be assigned to quadrant I
        ([0, 0], 1),
        # Point belongs to quandrants II and III and should be assigned to quadrant II
        ([-1, 0], 2),
        # Point belongs to quandrants III and IV and should be assigned to quadrant III
        ([0, -1], 3),
        # Point belongs to quandrants I and IV and should be assigned to quadrant I
        ([0, 1], 1),
        # Point belongs to quandrants I and II and should be assigned to quadrant I
        ([1, 0], 1),
        # Point belongs to quadrant IV
        ([1, -1], 4),
    ],
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
