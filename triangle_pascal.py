from likeprophy import *

space = SpacePro()
space.gravity = (0, 981)
vanne = KinematicRect(space, 395, 220, 50, 10)

def setup():
    global vanne
    createCanvas(800, 700)
    background("grey")
    angleMode("deg")
    space.add_obj(StaticRect(space, 100, 0, 10, 50))
    space.add_obj(StaticRect(space, 110, 50, 340, 10, angle=radians(-30)))
    space.add_obj(StaticRect(space, 700, 0, 10, 50))
    space.add_obj(StaticRect(space, 705, 60, 326, 10, angle=radians(-149)))
    space.add_obj(StaticRect(space, 395, 220, 10, 50))
    space.add_obj(StaticRect(space, 420, 220, 10, 50))
    space.add_obj(vanne)
    space.add_obj(StaticRect(space,0,680,800,20))
    for i in range(12):
        space.add_obj(StaticRect(space,58+i*64, 560, 5, 130))
    for i in range(12):
        for j in range(20):
            if i % 2 == 0:
                space.add_obj(StaticCircle(space, 90 + j * 32, 280 + i * 20, 3))
            else:
                space.add_obj(StaticCircle(space, 106 + j * 32, 280 + i * 20, 3))

    for j in range(10):
        for i in range(90):
            space.add_obj(Ball(space, random(200, 650), 0, 3.5,elasticity=0.5,fill="red"))
            space.step(1 / 50)


def compute():
    global  vanne
    space.step(1 / 50)
    if mouse_click_down():
        if vanne.position == (395,220):
            vanne.position = 340, 220
        else:
            vanne.position = 395, 220
def draw():
    space.draw()


run(globals())
