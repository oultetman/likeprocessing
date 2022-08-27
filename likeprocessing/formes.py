import math

import likeprocessing.processing as processing
import pygame


def rectMode(corners_center: str):
    """change center mode 'CORNERS' or 'CENTER' """
    if corners_center.upper() == "CORNERS":
        processing.__rect_center_mode = False
    elif corners_center.upper() == "CENTER":
        processing.__rect_center_mode = True


def rect(x: int, y: int, largeur: int, hauteur: int, **kwarsg):
    """crée un rectangle aux coordonneés x,y de largeur largeur et de hauteur
     hauteur si rectMode('center') x et y sont les coordonnées du centre du rectangle
     si rectMode('corners') x,y sont les coordonnées du coin haut gauche
     le rectangle est rempli pas la couleur definie par fill(couleur)
     si le paramètre image est renseigné le fond sur rectangle sera occupé pas l'image retaillée
     aux dimensions du rectangle sauf si largeur et/ou hauteur sont nulles largeur et/ou hauteur
     seront celle de l'image. L'image sera
     """

    if processing.__rect_center_mode:
        x -= largeur / 2
        y -= hauteur / 2
    image = kwarsg.get("image", None)
    allign_h = kwarsg.get("allign_h", "left")
    allign_v = kwarsg.get("allign_v", "top")
    if image is None:
        if processing.__no_fill is False:
            pygame.draw.rect(processing.screen, processing.__fill_color,
                             (x + processing.__dx, y + processing.__dy, largeur, hauteur), 0)
    else:
        dx = 0  # left
        dy = 0  # top
        if hauteur == 0:
            hauteur = image.get_height()
        if largeur == 0:
            largeur = image.get_width()
        if allign_h == "left":
            dx = 0
        elif allign_h == "right":
            dx = max(0, largeur - image.get_width())
        elif allign_h == "center":
            dx = max(0, (largeur - image.get_width()) // 2)
        if allign_v == "center":
            dy = max(0, (hauteur - image.get_height()) // 2)
        elif allign_v == "bottom":
            dy = max(0, hauteur - image.get_height())
        processing.screen.blit(image,
                               (x + dx, y + dy),
                               (0, 0, largeur, hauteur))
    if processing.__border_width > 0:
        pygame.draw.rect(processing.screen, processing.__border_color,
                         (x + processing.__dx, y + processing.__dy, largeur, hauteur), processing.__border_width)


def square(x: int, y: int, largeur: int):
    # pygame.draw.rect(processing.screen, processing.__fill_color,
    #                  (x + processing.__dx, y + processing.__dy, largeur, largeur), processing.__border_width)
    processing.rect(x, y, largeur, largeur)


def point(x: int, y: int):
    square(x, y, 2)


def line(x1: int, y1: int, x2: int, y2: int):
    pygame.draw.line(processing.screen, processing.__border_color, (x1 + processing.__dx, y1 + processing.__dy),
                     (x2 + processing.__dx, y2 + processing.__dy), processing.__border_width)


def ellipseMode(corners_center: str):
    """change center mode 'CORNERS' or 'CENTER' """
    if corners_center.upper() == "CORNERS":
        processing.__rect_center_mode = False
    elif corners_center.upper() == "CENTER":
        processing.__rect_center_mode = True


def ellipse(x: int, y: int, largeur: int, hauteur: int):
    if processing.__ellipse_center_mode:
        x -= largeur / 2
        y -= hauteur / 2
    if processing.__no_fill == False:
        pygame.draw.ellipse(processing.screen, processing.__fill_color,
                            (x - largeur // 2 + processing.__dx, y - hauteur // 2 + processing.__dy, largeur, hauteur),
                            0)
    if processing.__border_width > 0:
        pygame.draw.ellipse(processing.screen, processing.__border_color,
                            (x - largeur // 2 + processing.__dx, y - hauteur // 2 + processing.__dy, largeur, hauteur),
                            processing.__border_width)


def arc(x: int, y: int, largeur: int, hauteur: int, angleDebut: float, angleFin: float):
    pygame.draw.arc(processing.screen, processing.__fill_color,
                    (x - largeur // 2 + processing.__dx, y - hauteur // 2 + processing.__dy, largeur, hauteur),
                    angleDebut, angleFin,
                    processing.__border_width)


def circle(x: int, y: int, diametre: int):
    ellipse(x, y, diametre, diametre)


def triangle(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
    if processing.__no_fill is True:
        line(x1 + processing.__dx, y1 + processing.__dy, x2 + processing.__dx, y2 + processing.__dy)
        line(x2 + processing.__dx, y2 + processing.__dy, x3 + processing.__dx, y3 + processing.__dy)
        line(x3 + processing.__dx, y3 + processing.__dy, x1 + processing.__dx, y1 + processing.__dy)
    else:
        pygame.draw.polygon(processing.screen, processing.__fill_color,
                            [(x1 + processing.__dx, y1 + processing.__dy), (x2 + processing.__dx, y2 + processing.__dy)
                                , (x3 + processing.__dx, y3 + processing.__dy)], width=processing.__border_width)


def quad(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int):
    if processing.__no_fill is True:
        line(x1 + processing.__dx, y1 + processing.__dy, x2 + processing.__dx, y2 + processing.__dy)
        line(x2 + processing.__dx, y2 + processing.__dy, x3 + processing.__dx, y3 + processing.__dy)
        line(x3 + processing.__dx, y3 + processing.__dy, x4 + processing.__dx, y4 + processing.__dy)
        line(x1 + processing.__dx, y1 + processing.__dy, x4 + processing.__dx, y4 + processing.__dy)
    else:
        pygame.draw.polygon(processing.screen, processing.__fill_color,
                            [(x1 + processing.__dx, y1 + processing.__dy), (x2 + processing.__dx, y2 + processing.__dy)
                                , (x3 + processing.__dx, y3 + processing.__dy),
                             (x4 + processing.__dx, y4 + processing.__dy)])


def arc1(x: int, y: int, rayon: int, angleDebut: int, angleFin: int):
    points = [(x + processing.__dx, y + processing.__dy)]
    if angleDebut>angleFin:
        angleFin+=360
    for angle in range(angleDebut, angleFin):
        points.append((rayon * math.cos(angle * processing.PI / 180) + processing.__dx + x,
                       -rayon * math.sin(angle * processing.PI / 180) + processing.__dy + y))
    pygame.draw.polygon(processing.screen, processing.__fill_color, points)
    if processing.__border_width > 0:
        pygame.draw.polygon(processing.screen, processing.__border_color, points, width=processing.__border_width)


def dist(x1, y1, x2, y2):
    """retourne la distance entre deux points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
