from time import sleep
from likeprocessing.processing import *
from likeprocessing.print_vars import *

ihm = IhmScreen()


def click(name):
    print(f"ligne{name}")


def all():
    ihm.objet_by_name("liste").select_all()


def des():
    ihm.objet_by_name("liste").unseselect_all()


def setup():
    createCanvas(400, 300)
    background("grey")
    ihm.init()
    ihm.addObjet(ListBox(ihm, (230, 100, 100, 90), [f"ligne {i}" for i in range(10)]), "liste")
    ihm.addObjet(Bouton(ihm, (10, 10, 100, 30), "tout\nselectionner", command=all), "all")
    ihm.addObjet(Bouton(ihm, (120, 10, 100, 30), "tout\ndéssélectionner", command=des), "des")


def compute():
    ihm.scan_events()


def draw():
    ihm.draw()


run(globals())
