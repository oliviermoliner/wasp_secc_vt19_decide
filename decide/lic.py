import math


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
        dist = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
        if dist > parameters["length1"]:
            return True
    return False
