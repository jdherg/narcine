# import sys
from math import pi, floor, sqrt
import png_writer
from random import randint


class Point():
    """A class with methods for treating 3-tuples of numbers
    as points (x, y, z).
    """

    @classmethod
    def distance(cls, start, end):
        """Finds the distance between two points."""
        return sqrt((start[0] - end[0])**2 +
                    (start[1] - end[1])**2 +
                    (start[2] - end[2])**2)

    @classmethod
    def add(cls, point, vector):
        return (point[0] + vector[0],
                point[1] + vector[1],
                point[2] + vector[2])


class Vector():
    """A class with methods for treating 3-tuples of numbers
       as vectors (x, y, z).
       """

    @classmethod
    def make_vec(cls, terminal, origin):
        """Given an end and start point, returns a tuple representing
        that vector translated to the origin.
        """
        return (terminal[0] - origin[0],
                terminal[1] - origin[1],
                terminal[2] - origin[2])

    @classmethod
    def length(cls, vec):
        """Finds the length of a given vector."""
        return sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)

    @classmethod
    def unit(cls, vec):
        """Returns a unit vector in the same direction as a given vector."""
        length = Vector.length(vec)
        return (
            vec[0] / length,
            vec[1] / length,
            vec[2] / length)

    @classmethod
    def dot(cls, first, second):
        """Finds the dot product of two vectors."""
        return first[0] * second[0] + \
            first[1] * second[1] + \
            first[2] * second[2]

    @classmethod
    def scale(cls, vec, scalar):
        return (vec[0] * scalar,
                vec[1] * scalar,
                vec[2] * scalar)


class Ray():
    """A ray starting at the given location
    and extending in the given direction.
    """

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = Vector.unit(direction)

    def intersect_to_point(self, t):
        """Returns a point given a distance along the ray."""
        return Point.add(self.origin, Vector.scale(self.direction, t))


class Sphere():
    """Represents a sphere in a 3d coordinate space."""

    def __init__(self, center, radius, color=None):
        self.center = center
        self.radius = radius
        if not color:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color

    def ray_intersect(self, ray):
        """Finds the nearest intersection of a ray with the sphere.
        Returns a tuple: (distance along the ray, the sphere)
        or None if the ray and sphere don't intersect.
        """
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
        """Returns a vector normal to the sphere at the given location."""
        return Vector.make_vec(loc, self.center)


class Plane():
    """Represents a plane in a 3d coordinate space."""

    def __init__(self, point, normal, color=None):
        self.point = point
        self._normal = normal
        if not color:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color

    def ray_intersect(self, ray):
        """Finds the nearest intersection of a ray with the plane.
        Returns a tuple: (distance along the ray, the plane)
        or None if the ray and plane are parallel.
        """
        n = self._normal
        p = self.point
        d = ray.direction
        o = ray.origin
        denom = Vector.dot(n, d)
        if not denom:
            return None
        return (Vector.dot(n, Vector.make_vec(p, o))/denom, self)

    def normal(self, point):
        """Returns a vector normal to the plane at the given location."""
        return self._normal


class Camera():
    """Represents a pinhole camera and view plane in a 3d coordinate space."""

    def __init__(self, position, direction, distance=30):
        self.loc = position
        self.direction = Vector.unit(direction)
        self.distance = distance
        self.pix_dim = 500
        self.log_dim = 20
        self.y_min = -1 * self.log_dim//2
        self.y_max = self.log_dim//2
        self.y_inc = (self.y_max - self.y_min)/self.pix_dim
        self.x_min = -1 * self.log_dim//2
        self.x_max = self.log_dim//2
        self.x_inc = (self.x_max - self.x_min)/self.pix_dim

    def screen_loc(self, x, y):
        """Maps the 2d viewplane into the 3d coordinate space."""
        return (x, y, self.loc[2] + self.direction[2] * self.distance)

    def ray_to(self, dest):
        """Returns a ray from the camera to the given point."""
        return Ray(self.loc, Vector.make_vec(dest, self.loc))


class Light():
    """Represents a light in a 3d coordinate space."""

    def __init__(self, position, color=None):
        if not color:
            color = (255, 255, 255)
        self.color = color
        self.loc = position


class Scene():
    """Represents a scene to be rendered,
    including camera, lighting, and objects.
    """

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
        """Finds the color at a given location."""
        base_color = obj.color
        intersect_point = ray.intersect_to_point(intersect)
        normal = obj.normal(intersect_point)
        diffuse_level = 0.0
        specular_level = 0.0
        for light in self.lights:
            light_vec = Vector.make_vec(light.loc, intersect_point)
            diffuse_level += max(
                Vector.dot(Vector.unit(normal), Vector.unit(light_vec)),
                0)
        diffuse_level = min(diffuse_level, 1.0)
        lightness = min(diffuse_level + specular_level, 1.0)
        return (floor(base_color[0] * lightness),
                floor(base_color[1] * lightness),
                floor(base_color[2] * lightness))

    def ray_intersect(self, ray):
        """Finds the color at the point at which the given ray
        intersects with the scene.
        Returns (0, 0, 0) (Black) for no intersection.
        """
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
    """Renders the given scene, producing a list of rows (lists)
    of color tuples.
    """
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
    """Converts a rendered scene into ASCII. Deprecated."""
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
    """Renders a scene as PNG data."""
    grid = render(scene)
    return png_writer.gen_png_data(grid)


def main():
    pass

if __name__ == '__main__':
    main()
