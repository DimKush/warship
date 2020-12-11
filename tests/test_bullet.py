from math import pi
from unittest import TestCase

from back.effects import EffectFactory
from back.entities import Bullet, SpaceShip, Statics
from tests.helpers import round_list


class Test(TestCase):
    def setUp(self):
        self.pl = SpaceShip(0, 0)
        self.pl.set_effect_factory(EffectFactory())
        self.ent = Bullet(1, 2, 90 * pi / 180, self.pl)

    def test_action_on_collision_false(self):
        ent_other = Bullet(-12, 10, 0, self.pl)
        self.ent.next(0.02, [ent_other])
        self.assertEqual(1, self.ent.hp)
        self.assertEqual([[26.0, 3.0], [-9.0, 3.0]], round_list(self.ent.physics.bounds, 0))

    def test_action_on_collision_true(self):
        ent_other = Bullet(-5, 10, 0, self.pl)
        old_pos = self.ent.physics.bounds[:]
        self.ent.next(0.02, [ent_other])
        self.assertEqual(0, self.ent.hp)
        self.assertEqual(old_pos, self.ent.physics.bounds)

    def test_action_on_collision_with_statics(self):
        ent_other = Statics(0, 0)
        ent_other.hp = 983
        self.assertEqual(983, ent_other.hp)

        self.ent.action_on_collision(ent_other)
        self.assertEqual(0, self.ent.hp)
        self.assertEqual(983, ent_other.hp)

    def test_action_on_collision_with_player(self):
        ent_other = SpaceShip(0, 0)
        ent_other.hp = 100
        self.ent.damage = 99
        self.ent.owner.score = 1

        self.ent.action_on_collision(ent_other)
        self.assertEqual(0, self.ent.hp)
        self.assertEqual(1, ent_other.hp)
        self.assertEqual(11, self.ent.owner.score)

    def test_action_on_collision_with_player_destroy(self):
        ent_other = SpaceShip(1, 1)
        ent_other.hp = 1
        self.ent.damage = 100
        self.ent.owner.score = 1

        self.ent.action_on_collision(ent_other)
        self.assertEqual(0, self.ent.hp)
        self.assertEqual(-99, ent_other.hp)
        self.assertEqual(51,  self.ent.owner.score)

    def test_action_on_collision_with_bad_type(self):
        self.assertEqual(1, self.ent.hp)
        self.assertEqual(0, self.ent.owner.score)
        self.ent.action_on_collision(None)
        self.assertEqual(1, self.ent.hp)
        self.assertEqual(0, self.ent.owner.score)

    def test_get_info(self):
        exp_res = {'id': 1,
                   'type': 'Bullet',
                   'c': '1 2 1.57',
                   'aabb': (1, 2, 36, 3),
                   'context_id': 'ship_00123412'}
        res = self.ent.get_info()
        self.assertEqual(exp_res, res)
