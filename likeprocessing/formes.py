import math

import likeprocessing.processing as processing
import likeprocessing.trigo as trigo
import pygame


def in_polygone(x, y, points: list) -> bool:
    """retourne True si le point (x,y) est dans le polygone"""
    segment = []
    for i in range(0, len(points) - 1):
        if (points[i][0] >= x or points[i + 1][0] >= x) and (
                points[i][1] < y < points[i + 1][1] or points[i][1] > y > points[i + 1][1]):
            segment.append((points[i], points[i + 1]))
    if (points[0][0] >= x or points[-1][0] >= x) and (
            points[0][1] < y < points[-1][1] or points[0][1] > y > points[-1][1]):
        segment.append((points[0], points[-1]))
    if len(segment) % 2 == 1:
        return True
    else:
        nb = 0
        for s in segment:
            if (s[1][0] - s[0][0]) != 0:
                a = (s[1][1] - s[0][1]) / (s[1][0] - s[0][0])
                b = s[1][1] - a * s[1][0]
                if (y - b) / a >= x:
                    nb += 1
            else:
                nb += 1
        return nb % 2 == 1


def in_line(x, y, x1, y1, x2, y2) -> bool:
    points = [(x1 - 1, y1 - 1), (x1 + 1, y1 + 1), (x2 + 1, y2 + 1), (x2 - 1, y2 - 1)]
    return in_polygone(x, y, points)


def in_ellipse(x, y, xe, ye, largeur, hauteur) -> bool:
    """retourne True si le point (x,y) est dans l'ellipse"""
    angle = math.atan2(y - ye, x - xe)
    r = math.sqrt((largeur * math.cos(angle) / 2) ** 2 + (hauteur * math.sin(angle) / 2) ** 2)
    return dist(x, y, xe, ye) < r * 0.95


def in_circle(x, y, xc, yc, diametre) -> bool:
    """retourne True si le point (x,y) est dans le cercle"""
    return dist(x, y, xc, yc) < diametre / 2


def rectMode(corners_center: str = "") -> str:
    """change center mode 'CORNERS' or 'CENTER' and return rectMode mode"""
    if corners_center.upper() == "CORNERS":
        processing.set_rect_center_mode(False)
    elif corners_center.upper() == "CENTER":
        processing.set_rect_center_mode(True)
    else:
        if processing.get_rect_center_mode():
            return "center"
        else:
            return "corners"
    return corners_center


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
    points = [[x, y],
              [x + largeur, y],
              [x + largeur, y + hauteur],
              [x, y + hauteur]]

    # if image is None:
    polygone(points)
    if image is not None:

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
        r = processing.get_rotation_rad() * 180 / math.pi
        img = pygame.transform.rotate(image, r)
        x += image.get_width() / 2
        y += image.get_height() / 2
        h, v = False, False
        if processing.__flip_axe_v is not None:
            v = True
        if processing.__flip_axe_h is not None:
            h = True
        img = pygame.transform.flip(img, v, h)
        x, y = processing.transformation([[x + dx + processing.__dx, y + dy + processing.__dy]])[0]
        processing.screen.blit(img,
                               (x - img.get_width() / 2, y - img.get_height() / 2),
                               (0, 0, img.get_width(), img.get_height()))
        if processing.__border_width > 0:
            processing.not_filled_polygone(points)


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
    points = processing.transformation(points)
    if processing.__fill_color_mouse_on is not None and in_line(*processing.mouseXY(), x1, y1, x2, y2):
        pygame.draw.line(processing.screen, processing.__fill_color_mouse_on, *points, processing.__border_width)
    else:
        pygame.draw.line(processing.screen, processing.__border_color, *points, processing.__border_width)


def ellipseMode(corners_center: str = ""):
    """change center mode 'CORNERS' or 'CENTER' """
    if corners_center.upper() == "CORNERS":
        processing.__ellipse_center_mode = False
    elif corners_center.upper() == "CENTER":
        processing.__ellipse_center_mode = True
    else:
        if processing.get_ellipse_center_mode():
            return "center"
        else:
            return "corners"
    return corners_center


def get_ellipse_center_mode() -> str:
    """retourne ellipse_center_mode"""
    return processing.__ellipse_center_mode


def ellipse(x: int, y: int, largeur: int, hauteur: int):
    """Trace une ellipse dont le centre a pour coordonnées (x, y) et dont la largeur
    et la hauteur prennent les valeurs fixées."""
    if processing.get_rotation_rad() == 0 and processing.__flip_axe_h is None and processing.__flip_axe_v is None:
        if processing.__ellipse_center_mode:
            x -= largeur / 2
            y -= hauteur / 2
        if processing.__no_fill == False:
            if processing.__fill_color_mouse_on is not None and in_ellipse(*processing.mouseXY(), x + largeur / 2,
                                                                           y + hauteur / 2, largeur, hauteur):
                pygame.draw.ellipse(processing.screen, processing.__fill_color_mouse_on,
                                    (x + processing.__dx, y + processing.__dy, largeur, hauteur),
                                    0)
            else:
                pygame.draw.ellipse(processing.screen, processing.__fill_color,
                                    (x + processing.__dx, y + processing.__dy, largeur, hauteur),
                                    0)

        if processing.__border_width > 0:
            pygame.draw.ellipse(processing.screen, processing.__border_color,
                                (x + processing.__dx, y + processing.__dy, largeur, hauteur),
                                processing.__border_width)
    else:
        arc(x, y, largeur, hauteur, pie=False)


