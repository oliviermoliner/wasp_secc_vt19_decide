import math
import numpy as np


def lic_0(points, parameters):
    """ Checks whether Launch Interceptor Condition 0 is met

    Determines whether there exist two consecutive points that are a distance
    greater than LENGTH1 apart

    Args:
        points (list): List of coordinates of data points
        parameters (dict): Parameters for the LICs

    Returns
        bool: True if the condition is met
    """
    for i in range(len(points) - 1):
        point1 = [points[i][0], points[i][1]]
        point2 = [points[i + 1][0], points[i + 1][1]]
        dist = distance(point1, point2)
        if dist > parameters["length1"]:
            return True
    return False


def lic_1(points, parameters):
    """ Checks whether Launch Interceptor Condition 1 is met

    Determines whether there exists at least one set of three consecutive data points
    that cannot all be contained within or on a circle of radius RADIUS1

    Args:
        points (list): List of coordinates of data points
        parameters (dict): Parameters for the LICs

    Returns
        bool: True if the condition is met
    """
    for i in range(len(points) - 2):
        point1 = [points[i][0], points[i][1]]
        point2 = [points[i + 1][0], points[i + 1][1]]
        point3 = [points[i + 2][0], points[i + 2][1]]

        # If a, b and c are the lengths of the sides and A is the area of the given
        # triangle, the radius of the circumscribed circle is given by : R = a*b*c/(4*A)
        a = distance(point1, point2)
        b = distance(point1, point3)
        c = distance(point2, point3)
        A = triangle_area(point1, point2, point3)
        if A == 0:
            # The points are collinear: R is the longest length
            R = np.max([a, b, c])
        else:
            # calculate the radius
            R = a * b * c / (A * 4)
        if R > parameters["radius1"] and not float_almost_equal(
            R, parameters["radius1"]
        ):
            return True
    return False


def lic_2(points, parameters):
    """ Checks whether Launch Interceptor Condition 2 is met

    Determines whether there exists at least one set of three consecutive data points
    which form an angle such that: angle < (PI − EPSILON) or angle > (PI + EPSILON)

    Args:
        points (list): List of coordinates of data points
        parameters (dict): Parameters for the LICs

    Returns
        bool: True if the condition is met
    """
    if parameters["epsilon"] < 0 or parameters["epsilon"] >= math.pi:
        raise ValueError("EPSILON value outside allowed range")
    for i in range(len(points) - 2):
        first_point = [points[i][0], points[i][1]]
        vertex = [points[i + 1][0], points[i + 1][1]]
        last_point = [points[i + 2][0], points[i + 2][1]]

        if vertex in (first_point, last_point):
            # If either the first point or the last point (or both) coincides with the
            # vertex, the angle is undefined and the LIC is not satisfied by those
            # three points.
            continue
        else:
            angle = math.atan2(
                last_point[1] - vertex[1], last_point[0] - vertex[0]
            ) - math.atan2(first_point[1] - vertex[1], first_point[0] - vertex[0])
            if angle < 0:
                angle = angle + 2 * math.pi
            if not float_almost_equal(math.pi, angle, parameters["epsilon"]):
                return True
    return False


def lic_3(points, parameters):
    """ Checks whether Launch Interceptor Condition 3 is met

    Determines whether there exists at least one set of three consecutive data points
    that are the vertices of a triangle with area greater than AREA1

    Args:
        points (list): List of coordinates of data points
        parameters (dict): Parameters for the LICs

    Returns
        bool: True if the condition is met
    """
    if parameters["area1"] < 0:
        raise ValueError("AREA1 value outside allowed range")
    for i in range(len(points) - 2):
        point1 = [points[i][0], points[i][1]]
        point2 = [points[i + 1][0], points[i + 1][1]]
        point3 = [points[i + 2][0], points[i + 2][1]]

        if triangle_area(point1, point2, point3) > parameters["area1"]:
            return True
    return False


def float_almost_equal(a, b, epsilon=0.00000001):
    if abs(a - b) < epsilon:
        return True
    else:
        return False


def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


def triangle_area(point1, point2, point3):
    """ Calculates the area of a triangle using Heron's formula
    Args:
        point1 (float): First vertex of the triangle
        point2 (float): Second vertex of the triangle
        point3 (float): Third vertex of the triangle

    Returns
        float: The area

    """
    a = distance(point1, point2)
    b = distance(point1, point3)
    c = distance(point2, point3)

    # calculate the semi-perimeter
    s = (a + b + c) / 2
    # calculate the area
    return math.sqrt((s * (s - a) * (s - b) * (s - c)))


def quadrant(point):
    """ Determines which quadrant a point lies in

    Where there is ambiguity as to which quadrant contains a given point, priority of
    decision will be by quadrant number, i.e., I, II, III, IV

    Args:
        point (list): Coordinates of the point

    Returns
        int: The quadrant number (1-4)
    """
    if point[0] >= 0.0 and point[1] >= 0.0:
        return 1

    if point[0] <= 0.0 and point[1] >= 0.0:
        return 2

    if point[0] <= 0.0 and point[1] <= 0.0:
        return 3

    if point[0] >= 0.0 and point[1] <= 0.0:
        return 4
