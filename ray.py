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
    pix_dim = 20
    log_dim = 20
    s = Sphere(Point(0, 0, 0), 5)
    y_min = -1 * log_dim//2
    y_max = log_dim//2+1
    y_inc = (y_max - y_min)/pix_dim
    x_min = -1 * log_dim//2
    x_max = log_dim//2+1
    x_inc = (x_max - x_min)/pix_dim
    rep = ""
    rep += "*" + "-" * pix_dim + "*\n"
    for row in range(pix_dim):
        rowrep = ""
        rowrep += "|"
        row_coord = y_min + y_inc * row
        for col in range(pix_dim):
            col_coord = x_min + x_inc * col
            r = Ray(Point(col_coord,row_coord,-10), Vector(Point(0,0,1)))
            if(s.ray_intersect(r)):
                rowrep += "*"
            else:
                rowrep += " "
        rowrep += "|"
        rowrep += "\n"
        rep += rowrep
    rep += "*" + "-" * pix_dim + "*"
    return rep



def main():
    print(render())

if __name__ == '__main__':
    main()
