import json
import uuid
from copy import copy
from math import cos, sin, pi
from typing import List

from back.config import AREA_WIDTH, AREA_HEIGHT
from back.point import Point, Movement, AngleMovement, PointEncoder
from back.ships import MainShip


class Entity:
    def __init__(self, x: float, y: float):
        self.axis = Point(x, y)
        self.bounds = None
        self.prev_axis = None
        self.prev_bounds = self.bounds
        self.z_index = 1
        self.tangible = True
        self.id = 0
        self.angle_motion = AngleMovement(delta=10, max_value=1)
        self.vector_motion = Movement(delta=50, max_value=100)
        self.prev_angle = self.angle_motion
        self.prev_vector = self.vector_motion
        self.type = 'Object'

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

    def next(self, t: float, others):
        self.prev_angle = AngleMovement(-1 * self.angle_motion.curr,
                                                    self.angle_motion.delta * 180 / pi,
                                                    self.angle_motion.max * 180 / pi,
                                                    self.angle_motion.angle_current)

        self.prev_vector = Movement(-1 * self.vector_motion.curr,
                                                self.vector_motion.delta,
                                                self.vector_motion.max)
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
        self.prev_bounds = copy(self.bounds)
        self.bounds = new_bounds

        self.prev_axis = Point(self.x, self.y)
        self.axis.x -= x_delta
        self.axis.y += y_delta

        for entity in others:
            if entity != self:
                if self.box_collision(entity, self) and self.detail_collision(entity, self):
                    self.axis = self.prev_axis
                    self.bounds = self.prev_bounds

                    if self.vector_motion.curr != 0:
                        self.vector_motion = self.prev_vector
                    if self.angle_motion.curr != 0:
                        self.angle_motion = self.prev_angle

        self.axis.x = self.axis.x % AREA_WIDTH
        self.axis.y = self.axis.y % AREA_HEIGHT

    def set_moving(self, angle_moving, speed_moving):
        self.angle_motion.moving = angle_moving
        self.vector_motion.moving = speed_moving

    def set_shot(self, flag: int):
        pass

    def shot(self, time_delta):
        pass

    def get_info(self):
        return json.loads(json.dumps({'id': self.id,
                                      'x': self.x,
                                      'y': self.y,
                                      'r': self.angle_motion.angle_current,
                                      'bounds': self.bounds,
                                      'aabb': self.bounding_box,
                                      'type': self.type
                                      }, cls=PointEncoder))

    def rollback_coords(self):
        self.axis = self.prev_axis
        self.bounds = self.prev_bounds
        self.vector_motion = self.prev_vector
        self.angle_motion = self.prev_angle



    @staticmethod
    def box_collision(entity_1, entity_2):
        x1, y1, x2, y2 = entity_1.bounding_box
        x3, y3, x4, y4 = entity_2.bounding_box
        if (x2 >= x3) and (x4 >= x1) and (y2 >= y3) and (y4 >= y1):
            return True
        return False

    @staticmethod
    def vector_multiple(p0: Point, p1: Point, p2: Point):
        return (p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y)

    def detail_collision(self, entity_1, entity_2):
        for p1, p2 in self.get_segments(entity_1.bounds):
            for p3, p4 in self.get_segments(entity_2.bounds):
                if self.vector_multiple(p1, p3, p2) * self.vector_multiple(p1, p4, p2) <= 0 and \
                        self.vector_multiple(p3, p1, p4) * self.vector_multiple(p3, p2, p4) <= 0:
                    return True
        return False

    @staticmethod
    def get_segments(bounds: List[Point]):
        return [(bounds[i], bounds[(i + 1) % len(bounds)]) for i in range(0, len(bounds))]


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.id = str(uuid.uuid1())
        self.hp = 100
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
                                      'aabb': self.bounding_box,
                                      'type': self.ship_model.name,
                                      'hp': self.hp
                                      }, cls=PointEncoder))

    def set_shot(self, flag: int):
        self.shoting = flag != 0

    def shot(self, time_delta):
        if self.shot_counter <= 0:
            if self.shoting:
                bullet = Bullet(self.x, self.y, self.angle_motion.angle_current, self.id)
                self.shot_counter = 60
                return bullet
        elif self.shot_counter > 0:
            self.shot_counter -= 1 * time_delta * 100
        return None


class Bullet(Entity):
    def __init__(self, x: float, y: float, r: float, owner_id: str = ''):
        super().__init__(x, y)
        self.id = 1
        self.owner_id = owner_id
        self.damage = 5
        self.bounds = [Point(self.x, self.y), Point(self.x, self.y - 12)]
        self.angle_motion = AngleMovement()
        self.angle_motion.moving = 1
        self.angle_motion.angle_curr = r
        self.type = 'Bullet'
        new_bounds = []
        for point in self.bounds:
            x = self.x + (point.x - self.x) * cos(self.angle_motion.angle_curr) - (point.y - self.y) * sin(
                self.angle_motion.angle_curr)
            y = self.y + (point.y - self.y) * cos(self.angle_motion.angle_curr) + (point.x - self.x) * sin(
                self.angle_motion.angle_curr)
            new_bounds.append(Point(x, y))
        self.bounds = new_bounds
        self.vector_motion = Movement(curr_value=200, delta=0, max_value=200)


class Statics(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.bounds = [Point(0, 0),
                       Point(AREA_WIDTH -1, 0),
                       Point(AREA_WIDTH -1, 2),
                       Point(0, 2)]
