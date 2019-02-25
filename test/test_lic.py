import pytest
import math

from decide import decide


def test_lic0_met():
    """LIC 0 should be met when two consecutive points are more than LENGTH1 apart"""
    lauch_conditions = decide.LaunchInterceptorConditions({"length1": 2})
    assert lauch_conditions.lic_0([[0, 0], [1, 1], [3, 3]]) is True


def test_lic0_not_met():
    """LIC 0 should not be met when no consecutive points are more than LENGTH1 apart"""
    lauch_conditions = decide.LaunchInterceptorConditions({"length1": 2})
    assert lauch_conditions.lic_0([[0, 0], [1, 1], [2, 2]]) is False


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
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_1(points) is True


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
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_1(points) is False


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
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_1(points) is expected


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
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_2(points) is True


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
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_2(points) is False


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
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_2(points) is False


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
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    with pytest.raises(ValueError):
        lauch_conditions.lic_2(points)


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[23, 30], [15, 15], [50, 25]], {"area1": 200}),
        ([[10, 0], [0, 0], [5, 8.66]], {"area1": 43}),
    ],
)
def test_lic3_met(points, parameters):
    """
    LIC 3 should be met when three consecutive points are the vertices of a triangle
    with area greater than AREA1
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_3(points) is True


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[0, 0], [2, 2], [4, 4]], {"area1": 0.0001}),  # Collinear points
        ([[0, 0], [2, 0], [4, 0]], {"area1": 0.0001}),  # Collinear points
        ([[10, 0], [0, 0], [5, 8.66]], {"area1": 44}),
    ],
)
def test_lic3_not_met(points, parameters):
    """
    LIC 3 should not be met when no set of three consecutive points are the vertices of a triangle
    with area greater than AREA1
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_3(points) is False


@pytest.mark.parametrize(
    "points,parameters", [([[-1, 0], [0, 0], [1, 0]], {"area1": -1})]
)
def test_lic3_area1_value_error(points, parameters):
    """
    AREA1 should be greater or equal than 0
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    with pytest.raises(ValueError):
        lauch_conditions.lic_3(points)


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[1, 1], [1, 1], [1, 1], [1, -1], [1, -1]], {"q_pts": 3, "quads": 1}),
        ([[1, 1], [1, 1], [1, 1], [1, -1], [1, -1]], {"q_pts": 5, "quads": 1}),
        ([[1, 1], [1, -1], [-1, -1], [-1, 1], [1, 1]], {"q_pts": 4, "quads": 3}),
    ],
)
def test_lic4_met(points, parameters):
    """
    LIC 4 should be met when at least Q_PTS consecutive data points lie in more than
    QUADS quadrants
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_4(points) is True


@pytest.mark.parametrize(
    "points,parameters",
    [
        # All points lie in the same quadrant
        ([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]], {"q_pts": 2, "quads": 1}),
        ([[1, 1], [1, 1], [1, 1], [1, -1], [1, -1]], {"q_pts": 5, "quads": 2}),
        # If Q_PTS <= QUADS: the condition can never be met
        ([[1, 1], [1, -1], [-1, -1], [-1, 1], [1, 1]], {"q_pts": 2, "quads": 3}),
    ],
)
def test_lic4_not_met(points, parameters):
    """
    LIC 4 should not be met when no set of Q_PTS consecutive points lie in more than
    QUADS quadrants
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_4(points) is False


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]], {"q_pts": 1, "quads": 1}),
        ([[1, 1], [1, 1]], {"q_pts": 3, "quads": 1}),
    ],
)
def test_lic4_q_pts_value_error(points, parameters):
    """
    Allowed values of Q_PTS should be between 2 (inclusive) and NUMPOINTS (inclusive)
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    with pytest.raises(ValueError):
        lauch_conditions.lic_4(points)


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]], {"q_pts": 1, "quads": 4}),
        ([[1, 1], [1, 1]], {"q_pts": 2, "quads": 0}),
    ],
)
def test_lic4_quads_value_error(points, parameters):
    """
    Allowed values of QUADS should be between 1 (inclusive) and 3 (inclusive)
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    with pytest.raises(ValueError):
        lauch_conditions.lic_4(points)


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[0, 0], [1, 0], [0.5, 0.86602539]], {}),
        ([[0, 0], [1, 0], [2, 10], [1, 10]], {}),
    ],
)
def test_lic5_met(points, parameters):
    """
    LIC 5 should be met when there exists at least one set of two consecutive data
    points, (X[i],Y[i]) and (X[j],Y[j]), such that X[j] - X[i] < 0. (where i = j-1)
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_5(points) is True


