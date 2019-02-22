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
        point1 = Point(points[i])
        point2 = Point(points[i + 1])
        dist = point1.distance(point2)
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
        point1 = Point(points[i])
        point2 = Point(points[i + 1])
        point3 = Point(points[i + 2])

        # If a, b and c are the lengths of the sides and A is the area of the given
        # triangle, the radius of the circumscribed circle is given by : R = a*b*c/(4*A)
        a = point1.distance(point2)
        b = point1.distance(point3)
        c = point2.distance(point3)
        triangle = Triangle(point1, point2, point3)
        A = triangle.area()
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
        first_point = Point(points[i])
        vertex = Point(points[i + 1])
        last_point = Point(points[i + 2])

        if vertex in (first_point, last_point):
            # If either the first point or the last point (or both) coincides with the
            # vertex, the angle is undefined and the LIC is not satisfied by those
            # three points.
            continue
        else:
            angle = math.atan2(
                last_point.y - vertex.y, last_point.x - vertex.x
            ) - math.atan2(first_point.y - vertex.y, first_point.x - vertex.x)
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
        triangle = Triangle(
            Point(points[i]), Point(points[i + 1]), Point(points[i + 2])
        )

        if triangle.area() > parameters["area1"]:
            return True
    return False


def lic_4(points, parameters):
    """ Checks whether Launch Interceptor Condition 4 is met

    Determines whether there exists at least one set of Q_PTS consecutive data points
    that lie in more than QUADS quadrants.

    Args:
        points (list): List of coordinates of data points
        parameters (dict): Parameters for the LICs

    Returns
        bool: True if the condition is met
    """
    if parameters["q_pts"] < 2 or parameters["q_pts"] > len(points):
        raise ValueError("Q_PTS value outside allowed range")
    if parameters["quads"] < 1 or parameters["quads"] > 3:
        raise ValueError("QUADS value outside allowed range")

    # Rolling list containing the quadrant ids of the latest Q_PTS points
    quadrants_list = [None] * parameters["q_pts"]

    for i in range(len(points)):
        point = Point(points[i])
        # Add the quadrant id of the current point to the rolling list
        quadrants_list[i % parameters["q_pts"]] = point.quadrant()
        # Count the number of unique quadrants in the list
        num_quads = len(
            set([value for idx, value in enumerate(quadrants_list, 1) if value])
        )

        if num_quads > parameters["quads"]:
            return True
    return False


def float_almost_equal(a, b, epsilon=0.00000001):
    if abs(a - b) < epsilon:
        return True
    else:
        return False


class Point:
    """Point class

    Attributes:
        coordinates (list): [x,y] coordinates of the point
    """

    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def quadrant(self):
        """ Determines which quadrant the point lies in

        Where there is ambiguity as to which quadrant contains a given point, priority
        of decision will be by quadrant number, i.e., I, II, III, IV

        Returns
            int: The quadrant number (1-4)
        """
        if self.x >= 0.0 and self.y >= 0.0:
            return 1

        if self.x <= 0.0 and self.y >= 0.0:
            return 2

        if self.x <= 0.0 and self.y <= 0.0:
            return 3

        if self.x >= 0.0 and self.y <= 0.0:
            return 4

    def distance(self, other_point):
        """ Determines the distance to another point

        Args:
            other_point (Point): The other point

        Returns
            float: The distance
        """
        return math.sqrt((other_point.x - self.x) ** 2 + (other_point.y - self.y) ** 2)


class Triangle:
    """Triangle class

    Attributes:
        a (Point): first vertex
        b (Point): second vertex
        c (Point): third vertex
    """

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self._area = None

    def area(self):
        """ Calculates the area of the triangle using Heron's formula

        Returns
            float: The area

        """
        if self._area is None:
            length1 = self.a.distance(self.b)
            length2 = self.a.distance(self.c)
            length3 = self.b.distance(self.c)

            # calculate the semi-perimeter
            s = (length1 + length2 + length3) / 2
            # calculate the area
            self._area = math.sqrt((s * (s - length1) * (s - length2) * (s - length3)))
        return self._area
