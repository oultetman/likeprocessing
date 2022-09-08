from likeprocessing.processing import *

x = 0
img = copy_image(loadImage("fantome_jaune.png"),(5,5,20,20))
def setup():
    createCanvas(400, 200)
    background("grey")
    rectMode("center")

def compute():
    global x
    if keyIsPressed():
        if keyIsDown(K_RIGHT):
            x += 1

def draw():
    rect(x, 100, 50, 25)
    image(img,0,0)

run(globals())
