import json
import uuid
from copy import deepcopy
from math import cos, sin
from os.path import join

from back import config
from back.config import AREA_WIDTH, AREA_HEIGHT, SHIPS_PATH, ENTITY_PATH, STATICS_PATH
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
        self.texture = ''
        self.width = 0
        self.height = 0
        self.offset_x = 0
        self.offset_y = 0
        self.context_id = ''

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
                                      'type': self.type,
                                      'texture': self.texture,
                                      'width': self.width,
                                      'height': self.height,
                                      'offset_x': self.offset_x,
                                      'offset_y': self.offset_y,
                                      'context_id': self.context_id
                                      }, cls=PointEncoder))


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.id = str(uuid.uuid1())
        self.ship_model = MainShip()
        self.load_body_configuration(self.ship_model.name)
        self.geometry.bounds = [Point(self.x + p.x, self.y + p.y) for p in self.geometry.bounds]
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
                                      'type': 'Main ship',
                                      'hp': self.hp,
                                      'width': self.width,
                                      'height': self.height,
                                      'offset_x': self.offset_x,
                                      'offset_y': self.offset_y,
                                      'context_id': self.context_id
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
        if isinstance(entity, Player) or isinstance(entity, Statics):
            self.geometry = self.prev_geometry
            self.geometry.vector_motion.curr *= -1
            self.geometry.angle_motion.curr *= -1

    def load_body_configuration(self, file_name: str):
        file_name = file_name if file_name.endswith('.json') else f'{file_name}.json'
        with open(f'{join(SHIPS_PATH, file_name)}', 'r') as f:
            obj = json.loads(f.read())
            self.texture = obj['texture']
            self.context_id = obj['context_id']
            self.width, self.height = obj['width'], obj['height']
            self.offset_x, self.offset_y = obj['offset_x'], obj['offset_y']
            self.geometry.bounds = [Point(p['x'] + obj['offset_x'], p['y'] + obj['offset_y']) for p in obj['points']]


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
        elif isinstance(entity, Statics):
            self.hp = 0


class Statics(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.type = 'Statics'
        self.geometry.bounds = []

    def load_body_configuration(self, file_name: str = None):
        file_name = file_name if file_name.endswith('.json') else f'{file_name}.json'
        f = open(f'{join(STATICS_PATH, file_name)}', 'r')
        obj = json.loads(f.read())

        self.texture = obj['texture']
        self.context_id = obj['context_id']
        self.geometry.axis.x, self.geometry.axis.y = obj['x'], obj['y']
        self.width, self.height = obj['width'], obj['height']
        self.geometry.bounds = [Point(p['x'] + obj['x'] + obj['offset_x'], p['y'] + obj['y'] + obj['offset_y']) for p in obj['points']]