# import sys
from math import pi, floor, sqrt
import png_writer
from random import randint


class Point():
    @classmethod
    def distance(cls, start, end):
        return sqrt((start[0] - end[0])**2 +
                    (start[1] - end[1])**2 +
                    (start[2] - end[2])**2)

    @classmethod
    def add(cls, point, vector):
        return (point[0] + vector[0],
                point[1] + vector[1],
                point[2] + vector[2])


class Vector():
    @classmethod
    def make_vec(cls, terminal, origin):
        return (terminal[0] - origin[0],
                terminal[1] - origin[1],
                terminal[2] - origin[2])

    @classmethod
    def length(cls, vec):
        return sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)

    @classmethod
    def unit(cls, vec):
        length = Vector.length(vec)
        return (
            vec[0] / length,
            vec[1] / length,
            vec[2] / length)

    @classmethod
    def dot(cls, first, second):
        return first[0] * second[0] + \
               first[1] * second[1] + \
               first[2] * second[2]

    @classmethod
    def angle_ish(cls, first, second):
        distance = Point.distance(Vector.unit(first), Vector.unit(second))
        return distance * pi / 2.0

    @classmethod
    def scale(cls, vec, scalar):
        return (vec[0] * scalar,
                vec[1] * scalar,
                vec[2] * scalar)


class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = Vector.unit(direction)

    def intersect_to_point(self, t):
        return Point.add(self.origin, Vector.scale(self.direction, t))


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
        v = Vector.make_vec(ray.origin, c)
        d = ray.direction
        vd = Vector.dot(v, d)
        disc = pow(vd, 2) - (pow(Vector.length(v), 2) - r*r)
        ts = list()
        if disc == 0:
            ts.append(-1*vd)
        elif disc > 0:
            disc = pow(disc, 0.5)
            pre = vd * -1
            ts.append(pre + disc)
            ts.append(pre - disc)
        ts = [t for t in ts if t >= 0]
        if ts:
            return (min(ts), self)
        return None

    def normal(self, loc):
        return Vector.make_vec(loc, self.center)


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
        denom = Vector.dot(n, d)
        if not denom:
            return None
        return (Vector.dot(n, Vector.make_vec(p, o))/denom, self)

    def normal(self, point):
        return self._normal


class Camera():
    def __init__(self, position, direction, distance=30):
        self.loc = position
        self.direction = Vector.unit(direction)
        self.distance = distance
        self.pix_dim = 200
        self.log_dim = 20
        self.y_min = -1 * self.log_dim//2
        self.y_max = self.log_dim//2
        self.y_inc = (self.y_max - self.y_min)/self.pix_dim
        self.x_min = -1 * self.log_dim//2
        self.x_max = self.log_dim//2
        self.x_inc = (self.x_max - self.x_min)/self.pix_dim

    def screen_loc(self, x, y):
        return (x, y, self.loc[2] + self.direction[2] * self.distance)

    def ray_to(self, dest):
        return Ray(self.loc, Vector.make_vec(dest, self.loc))


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
            light_vec = Vector.make_vec(light.loc, intersect_point)
            angle = Vector.angle_ish(normal, light_vec)
            diffuse_level += 1 - angle / pi
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


def render_png(scene):
    grid = render(scene)
    return png_writer.gen_png_data(grid)


def main():
    pass

if __name__ == '__main__':
    main()
