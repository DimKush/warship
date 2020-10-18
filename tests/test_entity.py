from unittest import TestCase

from back.entities import Entity
from back.movement import AngleMovement, Movement

from math import pi


class Test(TestCase):
    def setUp(self):
        self.ent = Entity(1, 2)
        self.ent.physics.angle_motion = AngleMovement(curr_value=100, delta=10, max_value=100, angle_curr=90 * pi / 180)
        self.ent.physics.vector_motion = Movement(curr_value=1.0, delta=0.0, max_value=0.0)

    def test_props(self):
        self.assertEqual(1, self.ent.x)
        self.assertEqual(2, self.ent.y)
        self.assertEqual(1.57, round(self.ent.r, 2))

    def test_set_moving(self):
        self.ent.set_moving(1, 1)
        self.assertEqual(1, self.ent.physics.angle_motion.moving)
        self.assertEqual(1, self.ent.physics.vector_motion.moving)

