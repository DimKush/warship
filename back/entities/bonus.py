from enum import Enum

from back.entities import Entity
import back.entities as ee
characteristic = Enum('bonus_shoot', 'bonus_speed')


class Bonus(Entity):
    def __init__(self, x, y, duration, char: characteristic, value):
        context = 'bonus_shoot' if char == 'bonus_shoot' else 'bonus_speed'
        super().__init__(x, y, 0, context)
        self.physics.load_points(context)
        self.duration = duration
        self.characteristic = char
        self.value = value

    def action_on_collision(self, entity):
        if isinstance(entity, ee.SpaceShip):
            self.hp = 0
