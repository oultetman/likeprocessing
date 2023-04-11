# -------------------------------------------------------------------------------
# Nom:        module1
# Description:
#
# Auteur:      Utilisateur
#
# Created:     30/05/2019
# Copyright:   (c) Utilisateur 2019
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import pygame
from pygame import Rect
from likeprocessing.processing import *
from likeprocessing.jauge import Jauge


class Point:
    def __init__(self, *coordonnees):
        if len(coordonnees) == 2:
            self.x = coordonnees[0]
            self.y = coordonnees[1]
        else:
            self.x = coordonnees[0][0]
            self.y = coordonnees[0][1]

    def value(self):
        return self.x, self.y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Animation:
    def __init__(self, fps=1, tempo_ms=50, image=None, largeur=None, hauteur=None):
        self.images = []
        if image:
            self.split_image(image, largeur, hauteur)
        self.fps = fps
        self.tempo_ms = tempo_ms
        self.t = 0
        self.ligne = 0
        self.colonne = 0

    def split_image(self, image: Image, largeur, hauteur):
        self.images = []
        for y in range(0, image.get_height(), hauteur):
            for x in range(0, image.get_width(), largeur):
                self.add_image_ligne(copy_image(image,(x,y,largeur,hauteur)), y // hauteur)

    def add_image_ligne(self, image, ligne=-1):
        if len(self.images) == ligne or ligne == -1:
            self.images.append([])
            self.images[len(self.images) - 1].append(image)
        elif 0 <= ligne < len(self.images):
            self.images[ligne].append(image)
        else:
            raise IndexError

    def image_courante(self, ligne=None, colonne=None):
        if ligne is not None and self.ligne != ligne:
            self.ligne = ligne
            self.colonne = 0
            self.t = 0
        if colonne is not None and self.colonne != colonne:
            self.colonne = colonne
            self.t = 0
        self.t += self.tempo_ms
        if self.t > self.fps * 1000:
            self.colonne += 1
            # print("colonne", self.colonne, "ligne", self.ligne)
            if self.colonne == len(self.images[self.ligne]):
                self.colonne = 0
            self.t = 0
        return self.images[self.ligne][self.colonne]

    def nb_ligne(self):
        return len(self.images)

    def __str__(self):
        return str(self.images)

    # def draw(self, qpainter, qrect):
    #     qpainter.drawImage(qrect, self._image_courante())


class Chemin:
    """
    Classe qui permet de créer un chemin sous forme de liste de points par lesquels
    les b2ds devront passer.
    """
    points = []

    def __init__(self, points, boucle=0):
        """Param       points      liste de tuples      liste de points sous la forme de
                                                     tuples comme par exemple
                                                     [(1,2),(5,7)] ou une liste de Bloc2D

                    boucle      int                  si boucle = 1 --> boucle on --> les
                                                     b2ds reviennent au premier
                                                     point après avoir terminés leurs
                                                     parcours sans passer par les autres
                                                     points
                                                     si boucle = 0 --> boucle off -->
                                                     les b2ds ne reviennent pas au
                                                     premier point après avoir terminés
                                                     leurs parcours.

        Prereq      boucle = 0 ou 1
                    points liste de tuples, valeurs >= 0
        """
        self.points = points
        self.index = 0
        self.boucle = boucle

    def __str__(self):
        """
        Créer une chaine de caractère contenant la liste de points du chemin par
        lesquels les b2ds devront passer, de la forme:
            "[(x, y), (x1, y1),...]"

        return: La chaine de caractère créée
        """
        return str(self.points) + "\nindex=" + str(self.index)

    def courant(self):
        return self.points[self.index]

    def suivant(self):
        if self.index < len(self.points) - 1:
            self.index += 1
        elif self.boucle == 1 and self.index == len(self.points) - 1:
            self.index = 0
        return self.points[self.index]

    def add(self, pos, point):
        """
        Méthode qui ajoute une liste de points à la position: pos.
        pos : index de l'insertion
        point: liste de points  exemple: [(1,2),(5,7)]"""
        if type(point) == tuple:
            point = [point]
        self.points = self.points[0:pos] + point + self.points[pos:]

    def delete(self, pos):
        self.points = self.points[0:pos] + self.points[pos + 1:]

    def boucle_on(self):
        self.boucle = 1

    def boucle_off(self):
        self.boucle = 0

    def pos_x(self):
        """renvoie l'abscisse du point courant si c'est un tuple et
        l'abscisse du centre si c'est un Bloc2D"""
        if isinstance(self.points[self.index], Bloc2D):
            return self.points[self.index].center().x
        return self.points[self.index][0]

    def pos_y(self):
        """renvoie l'ordonnée du point courant si c'est un tuple et
        l'ordonnée du centre si c'est un Bloc2D"""
        if isinstance(self.points[self.index], Bloc2D):
            return self.points[self.index].centery
        return self.points[self.index][1]

    def pos_xy(self):
        return Point(self.pos_x(), self.pos_y()).value()

    def dx(self):
        if isinstance(self.points[self.index], Bloc2D):
            return self.points[self.index].dx
        else:
            return 0

    def dy(self):
        if isinstance(self.points[self.index], Bloc2D):
            return self.points[self.index].dy
        else:
            return 0


def fill_image(taille: tuple | list, couleur) -> Image:
    """Créer une surface de dimension taille"""
    s: pygame.Surface = pygame.Surface(taille)
    s.fill(processing.rgb_color(couleur))
    return s


class Bloc2D(Rect):
    """Cette classe permet d'instancier un objet de type Bloc2D
    qui hérite de QRectF"""

    def __init__(self, image_or_bloc2d, x=0, y=0):
        if isinstance(image_or_bloc2d, Bloc2D):
            x = image_or_bloc2d.x
            y = image_or_bloc2d.y
            image = image_or_bloc2d.image
            super().__init__(x, y, image.get_width(), image.get_height())
            self.image = image
            self.animation = None
        elif type(image_or_bloc2d) != Animation:
            super().__init__(x, y, image_or_bloc2d.get_width(), image_or_bloc2d.get_height())
            self.image = image_or_bloc2d
            self.animation = None
        elif type(image_or_bloc2d) == Animation:
            super().__init__(x, y, image_or_bloc2d.images[0][0].get_width(), image_or_bloc2d.images[0][0].get_height())
            self.image = image_or_bloc2d.images[0][0]
            self.animation: Animation = image_or_bloc2d

        """
        Initialise le bloc (cheminImage : str ou image : QImage ou bloc : Bloc2D,x,y).

        param :     cheminImage     str     Le chemin de l'image dans le disque dur (ex : "/documents/image.png")
                    chemin          Array   Un tableau de tuples (x,y) qui sont les differents points par lesquels le Bloc2D
                                            passera. Exemple : [(1,2),(5,7)]
                    v               int     La vitesse du Bloc2D en px/s
                    dx,dy           float   déplacement en x et en y précedent
                    pv              int     point de vie courant
                    pvMax           int     point de vie max
                    force           int     Les dégats qu'il inflige
                    buttin          int     L'argent gagne lors du kill de ce Bloc2D
                    xp              int     L'xp que ce Bloc2D rapportera lors de sa mort
                    start           bool    permet le déplacement si True
                    visible         bool    rend le bloc invisible si False
                    slave           bool    rend le bloc asservi à un autre si true
                    tempo_ms        int     valeur du rafraichissement de l'ecran de jeu en ms
                    zone            Qrect   zone dans laquelle le bloc peut se déplacer
                    rebondi         bool    le bloc  peut rebondir contre un autre bloc si rebondi est True
                                            pour les deux blocs

        prereq : v, pv, force, buttin, xp >= 0

        """
        self.chemin: [Chemin | None] = None
        self.bloc2_ds: list[Bloc2D] = []
        self.dx = 0
        self.dy = 0
        self.master_dx = 0
        self.master_dy = 0
        self.angle = 0

        self.v = 0
        self.zone = None
        self.pv = 70
        self.pv_max = 0
        self.force = 0
        self.buttin = 0
        self.degats = 10
        self.xp = 0
        self.tempo_ms = 50
        self.jauge = None
        self.visible = True
        self.start = True
        self.rotate = False
        self.slave = False
        self.rebondi = False
        self.key_board_control = False
        self.keys_control = [K_RIGHT, K_LEFT, K_UP, K_DOWN, K_SPACE]
        self.vx = 3
        self.vy0 = 100
        self.vy = 0.1
        self.t0 = 0
        self.y0 = self.centery
        self.gravite = False
        self.gravite_stop = False
        self.gravity_value = 2
        self.debug = False
        self.__on_point = False

    def on_point(self,index)->bool:
        return self.__on_point and index == (self.chemin.index -1) % len(self.chemin.points)

    def init_vitalite(self, pv=None, pv_max=None, force=None, buttin=None, xp=None):
        if pv_max:
            self.set_pv_max(pv_max)
        if pv:
            self.set_pv(pv)
        if force:
            self.set_force(force)
        if buttin:
            self.set_buttin(buttin)
        if xp:
            self.set_xp(xp)

    def init_deplacement(self, vitesse=None, zone=None):
        if vitesse:
            self.set_vitesse(vitesse)
        if zone:
            self.set_zone(zone)

    def set_vitesse(self, valeur):
        self.v = valeur

    def set_zone(self, rect):
        self.zone = Rect(rect)

    def init_comportement(self, jauge=None, visible=None, start=None, rotate=None, slave=None, rebondi=None):
        if jauge:
            self.set_jauge(jauge)
        if visible is not None:
            self.set_visible(visible)
        if rotate is not None:
            self.set_rotate(rotate)
        if slave is not None:
            self.set_slave(slave)
        if rebondi is not None:
            self.set_rebondi(rebondi)

    def set_pv(self, valeur):
        """initialise la valeur des pv"""
        self.pv = max(0, min(self.pv_max, valeur))

    def set_pv_max(self, valeur):
        """initialise la valeur max des pv"""
        self.pv_max = max(0, valeur)

    def set_force(self, valeur):
        """initialise la valeur de la force"""
        self.force = max(0, valeur)

    def set_buttin(self, valeur):
        """initialise la valeur de la force"""
        self.buttin = max(0, valeur)

    def set_xp(self, valeur):
        """initialise la valeur de la force"""
        self.xp = max(0, valeur)

    def set_jauge(self, jauge):
        if isinstance(jauge, Jauge):
            self.jauge = jauge

    def set_visible(self, valeur):
        if type(valeur) == bool:
            self.visible = valeur

    def set_rotate(self, valeur):
        if type(valeur) == bool:
            self.rotate = valeur

    def set_slave(self, valeur):
        if type(valeur) == bool:
            self.slave = valeur
            if self.slave is False:
                self.chemin = None
        if type(valeur) == Bloc2D:
            self.chemin = Chemin([valeur])
            self.slave = True
            self.start = True

    def set_rebondi(self, valeur):
        if type(valeur) == bool:
            self.rebondi = valeur

    def set_mur(self, valeur):
        if type(valeur) == bool:
            self.mur = valeur

    def set_bloc2_d(self, blocs):
        self.bloc2_ds = []
        for b in blocs:
            if isinstance(b, Bloc2D):
                self.bloc2_ds.append(b)

    def go(self):
        self.start = True

    def stop(self):
        self.start = False

    def add_pv(self, valeur):
        """ajoute des pv par valeur ou par force de Bloc2D"""
        if isinstance(valeur, Bloc2D):
            valeur = valeur.force
        self.pv = max(0, min(self.pv_max, valeur + self.pv))

    def dec_pv(self, valeur):
        """decremente les pv par valeur ou par degats de Bloc2D"""
        if isinstance(valeur, Bloc2D):
            valeur = valeur.degats
        self.pv = max(0, min(self.pv_max, self.pv - valeur))
        if self.pv == 0:
            self.visible = False

    def draw(self):
        """
        La méthode draw permet...
        """
        self.start = True
        if self.visible:
            if self.animation:
                if self.animation.nb_ligne() == 4:
                    if self.dx != 0 or self.dy != 0:
                        if abs(self.dx) >= abs(self.dy):
                            if self.dx > 0:
                                self.image = self.animation.image_courante(2)
                                print("droite")
                            else:
                                self.image = self.animation.image_courante(1)
                                print("gauche")
                        else:
                            if self.dy > 0:
                                self.image = self.animation.image_courante(0)
                                print("bas")
                            else:
                                self.image = self.animation.image_courante(3)
                                print("haut")
                rect(self.x, self.y, self.width, self.height, image=self.image,no_fill=True, no_stroke=True)
            else:
                rect(self.x, self.y, self.width, self.height, image=self.image, no_fill=True, no_stroke=True)
            if self.jauge:
                # dessine la jauge de vie du bloc
                self.jauge.setPos(self.x, self.y - self.jauge.height - 1)
                self.jauge.setValeur(self.pv)
                self.jauge.draw()
            if self.debug:
                rect(self.zone.x, self.zone.y, self.zone.width, self.zone.height, no_fill=True)

    def surveille_collision(self):
        for b in self.bloc2_ds:
            # Pour tous les bloc2D d'un bloc
            if b != self and self.colliderect(b) and b.visible:
                # calcule les dégats
                ##                print("b force {} pv {} type {}".format(b.force,b.pv,type(b)))
                ##                print("self force {} pv {} type {}\n".format(self.force,self.pv,type(self)))
                if b.force < 9999 and self.force < 9999 and b.pv > 0 and self.pv > 0 and type(b) != type(self):
                    self.dec_pv(b)
                    b.dec_pv(self)
                rect = self.intersect(b)
                if rect.width > 1 and rect.height > 1:
                    # si bloc de meme force
                    if self.force == b.force:
                        b1 = self
                        b2 = b
                        if rect.width >= rect.height:
                            if b1.y == rect.y:
                                b1.top = b2.bottom - rect.height / 2
                                b2.bottom = b1.top
                            else:
                                b1.bottom = b2.top + rect.height / 2
                                b2.top = b1.bottom
                        else:
                            if b1.x == rect.x:
                                b1.left = b2.right - rect.width / 2
                                b2.right = b1.left
                            else:
                                b1.right = b2.left + rect.width / 2
                                b2.left = b1.right
                    else:
                        # bloc de force differente
                        if self.force < b.force:
                            b1 = self
                            b2 = b
                        elif self.force > b.force:
                            b2 = self
                            b1 = b
                        if rect.width >= rect.height:
                            # intersection par le dessus ou le dessous
                            self.t0 = 0
                            self.vy0 = 0
                            if b1.y == rect.y:
                                # intersection par le dessous
                                self.vy = 0.1
                                b1.top = b2.bottom
                                # print("par le dessous")
                            else:
                                # intersection par le dessus
                                b1.vy = 0
                                b1.bottom = b2.top + 1
                                if b2.force == 9999 and self.key_board_control:
                                    # le bloc b2 est une plateforme
                                    # On copie b2 dans b1.chemin et on rend b1 esclave de b2
                                    if b2.chemin is not None:
                                        b1.chemin = Chemin([b2])
                                    b1.slave = True
                                    b1.master_dx = b2.centerx - b1.centerx
                                    b1.master_dy = b2.centery - b1.centery
                                    self.vy = 0
                                    # print("par le dessus",b2.force,"esclave")
                                    # ***************************
                            self.y0 = b1.centery
                        else:
                            # intersection par les cotes
                            if b1.x == rect.x:
                                # par le cote droit
                                b1.left = b2.right
                            else:
                                # par le cote gauche
                                b1.right = b2.left


            if self.chemin and b == self.chemin.courant():
                # si le bloc test est le maitre de self
                if self.right < b.left or self.left > b.right:
                    # si self n'est plus sur son maitre alors on rend sa liberté à self
                    self.slave = False
                    self.chemin = None
                    self.t0 = 0
                    self.vy0 = 0
                    self.vy = 0.1
                    self.y0 = self.centery

                    ##                    print("liberé")

    def intersection(self, b: "Bloc2D"):
        rect = None
        if self.contains(b):
            rect = b
        elif self.collidepoint(b.x, b.y):
            if self.collidepoint(b.right, b.y):
                rect = Rect(b.x, b.y, b.width, abs(self.bottom - b.y))
            elif self.collidepoint(b.x, b.bottom):
                rect = Rect(b.x, b.y, abs(self.right - b.x), b.height)
            else:
                rect = Rect(b.x, b.y, abs(self.right - b.x), abs(self.bottom - b.y))
        elif self.collidepoint(b.x, b.bottom):
            if self.collidepoint(b.right, b.bottom):
                rect = Rect(b.x, self.y, b.width, abs(self.y - b.bottom))
            else:
                rect = Rect(b.x, self.y, abs(self.right - b.x), abs(b.bottom - self.y))
        elif self.collidepoint(b.right, b.y):
            if self.collidepoint(b.right, b.bottom):
                rect = Rect(self.x, b.y, abs(b.right - self.x), b.height)
            else:
                rect = Rect(self.x, b.y, abs(b.right - self.x), abs(self.bottom - b.y))
        return rect

    def intersect(self, b: "Bloc2D"):
        rect = self.intersection(b)
        if rect is None:
            return b.intersection(self)
        return rect

    def moving(self):
        """
            La méthode move permet mettre le Bloc2D en mouvement avec une vitesse,
            et une liste de points donnés.
        """
        if self.start:
            if self.chemin != None and not self.key_board_control:
                if not self.slave:
                    x = self.chemin.pos_x()
                    y = self.chemin.pos_y()
                    dx = x - self.centerx
                    dy = y - self.centery
                    if (abs(dx) < 2 and abs(dy) < 2):
                        self.__on_point = True
                        self.chemin.suivant()
                    else:
                        self.__on_point = False
                    alpha = atan2(dy, dx)
                    self.angle = alpha * 180 / math.pi + 90
                    vx = self.v * cos(alpha)
                    vy = self.v * sin(alpha)
                    t = self.tempo_ms / 1000
                    self.dx += vx * t
                    self.dy += vy * t
                else:
                    self.dx = self.chemin.dx()
                    self.dy = self.chemin.dy()
                if abs(self.dx) >= 1 or abs(self.dy) >= 1:
                    self.move_ip(self.dx, self.dy)
                    if abs(self.dx) >= 1:
                        self.dx = 0
                    if abs(self.dy) >= 1:
                        self.dy = 0

            elif self.key_board_control:
                t = self.tempo_ms / 150
                if self.slave and self.chemin is not None:
                    x = self.chemin.courant().centerx - self.master_dx
                    self.bottom = self.chemin.courant().top + 1
                else:
                    x = self.centerx
                y = self.centery
                # print(y,self.vy,self.vy0,touche,self.slave)
                self.dx = 0
                self.dy = 0
                if keyIsPressed():
                    if keyIsDown(self.keys_control[2]) and (self.vy == 0 or self.slave or not self.gravite):
                        # haut
                        self.slave = False
                        self.chemin = None
                        self.dy = -self.vx * t
                        y += self.dy
                    if keyIsDown(self.keys_control[4]):
                        if self.gravite and self.vy == 0:
                            self.slave = False
                            self.chemin = None
                            self.vy = -1.5 * self.v
                            self.vy0 = 1.5 * self.v
                            self.t0 = 0
                            self.y0 = self.y

                    if keyIsDown(self.keys_control[0]):
                        # droite
                        self.dx = self.vx * t
                        x += self.dx
                        self.master_dx -= self.vx * t
                        # self.image=self.droite
                    if keyIsDown(self.keys_control[1]):
                        # gauche
                        # self.image=self.gauche
                        x -= self.vx * t
                        self.dx = -self.vx * t
                        self.master_dx += self.vx * t
                        # print("esclave")
                    if keyIsDown(self.keys_control[3]):
                        # bas
                        if not self.gravite:
                            self.dy = self.vx * t
                            y += self.dy
                            self.master_dy -= self.vx * t

                    # print("************", y, self.vy0, self.slave)
                if self.gravite and not self.slave:
                    self.dy = y
                    y = (self.gravity_value * (t + self.t0) ** 2) / 2 - self.vy0 * (t + self.t0) + self.y0
                    self.dy += y
                    self.t0 += t
                    # print("to {}".format(self.t0))
                self.center = x, y
            self.surveille_collision()
            if self.zone:
                if self.x < self.zone.x:
                    self.left = self.zone.x
                elif self.right > self.zone.right:
                    self.right = self.zone.right
                if self.bottom > self.zone.bottom:
                    self.bottom = self.zone.bottom
                    if self.key_board_control:
                        self.vy = 0
                        self.t0 = 0
                        self.vy0 = 0
                        self.y0 = self.centery+1
                elif self.top < self.zone.top:
                    self.top = self.zone.top
                    if self.key_board_control:
                        self.vy = 0.1
                        self.t0 = 0
                        self.vy0 = 0
                        self.y0 = self.centery
        if debug:
            print(self.center)

    def setChemin(self, chemin):
        self.chemin = chemin
        self.center = self.chemin.pos_xy()

    def distance(self, b2d):
        return math.sqrt((self.x - b2d.x) ** 2 + (self.y - b2d.y) ** 2)

    def copie(self, b2d):
        """
        La méthode copie permet de copier les caractéristique d'un autre Bloc2D et donc d'en créer un nouveau identique au premier.

        Param:          bloc2_d     Objet     Objet Bloc2D à copier.
        """
        self.x = b2d.x
        self.y = b2d.y
        self.image = b2d.image_puzzle
        self.width = b2d.width
        self.height = b2d.height
        self.image = b2d.image_puzzle
        self.chemin = b2d.chemin
        self.v = b2d.v
        self.pv = b2d.pv
        self.force = b2d.force
        self.buttin = b2d.buttin
        self.xp = b2d.xp

    def seReproduire(self):
        """
        La méthode permet de copier les caractéristique d'un autre bloc2_d et donc d'en créer un nouveau identique au premier.

        return:      Caractéristiques du nouveau bloc2_d identique au premier.
        """
        m = Bloc2D(self.image, self.chemin, self.v, self.pv, self.force, self.buttin, self.xp)
        return m

    def __str__(self):
        """
        La méthode __str__ cree une chaine de caracteres decrivant les caracteristiques du bloc2_d, de la forme :
          "image :
           position x :
           position y :
           vitesse v :
           pv :
           force :
           butin :
           xp:     "

        return : La chaine de caracteres creee
        """
        return "image : {}\n : {}\nchemin : {}\nvitesse v : {}\npv : {}\nforce : {}\nbuttin : {}\nxp : {}".format(
            self.image, super().__str__(), self.chemin, self.v, self.pv, self.force, self.buttin, self.xp)


if __name__ == '__main__':
    from likeprocessing.processing import *

    j = Jauge(100, 10, 100)
    j.setValeur(0)
    t = Tempo(500)
    r = Bloc2D(loadImage("fantomme_jaune.png"), 100, 100)
    b = Bloc2D(loadImage("fantomme_jaune.png"), 200, 100)
    r.key_board_control = False
    b.key_board_control = True
    r.init_deplacement(10, (10, 10, 380, 280))
    b.init_deplacement(10, (10, 10, 380, 280))
    r.init_comportement(Jauge(30, 3, 100))
    r.setChemin(Chemin([(25, 25), (100, 100), (100, 200)], 1))


    def setup():
        createCanvas(400, 300)
        background("grey")


    def compute():
        if t.fin():
            j.incremente(10)


    def compute():
        b.moving()
        r.moving()


    def draw():
        r.draw()
        j.draw()


    run(globals())
