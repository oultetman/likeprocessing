from likeprocessing.processing import *

pos_tete = 0
etat = "-1"
erreur = True
ecriture = None
pos_tete_suivante = None
y_sous_tete = 0
dx = 0
vitesse = 30
pos_a_atteindre = -1
nb_position = 100
ruban = [-1 for i in range(nb_position)]


def marche():
    global erreur, etat, pos_tete
    erreur = False
    etat = "0"


def init():
    global pos_a_atteindre
    if erreur:
        if init_pos.texte != "":
            print(init_pos.text())
            try:
                pos_a_atteindre = int(init_pos.text()) % nb_position
            except:
                pos_a_atteindre = 25


bp_marche = Bouton(None, (10, 20, 100, 20), 'Marche', command=marche)
bp_init = Bouton(None, ((10, 45, 100, 20)), 'initialisation', command=init)
init_pos = LineEdit(None, (10, 80, 100, 15), "0 _ _ g 0")
texte = MultiLineText(None,(120, 20, 100, 100),"bonjour\nles\namis")
def scan_event():
    bp_marche.scan_mouse()
    bp_init.scan_mouse()
    init_pos.scan_mouse()
    init_pos.update(processing.__events)


def programme():
    global ruban, pos_tete, etat, erreur, ecriture, pos_tete_suivante
    if etat == "-1":
        init = [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        pos_init = 2
        ruban[pos_init:pos_init + len(init)] = init
        etat = "0"
    elif ecriture is None and pos_tete_suivante is None:
        prog = ["0;-1;-1;g;0", "0;1;0;g;1", "0;0;1;g;1", "1;0;1;g;1",
                "1;1;0;g;1", "1;-1;-1;d;2", "2;1;1;d;2", "2;0;0;d;2", "2;-1;-1;g;0"]
        table = [l.split(";") for l in prog]
        erreur = True
        for l in table:
            if l[0] == etat and str(ruban[pos_tete]) == l[1]:
                ecriture = int(l[2])
                if ecriture == ruban[pos_tete]:
                    ecriture = None
                if l[3].lower() == "g":
                    pos_tete_suivante = (pos_tete + 1) % nb_position
                elif l[3].lower() == "d":
                    pos_tete_suivante = (pos_tete - 1) % nb_position
                else:
                    pos_tete_suivante = None
                etat = l[4]
                erreur = False
                break


def deplacement_ecriture():
    global ecriture, y_sous_tete, pos_tete, ruban

    if ecriture is not None and ruban[pos_tete] != ecriture:
        if ruban[pos_tete] < ecriture:
            y_sous_tete -= 0.01 * vitesse
        else:
            y_sous_tete += 0.01 * vitesse
        if abs(y_sous_tete) >= abs(ruban[pos_tete] - ecriture):
            ruban[pos_tete] = ecriture
            ecriture = None
            y_sous_tete = 0


def deplacement_ruban():
    global pos_tete_suivante, pos_tete, dx, pos_a_atteindre
    if pos_a_atteindre >= 0:
        if 0 < pos_a_atteindre - pos_tete < nb_position / 2 or pos_a_atteindre + nb_position - pos_tete < nb_position / 2:
            pos_tete_suivante = (pos_tete + 1) % nb_position
        elif -50 < pos_a_atteindre - pos_tete < 0 or pos_tete + nb_position - pos_a_atteindre < nb_position / 2:
            pos_tete_suivante = (pos_tete - 1) % nb_position
        else:
            pos_a_atteindre = -1
    if ecriture is None and pos_tete_suivante is not None:
        if pos_tete_suivante == 99 and pos_tete == 0:
            dx += 0.01 * vitesse
        elif pos_tete_suivante == 0 and pos_tete == 99:
            dx -= 0.01 * vitesse
        elif pos_tete < pos_tete_suivante:
            dx -= 0.01 * vitesse
        else:
            dx += 0.01 * vitesse
        if abs(dx) >= 1:
            pos_tete = pos_tete_suivante
            pos_tete_suivante = None
            dx = 0


def compute():
    global pos_tete, ruban, y_sous_tete, ecriture, dx, pos_tete_suivante
    if erreur is True and keyIsPressed() and pos_tete_suivante is None and ecriture is None:
        if keyIsDown(K_RIGHT):
            pos_tete_suivante = (pos_tete - 1) % nb_position
        elif keyIsDown(K_LEFT):
            pos_tete_suivante = (pos_tete + 1) % nb_position
        elif keyIsDown(K_UP) and ruban[pos_tete] < 1:
            ecriture = ruban[pos_tete] + 1
        elif keyIsDown(K_DOWN) and ruban[pos_tete] > -1:
            ecriture = ruban[pos_tete] - 1
    if erreur is False:
        programme()
    deplacement_ecriture()
    deplacement_ruban()


def draw_ruban():
    line(500, 0, 500, 400)
    textSize(16)
    text("état", 500, 25, 100, 25)
    text(f"{etat}", 500, 55, 100, 25)
    t = str(ruban[pos_tete])
    if t == "-1": t = "_"
    text("lecture", 500, 100, 100, 25)
    text(f"{t}", 500, 130, 100, 25)
    translate(dx * 20, 0)
    j = 0
    for i in range(pos_tete - 25, pos_tete + 27):
        if i == pos_tete and ecriture is not None:
            rect(500, 200 - 10 * ruban[pos_tete] + y_sous_tete * 10, 15, 60)
        elif ruban[i % nb_position] == -1:
            rect(j * 20, 210, 15, 60)
        elif ruban[(i) % nb_position] == 0:
            rect(j * 20, 200, 15, 60)
        elif ruban[(i) % nb_position] == 1:
            rect(j * 20, 190, 15, 60)
        j += 1
    rect(0, 200, 2100, 30)
    textSize(10)
    for i in range(25):
        text(f"{(i + pos_tete - 25) % nb_position}", i * 20, 200, 18, 16)
    for i in range(27):
        if i == 0:
            fill("yellow")
        else:
            fill("white")
        text(f"{(i + pos_tete) % nb_position}", i * 20 + 500, 200, 16, 16)


def setup():
    createCanvas(1000, 400)
    background("grey")
    rectMode("center")
    textAlign("center", "center")


def draw():
    bp_marche.draw()
    bp_init.draw()
    init_pos.draw()
    texte.draw()
    draw_ruban()


run(globals())
