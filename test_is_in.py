from likeprocessing.processing import *


def draw_title():
    save_fill_stroke()
    noStroke()
    fill("orange")
    title(str(mouseXY()))
    rect(100, 100, 50, 50)
    restore_fill_stroke()


def setup():
    angleMode("deg")
    createCanvas(400, 200)
    background("grey")
    fill("white")
    fill_mouse_on("red")

def draw():
    draw_title()
    triangle(20, 10, 50, 15, 40, 70)
    fill((250,265,12))
    circle(200, 110, 80)
    text("bonjour", 50, 10)
    line(0, 100, 400, 200)


run(globals())
