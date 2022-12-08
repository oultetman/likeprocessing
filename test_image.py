from likeprocessing.processing import *

img: Image
img1: Image


def setup():
    global img, img1
    createCanvas(400, 200)
    background("grey")
    img = loadImage("fantome_jaune.png")
    img1 = resize_image(img, (100, 100))


def draw():
    image(img, 10, 10)
    image(img1, 100, 100)


run(globals())
