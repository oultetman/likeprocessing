from likeprocessing.processing import *

couleur = ("black", "red", "orange", "yellow", "green", "blue")


def setup():
    createCanvas(220, 200,True)
    background("darkblue")
    stroke("white")


def draw():
    x = (mouseX()-20)//20
    y = (mouseY()-20)//20
    if 0<=x<=7 and 0<=y<=7 :
        title(f"x={x} y={y}")
    else:
        title("grille")
    for i in range(9):
        line(20 + i * 20, 20, 20 + i * 20, 180)
        line(20, 20 + i * 20, 180, 20 + i * 20)


run(globals())
