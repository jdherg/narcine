# import sys
from math import pi, floor, sqrt
import png_writer
from random import randint


class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.coords = (x, y, z)

    def distance(self, other):
        return sqrt(
            sum([pow(x_i - y_i, 2)
                for x_i, y_i
                in zip(self.coords, other.coords)]))

    def __add__(self, other):
        if(type(other) == Vector):
            return Point(self.x + other.terminal.x,
                         self.y + other.terminal.y,
                         self.z + other.terminal.z)

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

    def angle_ish(self, other):
        distance = self.unit().terminal.distance(other.unit().terminal)
        return distance * pi / 2.0

    def __mul__(self, other):
        if(type(other) == int or type(other) == float):
            return Vector(Point(self.terminal.x * other,
                                self.terminal.y * other,
                                self.terminal.z * other))
        else:
            raise NotImplementedError


class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.unit()

    def intersect_to_point(self, t):
        return self.origin + self.direction * t


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
        disc = pow(v.dot(d), 2) - (pow(v.length(), 2) - r*r)
        ts = list()
        if disc == 0:
            ts.append(-1*v.dot(d))
        elif disc > 0:
            disc = pow(disc, 0.5)
            ts.append(-1*v.dot(d) + disc)
            ts.append(-1*v.dot(d) - disc)
        ts = [t for t in ts if t >= 0]
        if len(ts) > 0:
            return (min(ts), self)
        return None

    def normal(self, loc):
        return Vector(loc, self.center)


class Plane():
    def __init__(self, point, normal, color=None):
        self.point = point
        self._normal = normal
        if not color:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color

    def ray_intersect(self, ray):
        n = self._normal
        p = self.point
        d = ray.direction
        o = ray.origin
        denom = n.dot(d)
        if not denom:
            return None
        return (n.dot(Vector(p, o))/denom, self)

    def normal(self, point):
        return self._normal


class Camera():
    def __init__(self, position, direction, distance=30):
        self.loc = position
        self.direction = direction.unit()
        self.distance = distance
        self.pix_dim = 200
        self.log_dim = 20
        self.y_min = -1 * self.log_dim//2
        self.y_max = self.log_dim//2+1
        self.y_inc = (self.y_max - self.y_min)/self.pix_dim
        self.x_min = -1 * self.log_dim//2
        self.x_max = self.log_dim//2+1
        self.x_inc = (self.x_max - self.x_min)/self.pix_dim

    def screen_loc(self, x, y):
        return Point(
            x, y, self.loc.z + self.direction.terminal.z * self.distance)

    def ray_to(self, dest):
        return Ray(self.loc, Vector(dest, self.loc))


class Light():
    def __init__(self, position, color=None):
        if not color:
            color = (255, 255, 255)
        self.color = color
        self.loc = position


class Scene():
    def __init__(self):
        self.objects = list()
        self.lights = list()

    def add_camera(self, camera):
        self.camera = camera

    def add_light(self, light):
        self.lights.append(light)

    def add_object(self, obj):
        self.objects.append(obj)

    def calc_lighting(self, obj, ray, intersect):
        base_color = obj.color
        intersect_point = ray.intersect_to_point(intersect)
        normal = obj.normal(intersect_point)
        diffuse_level = 0.0
        specular_level = 0.0
        for light in self.lights:
            diffuse_level += 1 - normal.angle_ish(
                Vector(light.loc, intersect_point)) / pi
        diffuse_level = min(diffuse_level, 1.0)
        lightness = min(diffuse_level + specular_level, 1.0)
        return (floor(base_color[0] * lightness),
                floor(base_color[1] * lightness),
                floor(base_color[2] * lightness))

    def ray_intersect(self, ray):
        intersects = list()
        for obj in self.objects:
            intersect = obj.ray_intersect(ray)
            if intersect:
                intersects.append(intersect)
        intersects = sorted(intersects, key=lambda x: x[0])
        if intersects:
            return self.calc_lighting(intersects[0][1], ray, intersects[0][0])
        return (0, 0, 0)


def render(scene):
    res = list()
    camera = scene.camera
    for row in range(camera.pix_dim):
        row_res = list()
        row_coord = camera.y_min + camera.y_inc * row
        for col in range(camera.pix_dim):
            col_coord = camera.x_min + camera.x_inc * col
            r = camera.ray_to(camera.screen_loc(col_coord, row_coord))
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


def make_scene():
    scene = Scene()
    s1 = Sphere(Point(0, 0, 0), 5, (255, 0, 0))
    s2 = Sphere(Point(-2, -2, 10), 5, (0, 0, 255))
    scene.add_object(s1)
    scene.add_object(s2)
    p1 = Plane(Point(4, 4, 15), Vector(Point(5, 5, -5)), (0, 255, 0))
    scene.add_object(p1)
    camera = Camera(Point(0, 0, -40), Vector(Point(0, 0, 1)))
    scene.add_camera(camera)
    light1 = Light(Point(8, -8, -8))
    scene.add_light(light1)
    light2 = Light(Point(-8, 8, -8))
    scene.add_light(light2)
    return scene


def main():
    scene = make_scene()
    grid = render(scene)
    png_data = gen_png(grid)
    with open('tmp.png', 'wb') as f:
        f.write(png_data)

if __name__ == '__main__':
    main()
