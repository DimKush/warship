from unittest import TestCase

from back.physics import CasualPhysics


class TestEnemy(TestCase):
    def setUp(self):
        self.test_physic = CasualPhysics(50, 50, 0)
        self.test_physic.bounds = [[40, 30], [60, 30], [60, 70], [40, 70]]
        self.test_physic.eval_natural_aabb()
        self.test_physic.vector_motion.set_delta(13)
        self.test_physic.vector_motion.set_max_current(140)
        self.test_physic.vector_motion.set_moving(1)

    def test_update(self):
        for _ in range(10):
            self.test_physic.update(0.1)
            self.test_physic.update(0.1)
            self.test_physic.rollback()

        print(self.test_physic)
