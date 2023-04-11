# -------------------------------------------------------------------------------
# Nom:        module1
# Description:
#
# Auteur:      Utilisateur
#
# Created:     19/05/2019
# Copyright:   (c) Utilisateur 2019
# Licence:     <your licence>
# -------------------------------------------------------------------------------
from pygame import Rect
from likeprocessing.processing import *


class Jauge(Rect):
    def __init__(self, largeur, hauteur, valeurMax, couleur="red"):
        super().__init__(0, 0, largeur, hauteur)
        self.largeur = largeur
        self.valeurMax = valeurMax
        self.couleur = couleur
        self.valeur = valeurMax

    def setPos(self, x, y):
        self.topleft = x, y

    def setValeur(self, valeur):
        self.valeur = max(0, valeur)
        self.valeur = min(self.valeur, self.valeurMax)
        self.width = self.valeur / self.valeurMax * self.largeur

    def decremente(self, valeur):
        self.setValeur(self.valeur - valeur)

    def incremente(self, valeur):
        self.setValeur(self.valeur + valeur)

    def draw(self):
        rect(*self, fill=self.couleur)


if __name__ == '__main__':
    from likeprocessing.processing import *

    j = Jauge(100, 10, 100)
    j.setValeur(0)
    t = Tempo(500)

    def setup():
        createCanvas(400, 200)
        background("grey")
        j.setPos(10, 10)


    def compute():
        if t.fin():
            j.incremente(10)


    def draw():

        j.draw()

    run(globals())
