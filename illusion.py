from likeprocessing.processing import *

angle = 0
img = loadImage("fantome_jaune.png")


def setup():
    createCanvas(400, 200)
    background("grey")
    ellipseMode("center")
    rectMode("center")
    angleMode("deg")
    noStroke()


def compute():
    global angle
    angle = (angle + 1) % 360


def draw():
    global angle
    line(300, 0, 300, 200)
    line(0, 100, 400, 100)
    rotate(angle, (100, 100))
    for i in range(9):
        if i % 2 == 0:
            fill("black")
        else:
            fill('white')
        circle(100, 100 - i * 5, 200 - i * 10)
    for i in range(11):
        if i % 2 == 0:
            fill("black")
        else:
            fill('white')
        circle(100, 60 + i * 5, 120 - i * 10)
    rotate(angle, (300, 100))
    fill("grey")
    rect(300, 100, 0, 0, image=img)


run(globals())
