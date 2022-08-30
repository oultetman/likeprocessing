import math

import likeprocessing.processing as processing
import likeprocessing.trigo as trigo
import pygame


def rectMode(corners_center: str):
    """change center mode 'CORNERS' or 'CENTER' """
    if corners_center.upper() == "CORNERS":
        processing.__rect_center_mode = False
    elif corners_center.upper() == "CENTER":
        processing.__rect_center_mode = True


def rect1(x: int, y: int, largeur: int, hauteur: int, **kwarsg):
    """Créer un rectangle aux coordonnées x,y de largeur largeur et de hauteur.
    Si rectMode('center') x et y sont les coordonnées du centre du rectangle.
    Si rectMode('corners') x,y sont les coordonnées du coin haut gauche.
    Le rectangle est rempli par la couleur définie par fill(couleur).
    Si le paramètre image est renseigné le fond du rectangle sera occupé pas l'image retaillée
    aux dimensions du rectangle sauf si largeur et/ou hauteur sont nulles (ou non renseignées).
    largeur et/ou hauteur seront alors celle de l'image. Les paramètres allign_h (left, center et right) et
    allign_v (top,center et bottom) permettent d'aligner l'image dans un cadre plus grand qu'elle.
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


def rect(x: int, y: int, largeur: int = 0, hauteur: int = 0, **kwarsg):
    """Créer un rectangle aux coordonnées x,y de largeur largeur et de hauteur.
    Si rectMode('center') x et y sont les coordonnées du centre du rectangle.
    Si rectMode('corners') x,y sont les coordonnées du coin haut gauche.
    Le rectangle est rempli par la couleur définie par fill(couleur).
    Si le paramètre image est renseigné le fond du rectangle sera occupé pas l'image retaillée
    aux dimensions du rectangle sauf si largeur et/ou hauteur sont nulles (ou non renseignées).
    largeur et/ou hauteur seront alors celle de l'image. Les paramètres allign_h (left, center et right) et
    allign_v (top,center et bottom) permettent d'aligner l'image dans un cadre plus grand qu'elle.
     """

    image: pygame.surface = kwarsg.get("image", None)
    allign_h = kwarsg.get("allign_h", "left")
    allign_v = kwarsg.get("allign_v", "top")
    if image is not None:
        if hauteur == 0:
            hauteur = image.get_height()
        if largeur == 0:
            largeur = image.get_width()
    if processing.__rect_center_mode:
        x -= largeur / 2
        y -= hauteur / 2
    points = [[x + processing.__dx, y + processing.__dy],
              [x + processing.__dx + largeur, y + processing.__dy],
              [x + processing.__dx + largeur, y + processing.__dy + hauteur],
              [x + processing.__dx, y + processing.__dy + hauteur]]
    points = processing.rotation(points)
    if image is None:
        if processing.__no_fill is False:
            pygame.draw.polygon(processing.screen, processing.__fill_color, points)
    else:
        dx = 0  # left
        dy = 0  # top
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
        r = processing.get_rotation() * 180 / math.pi
        img = pygame.transform.rotate(image, r)
        x += image.get_width()/2
        y += image.get_height()/2
        x, y = processing.rotation([[x + dx + processing.__dx, y + dy + processing.__dy]])[0]
        processing.screen.blit(img,
                               (x-img.get_width()/2, y-img.get_height()/2),
                               (0, 0, img.get_width(), img.get_height()))
    if processing.__border_width > 0:
        pygame.draw.polygon(processing.screen, processing.__border_color,
                            points, width=processing.__border_width)


def square(x: int, y: int, largeur: int):
    # pygame.draw.rect(processing.screen, processing.__fill_color,
    #                  (x + processing.__dx, y + processing.__dy, largeur, largeur), processing.__border_width)
    processing.rect(x, y, largeur, largeur)


def point(x: int, y: int):
    """Trace un point de coordonnées(x, y). carré de 2x2 pixel"""
    square(x, y, 2)


def line(x1: int, y1: int, x2: int, y2: int):
    """Trace un segment reliant les deux points de coordonnées (x1, y1) et (x2, y2)."""
    points = [(x1 + processing.__dx, y1 + processing.__dy), (x2 + processing.__dx, y2 + processing.__dy)]
    points = processing.rotation(points)
    pygame.draw.line(processing.screen, processing.__border_color,*points, processing.__border_width)


def ellipseMode(corners_center: str):
    """change center mode 'CORNERS' or 'CENTER' """
    if corners_center.upper() == "CORNERS":
        processing.__ellipse_center_mode = False
    elif corners_center.upper() == "CENTER":
        processing.__ellipse_center_mode = True


def ellipse(x: int, y: int, largeur: int, hauteur: int):
    """Trace une ellipse dont le centre a pour coordonnées (x, y) et dont la largeur
    et la hauteur prennent les valeurs fixées."""

    if processing.__ellipse_center_mode:
        x -= largeur / 2
        y -= hauteur / 2
    if processing.__no_fill == False:
        pygame.draw.ellipse(processing.screen, processing.__fill_color,
                            (x + processing.__dx, y + processing.__dy, largeur, hauteur),
                            0)
    if processing.__border_width > 0:
        pygame.draw.ellipse(processing.screen, processing.__border_color,
                            (x + processing.__dx, y + processing.__dy, largeur, hauteur),
                            processing.__border_width)


def circle(x: int, y: int, diametre: int):
    """Trace un cercle dont le centre a pour coordonnées (x, y) et dont le diamètre prend la valeur fixée.
    Idem ellipse((x, y, diametre, diametre)"""
    ellipse(x, y, diametre, diametre)


def triangle(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
    """Trace un triangle dont les trois sommets ont pour coordonnées (x1, y1), (x2, y2), et (x3, y3)."""
    points = [(x1 + processing.__dx, y1 + processing.__dy), (x2 + processing.__dx, y2 + processing.__dy)
                                , (x3 + processing.__dx, y3 + processing.__dy)]
    points = processing.rotation(points)
    if processing.__no_fill is True:
        pygame.draw.polygon(processing.screen, processing.__border_color,points
                            , width=processing.__border_width)
    else:
        pygame.draw.polygon(processing.screen, processing.__fill_color,
                            points)
        if processing.__border_width != 0:
            pygame.draw.polygon(processing.screen, processing.__border_color,
                                points, width=processing.__border_width)


def quad(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int):
    """Trace un quadrilatère dont les quatre sommets ont pour coordonnées (x1, y1), (x2, y2), (x3, y3) et (x4, y4)."""
    points = [(x1 + processing.__dx, y1 + processing.__dy), (x2 + processing.__dx, y2 + processing.__dy)
                                , (x3 + processing.__dx, y3 + processing.__dy),
                             (x4 + processing.__dx, y4 + processing.__dy)]
    points = processing.rotation(points)
    if processing.__no_fill is True:
        pygame.draw.polygon(processing.screen, processing.__border_color,
                            points, width=processing.__border_width)
    else:
        pygame.draw.polygon(processing.screen, processing.__fill_color,
                            points)
        if processing.__border_width != 0:
            pygame.draw.polygon(processing.screen, processing.__border_color,
                                points, width=processing.__border_width)


def not_filled_polygone(points: list) -> None:
    points.append(points[0])
    for i in range(len(points) - 1):
        line(points[i][0] + processing.__dx, points[i][1] + processing.__dy, points[i + 1][0] + processing.__dx,
             points[i + 1][1] + processing.__dy)


def k_line(points: list) -> None:
    """trace un ligne brisée à partir d'une liste de points
    [[1,2],[5,6],[8,3],.....]
    nb_point = nb_segments + 1"""
    for i in range(len(points) - 1):
        line(points[i][0] + processing.__dx, points[i][1] + processing.__dy, points[i + 1][0] + processing.__dx,
             points[i + 1][1] + processing.__dy)


def sector(x: int, y: int, rayon: int, angleDebut: float, angleFin: float):
    angleDebut *= trigo.angleMode()
    angleFin *= trigo.angleMode()
    points = [(x + processing.__dx, y + processing.__dy)]
    if angleDebut > angleFin:
        angleFin += 2 * math.pi
    angle = angleDebut
    while angle < angleFin - 0.01:
        points.append((rayon * math.cos(angle) + processing.__dx + x,
                       -rayon * math.sin(angle) + processing.__dy + y))
        angle += 0.01
    points.append((rayon * math.cos(angleFin) + processing.__dx + x,
                   -rayon * math.sin(angleFin) + processing.__dy + y))
    if processing.__no_fill is True:
        k_line(points)
    else:
        pygame.draw.polygon(processing.screen, processing.__fill_color, points)
        if processing.__border_width > 0:
            pygame.draw.polygon(processing.screen, processing.__border_color, points, width=processing.__border_width)


def arc(x: int, y: int, largeur: int, hauteur: int, angleDebut: float, angleFin: float):
    """Créer une portion d'ellipse type part de tarte qui pourra être rempli entre les points repérés par
    les angles angleDébut et angleFin (en radians). x et y sont les coordonnées du centre du cercle."""
    if not processing.__ellipse_center_mode:
        x += largeur / 2
        y += hauteur / 2
    angleDebut *= trigo.angleMode()
    angleFin *= trigo.angleMode()
    points = [(x + processing.__dx, y + processing.__dy)]
    if angleDebut > angleFin:
        angleFin += 2 * math.pi
    angle = angleDebut
    while angle < angleFin - 0.1:
        points.append((largeur * math.cos(angle) / 2 + processing.__dx + x,
                       -hauteur * math.sin(angle) / 2 + processing.__dy + y))
        angle += 0.1
    points.append((largeur * math.cos(angleFin) / 2 + processing.__dx + x,
                   -hauteur * math.sin(angleFin) / 2 + processing.__dy + y))
    if processing.__no_fill is True:
        k_line(points)
    else:
        pygame.draw.polygon(processing.screen, processing.__fill_color, points)
        if processing.__border_width > 0:
            pygame.draw.polygon(processing.screen, processing.__border_color, points, width=processing.__border_width)


def circle_arc(x: int, y: int, rayon: int, angleDebut: float, angleFin: float):
    """idem arc mais à partir d'un disque"""
    arc(x, y, rayon, rayon, angleDebut, angleFin)


def dist(x1, y1, x2, y2):
    """retourne la distance entre deux points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

