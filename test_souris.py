from likeprocessing.processing import *

__print_x, __print_y = 10, 10
xprec, yprec = __print_x, __print_y
t = Tempo(1000)


def setup():
    createCanvas(400, 200)
    background("grey")
    cursor(SYSTEM_CURSOR_IBEAM)


def compute():
    global __print_x, __print_y, xprec, yprec
    if mouse_click_down():
        if in_polygone(*mouseXY(), [[x, y], [x + 50, y], [x + 50, y + 50], [x, y + 50]]):
            xprec, yprec = x, y
            x, y = random(0, width()-50), random(0, height()-50)
            fill("green")
            t.reset()
    if t.fin() and (xprec, yprec == x, y):
        fill("red")

def draw():
    rect(__print_x, __print_y, 50, 50)


run(globals())
