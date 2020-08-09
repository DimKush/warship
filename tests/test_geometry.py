from unittest import TestCase

from back.geometry import Geometry, GeometryLine
from back.point import AngleMovement, Movement


class TestGeometry(TestCase):
    def setUp(self):
        self.test_geometry = Geometry(1, 2)
        self.test_geometry.angle_motion = AngleMovement(curr_value=100, delta=10, max_value=100, angle_curr=15)
        self.test_geometry.vector_motion = Movement(curr_value=1.0, delta=0.0, max_value=0.0)
        self.test_geometry_line = GeometryLine(1, 2, 90 * 3.14 / 180)
        self.test_geometry_line.vector_motion = Movement(curr_value=1.0, delta=0.0, max_value=0.0)

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

    def test_box_collision_true(self):
        self.test_geometry.bounds = [[1, 0], [2, 3], [-1, -1], [3, -3]]
        self.test_geometry.eval_true_bounding_box()
        self.assertTrue(self.test_geometry.box_collision([3, -1.2, 5, 6]))

    def test_box_collision_false(self):
        self.test_geometry.bounds = [[1, 0], [2, 3], [-1, -1], [3, -3]]
        self.test_geometry.eval_true_bounding_box()
        self.assertFalse(self.test_geometry.box_collision([4, -1.2, 5, 6]))

    def test_detail_collision_true(self):
        self.test_geometry.bounds = [[1, 0], [2, 3], [-1, -1]]
        self.assertTrue(self.test_geometry.detail_collision([[2, 0], [1, 4], [3, 4]]))

    def test_detail_collision_false(self):
        self.test_geometry.bounds = [[1, 0], [2, 3], [-1, -1]]
        self.assertFalse(self.test_geometry.detail_collision([[2, 0], [2.2, 4], [3, 4]]))

    def test_vector_multiple(self):
        p1 = [1, 1]
        p2 = [3, 3]
        p3 = [2, 0]
        p4 = [2, 3]
        self.assertEqual(4, self.test_geometry.vector_multiple(p1, p3, p2))
        self.assertEqual(-3, self.test_geometry.vector_multiple(p3, p1, p4))

        self.assertEqual(-2, self.test_geometry.vector_multiple(p1, p4, p2))
        self.assertEqual(3, self.test_geometry.vector_multiple(p3, p2, p4))

    def test_get_segments(self):
        self.assertEqual([(1, 4), (4, 19), (19, 1)], self.test_geometry.get_segments([1, 4, 19]))

    def test_next_geometry(self):
        self.test_geometry.bounds = [[1, 0], [2, 3], [-1, -1]]
        self.test_geometry.eval_true_bounding_box()
        self.test_geometry.next(5)
        self.test_geometry.bounds = list(map(lambda x: [round(x[0], 2), round(x[1], 2)], self.test_geometry.bounds))
        self.test_geometry.bounding_box = list(map(lambda x: round(x, 2), self.test_geometry.bounding_box))
        self.assertEqual([[-5.41, 3.76], [-2.26, 3.51], [-6.86, 5.46]], self.test_geometry.bounds)
        self.assertEqual([-5.47, 1.24, -2.47, 5.24], self.test_geometry.bounding_box)

    def test_next_geometry_line(self):
        self.test_geometry_line.bounds = [[1, 1], [2, 3], [3, -1]]
        self.test_geometry_line.eval_true_bounding_box()
        self.test_geometry_line.next(3)
        self.test_geometry_line.bounds = list(map(lambda x: [round(x[0], 2), round(x[1], 2)], self.test_geometry_line.bounds))
        self.test_geometry_line.bounding_box = list(map(lambda x: round(x, 2), self.test_geometry_line.bounding_box))
        self.assertEqual([[-2.0, 1.0], [-1.0, 3.0], [0.0, -1.0]], self.test_geometry_line.bounds)
        self.assertEqual([-2.0, -1.0, 0.0, 3.0], self.test_geometry_line.bounding_box)

    def test_rebuild_geometry_line(self):
        self.test_geometry_line.bounds = [[0, 3], [1, -1], [-1, -1]]
        self.test_geometry_line.rebuild()
        self.test_geometry_line.bounds = list(map(lambda x: [round(x[0], 2), round(x[1], 2)], self.test_geometry_line.bounds))
        self.assertEqual([[0.0, 1.0], [4.0, 2.0], [4.0, 0.0]], self.test_geometry_line.bounds)
