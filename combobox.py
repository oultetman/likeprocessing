from likeprocessing.processing import *

ihm = IhmScreen()


def open():
    if ihm.objet_by_name("combo").height == 22:
        ihm.objet_by_name("combo").height = 100
    else:
        ihm.objet_by_name("combo").height = 22


def file_select():
    b = AskOkCancel(ihm, "essai", "comment allez-vous").response()
    print(b)


def calcul(name):
    dico = {"x²": "**2", "x": "*", "^": "**", "EE": "e", "pi": str(round(math.pi, 14))}
    affichage = ihm.objet_by_name("ecran")
    if name == "=":
        affichage.text(str(round(eval(affichage.text()), 10)))
    elif name == "CA":
        affichage.text("0")
    elif name == "cos(" or name == "sin(" or name == "tan(":
        if affichage.text()[-1] not in ["*-+/"]:
            affichage.text(affichage.text() + "*" + dico.get(name, name))
        else:
            affichage.text(affichage.text() + dico.get(name, name))
    else:
        if len(affichage.text()) == 1 and affichage.text() == "0":
            affichage.text(dico.get(name, name))
        else:
            affichage.text(affichage.text() + dico.get(name, name))


def setup():
    createCanvas(200, 250)
    background("grey")
    ihm.init()
    ihm.addObjet(
        ListRadio(ihm, (10, 10, 60, 0), ["degrés", "radian", "grades"], title="Angles", no_fill=True, ligxcol="1x3"),
        "liste")
    ihm.addObjet(Label(ihm, (10, 55, 180, 30), "0", align_h="right", align_v="bottom", stroke="black", font_size=20),
                 "ecran")
    touches = [["log", "x²", "(", ")", "^", "x"], ["ln", "sin(", "7", "8", "9", "/"],
               ["sto", "cos(", "4", "5", "6", "-"], ["pi", "tan(", "1", "2", "3", "+"],
               ["CA", "EE", "0", ".", "(-)", "="]]
    for i, l in enumerate(touches):
        for j, t in enumerate(l):
            ihm.addObjet(Bouton(ihm, (10 + 30 * j, 90 + 30 * i, 30, 30), t, command=calcul, name=t))


def compute():
    v = ihm.objet_by_name("liste").values()[0]
    if v == 0:
        angleMode("deg")
    elif v == 1:
        angleMode("rad")
    elif v == 2:
        angleMode("grd")
    ihm.scan_events()


def draw():
    ihm.draw()


run(globals())
