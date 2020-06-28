import json
import uuid
from copy import deepcopy
from math import cos, sin

from back.config import AREA_WIDTH, AREA_HEIGHT
from back.geometry import Geometry, GeometryLine
from back.point import Point, Movement, AngleMovement, PointEncoder
from back.ships import MainShip


class Entity:
    def __init__(self, x: float, y: float):
        self.geometry: Geometry = Geometry(x, y)
        self.prev_geometry: Geometry = self.geometry
        self.type = 'Object'
        self.id = 0
        self.hp = 1

    @property
    def x(self):
        return self.geometry.x

    @property
    def y(self):
        return self.geometry.y

    def next(self, t: float, others):
        self.prev_geometry = deepcopy(self.geometry)
        self.geometry.next(t)

        for entity in others:
            if entity != self and \
                    not (isinstance(self, Bullet) and self.owner_id == entity.id) and \
                    not (isinstance(entity, Bullet) and entity.owner_id == self.id):
                if self.geometry.box_collision(entity.geometry.bounding_box) and \
                        self.geometry.detail_collision(entity.geometry.bounds):
                    self.action_on_collision(entity)

    def action_on_collision(self, entity):
        pass

    def set_moving(self, angle_moving, speed_moving):
        self.geometry.angle_motion.moving = angle_moving
        self.geometry.vector_motion.moving = speed_moving

    def set_action(self, flag: int):
        pass

    def do_action(self, time_delta):
        pass

    def get_info(self):
        return json.loads(json.dumps({'id': self.id,
                                      'x': self.x,
                                      'y': self.y,
                                      'r': self.geometry.angle_motion.angle_current,
                                      'bounds': self.geometry.bounds,
                                      'aabb': self.geometry.bounding_box,
                                      'type': self.type
                                      }, cls=PointEncoder))


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.id = str(uuid.uuid1())
        self.ship_model = MainShip()
        self.geometry.bounds = [Point(self.x + p.x, self.y + p.y) for p in self.ship_model.bounds]
        self.geometry.vector_motion = Movement(delta=self.ship_model.acceleration,
                                               max_value=self.ship_model.speed)
        self.geometry.angle_motion = AngleMovement(delta=self.ship_model.mobility * 2.8,
                                                   max_value=self.ship_model.mobility)
        self.hp = self.ship_model.hp
        self.shot_counter = 0
        self.shoting = False

    def get_info(self):
        return json.loads(json.dumps({'id': self.id, 'x': self.x, 'y': self.y,
                                      'r': self.geometry.angle_motion.angle_current,
                                      'bounds': self.geometry.bounds,
                                      'aabb': self.geometry.bounding_box,
                                      'type': self.ship_model.name,
                                      'hp': self.hp
                                      }, cls=PointEncoder))

    def set_action(self, flag: int):
        self.shoting = flag != 0

    def do_action(self, time_delta):
        if self.shot_counter <= 0:
            if self.shoting:
                bullet = Bullet(self.x, self.y, self.geometry.angle_motion.angle_current, self)
                self.shot_counter = 1 / self.ship_model.shot_speed
                return bullet
        elif self.shot_counter > 0:
            self.shot_counter -= time_delta
        return None

    def action_on_collision(self, entity):
        if isinstance(entity, Player):
            self.geometry = self.prev_geometry
            self.geometry.vector_motion.curr *= -1
            self.geometry.angle_motion.curr *= -1


class Bullet(Entity):
    def __init__(self, x: float, y: float, r: float, owner: Player):
        super().__init__(x, y)
        self.id = 1
        self.owner_id = owner.id
        self.damage = owner.ship_model.bullet_damage
        self.geometry = GeometryLine(x, y, r)

        self.geometry.vector_motion = Movement(curr_value=owner.ship_model.bullet_speed,
                                               max_value=owner.ship_model.bullet_speed)
        self.type = 'Bullet'

    def action_on_collision(self, entity):
        if isinstance(entity, Player):
            entity.hp -= self.damage
            self.hp = 0


class Statics(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.geometry.bounds = [Point(4, 4),
                                Point(AREA_WIDTH - 8, 4),
                                Point(AREA_WIDTH - 8, AREA_HEIGHT - 8),
                                Point(AREA_HEIGHT - 8, 4)]
