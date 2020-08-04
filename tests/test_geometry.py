from unittest import TestCase

from back.geometry import Geometry


class TestGeometry(TestCase):
    def setUp(self):
        self.test_geometry = Geometry(1, 2)

    def test_eval_true_bounding_box_empty(self):
        self.test_geometry.eval_true_bounding_box()
        self.assertEqual([0, 0, 0, 0], self.test_geometry.bounding_box)

    def test_eval_true_bounding_box(self):
        self.test_geometry.bounds = [[1, 0], [2, 3], [-1, -1], [3, -3]]
        self.test_geometry.eval_true_bounding_box()
        self.assertEqual([-1, -3, 3, 3], self.test_geometry.bounding_box)

    def test_eval_approximately_bounding_box(self):
        self.test_geometry.eval_approximately_bounding_box()
        self.assertEqual([-39, -38, 41, 42], self.test_geometry.bounding_box)

