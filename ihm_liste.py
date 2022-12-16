"""Base programm likeprocessing"""

from likeprocessing.processing import *

ihm = IhmScreen()

def setup():
    createCanvas(400, 400)
    background("grey")
    ihm.init()
    ihm.addObjet(ListBox(ihm,(10,10,100,200),[f"ligne {i}" for i in range(15)]))

def compute():
    ihm.scan_events()


def draw():
    ihm.draw()


run(globals())