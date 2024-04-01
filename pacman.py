import pygame

from likeprocessing.processing import *

__print_x = -200
t = Tempo(100)
angle = 0
nb_ligne = 10
nb_colonne = 6
tab = [[random(4) for i in range(nb_colonne)] for j in range(nb_ligne)]
valeur = 0
rate = False
score = 0
points = 0
couleurs = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "cyan", "magenta"]
vies = 5
coeur = loadImage("images/heart.png")
coeur = resize_image(coeur, (25, 25))


def exit():
    global score, vies, tab
    set_quit(False)
    if AskYesNo(None, "Voulez-vous Vraiment\nquitter le jeu").response() == 0:
        set_quit(True)
    else:
        score = 0
        vies = 5
        tab = [[random(4) for i in range(nb_colonne)] for j in range(nb_ligne)]

def click(name):
    global tab
    i, j = name
    tab[i][j] = 0


def setup():
    createCanvas(400, 400)
    background("grey")
    ellipseMode("center")
    # rectMode("center")
    angleMode("deg")


def compute():
    global tab, valeur, rate, score, points, vies
    if mouseIsPressed() and rate is False:
        # calcule la position de la souris dans le tableau
        i = borner(nb_ligne - int((mouseY() - 50) / 25), 0, nb_ligne - 1)  # ligne du tableau
        j = borner(int((mouseX() - 50) / 25), 0, nb_colonne - 1)  # colonne du tableau
        if mouse_click_down():
            print(f"valeur = {valeur}, i = {i}, j = {j}")
            valeur = 2 ** tab[i][j]

        if 2 ** tab[i][j] == valeur:
            tab[i][j] = -1
            points += 1
        elif tab[i][j] != -1:
            rate = True
            if valeur <= points:
                score += (points * valeur) ** 2
            else:
                score -= valeur * (valeur - points) ** 2
                if points < round(valeur * 2 / 3):
                    vies -= 1
            points = 0
    else:
        if t.fin():
            decale = True
            for j in range(len(tab[0])):
                if tab[-1][j] == -1:
                    tab[-1][j] = random(4)
                    decale = True
            for j in range(len(tab[0])):
                i = len(tab) - 2
                while i >= 0 and decale is True:
                    if tab[i][j] == -1:
                        tab[i][j], tab[i + 1][j] = tab[i + 1][j], tab[i][j]
                        decale = True
                    i -= 1
    if mouse_click_up():
        if rate is False:
            if valeur <= points:
                score += (points * valeur) ** 2
            else:
                score -= valeur * (valeur - points) ** 2
                if points < round(valeur * 2 / 3):
                    vies -= 1
            points = 0
        rate = False

    title(f"Score : {score}")
    if vies <= 0:
        ShowInfo(None, f"Vous avez perdu \nVotre score est de \n{score} points.").response()
        set_quit(True)


def draw():
    for j in range(vies):
        image(coeur, 50 + j * 25, 30)

    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if tab[i][j] != -1:
                text(2 ** tab[i][j], 50 + j * 25, 300 - i * 25, 25, 25, align_h="center", align_v="center",
                     command=click,
                     name=(i, j), fill=couleurs[tab[i][j] - 1])


run(globals())
