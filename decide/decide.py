import math
import numpy as np


class Decide:
    """Decide class

    Attributes:
        parameters (dict): Parameters for the LICs
        lcm (list): Logical Connector Matrix
        puv (list): Preliminary Unlocking Vector
    """

    def __init__(self, parameters, lcm, puv):
        self.parameters = parameters
        self.lcm = lcm
        self.puv = puv

    def compute_preliminary_unlocking_matrix(self, cmv):
        """ Computes the Preliminary Unlocking Matrix

        Uses the Conditions Met Vector in conjunction with the Logical Connector Matrix
        to form the Preliminary Unlocking Matrix (PUM)

        Args:
            points (list): List of coordinates of data points

        Returns
            list: The PUM as a 2-d list of booleans
        """
        pum = [[None] * 15 for i in range(15)]

        for row in range(15):
            for column in range(15):
                if self.lcm[row][column] == "ANDD":
                    pum[row][column] = cmv[row] and cmv[column]
                elif self.lcm[row][column] == "ORR":
                    pum[row][column] = cmv[row] or cmv[column]
                else:
                    pum[row][column] = True
        return pum


class LaunchInterceptorConditions:
    """Launch Interceptor Conditions class

    Contains methods to evaluate each of the Launch Interceptor Conditions (LIC) on
    data points given the parameter values.

    Attributes:
        parameters (dict): Parameters for the LICs
    """

    def __init__(self, parameters):
        self.parameters = parameters

    def get_conditions_met_vector(self, points):
        """ Gets the Conditions Met Vector for the data points

        Each element of the Conditions Met Vector (CMV) is set according to the evaluation
        of each of the Launch Interceptor Conditions (LIC) given the parameter values.

        Args:
            points (list): List of coordinates of data points

        Returns
            list: The CMV as a list of booleans
        """
        cmv = [False] * 15

        cmv[0] = self.lic_0(points)
        cmv[1] = self.lic_1(points)
        cmv[2] = self.lic_2(points)
        cmv[3] = self.lic_3(points)
        cmv[4] = self.lic_4(points)
        cmv[5] = self.lic_5(points)
        cmv[6] = self.lic_6(points)

        return cmv

    def lic_0(self, points):
        """ Checks whether Launch Interceptor Condition 0 is met

        Determines whether there exist two consecutive points that are a distance
        greater than LENGTH1 apart

        Args:
            points (list): List of coordinates of data points

        Returns
            bool: True if the condition is met
        """
        for i in range(len(points) - 1):
            point1 = Point(points[i])
            point2 = Point(points[i + 1])
            dist = point1.distance(point2)
            if dist > self.parameters["length1"]:
                return True
        return False

    def lic_1(self, points):
        """ Checks whether Launch Interceptor Condition 1 is met

        Determines whether there exists at least one set of three consecutive data points
        that cannot all be contained within or on a circle of radius RADIUS1

        Args:
            points (list): List of coordinates of data points

        Returns
            bool: True if the condition is met
        """
        for i in range(len(points) - 2):
            triangle = Triangle(
                Point(points[i]), Point(points[i + 1]), Point(points[i + 2])
            )
            R = triangle.circumradius()
            if R > self.parameters["radius1"] and not float_almost_equal(
                R, self.parameters["radius1"]
            ):
                return True
        return False

    def lic_2(self, points):
        """ Checks whether Launch Interceptor Condition 2 is met

        Determines whether there exists at least one set of three consecutive data points
        which form an angle such that: angle < (PI − EPSILON) or angle > (PI + EPSILON)

        Args:
            points (list): List of coordinates of data points

        Returns
            bool: True if the condition is met
        """
        if self.parameters["epsilon"] < 0 or self.parameters["epsilon"] >= math.pi:
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
                angle = Triangle(first_point, vertex, last_point).angle_abc()
                if not float_almost_equal(math.pi, angle, self.parameters["epsilon"]):
                    return True
        return False

    def lic_3(self, points):
        """ Checks whether Launch Interceptor Condition 3 is met

        Determines whether there exists at least one set of three consecutive data points
        that are the vertices of a triangle with area greater than AREA1

        Args:
            points (list): List of coordinates of data points

        Returns
            bool: True if the condition is met
        """
        if self.parameters["area1"] < 0:
            raise ValueError("AREA1 value outside allowed range")
        for i in range(len(points) - 2):
            triangle = Triangle(
                Point(points[i]), Point(points[i + 1]), Point(points[i + 2])
            )

            if triangle.area() > self.parameters["area1"]:
                return True
        return False

    def lic_4(self, points):
        """ Checks whether Launch Interceptor Condition 4 is met

        Determines whether there exists at least one set of Q_PTS consecutive data points
        that lie in more than QUADS quadrants.

        Args:
            points (list): List of coordinates of data points

        Returns
            bool: True if the condition is met
        """
        if self.parameters["q_pts"] < 2 or self.parameters["q_pts"] > len(points):
            raise ValueError("Q_PTS value outside allowed range")
        if self.parameters["quads"] < 1 or self.parameters["quads"] > 3:
            raise ValueError("QUADS value outside allowed range")

        # Rolling list containing the quadrant ids of the latest Q_PTS points
        quadrants_list = [None] * self.parameters["q_pts"]

        for i in range(len(points)):
            point = Point(points[i])
            # Add the quadrant id of the current point to the rolling list
            quadrants_list[i % self.parameters["q_pts"]] = point.quadrant()
            # Count the number of unique quadrants in the list
            num_quads = len(
                set([value for idx, value in enumerate(quadrants_list, 1) if value])
            )

            if num_quads > self.parameters["quads"]:
                return True
        return False

    def lic_5(self, points):
        """ Checks whether Launch Interceptor Condition 5 is met

        Determines whether there exists at least one set of two consecutive data points,
        (X[i],Y[i]) and (X[j],Y[j]), such that X[j] - X[i] < 0. (where i = j-1)

        Args:
            points (list): List of coordinates of data points

        Returns
            bool: True if the condition is met
        """
        for i in range(len(points) - 1):
            if Point(points[i + 1]).x < Point(points[i]).x:
                return True
        return False

    def lic_6(self, points):
        """ Checks whether Launch Interceptor Condition 6 is met

        Determines whether there exists  at least one set of N PTS consecutive data points
        such that at least one of the points lies a distance greater than DIST from the
        line joining the first and last of these N PTS points. If the first and last points
        of these N PTS are identical, then the calculated distance to compare with DIST
        will be the distance from the coincident point to all other points of the N PTS
        consecutive points. The condition is not met when NUMPOINTS < 3

        Args:
            points (list): List of coordinates of data points

        Returns
            bool: True if the condition is met
        """
        if self.parameters["n_pts"] > len(points):
            raise ValueError("N_PTS value outside allowed range")
        if self.parameters["dist"] < 0:
            raise ValueError("DIST value outside allowed range")

        n_pts = self.parameters["n_pts"]

        for i in range(len(points) - n_pts + 1):
            start_point = Point(points[i])
            end_point = Point(points[i + n_pts - 1])

            if start_point == end_point:
                for j in range(1, n_pts - 1):
                    dist = start_point.distance(Point(points[i + j]))
                    if dist > self.parameters["dist"]:
                        return True
            else:
                """
                If the points are distinct, the distance from a point P to the line defined
                by start_point and end_point is the perpendicular height from P of the
                triangle defined by P, start_point and end_point.
                The standard formula of the area of the triangle is A = (b*h)/2, where b
                is the length of the base (i.e. the distance between start_point and end_point),
                and h is the height we want to find. Thus h = 2*A / b.
                """
                b = start_point.distance(end_point)
                for j in range(1, n_pts - 1):
                    triangle = Triangle(start_point, end_point, Point(points[i + j]))
                    h = 2 * triangle.area() / b
                    if h > self.parameters["dist"]:
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

    def circumradius(self):
        """ Calculates the radius of the smallest circle containing this Triangle

        If a, b and c are the lengths of the sides and A is the area of the given
        triangle, the radius of the circumscribed circle is given by : R = a*b*c/(4*A)

        Returns
            float: The radius
        """
        length1 = self.a.distance(self.b)
        length2 = self.a.distance(self.c)
        length3 = self.b.distance(self.c)

        if self.area() == 0:
            # The points are collinear: R is the longest length
            R = np.max([length1, length2, length3])
        else:
            # calculate the radius
            R = length1 * length2 * length3 / (self.area() * 4)
        return R

    def angle_abc(self):
        """ Calculates the angle of the triangle at vertex b

        Returns
            float: The angle (0 - 2*PI)

        """
        angle = math.atan2(self.c.y - self.b.y, self.c.x - self.b.x) - math.atan2(
            self.a.y - self.b.y, self.a.x - self.b.x
        )
        if angle < 0:
            angle = angle + 2 * math.pi
        return angle
