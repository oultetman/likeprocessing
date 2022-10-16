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
progtxt = "0 _ _ g 0\n0 1 0 g 1\n0 0 1 g 1\n1 0 1 g 1\n1 1 0 g 1\n1 _ _ d 2\n2 1 1 d 2\n2 0 0 d 2\n2 _ _ g 0"
t = Tempo(1000)


def marche():
    global erreur, etat, pos_tete
    erreur = False
    etat = "-1"
    ihm.disabled("all")
    ihm.enabled("stop")


def arret():
    global erreur
    erreur = True
    ihm.disabled("stop")
    ihm.enabled("all")


def init():
    global pos_a_atteindre
    if erreur:
        if ihm.objet.get("pos_init").text() != "":
            print(ihm.objet.get("pos_init").text())
            try:
                pos_a_atteindre = int(ihm.objet.get("pos_init").text()) % nb_position
            except:
                pos_a_atteindre = 25


def monte():
    global ecriture
    if ruban[pos_tete] < 1:
        ecriture = ruban[pos_tete] + 1

def descend():
    global ecriture
    if ruban[pos_tete] > -1:
        ecriture = ruban[pos_tete] - 1


def gauche():
    global pos_tete_suivante
    pos_tete_suivante = (pos_tete + 1) % nb_position


def droite():
    global pos_tete_suivante
    pos_tete_suivante = (pos_tete - 1) % nb_position


def cls():
    ihm.objet.get("editeur").set_text("")


ihm = IhmScreen()


def scan_event():
    ihm.scan_events()


def programme(prg=None):
    global ruban, pos_tete, etat, erreur, ecriture, pos_tete_suivante
    if etat == "-1":
        init = [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        pos_init = 2
        ruban[pos_init:pos_init + len(init)] = init
        etat = "0"
    elif ecriture is None and pos_tete_suivante is None:
        if prg is None:
            prog = ["0;-1;-1;g;0", "0;1;0;g;1", "0;0;1;g;1", "1;0;1;g;1",
                    "1;1;0;g;1", "1;-1;-1;d;2", "2;1;1;d;2", "2;0;0;d;2", "2;-1;-1;g;0"]
            table = [l.split(";") for l in prog]
        else:
            p = []
            for l in prg:
                if l != "":
                    p.append(l.replace("_", "-1"))
            table = [l.split(" ") for l in p]
        erreur = True
        for ligne in table:
            if ligne[0] == etat and str(ruban[pos_tete]) == ligne[1]:
                ecriture = int(ligne[2])
                if ecriture == ruban[pos_tete]:
                    ecriture = None
                if ligne[3].lower() == "g":
                    pos_tete_suivante = (pos_tete + 1) % nb_position
                elif ligne[3].lower() == "d":
                    pos_tete_suivante = (pos_tete - 1) % nb_position
                else:
                    pos_tete_suivante = None
                etat = ligne[4]
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
    if erreur is True and keyIsPressed() and pos_tete_suivante is None and ecriture is None and ihm.objet[
        "editeur"].focus is not True and not ihm.objet_focus:
        if keyIsDown(K_RIGHT):
            droite()
        elif keyIsDown(K_LEFT):
            gauche()
        elif keyIsDown(K_UP):
            monte()
        elif keyIsDown(K_DOWN):
            descend()
    if erreur is False:
        programme(ihm.objet.get("editeur").text())
    deplacement_ecriture()
    deplacement_ruban()


def draw_ruban(posy):
    rm = rectMode()
    rectMode("center")
    line(width() // 2, 0, width() // 2, height())
    textSize(16)
    text("état", width() // 2, 25, 100, 25)
    text(f"{etat}", width() // 2, 55, 100, 25)
    t = str(ruban[pos_tete])
    if t == "-1": t = "_"
    text("lecture", width() // 2, 100, 100, 25)
    text(f"{t}", width() // 2, 130, 100, 25)
    translate(dx * 20, 0)
    j = 0
    # dessin rectangle datas
    for i in range(pos_tete - 25, pos_tete + 27):
        if i == pos_tete and ecriture is not None:
            rect(width() // 2, posy - 10 * ruban[pos_tete] + y_sous_tete * 10, 15, 60)
        elif ruban[i % nb_position] == -1:
            rect(j * 20, posy+10, 15, 60)
        elif ruban[i % nb_position] == 0:
            rect(j * 20, posy, 15, 60)
        elif ruban[i % nb_position] == 1:
            rect(j * 20, posy-10, 15, 60)
        j += 1
    init_translate()
    rect(width() // 2-2, posy, width()+4, 30)
    textSize(10)
    translate(dx * 20, 0)
    # dessin numerotation case datas
    for i in range(25):
        text(f"{(i + pos_tete - 25) % nb_position}", i * 20, posy, 18, 16)
    for i in range(27):
        if i == 0:
            fill("yellow")
        else:
            fill("white")
        text(f"{(i + pos_tete) % nb_position}", i * 20 + width() // 2, posy, 16, 16)
    rectMode(rm)


def setup():
    global pos_tete_suivante, pos_tete
    createCanvas(1000, 400)
    title("Machine de Turing by likeprocessing")
    background("grey")
    textAlign("center", "center")
    img = loadImage("fantome_jaune.png")
    ihm.init()
    ihm.addObjet(Bouton(None, (20, 20, 45, 20), 'Run', command=marche), "run")
    ihm.addObjet(Bouton(None, (70, 20, 45, 20), 'stop', command=arret), 'stop')
    ihm.addObjet(Bouton(None, (20, 45, 45, 20), 'rotation', command=init), 'rotation')
    ihm.addObjet(LineEdit(None, (70, 45, 45, 20), "0"), "pos_init")
    ihm.addObjet(TextEdit(None, (120, 20, 100, 150), progtxt, largeurBord=1,police="courier"), "editeur")
    ihm.addObjet(Bouton(None, (60, 70, 20, 20), '^', command=monte), "monte")
    ihm.addObjet(Bouton(None, (60, 95, 20, 20), 'v', command=descend), "descend")
    ihm.addObjet(Bouton(None, (40, 82, 20, 20), '<', command=gauche), "gauche")
    ihm.addObjet(Bouton(None, (80, 82, 20, 20), '>', command=droite), "droite")
    ihm.addObjet(Bouton(None, (225, 20, 45, 20), 'cls', command=cls), "cls")
    ihm.objet_by_name("stop").is_disabled = True
    print(ihm.objet.keys())


def draw():
    ihm.draw()
    draw_ruban(280)
    # if t.fin():
    #     e = ihm.objet.get("editeur")
    #     print(e.ligne_actuelle)
    #     print(e.texte)


run(globals())
