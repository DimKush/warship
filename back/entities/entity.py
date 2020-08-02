import json
from copy import deepcopy
from os.path import join

from back.config import SHIPS_PATH
from back.effects import EffectFactory
from back.geometry import Geometry


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
        from back.entities.bullet import Bullet
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
                'aabb': self.geometry.bounding_box,
                'context_id': self.context_id
                }
