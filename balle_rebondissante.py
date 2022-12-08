from likeprocessing.processing import *


class Ball:
    def __init__(self, taille: int, couleur: str, x: int, y: int):
        self.taille = taille
        self.couleur = couleur
        self.x = 0
        self.y = 0
        self.top = 0
        self.bottom = 0
        self.right = 0
        self.left = 0
        self.sens_x = 1
        self.sens_y = 1
        self.vx = 3
        self.vy = 3
        self.set_x(x)
        self.set_y(y)

    def set_x(self, x):
        self.x = x
        self.right = x + self.taille // 2
        self.left = x - self.taille // 2

    def set_y(self, y):
        self.y = y
        self.bottom = y + self.taille // 2
        self.top = y - self.taille // 2

    def move(self):
        self.set_x(self.x + self.sens_x * self.vx)
        self.set_y(self.y + self.sens_y * self.vy)
        if self.right >= width():
            self.sens_x = -self.sens_x
            self.set_x(width() - 1 - self.taille // 2)
        elif self.left <= 0:
            self.sens_x = -self.sens_x
            self.set_x(1 + self.taille // 2)
        if self.top <= 0:
            self.sens_y = -self.sens_y
            self.set_y(1 + self.taille // 2)
        elif self.bottom > height():
            self.sens_y = -self.sens_y
            self.set_y(height() - 1 - self.taille // 2)

    def is_in(self, x, y):
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def colision(self, objets: ["Ball"]):
        for o in objets:
            if o != self:
                if self.is_in(o.left, o.__print_y) or self.is_in(o.right, o.__print_y) or self.is_in(o.__print_x, o.top) or self.is_in(o.__print_x,
                                                                                                                                       o.bottom):
                    self.sens_x = -self.sens_x
                    self.sens_y = -self.sens_y
                    o.sens_x = -o.sens_x
                    o.sens_y = -o.sens_y

    def draw(self):
        c = get_fill_color()
        cm = ellipseMode("center")
        fill(self.couleur)
        circle(self.x, self.y, self.taille)
        fill(c)
        ellipseMode(cm)


couleur = ["black", "white", "green", "yellow", "red", "blue", "orange"]
balls = [Ball(30, couleur[i], 10 + 30 * i, 10 + (i % 2) * 30 * i) for i in range(7)]


def setup():
    createCanvas(400, 200)
    background("grey")


def compute():
    for b in balls:
        b.colision(balls)
        b.move()


def draw():
    for b in balls:
        b.draw()


run(globals())
