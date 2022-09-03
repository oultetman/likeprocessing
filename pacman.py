import pygame

from likeprocessing.processing import *


x = -200
t = Tempo(500)
angle = 0
vitesse = 10
sens = 1

def setup():
    createCanvas(400, 200)
    background("grey")
    ellipseMode("center")
    rectMode("center")
    angleMode("deg")

def compute():
    global x, angle,sens
    if t.fin():
        x += sens*vitesse
    if keyIsPressed():
        if keys()[K_UP]:
            angle = 45
        elif keyIsDown(K_DOWN):
            angle = -45
        elif keyIsDown(K_LEFT):
            sens = -1
        elif keyIsDown(K_RIGHT):
            sens = 1
    else:
        angle = 0

def draw():
    line(200, 0, 200, 200)
    line(0, 100, 400, 100)
    translate(x, 0)
    fill("yellow")
    rotate(angle, (200, 100))
    line(200, 100, 400, 100)
    circle(200, 100, 50)
    fill("white")
    circle(200, 90, 15)
    fill("black")
    circle(202, 90, 5)
    arc(200, 100, 50, 50, 350, 370)
    rect(300, 100, 50, 26)



run(globals())
