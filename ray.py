# import sys
import math
import png_writer
from random import randint


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
    def __init__(self, center, radius, color=None):
        self.center = center
        self.radius = radius
        if not color:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color

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
            disc = math.pow(disc, 0.5)
            ts.append(-1*v.dot(d) + disc)
            ts.append(-1*v.dot(d) - disc)
        ts = [t for t in ts if t >= 0]
        if len(ts) > 0:
            return (min(ts), self.color)
        return None


class Scene():
    def __init__(self):
        self.objects = list()

    def add_object(self, obj):
        self.objects.append(obj)

    def ray_intersect(self, ray):
        intersects = list()
        for obj in self.objects:
            intersect = obj.ray_intersect(ray)
            if intersect:
                intersects.append(intersect)
        intersects = sorted(intersects, key=lambda x: x[0])
        if intersects:
            return intersects[0][1]
        return (0, 0, 0)


def render():
    pix_dim = 200
    log_dim = 20
    scene = Scene()
    s1 = Sphere(Point(2, 2, 0), 5, (255, 0, 0))
    s2 = Sphere(Point(-2, -2, 0), 5, (0, 0, 255))
    scene.add_object(s1)
    scene.add_object(s2)

    y_min = -1 * log_dim//2
    y_max = log_dim//2+1
    y_inc = (y_max - y_min)/pix_dim
    x_min = -1 * log_dim//2
    x_max = log_dim//2+1
    x_inc = (x_max - x_min)/pix_dim
    res = list()
    for row in range(pix_dim):
        row_res = list()
        row_coord = y_min + y_inc * row
        for col in range(pix_dim):
            col_coord = x_min + x_inc * col
            camera_loc = Point(0, 0, -40)
            screen_loc = Point(col_coord, row_coord, -10)
            r = Ray(screen_loc, Vector(screen_loc, camera_loc))
            row_res.append(scene.ray_intersect(r))
        res.append(row_res)
    return res


def ascii_display(grid):
    rep = ""
    rep += "*" + "-" * len(grid[0]) + "*\n"
    for row in grid:
        rowrep = ""
        rowrep += "|"
        for col in row:
            if(col):
                rowrep += "*"
            else:
                rowrep += " "
        rowrep += "|"
        rowrep += "\n"
        rep += rowrep
    rep += "*" + "-" * len(grid[-1]) + "*"
    return rep


def gen_png(grid):
    return png_writer.gen_png_data(grid)


def main():
    grid = render()
    png_data = gen_png(grid)
    with open('tmp.png', 'wb') as f:
        f.write(png_data)

if __name__ == '__main__':
    main()
