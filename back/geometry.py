from math import sin, cos
from typing import List

from back.point import AngleMovement, Movement


class Geometry:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.bounds = []
        self.bounding_box = [0, 0, 0, 0]
        self.angle_motion = AngleMovement()
        self.vector_motion = Movement()

    def eval_true_bounding_box(self):
        if self.bounds:
            min_x = min(self.bounds, key=lambda a: a[0])[0]
            min_y = min(self.bounds, key=lambda a: a[1])[1]
            max_x = max(self.bounds, key=lambda a: a[0])[0]
            max_y = max(self.bounds, key=lambda a: a[1])[1]
            self.bounding_box = [min_x, min_y, max_x, max_y]
        else:
            self.bounding_box = [0, 0, 0, 0]

    def eval_approximately_bounding_box(self):
        s = 40
        self.bounding_box = [self.x - s, self.y - s, self.x + s, self.y + s]

    def next(self, t):
        self.angle_motion.set_next(t)
        self.vector_motion.set_next(t)

        x_delta = self.vector_motion.current * sin(self.angle_motion.angle_current) * t
        y_delta = self.vector_motion.current * cos(self.angle_motion.angle_current) * t

        for point in self.bounds:
            tmp_x = (point[0] - self.x) * cos(self.angle_motion.current * t) + self.x - \
                    (point[1] - self.y) * sin(self.angle_motion.current * t) - x_delta
            point[1] = (point[1] - self.y) * cos(self.angle_motion.current * t) + self.y + \
                       (point[0] - self.x) * sin(self.angle_motion.current * t) + y_delta
            point[0] = tmp_x

        self.x -= x_delta
        self.y += y_delta

        self.bounding_box[0] -= x_delta
        self.bounding_box[2] -= x_delta
        self.bounding_box[1] += y_delta
        self.bounding_box[3] += y_delta

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
    def vector_multiple(p0, p1, p2):
        return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])

    @staticmethod
    def get_segments(bounds):
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
            point[0] -= x_delta
            point[1] += y_delta

        self.bounding_box[0] -= x_delta
        self.bounding_box[2] -= x_delta
        self.bounding_box[1] += y_delta
        self.bounding_box[3] += y_delta

        self.x -= x_delta
        self.y += y_delta

    def rebuild(self):
        for point in self.bounds:
            tmp_x = self.x + (point[0] - self.x) * cos(self.angle_motion.angle_curr) - (point[1] - self.y) * sin(
                self.angle_motion.angle_curr)
            point[1] = self.y + (point[1] - self.y) * cos(self.angle_motion.angle_curr) + (point[0] - self.x) * sin(
                self.angle_motion.angle_curr)
            point[0] = tmp_x
