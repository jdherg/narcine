# import sys
import math


class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.coords = (x, y, z)

    def distance(self, other):
        return math.sqrt(
            sum([math.pow(x_i - y_i, 2)
                for x_i, y_i
                in zip(self.coords, other.coords)]))

    def __str__(self):
        return "( %f , %f , %f )" % (self.x, self.y, self.z)


class Vector():
    def __init__(self, terminal, origin=None):
        if not origin:
            origin = Point(0, 0, 0)

        self.terminal = Point(terminal.x - origin.x,
                              terminal.y - origin.y,
                              terminal.z - origin.z)

    def length(self):
        return Point(0, 0, 0).distance(self.terminal)

    def unit(self):
        unit_term = Point(
            self.terminal.x / self.length(),
            self.terminal.y / self.length(),
            self.terminal.z / self.length())
        return Vector(unit_term)

    def __str__(self):
        return "< %s >" % (self.terminal)

    def dot(self, other):
        xd = self.terminal.x * other.terminal.x
        yd = self.terminal.y * other.terminal.y
        zd = self.terminal.z * other.terminal.z
        return xd + yd + zd


class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.unit()


class Sphere():
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def ray_intersect(self, ray):
        c = self.center
        r = self.radius
        v = Vector(ray.origin, c)
        d = ray.direction
        disc = math.pow(v.dot(d), 2) - (math.pow(v.length(), 2) - r*r)
        ts = list()
        if disc == 0:
            ts.append(-1*v.dot(d))
        elif disc > 0:
            ts.append(-1*v.dot(d) + disc)
            ts.append(-1*v.dot(d) - disc)
        for t in ts:
            if t >= 0:
                return True
        return False


def render():

    s = Sphere(Point(0, 0, 0), 5)
    rep = ""
    for row in range(-10, 11):
        rowrep = ""
        for col in range(-10, 11):
            r = Ray(Point(col, row, -5), Vector(Point(0, 0, 1)))
            if(s.ray_intersect(r)):
                rowrep += "*"
            else:
                rowrep += " "
        rowrep += "\n"
        rep += rowrep
    return rep



def main():
    print(render())

if __name__ == '__main__':
    main()
