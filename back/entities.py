import json
import uuid
from copy import deepcopy
from os.path import join

from back.config import SHIPS_PATH, STATICS_PATH
from back.effects import EffectFactory
from back.geometry import Geometry, GeometryLine
from back.point import Movement, AngleMovement
from back.ships import MainShip


class Entity:
    def __init__(self, x: float, y: float):
        self.geometry: Geometry = Geometry(x, y)
        self.prev_geometry: Geometry = deepcopy(self.geometry)
        self.id = 0
        self.hp = 1
        self.context_id = ''
        self.effect_factory = None

    @property
    def x(self):
        return self.geometry.x

    @property
    def y(self):
        return self.geometry.y

    @property
    def r(self):
        return self.geometry.angle_motion.angle_current

    def next(self, t: float, others):
        # save stat of geometry without deepcopy? for frequency
        self.prev_geometry.x = self.geometry.x
        self.prev_geometry.y = self.geometry.y
        self.prev_geometry.bounds = self.geometry.bounds[::]
        self.prev_geometry.bounding_box = self.geometry.bounding_box[::]

        self.prev_geometry.angle_motion.curr = self.geometry.angle_motion.curr
        self.prev_geometry.angle_motion.max = self.geometry.angle_motion.max
        self.prev_geometry.angle_motion.delta = self.geometry.angle_motion.delta
        self.prev_geometry.angle_motion.moving = self.geometry.angle_motion.moving
        self.prev_geometry.angle_motion.angle_curr = self.geometry.angle_motion.angle_curr

        self.prev_geometry.vector_motion.curr = self.geometry.vector_motion.curr
        self.prev_geometry.vector_motion.max = self.geometry.vector_motion.max
        self.prev_geometry.vector_motion.delta = self.geometry.vector_motion.delta
        self.prev_geometry.vector_motion.moving = self.geometry.vector_motion.moving
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

    def set_effect_factory(self, ef: EffectFactory):
        self.effect_factory = ef

    def load_body_configuration(self, file_name: str):
        file_name = file_name if file_name.endswith('.json') else f'{file_name}.json'
        with open(f'{join(SHIPS_PATH, file_name)}', 'r') as f:
            obj = json.loads(f.read())
            self.context_id = obj['context_id']
            self.geometry.bounds = [[p['x'] + obj['offset_x'] + self.x,
                                          p['y'] + obj['offset_y'] + self.y]
                                    for p in obj['points']]
        self.geometry.eval_true_bounding_box()

    def get_info(self):
        return {'id': self.id,
                'type': type(self).__name__,
                'x': self.x,
                'y': self.y,
                'r': self.r,
                'bounds': self.geometry.bounds,
                'aabb': self.geometry.bounding_box,
                'context_id': self.context_id
                }


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.id = str(uuid.uuid1())
        self.name = ''
        self.ship_model = MainShip()
        self.load_body_configuration(self.ship_model.name)
        self.geometry.vector_motion = Movement(delta=self.ship_model.acceleration,
                                               max_value=self.ship_model.speed)
        self.geometry.angle_motion = AngleMovement(delta=self.ship_model.mobility * 2.8,
                                                   max_value=self.ship_model.mobility)
        self.geometry.eval_approximately_bounding_box()
        self.hp = self.ship_model.hp
        self.hp_max = self.ship_model.hp_max
        self.shot_counter = 0
        self.shoting = False

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

    def get_info(self):
        data = super(Player, self).get_info()
        data.update({'hp': self.hp, 'hp_max': self.hp_max, 'name': self.name})
        return data


class Bullet(Entity):
    def __init__(self, x: float, y: float, r: float, owner: Player):
        super().__init__(x, y)
        self.id = 1
        self.owner_id = owner.id
        self.damage = owner.ship_model.bullet_damage
        self.effect_factory: EffectFactory = owner.effect_factory
        self.geometry = GeometryLine(x, y, r)
        self.load_body_configuration(f'bullet_{owner.ship_model.name}')
        self.geometry.rebuild()
        self.geometry.eval_true_bounding_box()
        self.geometry.vector_motion = Movement(curr_value=owner.ship_model.bullet_speed,
                                               max_value=owner.ship_model.bullet_speed)

    def action_on_collision(self, entity):
        if isinstance(entity, Player):
            entity.hp -= self.damage
            self.hp = 0
        elif isinstance(entity, Statics):
            self.hp = 0
        self.effect_factory.add_to_pool('exp1', self.x, self.y)


class Statics(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def load_body_configuration(self, file_name: str = None):
        file_name = file_name if file_name.endswith('.json') else f'{file_name}.json'
        f = open(f'{join(STATICS_PATH, file_name)}', 'r')
        obj = json.loads(f.read())

        self.context_id = obj['context_id']
        self.geometry.x, self.geometry.y = obj['x'], obj['y']
        self.geometry.bounds = [[p['x'] + obj['x'] + obj['offset_x'],
                                      p['y'] + obj['y'] + obj['offset_y']]
                                for p in obj['points']]
        self.geometry.eval_true_bounding_box()

    def next(self, t: float, others):
        pass
