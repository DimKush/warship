from unittest import TestCase

from back.ships import MainShip, RenegadeShip


class Test(TestCase):
    def check_common_attrs(self, obj):
        self.assertIsNotNone(obj.mobility)
        self.assertIsNotNone(obj.speed)
        self.assertIsNotNone(obj.acceleration)
        self.assertIsNotNone(obj.hp)
        self.assertIsNotNone(obj.hp_max)
        self.assertIsNotNone(obj.shot_speed)
        self.assertIsNotNone(obj.bullet_damage)
        self.assertIsNotNone(obj.bullet_speed)
        self.assertEqual((), obj.bounds)
        self.assertEqual(10, len(obj.__dict__.keys()))

    def test_main_ship(self):
        msh = MainShip()
        self.check_common_attrs(msh)
        self.assertEqual('predator', msh.name)

    def test_enemy_ship(self):
        msh = RenegadeShip()
        self.check_common_attrs(msh)
        self.assertEqual('predator_renegate', msh.name)
