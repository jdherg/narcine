import unittest

from ray import Point, Vector, Ray, Sphere

class TestPoints(unittest.TestCase):

    def test_dist(self):
        a = Point(0,0,0)
        b = Point(3,4,0)
        self.assertEqual(a.distance(b), 5.0)

class TestVectors(unittest.TestCase):

    def test_length(self):
        v = Vector(Point(3,4,0))
        self.assertEqual(v.length(), 5.0)

    def test_dot(self):
        v = Vector(Point(1,2,3))
        w = Vector(Point(3,4,5))
        self.assertEqual(v.dot(w), 26.0)

class TestIntersections(unittest.TestCase):

    def test_sphere_hit(self):
        s = Sphere(Point(0,0,0), 1.0)
        r = Ray(Point(-1,-1,-1), Vector(Point(1,1,1)))
        self.assertTrue(s.ray_intersect(r))

    def test_sphere_miss(self):
        s = Sphere(Point(0,0,0), 1.0)
        r = Ray(Point(-1,-1,-1), Vector(Point(-1,-1,-1)))
        self.assertFalse(s.ray_intersect(r))
