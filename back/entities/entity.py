import json
from os.path import join

from back.config import MODELS_PATH
from back.effects import EffectFactory
from back.physics import CasualPhysics, Physics


class Entity:
    def __init__(self, x: float, y: float, r: float):
        self.id = 0
        self.context_id = ''
        self.physics: Physics = CasualPhysics(x, y, r)
        self.hp = 1
        self.effect_factory = None

    @property
    def x(self):
        return self.physics.x

    @property
    def y(self):
        return self.physics.y

    @property
    def r(self):
        return self.physics.r

    def next(self, t: float, others):
        from back.entities.bullet import Bullet
        self.physics.update(t)

        for entity in others:
            if entity != self:
                if not (isinstance(self, Bullet) and self.owner.id == entity.id) and \
                        not (isinstance(entity, Bullet) and entity.owner.id == self.id):
                    if self.physics.aabb_collision(entity.physics.aabb):
                        if self.physics.detail_collision(entity.physics.bounds):
                            self.action_on_collision(entity)

    def action_on_collision(self, entity):
        pass

    def set_moving(self, angle_moving, speed_moving):
        self.physics.angle_motion.moving = angle_moving
        self.physics.vector_motion.moving = speed_moving

    def set_action(self, flag: int):
        pass

    def do_action(self, time_delta):
        pass

    def set_effect_factory(self, ef: EffectFactory):
        self.effect_factory = ef

    def get_info(self):
        return {'id': self.id,
                'type': type(self).__name__,
                'c': f'{int(self.x)} {int(self.y)} {round(self.r, 2)}',
                'aabb': self.physics.aabb_int,
                'context_id': self.context_id
                }

    def load_body_configuration(self, file_name: str):
        file_name = file_name if file_name.endswith('.json') else f'{file_name}.json'
        with open(f'{join(MODELS_PATH, file_name)}', 'r') as f:
            obj = json.loads(f.read())
            self.context_id = obj['context_id']
