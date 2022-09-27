from likeprocessing.processing import *

time = 0
s = 0
m = 0
h = 0
t = Tempo(10)


def setup():
    createCanvas(400, 400)
    background("grey")
    angleMode("deg")
    ellipseMode("center")
    strokWeight(2)

def compute():
    in_polygone(-1,-1,[(0,0),(4,0),(4,2),(0,2)])

def draw():
    global time, s, m, h
    stroke("black")
    circle(100, 100, 100)
    axe = (100, 100)
    if t.fin():
        s += 1
    text(f"{int(h):02}:{int(m):02}:{s:02}", 10, 20, 100, 20)
    rotate(-s * 6, axe)
    stroke("red")
    line(100, 100, 100, 50)
    rotate(-s / 10, axe)
    stroke("black")
    line(100, 100, 100, 60)
    rotate(-s / 120, axe)
    stroke("blue")
    line(100, 100, 100, 80)
    rotate(0)
    fill("white")
    circle_arc(200, 200, 50, 0, 270, pie=False)


run(globals())
