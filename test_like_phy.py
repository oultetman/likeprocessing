"""programme de base"""
from likeprophy import *
space = SpacePro()  # 2
space.gravity = (0.0, 981.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

def setup():
    createCanvas(400,400)
    background("grey")
    angleMode("deg")
    space.add_obj(StaticRect(space,100,100,100,100,fill="red"))
    space.add_obj(Ball(space,202, 50, 30, fill="blue",elasticity=0.9))
    space.add_obj(StaticRect(space,0,0,400,10,fill="green"))
    space.add_obj(StaticRect(space,0,320,400,10,fill="green",angle=radians(-10)))
    space.add_obj(StaticRect(space, 0, 0, 10, 400, fill="green"))
    space.add_obj(StaticRect(space, 390, 0, 10, 400, fill="green"))

def compute():
    space.step(1/50)

def draw():
    space.draw()
    # space.debug_draw(draw_options)
run(globals())