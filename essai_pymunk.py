"""programme de base"""
from likeprocessing.processing import *
from likeprophy import *


space = SpacePro()  # 2
space.gravity = (0.0, 981.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)
vanne = None


def setup():
    global vanne
    createCanvas(800, 600)
    background("grey")
    ellipseMode("center")
    noStroke()
    fill("blue")
    angleMode("deg")
    for i in range(4):
        if i%2==0:
            d=0
            a=1
        else:
            d=200
            a=-1
        space.add_obj(StaticRect(space,200-d,200+100*i,800-d,30,angle=radians(a),friction=0.2))
    space.add_obj(StaticRect(space, 0, 0, 10, 600))
    space.add_obj(StaticRect(space, 790, 0, 10, 600))
    space.add_obj(StaticRect(space, 500, 0, 10, 170))
    space.add_obj(StaticRect(space, 520, 0, 10, 170))
    vanne = space.add_obj(KinematicRect(space, 510, 125, 10, 70, fill="brown"))
    for i in range(10):
        space.add_obj(DynamicRect(space,250,175-20*i,20,20,density=5,elasticity=0.1,friction=0.6,fill="brown"))
    for i in range(20):
        for j in range(200):
            space.add_obj(Ball(space, 540+j,150-i*2, 2,density=1,friction=0,elasticity=0.1))
def compute():
    global vanne
    if mouse_click():
        pass
    if mouse_click_up():
        if space.objets[vanne].position[1]==100:
            space.objets[vanne].position = (510, 125)
        else:
            space.objets[vanne].position = (510,100)
    space.step(1/50)


def draw():

    # space.debug_draw(draw_options)
    space.draw()


run(globals())
