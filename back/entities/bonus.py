from abc import ABC, abstractmethod
from enum import Enum

from back.entities import Entity
import back.entities as ee

characteristic = Enum('bonus_shoot', 'bonus_speed')


class Egg(ABC):
    def __init__(self):
        self.expired = False
        self._applied = False
        self._full_timer = 0
        self._timer = 0
        self._target = None
        self._context = 'default_egg'

    def set_target(self, target):
        self._target = target

    def update(self, delta_time):
        if not self._applied:
            self._applied = True
            self._full_timer = self._timer
            self._apply()
        self._timer -= delta_time
        if self._timer <= 0:
            self.expired = True
            self._unapply()

    def get_info(self):
        return {'full_timer': self._full_timer,
                'curr_timer': self._timer,
                'context': self._context}

    @abstractmethod
    def _apply(self):
        pass

    @abstractmethod
    def _unapply(self):
        pass


class FireEgg(Egg):
    def __init__(self):
        super().__init__()
        self._context = 'fire_egg'
        self._timer = 20

    def _apply(self):
        self.shoot_speed = self._target.gun_state.shot_speed
        self._target.gun_state.shot_speed *= 1.5

    def _unapply(self):
        self._target.gun_state.shot_speed = self.shoot_speed


class FasterEgg(Egg):
    def __init__(self):
        super().__init__()
        self._context = 'fast_egg'
        self._timer = 25

    def _apply(self):
        self._target.physics.vector_motion.set_delta(self._target.ship_model.acceleration * 2)
        self._target.physics.vector_motion.set_max_current(self._target.ship_model.speed * 2)
        self._target.physics.angle_motion.set_delta(self._target.ship_model.mobility * 3)

    def _unapply(self):
        self._target.physics.vector_motion.set_delta(self._target.ship_model.acceleration)
        self._target.physics.vector_motion.set_max_current(self._target.ship_model.speed)
        self._target.physics.angle_motion.set_delta(self._target.ship_model.mobility)


class Bonus(Entity):
    def __init__(self, x, y, char: characteristic):
        if char == 'bonus_shoot':
            context = 'bonus_shoot'
            egg = FireEgg()
        else:
            context = 'bonus_speed'
            egg = FasterEgg()

        super().__init__(x, y, 0, context)
        self.hp = 100
        self.physics.load_points(context)
        self.egg = egg

    def action_on_collision(self, entity):
        if isinstance(entity, ee.SpaceShip):
            entity.reg_bonus(self.egg)
            self.hp = 0
