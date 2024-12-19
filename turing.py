from likeprocessing.processing import *
from tkinter import filedialog

"""
0 _ _ g 0
0 1 1 g 1
0 0 0 g 1
1 1 1 g 1
1 0 0 g 1
1 _ _ d 2
2 0 1 d 1
2 1 0 d 2
4 1 1 d 4
4 0 0 d 4
4 _ _ g 1
"""

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
progtxt = "#initialisation du ruban\n0 _ _ g 0\n0 * /* g 1\n1 * * g 1\n1 _ _ _ fin\n"
t = Tempo(500)
table = []
pause = Monostable(1000)
last_prg = "prog_1.txt"

def marche():
    global erreur, pos_tete

    text = ihm.objet_by_name("frame").objet_by_name("editeur").text()
    if text.strip() == "":
        r = ShowError(ihm, "Votre programme est vide!").response()
    else:
        erreur = False
        init_prg(text)
        ihm.objet_by_name("frame").objet_by_name("ligne en cours").fill = "white"
        ihm.objet_by_name("frame").disable("all")
        ihm.objet_by_name("frame").enable(["stop", "ligne en cours"])
        pause.reset()
        pause.trigger(True)


def arret():
    global erreur
    erreur = True
    ihm.objet_by_name("frame").enable("all")
    ihm.objet_by_name("frame").disable("stop")


def reset_ruban():
    global ruban, pos_tete
    ruban = [-1 for i in range(nb_position)]
    init(0)


def init(pos=None):
    global pos_a_atteindre
    if erreur:
        if pos is not None:
            pos_a_atteindre = pos
        else:
            if ihm.objet_by_name("frame").objet_by_name("pos_init").text() != "":
                try:
                    pos_a_atteindre = int(ihm.objet_by_name("frame").objet_by_name("pos_init").text()) % nb_position
                except:
                    pos_a_atteindre = 25


def click(i):
    global ruban
    ruban[i] = (ruban[i] + 2) % 3 - 1


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
    ihm.objet_by_name("frame").objet_by_name("editeur").text("")


