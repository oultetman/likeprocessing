from likeprocessing.processing import *

def setup():
    createCanvas(400,200)
    background("grey")

def compute():
    if mouse_click_down():
        fill("red")
    elif mouse_click_up():
        fill("blue")

def draw():
    rect(10,10,100,50)

run(globals())