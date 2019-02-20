import pytest
import math

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


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[0, 1], [0, 0], [1, 0]], {"epsilon": 0.765}),
        ([[0, 1], [1, 0], [2, 0]], {"epsilon": 0.21}),
    ],
)
def test_lic2_met(points, parameters):
    """
    LIC 2 should be met when three consecutive points form an angle such that :
    angle < (PI − EPSILON) or angle > (PI + EPSILON)
    """
    assert lic.lic_2(points, parameters) is True


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[-1, 0], [0, 0], [1, 0]], {"epsilon": 0.0001}),
        ([[1, 1], [2, 2], [3, 3]], {"epsilon": 0.0001}),
        ([[0, 1], [0, 0], [1, 0]], {"epsilon": 1.6}),
    ],
)
def test_lic2_not_met(points, parameters):
    """
    LIC 2 should not be met when no set of three consecutive points form an angle such
    that angle < (PI − EPSILON) or angle > (PI + EPSILON)
    """
    assert lic.lic_2(points, parameters) is False


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[0, 0], [0, 0], [2, 2]], {"epsilon": 0.001}),
        ([[0, 0], [2, 2], [2, 2]], {"epsilon": 0.001}),
    ],
)
def test_lic2_undefined_angle(points, parameters):
    """
    LIC 2 should not be met when either the first or last point of the triplet coincide
    with the vertex
    """
    assert lic.lic_2(points, parameters) is False


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[-1, 0], [0, 0], [1, 0]], {"epsilon": -1}),
        ([[-1, 0], [0, 0], [1, 0]], {"epsilon": math.pi}),
        ([[-1, 0], [0, 0], [1, 0]], {"epsilon": 3.3}),
    ],
)
def test_lic2_epsilon_value_error(points, parameters):
    """
    Allowed values of EPSILON should be between 0 (inclusive) and PI (exclusive)
    """
    with pytest.raises(ValueError):
        lic.lic_2(points, parameters)
