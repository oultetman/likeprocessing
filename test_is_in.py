from likeprocessing.processing import *

def setup():
    angleMode("deg")
    createCanvas(400,200)
    background("grey")
    fill("white")
    fill_mouse_on("red")
def draw():
    title(str(mouseXY()))
    #rect(100,100,50,50)
    triangle(20,10,50,15,40,70)
    circle(200,110,80)


run(globals())