@pytest.mark.parametrize(
    "points,parameters",
    [([[0, 0], [1, 4], [2, 2]], {}), ([[0, 0], [0, -1], [0, -2]], {})],
)
def test_lic5_not_met(points, parameters):
    """
    LIC 5 should not be met when the x-coordinates of the points in the list increase
    monotonically
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_5(points) is False


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[0, 0], [1, 2], [3, 0]], {"n_pts": 3, "dist": 0}),
        ([[0, 0], [2, 2], [0, 0]], {"n_pts": 3, "dist": 1}),
        ([[0, 0], [1, 1], [2, 2], [0, 3]], {"n_pts": 4, "dist": 1.5}),
    ],
)
def test_lic6_met(points, parameters):
    """
    LIC 6 should be met when there exists N_PTS consecutive data points such that at
    least one of the points lies a distance greater than DIST from the line joining
    the first and last of these N_PTS points

    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_6(points) is True


@pytest.mark.parametrize(
    "points,parameters",
    [
        ([[0, 0], [1, 1]], {"n_pts": 2, "dist": 1}),
        ([[0, 0], [1, 2], [2, 0]], {"n_pts": 2, "dist": 1}),
        ([[0, 0], [1, 2], [3, 0]], {"n_pts": 3, "dist": 3}),
        ([[0, 0], [1, 1], [2, 2]], {"n_pts": 3, "dist": 0}),
    ],
)
def test_lic6_not_met(points, parameters):
    """
    LIC 6 should not be met when no set of lie a distance greater than DIST from the
    line joining the first and last point, or when NUMPOINTS<3
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.lic_6(points) is False


@pytest.mark.parametrize(
    "points,parameters", [([[0, 0], [2, 2], [0, 0]], {"n_pts": 4, "dist": 1})]
)
def test_lic6_n_pts_value_error(points, parameters):
    """
    Allowed values of N_PTS should be between 3 (inclusive) and NUMPOINTS (inclusive)
    But when N_PTS < 3 the function fails graciously (returns False) instead of raising
    an error
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    with pytest.raises(ValueError):
        lauch_conditions.lic_6(points)


@pytest.mark.parametrize(
    "points,parameters", [([[0, 0], [2, 2], [0, 0]], {"n_pts": 3, "dist": -1})]
)
def test_lic6_dist_value_error(points, parameters):
    """
    DIST parameter shall be positive
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    with pytest.raises(ValueError):
        lauch_conditions.lic_6(points)


@pytest.mark.parametrize(
    "points, parameters, expected_cmv",
    [
        (
            [[0, 0], [1, 0], [2, 0], [3, 0], [3, 3]],
            {
                "length1": 2,
                "epsilon": math.pi / 2,
                "area1": 2,
                "radius1": 1,
                "q_pts": 3,
                "quads": 1,
                "n_pts": 3,
                "dist": 1.5,
            },
            [
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            ],
        )
    ],
)
def test_populate_cmv(points, parameters, expected_cmv):
    """
    CMV should be correctly populated for a set of points given the parameters
    """
    lauch_conditions = decide.LaunchInterceptorConditions(parameters)
    assert lauch_conditions.get_conditions_met_vector(points) == expected_cmv
