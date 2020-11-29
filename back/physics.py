import json
from abc import ABC, abstractmethod
from math import sin, cos
from os.path import join

from typing import List

from back.config import MODELS_PATH
from back.movement import UniformlyMotion, ConstMotion


class Physics(ABC):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.bounds = []
        self.aabb = [0, 0, 0, 0]
        self._last_delta_time = 0

    @abstractmethod
    def update(self, delta_time):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @property
    def aabb_int(self):
        return int(self.aabb[0]), int(self.aabb[1]), int(self.aabb[2]), int(self.aabb[3])

    def load_points(self, file_name: str):
        file_name = file_name if file_name.endswith('.json') else f'{file_name}.json'
        with open(f'{join(MODELS_PATH, file_name)}', 'r') as f:
            obj = json.loads(f.read())
            self.bounds = [[p['x'] + obj['offset_x'] + self.x, p['y'] + obj['offset_y'] + self.y]
                           for p in obj['points']]
        self.eval_natural_aabb()

    def aabb_collision(self, target_aabb: List[float], ):
        x1, y1, x2, y2 = self.aabb
        x3, y3, x4, y4 = target_aabb
        if (x2 >= x3) and (x4 >= x1) and (y2 >= y3) and (y4 >= y1):
            return True
        return False

    def eval_natural_aabb(self):
        min_x = min(self.bounds, key=lambda a: a[0])[0]
        min_y = min(self.bounds, key=lambda a: a[1])[1]
        max_x = max(self.bounds, key=lambda a: a[0])[0]
        max_y = max(self.bounds, key=lambda a: a[1])[1]
        self.aabb = [min_x, min_y, max_x, max_y]

    def eval_approximately_aabb(self, radius=40):
        self.aabb = [self.x - radius, self.y - radius, self.x + radius, self.y + radius]

    def detail_collision(self, bounds):
        def vector_multiple(_p0, _p1, _p2):
            return (_p1[0] - _p0[0]) * (_p2[1] - _p0[1]) - (_p2[0] - _p0[0]) * (_p1[1] - _p0[1])

        def get_segments(_bounds):
            return [(_bounds[i], _bounds[(i + 1) % len(_bounds)]) for i in range(0, len(_bounds))]

        for p1, p2 in get_segments(self.bounds):
            for p3, p4 in get_segments(bounds):
                if vector_multiple(p1, p3, p2) * vector_multiple(p1, p4, p2) <= 0 and \
                        vector_multiple(p3, p1, p4) * vector_multiple(p3, p2, p4) <= 0:
                    return True
        return False


class CasualPhysics(Physics):
    def __init__(self, x: float, y: float, r: float):
        super().__init__(x, y, r)
        self.angle_motion = ConstMotion()
        self.vector_motion = UniformlyMotion()

    def calculate_coords(self, delta_time):
        r_delta = self.angle_motion.current * delta_time
        self.r += r_delta

        x_delta = self.vector_motion.current * sin(self.r) * delta_time
        y_delta = self.vector_motion.current * cos(self.r) * delta_time

        for point in self.bounds:
            tmp_x = (point[0] - self.x) * cos(self.r * delta_time) + self.x - \
                    (point[1] - self.y) * sin(self.r * delta_time) - x_delta
            point[1] = (point[1] - self.y) * cos(self.r * delta_time) + self.y + \
                       (point[0] - self.x) * sin(self.r * delta_time) + y_delta
            point[0] = tmp_x
        self.x -= x_delta
        self.y += y_delta

        self.aabb[0] -= x_delta
        self.aabb[2] -= x_delta
        self.aabb[1] += y_delta
        self.aabb[3] += y_delta

    def update(self, delta_time):
        self._last_delta_time = delta_time
        self.angle_motion.update(delta_time)
        self.vector_motion.update(delta_time)

        self.calculate_coords(delta_time=delta_time)

    def rollback(self):
        self.calculate_coords(delta_time=-1 * self._last_delta_time)

        self.vector_motion.switch_current()
        self.angle_motion.switch_current()


class LinePhysics(Physics):
    def __init__(self, x: float, y: float, r: float):
        super().__init__(x, y, r)
        self.vector_motion = ConstMotion(moving=1)

    def set_move_speed(self, speed):
        self.vector_motion.set_delta(speed)

    def update(self, delta_time):
        self.vector_motion.update(delta_time)

        x_delta = self.vector_motion.current * sin(self.r) * delta_time
        y_delta = self.vector_motion.current * cos(self.r) * delta_time

        for point in self.bounds:
            point[0] -= x_delta
            point[1] += y_delta

        self.aabb[0] -= x_delta
        self.aabb[2] -= x_delta
        self.aabb[1] += y_delta
        self.aabb[3] += y_delta

        self.x -= x_delta
        self.y += y_delta

    def rollback(self):
        self.update(-1 * self._last_delta_time)

    def load_points(self, file_name: str):
        super(LinePhysics, self).load_points(file_name=file_name)

        for point in self.bounds:
            tmp_x = self.x + (point[0] - self.x) * cos(self.r) - (point[1] - self.y) * sin(self.r)
            point[1] = self.y + (point[1] - self.y) * cos(self.r) + (point[0] - self.x) * sin(self.r)
            point[0] = tmp_x

        self.eval_natural_aabb()
