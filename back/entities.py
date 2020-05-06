import json
import uuid
from math import cos, sin

from back.config import AREA_WIDTH, AREA_HEIGHT
from back.point import Point, Movement, AngleMovement, PointEncoder
from back.ships import MainShip


class Entity:
    def __init__(self, x: float, y: float):
        self.axis = Point(x, y)
        self.bounds = None
        self.z_index = 1
        self.tangible = True
        self.angle_motion = AngleMovement(curr_value=10, delta=1.3, max_value=40)
        self.vector_motion = Movement(curr_value=0, delta=1, max_value=100)

    @property
    def x(self):
        return self.axis.x

    @property
    def y(self):
        return self.axis.y

    @property
    def bounding_box(self):
        if self.bounds is not None:
            min_x = min(point.x for point in self.bounds)
            min_y = min(point.y for point in self.bounds)
            max_x = max(point.x for point in self.bounds)
            max_y = max(point.y for point in self.bounds)
            return min_x, min_y, max_x, max_y
        else:
            return 0, 0, 0, 0

    def next(self, t: float):
        self.angle_motion.set_next(t)
        self.vector_motion.set_next(t)

        x_delta = self.vector_motion.current * sin(self.angle_motion.angle_current) * t
        y_delta = self.vector_motion.current * cos(self.angle_motion.angle_current) * t

        new_bounds = []
        for point in self.bounds:
            x = self.x + (point.x - self.x) * cos(self.angle_motion.current) - (point.y - self.y) * sin(
                self.angle_motion.current) - x_delta
            y = self.y + (point.y - self.y) * cos(self.angle_motion.current) + (point.x - self.x) * sin(
                self.angle_motion.current) + y_delta
            x %= AREA_WIDTH
            y %= AREA_HEIGHT
            new_bounds.append(Point(x, y))
        self.bounds = new_bounds

        self.axis.x -= x_delta
        self.axis.y += y_delta

        self.axis.x = self.axis.x % AREA_WIDTH
        self.axis.y = self.axis.y % AREA_HEIGHT

    def set_moving(self, angle_moving, speed_moving):
        self.angle_motion.moving = angle_moving
        self.vector_motion.moving = speed_moving

    def set_shot(self, flag: int):
        pass

    def shot(self):
        pass

    def get_info(self):
        return json.loads(json.dumps({'id': self.id,
                                      'x': self.x,
                                      'y': self.y,
                                      'r': self.angle_motion.angle_current,
                                      'bounds': self.bounds,
                                      'aabb': self.bounding_box
                                      }, cls=PointEncoder))


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.id = str(uuid.uuid1())
        self.ship_model = MainShip()
        self.bounds = [Point(self.x + p.x, self.y + p.y) for p in self.ship_model.bounds]
        self.shot_counter = 0
        self.shoting = False

    def get_info(self):
        return json.loads(json.dumps({'id': self.id,
                                      'x': self.x,
                                      'y': self.y,
                                      'r': self.angle_motion.angle_current,
                                      'bounds': self.bounds,
                                      'aabb': self.bounding_box
                                      }, cls=PointEncoder))

    def set_shot(self, flag: int):
        self.shoting = flag != 0

    def shot(self):
        if self.shot_counter == 0:
            if self.shoting:
                bullet = Bullet(self.x, self.y, self.angle_motion.angle_current)
                self.shot_counter = 60
                return bullet
        elif self.shot_counter > 0:
            self.shot_counter -= 1
        return None


class Bullet(Entity):
    def __init__(self, x: float, y: float, r: float):
        super().__init__(x, y)
        self.id = 1
        self.bounds = [Point(self.x + -12, self.y + 0), Point(self.x + 0, self.y + 20), Point(self.x + 12, self.y + 0)]
        self.angle_motion = AngleMovement()
        self.angle_motion.moving = 1
        self.angle_motion.angle_curr = r
        new_bounds = []
        for point in self.bounds:
            x = self.x + (point.x - self.x) * cos(self.angle_motion.angle_curr) - (point.y - self.y) * sin(
                self.angle_motion.angle_curr)
            y = self.y + (point.y - self.y) * cos(self.angle_motion.angle_curr) + (point.x - self.x) * sin(
                self.angle_motion.angle_curr)
            new_bounds.append(Point(x, y))
        self.bounds = new_bounds
        self.vector_motion = Movement(curr_value=200, delta=0, max_value=200)