def circle(x: int, y: int, diametre: int):
    """Trace un cercle dont le centre a pour coordonnées (x, y) et dont le diamètre prend la valeur fixée.
    Idem ellipse((x, y, diametre, diametre)"""

    points = [(x,y)]
    points = processing.transformation(points)
    x, y = points[0]
    if processing.__flip_axe_h is not None :
        y-=diametre
    if processing.__flip_axe_v is not None :
        x-=diametre
    if processing.__ellipse_center_mode:
        x -= diametre / 2
        y -= diametre / 2
    if processing.__no_fill is False:
        if processing.__fill_color_mouse_on is not None and in_circle(*processing.mouseXY(), x + diametre / 2,
                                                                      y + diametre / 2, diametre):
            pygame.draw.ellipse(processing.screen, processing.__fill_color_mouse_on,
                                (x, y, diametre, diametre),
                                0)
        else:
            pygame.draw.ellipse(processing.screen, processing.__fill_color,
                                (x, y, diametre, diametre),
                                0)
    if processing.__border_width > 0:
        pygame.draw.ellipse(processing.screen, processing.__border_color,
                            (x, y, diametre, diametre),
                            processing.__border_width)


def triangle(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
    """Trace un triangle dont les trois sommets ont pour coordonnées (x1, y1), (x2, y2), et (x3, y3)."""
    points = [(x1, y1), (x2, y2), (x3, y3)]
    polygone(points)


def quad(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int):
    """Trace un quadrilatère dont les quatre sommets ont pour coordonnées (x1, y1), (x2, y2), (x3, y3) et (x4, y4)."""
    points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    polygone(points)


def polygone(points: list):
    """Trace un polygone à partie d'une liste de points"""
    points = processing.transformation(points)
    if processing.__no_fill is True:
        pygame.draw.polygon(processing.screen, processing.__border_color,
                            points, width=processing.__border_width)
    else:
        if processing.__fill_color_mouse_on is None:
            pygame.draw.polygon(processing.screen, processing.__fill_color,
                                points)
        else:
            if processing.in_polygone(*processing.mouseXY(), points):
                pygame.draw.polygon(processing.screen, processing.__fill_color_mouse_on,
                                    points)
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


def arc(x: int, y: int, largeur: int, hauteur: int, angleDebut: float = None, angleFin: float = None, **kwargs):
    """Créer une portion d'ellipse type part de tarte qui pourra être rempli entre les points repérés par
    les angles angleDébut et angleFin. x et y sont les coordonnées du centre du cercle."""
    pie = kwargs.get("pie", True)
    # recalcule de x et y si x,y centre de l'ellipse
    if not processing.__ellipse_center_mode:
        x += largeur / 2
        y += hauteur / 2

    # conversion des angle en radians
    if angleDebut is None:
        angleDebut = 0
        angleFin = 2 * processing.PI
    else:
        angleDebut = processing.radians(angleDebut)
        angleFin = processing.radians(angleFin)
    points = []

    # calcul des points de l'arc
    if pie:
        points = [(x, y)]
    if angleDebut > angleFin:
        angleFin += 2 * math.pi
    angle = angleDebut
    while angle < angleFin - 0.1:
        points.append((largeur * math.cos(angle) / 2 + x,
                       -hauteur * math.sin(angle) / 2 + y))
        angle += 0.1
    points.append((largeur * math.cos(angleFin) / 2 + x,
                   -hauteur * math.sin(angleFin) / 2 + y))
    polygone(points)


def circle_arc(x: int, y: int, diametre: int, angleDebut: float, angleFin: float, **kwargs):
    """idem arc mais à partir d'un disque"""
    arc(x, y, diametre, diametre, angleDebut, angleFin, **kwargs)


def arc_points(x: int, y: int, largeur: int, hauteur: int, angleDebut: float, angleFin: float, sens_trigo=True) -> list:
    """retourne une liste des points du contour de l'ellipse entre les points repérés par
    les angles angleDébut et angleFin (en radians). x et y sont les coordonnées du centre du cercle."""
    # recalcule de x et y si x,y centre de l'ellipse
    if not processing.__ellipse_center_mode:
        x += largeur / 2
        y += hauteur / 2

    # conversion des angle en radians
    angleDebut *= trigo.angleMode()
    angleFin *= trigo.angleMode()
    points = []

    # calcul des points de l'arc
    pas = 0.1
    if angleDebut > angleFin and sens_trigo:
        angleFin += 2 * processing.PI
    if not sens_trigo:
        pas = -pas
    angle = angleDebut
    if pas > 0:
        while angle < angleFin - pas:
            points.append((largeur * math.cos(angle) / 2 + processing.__dx + x,
                           -hauteur * math.sin(angle) / 2 + processing.__dy + y))
            angle += pas
    else:
        while angle > angleFin - pas:
            points.append((largeur * math.cos(angle) / 2 + processing.__dx + x,
                           -hauteur * math.sin(angle) / 2 + processing.__dy + y))
            angle += pas
    points.append((largeur * math.cos(angleFin) / 2 + processing.__dx + x,
                   -hauteur * math.sin(angleFin) / 2 + processing.__dy + y))
    return points


def dist(x1, y1, x2, y2):
    """retourne la distance entre deux points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
