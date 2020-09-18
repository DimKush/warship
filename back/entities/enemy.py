from random import randint

import back.entities as ee
from back.effects import ActionFactory
from back.ships import RenegadeShip


class Enemy(ee.Player):
    def __init__(self, x: float, y: float, prepared_id=None, prepared_name=''):
        super().__init__(x, y, RenegadeShip)
        self.actions = ActionFactory()
        self.set_action(1)
        self.actions.add_to_pool(150, self.set_moving, randint(-1, 1), 1)
        self.actions.add_to_pool(250, self.set_moving, randint(-1, 1), 1)

    def action_on_collision(self, entity):
        super().action_on_collision(entity)
        if isinstance(entity, ee.Player):
            pass
        elif isinstance(entity, ee.Statics):
            self.actions.clear_pool()
            self.actions.add_to_pool(randint(20, 250), self.set_moving, randint(-1, 1), 0)
            self.actions.add_to_pool(150, self.set_moving, randint(-1, 1), 1)
            self.actions.add_to_pool(250, self.set_moving, randint(-1, 1), 1)
            self.actions.add_to_pool(100, self.set_moving, randint(-1, 1), 1)
            self.actions.add_to_pool(1, self.set_moving, 0, 1)
        elif isinstance(entity, ee.Bullet):
            pass
        else:
            print(f'Enemy. Not described case for type {type(entity)}')

    def next(self, t: float, others):
        super().next(t, others)
        self.actions.do_tick()
