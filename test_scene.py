from ray import Camera, Light, Plane, Scene, Sphere, render_png


def make_scene():
    scene = Scene()
    s1 = Sphere((-5, -5, 0), 5, (255, 0, 0))
    s2 = Sphere((5, -5, 10), 5, (0, 255, 0))
    s3 = Sphere((5, 5, 0), 5, (0, 0, 255))
    s4 = Sphere((-5, 5, 10), 5, (0, 0, 0))
    s5 = Sphere((0, 0, 20), 5, (255, 255, 255))
    scene.add_object(s1)
    scene.add_object(s2)
    scene.add_object(s3)
    scene.add_object(s4)
    scene.add_object(s5)
    p1 = Plane((0, 0, 40), (0, 0, -1), (128, 128, 128))
    scene.add_object(p1)
    camera = Camera((0, 0, -40), (0, 0, 1))
    scene.add_camera(camera)
    light1 = Light((0, 0, -10))
    scene.add_light(light1)
    return scene


def main():
    scene = make_scene()
    png_data = render_png(scene)
    with open('tmp.png', 'wb') as f:
        f.write(png_data)

if __name__ == '__main__':
    main()
