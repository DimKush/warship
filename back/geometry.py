from math import sin, cos
from typing import List

from back.point import Point, AngleMovement, Movement


class Geometry:
    def __init__(self, x: float, y: float):
        self.axis = Point(x, y)
        self.bounds = []
        self.angle_motion = AngleMovement()
        self.vector_motion = Movement()
        self.z_index = 1
        self.tangible = True

    @property
    def x(self):
        return self.axis.x

    @property
    def y(self):
        return self.axis.y

    @property
    def bounding_box(self):
        if self.bounds is not None:
            min_x = min(self.bounds, key=lambda a: a.x).x
            min_y = min(self.bounds, key=lambda a: a.y).y
            max_x = max(self.bounds, key=lambda a: a.x).x
            max_y = max(self.bounds, key=lambda a: a.y).y
            return min_x, min_y, max_x, max_y
        else:
            return 0, 0, 0, 0

    def next(self, t):
        self.angle_motion.set_next(t)
        self.vector_motion.set_next(t)

        x_delta = self.vector_motion.current * sin(self.angle_motion.angle_current) * t
        y_delta = self.vector_motion.current * cos(self.angle_motion.angle_current) * t

        for point in self.bounds:
            tmp_x = (point.x - self.x) * cos(self.angle_motion.current * t) + self.x - \
                (point.y - self.y) * sin(self.angle_motion.current * t) - x_delta
            point.y = (point.y - self.y) * cos(self.angle_motion.current * t) + self.y + \
                (point.x - self.x) * sin(self.angle_motion.current * t) + y_delta
            point.x = tmp_x

        self.axis.x -= x_delta
        self.axis.y += y_delta

    def box_collision(self, bounding_box: List[float]):
        x1, y1, x2, y2 = self.bounding_box
        x3, y3, x4, y4 = bounding_box
        if (x2 >= x3) and (x4 >= x1) and (y2 >= y3) and (y4 >= y1):
            return True
        return False

    def detail_collision(self, bounds):
        for p1, p2 in self.get_segments(self.bounds):
            for p3, p4 in self.get_segments(bounds):
                if self.vector_multiple(p1, p3, p2) * self.vector_multiple(p1, p4, p2) <= 0 and \
                        self.vector_multiple(p3, p1, p4) * self.vector_multiple(p3, p2, p4) <= 0:
                    return True
        return False

    @staticmethod
    def vector_multiple(p0: Point, p1: Point, p2: Point):
        return (p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y)

    @staticmethod
    def get_segments(bounds: List[Point]):
        return [(bounds[i], bounds[(i + 1) % len(bounds)]) for i in range(0, len(bounds))]


class GeometryLine(Geometry):
    def __init__(self, x: float, y: float, r: float):
        super().__init__(x, y)

        self.angle_motion.moving = 1
        self.angle_motion.angle_curr = r

    def next(self, t):
        x_delta = self.vector_motion.current * sin(self.angle_motion.angle_current) * t
        y_delta = self.vector_motion.current * cos(self.angle_motion.angle_current) * t

        for point in self.bounds:
            point.x -= x_delta
            point.y += y_delta

        self.axis.x -= x_delta
        self.axis.y += y_delta

    def rebuild(self):
        for point in self.bounds:
            tmp_x = self.x + (point.x - self.x) * cos(self.angle_motion.angle_curr) - (point.y - self.y) * sin(
                self.angle_motion.angle_curr)
            point.y = self.y + (point.y - self.y) * cos(self.angle_motion.angle_curr) + (point.x - self.x) * sin(
                self.angle_motion.angle_curr)
            point.x = tmp_x
