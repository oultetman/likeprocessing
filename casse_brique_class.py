from likeprocessing.processing import *

score = 0
class Rectangle:
    def __init__(self, center_position: tuple, largeur: int, hauteur: int, couleur: str):
        self.x, self.y = center_position
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.top = 0
        self.bottom = 0
        self.left = 0
        self.right = 0
        self.visible = True
        self.set_x(self.x)
        self.set_y(self.y)

    def set_x(self, x):
        self.x = x
        self.left = self.x - self.largeur // 2
        self.right = self.x + self.largeur // 2

    def set_y(self, y):
        self.y = y
        self.top = self.y - self.hauteur // 2
        self.bottom = self.y + self.hauteur // 2

    def is_in(self, x, y):
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def move(self):
        pass

    def draw(self):
        if self.visible:
            fill(self.couleur)
            rectMode("center")
            rect(self.x, self.y, self.largeur, self.hauteur)


class Brique(Rectangle):
    def __init__(self, center_position: tuple, largeur: int, hauteur: int, couleur: str, hurt_score=10, life=1):
        self.hurt_score = hurt_score
        self.start_life = life
        self.life = self.start_life
        super().__init__(center_position, largeur, hauteur, couleur)

    def decrease_life(self):
        if self.life >0:
            self.life-=1
            if self.life == 0:
                self.visible = False

class Raquette(Rectangle):
    def __init__(self, center_position: tuple, largeur: int, hauteur: int, couleur: str, lives: int):
        self.start_life = lives
        self.life = self.start_life
        super().__init__(center_position, largeur, hauteur, couleur)

    def move(self):
        self.set_x(mouseX())

    def decrease_life(self):
        pass


class Balle(Rectangle):
    def __init__(self, center_position: tuple, taille: int, couleur: str):
        self.sens_x = 1
        self.sens_y = -1
        self.vx = 2
        self.vy = 2
        super().__init__(center_position, taille, taille, couleur)

    def move(self):
        if self.left <= 0:
            self.sens_x = 1
        elif self.right >= width():
            self.sens_x = -1
        if self.top <= 0:
            self.sens_y = 1
        elif self.bottom >= height():
            self.sens_y = -1

        self.set_x(self.x + self.sens_x*self.vx)
        self.set_y(self.y + self.sens_y * self.vy)

    def collision(self, brique: list[Brique, Raquette]):
        for b in brique:
            if b.visible:
                if b.is_in(self.x, self.top):
                    self.sens_y = 1
                    b.decrease_life()

                elif b.is_in(self.x, self.bottom):
                    self.sens_y = -1
                    b.decrease_life()
                elif b.is_in(self.left, self.y):
                    self.sens_x = 1
                    b.decrease_life()
                elif b.is_in(self.right, self.y):
                    self.sens_x = -1
                    b.decrease_life()

    def draw(self):
        fill(self.couleur)
        circle(self.x,self.y,self.largeur)