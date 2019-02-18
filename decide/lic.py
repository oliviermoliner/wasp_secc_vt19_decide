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
        # calculate the semi-perimeter
        s = (a + b + c) / 2
        # calculate the area
        A = math.sqrt((s * (s - a) * (s - b) * (s - c)))
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


def float_almost_equal(a, b, epsilon=0.00000001):
    if abs(a - b) < epsilon:
        return True
    else:
        return False


def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
