"""connections composants"""
"""programme de base"""
from likeprocessing.processing import *


class Composant:
    def __init__(self, x: int, y: int, largeur: int, hauteur: int, nom: str, label: str):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.nom = nom
        self.label = label

    def move(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self):
        rect(self.x, self.y, self.largeur, self.hauteur)
        cm = rectMode()
        rectMode("center")
        textSize(24)
        text(self.label, self.x + self.largeur // 2, self.y + self.hauteur // 2, allign_h="center", allign_v="center",
             no_fill=True, no_stroke=True)
        textSize(12)
        text(self.nom, self.x + self.largeur // 2, self.y + self.hauteur // 4, allign_h="center", allign_v="center",
             no_fill=True, no_stroke=True)
        rectMode(cm)


class KConnection1:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.x3 = 0
        self.y3 = 0
        self.x4 = 0
        self.y4 = 0
        self.visible = False
        self.figed = False
        self.sens = 0

    def set_x2_y2(self, x, y):
        self.x2 = x
        self.y2 = y
        self.set_x34_y34()

    def set_x1_y1(self, x, y):
        self.x1 = x
        self.y1 = y
        self.visible = True

    def set_x34_y34(self):
        if self.figed and (dist(self.x1, self.y1, self.x2, self.y2) < 5):
            self.figed = False
        if not self.figed:
            if abs(self.x2 - self.x1) >= abs(self.y2 - self.y1):
                self.sens = 0
            else:
                self.sens = 1

        if self.sens == 0:
            if not self.figed:
                self.x3 = (self.x1 + self.x2) // 2
                self.x4 = self.x3
            self.y3 = self.y1
            self.y4 = self.y2
        elif self.sens == 1:
            if not self.figed:
                self.y3 = (self.y1 + self.y2) // 2
                self.y4 = self.y3
            self.x3 = self.x1
            self.x4 = self.x2

    def copy(self):
        c = KConnection(self.x1, self.y1, self.x2, self.y2)
        c.x3 = self.x3
        c.x4 = self.x4
        c.y3 = self.y3
        c.y4 = self.y4
        c.visible = True
        return c

    def __str__(self):
        return str([(self.x1, self.y1), (self.x3, self.y3), (self.x4, self.y4), (self.x2, self.y2)]) + str(self.sens)

    def draw(self):
        if self.visible:
            k_line([(self.x1, self.y1), (self.x3, self.y3), (self.x4, self.y4), (self.x2, self.y2)])


class KConnection:
    def __init__(self):
        self.points = [[0, 0] for i in range(4)]
        self.visible = False
        self.figed = False
        self.sens = 0

    def init(self):
        self.points = [[0, 0] for i in range(4)]
        self.visible = False
        self.figed = False
        self.sens = 0

    def set_x2_y2(self, x, y):
        self.points[-1] = [x, y]
        self.set_x34_y34()

    def set_x1_y1(self, x, y):
        self.points[-4] = [x, y]
        self.visible = True

    def set_x34_y34(self):
        if self.figed and (dist(*self.points[-4], *self.points[-1]) < 5):
            self.figed = False
        if not self.figed:
            if abs(self.points[-4][0] - self.points[-1][0]) >= abs(self.points[-4][1] - self.points[-1][1]):
                self.sens = 0
            else:
                self.sens = 1

        if self.sens == 0:
            if not self.figed:
                self.points[-3][0] = (self.points[-4][0] + self.points[-1][0]) // 2
                self.points[-2][0] = self.points[-3][0]
            self.points[-3][1] = self.points[-4][1]
            self.points[-2][1] = self.points[-1][1]
        elif self.sens == 1:
            if not self.figed:
                self.points[-3][1] = (self.points[-4][1] + self.points[-1][1]) // 2
                self.points[-2][1] = self.points[-3][1]
            self.points[-3][0] = self.points[-4][0]
            self.points[-2][0] = self.points[-1][0]

    def copy(self):
        c = KConnection()
        c.points = []
        for pos in self.points:
            c.points.append(pos)
        c.visible = True
        return c

    def __str__(self):
        return str(self.points)

    def draw(self):
        if self.visible:
            k_line(self.points)


class Connectique:
    def __init__(self):
        self.connections: list[KConnection] = []

    def add_connection(self, connection: KConnection):
        self.connections.append(connection)

    def connection_by_coord(self, x: int, y: int) -> [None, KConnection]:
        for c in self.connections:
            if c[0] == [x, y] or c[-1] == [x, y]:
                return c
        return None

    def draw(self):
        for c in self.connections:
            c.draw()


pt = KConnection()
t = Tempo(500)
connectiques = Connectique()
composant = Composant(10, 10, 60, 80, "U1", "&")


def mouse_xy(pas) -> tuple[int]:
    return (mouseX() // pas * pas, mouseY() // pas * pas)


def setup():
    createCanvas(600, 300)
    background("grey")


def compute():
    if keyIsPressed():
        if keyIsDown(K_SPACE) and t.fin():
            pt.figed = not pt.figed
    if mouse_click_down():
        if mouse_button_pressed() == 0:
            if pt.visible:
                connectiques.add_connection(pt.copy())
                pt.init()
            else:
                pt.set_x1_y1(*mouse_xy(10))
    if pt is not None:
        pt.set_x2_y2(*mouse_xy(10))

    composant.move(*mouse_xy(10))


def draw():
    title(f"figed: {pt.figed} {pt}")
    connectiques.draw()
    pt.draw()
    composant.draw()


run(globals())
