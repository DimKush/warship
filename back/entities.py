import json
import uuid
from copy import deepcopy
from math import cos, sin

from back.config import AREA_WIDTH
from back.geometry import Geometry
from back.point import Point, Movement, AngleMovement, PointEncoder
from back.ships import MainShip


class Entity:
    def __init__(self, x: float, y: float):
        self.curr_geometry: Geometry = Geometry(x, y)
        self.prev_geometry: Geometry = self.curr_geometry
        self.type = 'Object'
        self.id = 0

    @property
    def x(self):
        return self.curr_geometry.x

    @property
    def y(self):
        return self.curr_geometry.y

    def next(self, t: float, others):
        self.prev_geometry = deepcopy(self.curr_geometry)
        self.curr_geometry.next(t)

        for entity in others:
            if entity != self:
                if self.curr_geometry.box_collision(entity.curr_geometry.bounding_box) and \
                        self.curr_geometry.detail_collision(entity.curr_geometry.bounds):
                    self.curr_geometry = self.prev_geometry
                    self.curr_geometry.vector_motion.curr *= -1
                    self.curr_geometry.angle_motion.curr *= -1

    def set_moving(self, angle_moving, speed_moving):
        self.curr_geometry.angle_motion.moving = angle_moving
        self.curr_geometry.vector_motion.moving = speed_moving

    def set_action(self, flag: int):
        pass

    def do_action(self, time_delta):
        pass

    def get_info(self):
        return json.loads(json.dumps({'id': self.id,
                                      'x': self.curr_geometry.x,
                                      'y': self.curr_geometry.y,
                                      'r': self.curr_geometry.angle_motion.angle_current,
                                      'bounds': self.curr_geometry.bounds,
                                      'aabb': self.curr_geometry.bounding_box,
                                      'type': self.type
                                      }, cls=PointEncoder))


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.id = str(uuid.uuid1())
        self.ship_model = MainShip()
        self.curr_geometry.bounds = [Point(self.x + p.x, self.y + p.y) for p in self.ship_model.bounds]
        self.curr_geometry.vector_motion = Movement(delta=self.ship_model.acceleration,
                                                    max_value=self.ship_model.speed)
        self.curr_geometry.angle_motion = AngleMovement(delta=self.ship_model.mobility * 0.1,
                                                        max_value=self.ship_model.mobility * 0.02)
        self.shot_counter = 0
        self.shoting = False

    def get_info(self):
        return json.loads(json.dumps({'id': self.id,
                                      'x': self.x,
                                      'y': self.y,
                                      'r': self.curr_geometry.angle_motion.angle_current,
                                      'bounds': self.curr_geometry.bounds,
                                      'aabb': self.curr_geometry.bounding_box,
                                      'type': self.ship_model.name,
                                      'hp': self.ship_model.hp
                                      }, cls=PointEncoder))

    def set_action(self, flag: int):
        self.shoting = flag != 0

    def do_action(self, time_delta):
        if self.shot_counter <= 0:
            if self.shoting:
                bullet = Bullet(self.x, self.y, self.curr_geometry.angle_motion.angle_current, self.id)
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
        self.curr_geometry.bounds = [Point(0, 0),
                                     Point(AREA_WIDTH - 1, 0),
                                     Point(AREA_WIDTH - 1, 2),
                                     Point(0, 2)]
