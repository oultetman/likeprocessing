from likeprocessing.processing import *


def draw_title():
    title(str(mouseXY()))
    rect(100, 100, 50, 50, fill="blue", fill_mouse_on="green", stroke_weight=3)


def setup():
    createCanvas(400, 400)
    background("grey")
    fill("white")
    fill_mouse_on("red")
    angleMode("deg")
    rectMode('center')
    textAlign("center","center")

def draw():
    draw_title()
    triangle(20, 10, 50, 15, 40, 70, fill = "green", fill_mouse_on="yellow", stroke_weight=3)
    arc(200, 110,40,40,0,90)
    for angle in range(0,360,10):
        rotate(-angle,(200,200))
        text(str(angle), 200, 20,fill="pink",no_stroke=True)
        line(200,200,200,20)

    line(100, 100, 350, 150)
    save_fill_stroke()
    fill("black")
    point(100, 100)
    point(350, 150)
    restore_fill_stroke()


run(globals())
