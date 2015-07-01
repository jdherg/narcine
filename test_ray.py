import unittest

from ray import Point, Vector, Ray, Sphere


class TestPoints(unittest.TestCase):

    def test_dist(self):
        a = (0, 0, 0)
        b = (3, 4, 0)
        self.assertEqual(Point.distance(a, b), 5.0)


class TestVectors(unittest.TestCase):

    def test_length(self):
        v = (3, 4, 0)
        self.assertEqual(Vector.length(v), 5.0)

    def test_dot(self):
        v = (1, 2, 3)
        w = (3, 4, 5)
        self.assertEqual(Vector.dot(v, w), 26.0)

    def test_unit(self):
        v = (3, 3, 4)
        self.assertAlmostEqual(Vector.length(Vector.unit(v)), 1, delta=.0001)


class TestIntersections(unittest.TestCase):

    def setUp(self):
        self.s = Sphere((0, 0, 0), 1.0)

    def test_sphere_hit(self):
        r = Ray((-1, -1, -1), (1, 1, 1))
        self.assertTrue(self.s.ray_intersect(r))

    def test_sphere_miss(self):
        r = Ray((-1, -1, -1), (-1, -1, -1))
        self.assertFalse(self.s.ray_intersect(r))

    def test_intersect_distance(self):
        r = Ray((40, 40, 40), (-1, -1, -1))
        intersect = self.s.ray_intersect(r)
        t = intersect[0]
        self.assertAlmostEqual(
            t, Point.distance((0, 0, 0), (40, 40, 40)) - 1.0, delta=.0001)
