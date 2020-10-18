from unittest import TestCase

from back.movement import Movement, AngleMovement


class TestMovement(TestCase):
    def setUp(self):
        self.mov = Movement(50, 10, 100)

    def test_set_next_decrease_speed(self):
        self.assertEqual(50, self.mov.curr)
        self.mov.set_next(1)
        self.assertEqual(40, self.mov.curr)
        self.mov.set_next(10)
        self.assertEqual(0, self.mov.curr)

    def test_set_next_decrease_speed_back(self):
        self.mov.curr = -50
        self.assertEqual(-50, self.mov.curr)
        self.mov.set_next(1)
        self.assertEqual(-40, self.mov.curr)
        self.mov.set_next(10)
        self.assertEqual(0, self.mov.curr)

    def test_set_next_increase_speed(self):
        self.mov.moving = 1
        self.mov.set_next(1)
        self.assertEqual(60, self.mov.curr)
        self.mov.set_next(10)
        self.assertEqual(100, self.mov.curr)

    def test_set_next_increase_reverse_speed(self):
        self.mov.moving = -1
        self.mov.set_next(2)
        self.assertEqual(30, self.mov.curr)
        self.mov.set_next(10)
        self.assertEqual(-70, self.mov.curr)
        self.mov.set_next(10)
        self.assertEqual(-100, self.mov.curr)


class TestAngleMovement(TestCase):
    def setUp(self):
        self.amov = AngleMovement(50, 10, 100, 90)

    def test_set_next_no_moving(self):
        self.amov.moving = 0
        self.amov.set_next(6)
        self.assertEqual(0, self.amov.current)

    def test_set_next_decrease_moving_down(self):
        self.amov.moving = 0
        self.amov.set_next(3)
        self.assertEqual(20, self.amov.current)

    def test_set_next_decrease_moving_up(self):
        self.amov.moving = 0
        self.amov.current = -30
        self.amov.set_next(2)
        self.assertEqual(-10, self.amov.current)

    def test_set_next_increase_moving(self):
        self.amov.moving = 1
        self.amov.set_next(2)
        self.assertEqual(70, self.amov.current)
        self.assertEqual(230, self.amov.angle_current)
        self.amov.set_next(5)
        self.assertEqual(100, self.amov.current)
        self.assertEqual(730, self.amov.angle_current)

    def test_set_next_decrease_moving(self):
        self.amov.moving = -1
        self.amov.set_next(10)
        self.assertEqual(-50, self.amov.current)
        self.assertEqual(-410, self.amov.angle_current)
        self.amov.set_next(6)
        self.assertEqual(-100, self.amov.current)
        self.assertEqual(-1010, self.amov.angle_current)

    def test_set_next_incorrect_moving(self):
        self.amov.moving = -10
        self.amov.set_next(10)
        self.assertEqual(50, self.amov.current)
