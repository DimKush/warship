from math import pi
from unittest import TestCase

from back.effects import EffectFactory
from back.entities import Bullet, Player
from tests.helpers import round_list


class Test(TestCase):
    def setUp(self):
        self.pl = Player(0, 0)
        self.pl.set_effect_factory(EffectFactory())
        self.ent = Bullet(1, 2, 90 * pi / 180, self.pl)

    def test_action_on_collision_false(self):
        ent_other = Bullet(-12, 10, 0, self.pl)
        self.ent.next(0.02, [ent_other])
        self.assertEqual(1, self.ent.hp)
        self.assertEqual([[26.0, 3.0], [-9.0, 3.0]], round_list(self.ent.geometry.bounds, 0))

    def test_action_on_collision_true(self):
        ent_other = Bullet(-5, 10, 0, self.pl)
        old_pos = self.ent.geometry.bounds[:]
        self.ent.next(0.02, [ent_other])
        self.assertEqual(0, self.ent.hp)
        self.assertEqual(old_pos, self.ent.geometry.bounds)

    def test_get_info(self):
        exp_res = {'id': 1,
                   'type': 'Bullet',
                   'c': '1 2 1.57',
                   'aabb': (1, 2, 36, 3),
                   'context_id': 'ship_00123412'}
        res = self.ent.get_info()
        self.assertEqual(exp_res, res)
