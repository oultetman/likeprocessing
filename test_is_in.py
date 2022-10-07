from likeprocessing.processing import *


def draw_title():
    title(str(mouseXY()))
    rect(100, 100, 50, 50, fill="blue", fill_mouse_on="green", stroke_weight=3)


def setup():
    angleMode("deg")
    createCanvas(400, 200)
    background("grey")
    fill("white")
    fill_mouse_on("red")


def draw():
    draw_title()
    triangle(20, 10, 50, 15, 40, 70, fill_mouse_on="yellow", stroke_weight=3)
    arc(200, 110,40,40,0,90)
    text("bonjour", 150, 30)

    line(100, 100, 350, 150)
    save_fill_stroke()
    fill("black")
    point(100, 100)
    point(350, 150)
    restore_fill_stroke()


run(globals())
