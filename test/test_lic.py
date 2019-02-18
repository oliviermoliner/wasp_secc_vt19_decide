import pytest

from decide import lic


def test_lic0_met():
    """LIC 0 should be met when two consecutive points are more than LENGTH1 apart"""
    assert lic.lic_0([[0, 0], [1, 1], [3, 3]], {"length1": 2}) is True


def test_lic0_not_met():
    """LIC 0 should not be met when no consecutive points are more than LENGTH1 apart"""
    assert lic.lic_0([[0, 0], [1, 1], [2, 2]], {"length1": 2}) is False


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[0, 0], [1, 0], [0.5, 0.86602539]], {"radius1": 0.5}),
        ([[0, 0], [1, 0], [0.5, 10]], {"radius1": 5}),
    ],
)
def test_lic1_met(points, parameters):
    """
    LIC 1 should be met when three consecutive points cannot all be contained within
    or on a circle of radius RADIUS1
    """
    assert lic.lic_1(points, parameters) is True


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[0, 0], [0, 4], [2, 2]], {"radius1": 2}),
        ([[0, 0], [1, 0], [10, 2]], {"radius1": 24}),
    ],
)
def test_lic1_not_met(points, parameters):
    """
    LIC 1 should not be met when all sets of three consecutive points can becontained
    within or on a circle of radius RADIUS1
    """
    assert lic.lic_1(points, parameters) is False


@pytest.mark.parametrize(
    "points,parameters, expected",
    [
        ([[0, 0], [2, 2], [4, 4]], {"radius1": 3}, True),
        ([[0, 0], [0, 1], [0, 2]], {"radius1": 3}, False),
    ],
)
def test_lic1_collinear_case(points, parameters, expected):
    """
    The results of the lic_1 function should be consistent also when three points
    are collinear
    """
    assert lic.lic_1(points, parameters) is expected
