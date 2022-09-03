import pygame

from likeprocessing.processing import *

x = -200
t = Tempo(100)
angle = 0
vitesse = 2
sens = 1
flip = None
image = loadImage("fantome_jaune.png")

def setup():
    createCanvas(400, 400)
    background("grey")
    ellipseMode("center")
    # rectMode("center")
    angleMode("deg")


def compute():
    global x, angle, sens, flip
    x += sens * vitesse
    # if keyIsPressed():
    #     if keys()[K_UP]:
    #         angle = 45
    #     elif keyIsDown(K_DOWN):
    #         angle = -45
    #     elif keyIsDown(K_LEFT):
    #         sens = -1
    #     elif keyIsDown(K_RIGHT):
    #         sens = 1
    # else:
    #     angle = 0
    # if x<-150:
    #     sens = 1
    # if x>150:
    #     sens = -1
    # if sens>0:
    #     flip = None
    # else:
    #     flip= (x + 200)


def draw():
    # line(200, 0, 200, 200)
    # line(0, 100, 400, 100)
    # translate(x, 0)
    # fill("yellow")
    # rotate(angle, (200, 100))
    # flip_v(flip)
    # line(200, 100, 400, 100)
    # circle(200, 100, 50)
    # fill("white")
    # circle(200, 90, 15)
    # fill("black")
    # circle(202, 90, 5)
    # arc(200, 100, 50, 50, 350, 370)
    # rect(300, 100, 50, 26)
    line(170, 0, 170, 400)
    rotate(45, (200, 100))
    rect(200, 100, 100, 50, image=image, allign_v="center", allign_h='center')
    flip_v(170)
    rect(200, 100, 100, 50, image=image, allign_v="center", allign_h='center')


run(globals())
