from unittest import TestCase

from back.entities import SpaceShip, Bullet


class TestPlayer(TestCase):
    def setUp(self):
        self.pl = SpaceShip(40, 40)

    def test_do_action_not_action(self):
        self.pl.shot_counter = 10

        res = self.pl.do_action(0.4)

        self.assertEqual(9.6, self.pl.shot_counter)
        self.assertIsNone(res)

    def test_do_action_not_shoting(self):
        self.pl.shot_counter = -1
        self.pl.shoting = False

        res = self.pl.do_action(0.4)

        self.assertEqual(-1, self.pl.shot_counter)
        self.assertIsNone(res)

    def test_do_action_action(self):
        self.pl.shot_counter = -1
        self.pl.shoting = True

        res = self.pl.do_action(0.4)
        expext_res = Bullet(self.pl.x, self.pl.y, self.pl.geometry.angle_motion.angle_current, self.pl)

        self.assertEqual(1 / 6, self.pl.shot_counter)
        self.assertEqual(expext_res.get_info(), res.get_info())

    def test_get_info(self):
        exp_res = {'aabb': (0, 0, 80, 80),
                   'c': '40 40 0',
                   'context_id': 'ship_0019',
                   'hp': 100,
                   'hp_max': 100,
                   'name': '',
                   'score': 0,
                   'type': 'Player'}
        act_res = self.pl.get_info()
        del act_res['id']
        self.assertEqual(exp_res, act_res)
