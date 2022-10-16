from likeprocessing.processing import *
from casse_brique_class import Brique, Balle, Raquette, Rectangle

couleur = ["green", "blue", "yellow", "orange", "red"]
briques: list[Rectangle] = [Brique((20 + j * 40, 10 + i * 20), 40, 20, couleur[i % 5]) for j in range(10) for i
                                   in range(4)]
briques.append(Raquette((200, 380), 60, 20, "purple",3))
balle = Balle((200, 360), 10, "red")


def setup():
    createCanvas(400, 400)
    background("grey")


def compute():
    balle.move()
    balle.collision(briques)
    briques[-1].move()


def draw():
    for b in briques:
        b.draw()
    balle.draw()


run(globals())
