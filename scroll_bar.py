from time import sleep
from likeprocessing.processing import *

ihm = IhmScreen()


def click(name):
    print(f"ligne{name}")

def setup():
    createCanvas(400, 300)
    background("grey")
    ihm.init()
    ihm.addObjet(ListBox(ihm, (10, 10, 100, 100), [f"ligne {i}" for i in range(5)], command=click), "liste")


def compute():
    ihm.scan_events()
    # print(ihm.objet_by_name("liste").objet_by_name("scroll_v").value())


def draw():
    ihm.draw()


run(globals())