def sauver():
    global last_prg
    text = ihm.objet_by_name("frame").objet_by_name("editeur").text()
    if text.strip() == "":
        r = ShowError(ihm, "Votre programme est vide!").response()
    else:
        file = filedialog.asksaveasfilename(
            title="Sélectionner un fichier",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        if file == "":
            r = ShowError(ihm, "Nom de fichier vide!").response()
        else:
            if not file.endswith(".txt"):
                file += ".txt"
            with open(file, "w") as f:
                f.write(text)
            r = ShowInfo(ihm, "Programme sauvegardé!").response()
            last_prg = file


def load_file(file):
    with open(file, "r") as f:
        text = f.read()
    ihm.objet_by_name("frame").objet_by_name("editeur").text(text)


def charger():
    file = filedialog.askopenfilename(
        title="Sélectionner un fichier",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
    )
    if file == "":
        r = ShowError(ihm, "Nom de fichier vide!").response()
    else:
        load_file(file)


ihm = IhmScreen()


def scan_event():
    ihm.scan_events()


def init_prg(prg=None | str):
    global etat, ruban, pos_tete, pos_tete_suivante, ecriture, erreur, table
    if ihm.objet_by_name("frame").objet_by_name("init").text() != "":
        init_char = ihm.objet_by_name("frame").objet_by_name("init").text()
        init = []
        for c in init_char:
            if c == "0":
                init.append(0)
            elif c == "1":
                init.append(1)
            else:
                init.append(-1)
        pos_init = int(ihm.objet_by_name("frame").objet_by_name("pos_init").text()) % nb_position
        ruban[pos_init:pos_init + len(init)] = init

    if prg is None:
        prg = ["#initialisation du ruban", "0;-1;-1;g;0", "0;1;0;g;1", "0;0;1;g;1", "1;0;1;g;1",
               "1;1;0;g;1", "1;-1;-1;d;2", "2;1;1;d;2", "2;0;0;d;2", "2;-1;-1;g;0"]
    p = []
    etat = ""
    if isinstance(prg, str):
        prg = prg.split("\n")
    # compilation du programme
    if prg[0][1:].strip() != "# start":
        etat = prg[0].strip().split("=")[1].strip()
    for l in prg:
        if l != "" and l.strip()[0] != "#":
            ligne = l.replace("_", "-1")
            # caractère de vide
            ligne = ligne.replace("/*", "-3")
            # caractère d'inversion de la valeur
            ligne = ligne.replace("*", "-2")
            # caractère de valeur numérique
            ligne = ligne.replace("?", "-4")
            # caractère de n'importe quel caractère
            p.append(ligne)
    table = [l.split(" ") for l in p]
    if etat == "":
        etat = table[0][0]


def programme():
    global ruban, pos_tete, etat, erreur, ecriture, pos_tete_suivante

    if ecriture is None and pos_tete_suivante is None:
        erreur = True
        for ligne in table:
            if ligne[0] == etat and (str(ruban[pos_tete]) == ligne[1] or (ligne[1] == "-2" and ruban[pos_tete] >= 0) or ligne[1] == "-4"):
                ecriture = int(ligne[2])
                if ecriture == ruban[pos_tete] or ecriture == -2 or ecriture == -4:
                    # pas d'écriture
                    ecriture = None
                if ecriture == -3:
                    # inversions des valeurs numériques
                    ecriture = (ruban[pos_tete] + 1) % 2
                if ligne[3].lower() == "g" or ligne[3].lower() == "l":
                    # déplacement à gauche
                    pos_tete_suivante = (pos_tete + 1) % nb_position
                elif ligne[3].lower() == "d" or ligne[3].lower() == "r":
                    # déplacement à droite
                    pos_tete_suivante = (pos_tete - 1) % nb_position
                else:
                    pos_tete_suivante = None
                etat = ligne[4]
                erreur = False
                ihm.objet_by_name("frame").objet_by_name("ligne en cours").text(" ".join(ligne))
                break
        if erreur:
            ihm.objet_by_name("frame").objet_by_name("ligne en cours").fill = "Red"
            rep = ShowError(ihm, "Une erreur s'est produite").response()
            arret()
        if len(etat) >= 3 and etat[:3] in ["fin", "end"]:
            arret()


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
    if erreur is True and keyIsPressed() and pos_tete_suivante is None and ecriture is None and ihm.objet_by_name(
            "frame").objet_by_name("editeur").focus is not True and not ihm.objet_focus:
        if keyIsDown(K_RIGHT):
            droite()
        elif keyIsDown(K_LEFT):
            gauche()
        elif keyIsDown(K_UP):
            monte()
        elif keyIsDown(K_DOWN):
            descend()
    if pause.is_off():
        if erreur is False:
            programme()

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
            rect(width() // 2, posy - 10 * ruban[pos_tete] + y_sous_tete * 10, 15, 60, fill_mouse_on="0xff55ff", name=i,
                 command=click)
        elif ruban[i % nb_position] == -1:
            rect(j * 20, posy + 10, 15, 60, fill_mouse_on="0xff55ff", name=i, command=click)
        elif ruban[i % nb_position] == 0:
            rect(j * 20, posy, 15, 60, fill_mouse_on="0xff55ff", name=i, command=click)
        elif ruban[i % nb_position] == 1:
            rect(j * 20, posy - 10, 15, 60, fill_mouse_on="0xff55ff", name=i, command=click)
        j += 1
    init_translate()
    rect(width() // 2 - 2, posy, width() + 4, 30)
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
    ihm.init()
    frame = ihm.addObjet(Frame(ihm, (10, 5, 400, 220), title="Programme"), "frame")
    frame.addObjet(Bouton(frame, (30, 10, 45, 20), 'Run', command=marche), "run")
    frame.addObjet(Bouton(frame, (80, 10, 45, 20), 'stop', command=arret), 'stop')
    frame.addObjet(Bouton(frame, (30, 35, 45, 20), 'rotation', command=init), 'rotation')
    frame.addObjet(LineEdit(frame, (80, 35, 45, 21), "0"), "pos_init")
    frame.addObjet(TextEdit(frame, (130, 10, 200, 150), progtxt, largeurBord=1, police="courier"), "editeur")
    frame.addObjet(Bouton(frame, (70, 60, 20, 20), '^', command=monte), "monte")
    frame.addObjet(Bouton(frame, (70, 85, 20, 20), 'v', command=descend), "descend")
    frame.addObjet(Bouton(frame, (50, 72, 20, 20), '<', command=gauche), "gauche")
    frame.addObjet(Bouton(frame, (90, 72, 20, 20), '>', command=droite), "droite")
    frame.addObjet(Bouton(frame, (334, 10, 60, 20), 'Cls', command=cls), "cls")
    frame.addObjet(Bouton(frame, (334, 35, 60, 20), 'Sauver', command=sauver), "sauver")
    frame.addObjet(Bouton(frame, (334, 60, 60, 20), 'Charger', command=charger), "charger")
    frame.addObjet(Label(frame, (10, 110, 0, 0), "init"), "initpos")
    frame.addObjet(LineEdit(frame, (30, 110, 95, 20), "__010011001"), "init")
    frame.addObjet(Bouton(frame, (30, 140, 95, 20), "Reset ruban", command=reset_ruban), "reset ruban")
    frame.addObjet(Label(frame, (30, 170, 300, 20), "", fill="white", font_size=20, stroke=1), "ligne en cours")
    frame.objet_by_name("stop").disabled = True
    load_file(last_prg)


def draw():
    ihm.draw()
    draw_ruban(300)
    title(f"{ecriture},{pos_tete_suivante},{erreur}")


run(globals())
