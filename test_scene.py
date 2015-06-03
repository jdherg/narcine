from ray import Camera, Light, Plane, Scene, Sphere, render_png


def make_scene():
    scene = Scene()
    s1 = Sphere((0, 0, 0), 5, (255, 0, 0))
    s2 = Sphere((-2, -2, 10), 5, (0, 0, 255))
    scene.add_object(s1)
    scene.add_object(s2)
    p1 = Plane((4, 4, 15), (5, 5, -5), (0, 255, 0))
    scene.add_object(p1)
    camera = Camera((0, 0, -40), (0, 0, 1))
    scene.add_camera(camera)
    light1 = Light((8, -8, -8))
    scene.add_light(light1)
    light2 = Light((-8, 8, -8))
    scene.add_light(light2)
    return scene


def main():
    scene = make_scene()
    png_data = render_png(scene)
    with open('tmp.png', 'wb') as f:
        f.write(png_data)

if __name__ == '__main__':
    main()
