from likeprocessing.processing import *


def setup():
    createCanvas(400, 200)
    background("grey")

def draw():
    for i in range(60,160,20):
        circle(50,50,i)

run(globals())
