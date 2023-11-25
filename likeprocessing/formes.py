import math

import likeprocessing.processing as processing
import likeprocessing.trigo as trigo
import pygame


def in_polygone(x, y, points:list):
    """
    Vérifie si un point donné se trouve à l'intérieur d'un polygone donné.

    Args:
        point (tuple): Les coordonnées du point à tester sous la forme (x, y).
        points (list): Une liste de tuples contenant les coordonnées des sommets du polygone.

    Returns:
        bool: True si le point se trouve à l'intérieur du polygone, False sinon.
    """

    n = len(points)
    inside = False
    x, y = x - processing.x0, y - processing.y0
    p1x, p1y = points[0]
    for i in range(1, n+1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intersect = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_intersect:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def in_line(x, y, x1, y1, x2, y2) -> bool:
    """retourne True si la souris est sur le trait"""
    x, y = x - processing.x0, y - processing.y0
    d1 = dist(x, y, x1, y1)
    d2 = dist(x, y, x2, y2)
    d = dist(x1, y1, x2, y2)

    return d * 1.001 > d1 + d2


def in_ellipse(x, y, xe, ye, largeur, hauteur) -> bool:
    """retourne True si le point (x,y) est dans l'ellipse"""
    x, y = x - processing.x0, y - processing.y0
    angle = math.atan2(y - ye, x - xe)
    r = math.sqrt((largeur * math.cos(angle) / 2) ** 2 + (hauteur * math.sin(angle) / 2) ** 2)
    return dist(x, y, xe, ye) < r * 0.95


def in_circle(x, y, xc, yc, diametre) -> bool:
    """retourne True si le point (x,y) est dans le cercle"""
    return dist(x, y, xc, yc) < diametre / 2


def rectMode(corners_center: str = "") -> str:
    """change center mode 'CORNERS' or 'CENTER' and return previous rectMode mode.
    if no parameter return current value"""
    if processing.get_rect_center_mode():
        cc = "center"
    else:
        cc = "corners"

    if corners_center.upper() == "CORNERS":
        processing.set_rect_center_mode(False)
    elif corners_center.upper() == "CENTER":
        processing.set_rect_center_mode(True)

    return cc


def rect(x: int, y: int, largeur: int = 0, hauteur: int = 0, **kwargs):
    """Créer un rectangle aux coordonnées x,y de largeur largeur et de hauteur.
    Si rectMode('center') x et y sont les coordonnées du centre du rectangle.
    Si rectMode('corners') x,y sont les coordonnées du coin haut gauche.
    Le rectangle est rempli par la couleur définie par fill(couleur).
    paramètres optionnels :
    fill = couleur de remplissage prend le dessus sur fill()
    stroke : couleur du contour prend le dessus sur stroke()
    stroke_weight : largeur du trait prend le dessus sur strokeWeight()
    fill_mouse_on : couleur du fond quand la souris est dessus
    border_rounded = n arrondi les bords de la boite avec un rayon de n pixels
    command : nom de la fonction à appeler si le rectangle est cliqué
    name : valeur passée à la fonction désignée par command
    image = de fond
    Si le paramètre image est renseigné le fond du rectangle sera occupé pas l'image retaillée
    aux dimensions du rectangle sauf si largeur et/ou hauteur sont nulles (ou non renseignées).
    largeur et/ou hauteur seront alors celle de l'image. Les paramètres align_h (left, center et right) et
    align_v (top,center et bottom) permettent d'aligner l'image dans un cadre plus grand qu'elle.
     """

    image: pygame.surface = kwargs.get("image", None)
    align_h = kwargs.get("align_h", "left")
    align_v = kwargs.get("align_v", "top")
    rect_mode = kwargs.get("rect_mode", processing.__rect_center_mode)
    rect_mode = kwargs.get("center_mode", rect_mode)
    border_rounded = kwargs.get("border_rounded", 0)
    if image is not None:
        if hauteur == 0:
            hauteur = image.get_height()
        if largeur == 0:
            largeur = image.get_width()
    if rect_mode:
        x -= largeur / 2
        y -= hauteur / 2
    if border_rounded == 0:
        points = [[x, y],
                  [x + largeur, y],
                  [x + largeur, y + hauteur],
                  [x, y + hauteur]]
    else:
        am = processing.angleMode("rad")
        points = [[x + border_rounded, y],
                  [x + largeur - border_rounded, y]] + \
                 arc_points(x + largeur - border_rounded, y + border_rounded, border_rounded * 2, border_rounded * 2,
                            math.pi / 2, 0, False) + \
                 [[x + largeur, y + border_rounded], [x + largeur, y + hauteur - border_rounded]] + \
                 arc_points(x + largeur - border_rounded, y + hauteur - border_rounded, border_rounded * 2,
                            border_rounded * 2,
                            2 * math.pi, 3 * math.pi / 2, False) + \
                 [[x + largeur - border_rounded, y + hauteur],
                  [x + border_rounded, y + hauteur]] + \
                 arc_points(x + border_rounded, y + hauteur - border_rounded, border_rounded * 2, border_rounded * 2,
                            3 * math.pi / 2, math.pi, False) + \
                 [[x, y + hauteur - border_rounded],
                  [x, y + border_rounded]] + \
                 arc_points(x + border_rounded, y + border_rounded, border_rounded * 2, border_rounded * 2,
                            math.pi, math.pi / 2, False)
        processing.angleMode(am)
    # if image is None:
    polygone(points, **kwargs)
    if image is not None:
        dx = 0  # left
        dy = 0  # top
        if align_h == "left":
            dx += 0
        elif align_h == "right":
            dx = max(0, largeur - image.get_width())
        elif align_h == "center":
            dx = max(0, (largeur - image.get_width()) // 2)
        if align_v == "center":
            dy = max(0, (hauteur - image.get_height()) // 2)
        elif align_v == "bottom":
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
        x, y = processing.transformation([[x + dx, y + dy]])[0]
        processing.screen.blit(img,
                               (x - img.get_width() / 2, y - img.get_height() / 2),
                               (0, 0, img.get_width(), img.get_height()))
        if processing.in_polygone(*processing.mouseXY(), points):
            fill_mouse_on = kwargs.get("fill_mouse_on", processing.__fill_color_mouse_on)
            if fill_mouse_on is not None:
                if isinstance(fill_mouse_on, str):
                    fill_mouse_on = processing.rgb_color(fill_mouse_on)
                fill_mouse_on = list(fill_mouse_on)[:3] + [127]
                lx, ly = zip(*points)
                min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
                target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
                shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
                pygame.draw.polygon(shape_surf, fill_mouse_on, [(x - min_x, y - min_y) for x, y in points])
                processing.screen.blit(shape_surf, target_rect)


def square(x: int, y: int, largeur: int, **kwargs):
    """ trace un carré
    Si rectMode('center') x et y sont les coordonnées du centre du rectangle.
    Si rectMode('corners') x,y sont les coordonnées du coin haut gauche.
    Le rectangle est rempli par la couleur définie par fill(couleur).\n
    paramètres optionnels :\n
    fill = couleur de remplissage prend le dessus sur fill()\n
    stroke : couleur du contour prend le dessus sur stroke()\n
    stroke_weight : largeur du contour prend le dessus sur strokeWeight()\n
    fill_mouse_on : couleur du fond quand la souris est dessus\n
    border_rounded = n arrondi les bords de la boite avec un rayon de n pixels
    command : nom de la fonction à appeler si le carré est cliqué\n
    name : valeur passée à la fonction désignée par command\n
    image = de fond\n
    Si le paramètre image est renseigné le fond du rectangle sera occupé pas l'image retaillée
    aux dimensions du rectangle sauf si largeur et/ou hauteur sont nulles (ou non renseignées).
    largeur et/ou hauteur seront alors celle de l'image. Les paramètres align_h (left, center et right) et
    align_v (top,center et bottom) permettent d'aligner l'image dans un cadre plus grand qu'elle.
    """
    processing.rect(x, y, largeur, largeur, **kwargs)


def point(x: int, y: int):
    """Trace un point de coordonnées(x, y). carré de 3x3 pixel.
    x et y sont les coordonnées du centre quelque soit la valeur de rectMode """
    square(x, y, 3 / processing.get_scale(), center_mode=True)


def line(x1: int, y1: int, x2: int, y2: int, **kwargs):
    """Trace un segment reliant les deux points de coordonnées (x1, y1) et (x2, y2).
    paramètres optionnels :
    stroke : couleur du trait
    stroke_weight : largeur du trait
    fill_mouse_on : couleur du trait quand la souris est dessus
    arrow_start : si True pointe de fléche au début
    arrow_end : si True point de flèche à la fin
    command : nom de la fonction à appeler si les trait est cliqué
    name : valeur passée à la fonction désignée par command"""
    stroke = kwargs.get("stroke", processing.__border_color)
    points = [(x1, y1), (x2, y2)]
    points = processing.transformation(points)
    x1, y1 = points[0]
    x2, y2 = points[1]
    stroke_weight = kwargs.get("stroke_weight", processing.__border_width)
    fill_mouse_on = kwargs.get("fill_mouse_on", processing.__fill_color_mouse_on)
    arrow_start = kwargs.get("arrow_start", False)
    arrow_end = kwargs.get("arrow_end", False)
    command = kwargs.get("command", None)
    command_mouse_over = kwargs.get("command_mouse_over", None)
    name = kwargs.get("name", None)
    if fill_mouse_on is not None and in_line(*processing.mouseXY(), *points[0], *points[1]):
        if processing.mouse_click_down() and command is not None:
            if name is not None:
                command(name)
            else:
                command()
        if command_mouse_over is not None:
            if name is not None:
                command_mouse_over(name)
            else:
                command_mouse_over()
        stroke = fill_mouse_on
    pygame.draw.line(processing.screen, stroke, *points, stroke_weight)
    if arrow_start:
        angle = trigo.atan2(y2 - y1, x2 - x1)
        r = processing.rotate(-angle, (x1, y1))
        triangle(x1, y1, x1 + 5, y1 - 3, x1 + 5, y1 + 3, fill=stroke, no_fill=False, no_stroke=False)
        processing.rotate(*r)
    if arrow_end:
        angle = trigo.atan2(y2 - y1, x2 - x1)
        r = processing.rotate(-angle, (x2, y2))
        triangle(x2, y2, x2 - 5, y2 - 3, x2 - 5, y2 + 3, fill=stroke,
                 no_fill=False, no_stroke=False)
        processing.rotate(*r)


def ellipseMode(corners_center: str = ""):
    """change center mode 'CORNERS' or 'CENTER' et retourne la valeur précedente.
    si pas de paramètre retourne la valeur courante """
    if processing.get_ellipse_center_mode():
        cc = "center"
    else:
        cc = "corners"
    if corners_center.upper() == "CORNERS":
        processing.__ellipse_center_mode = False
    elif corners_center.upper() == "CENTER":
        processing.__ellipse_center_mode = True
    return cc


def get_ellipse_center_mode() -> bool:
    """retourne ellipse_center_mode"""
    return processing.__ellipse_center_mode


def ellipse(x: int, y: int, largeur: int, hauteur: int, **kwargs):
    """Trace une ellipse.\n
    Si ellipseMode('center') x et y sont les coordonnées du centre de l'ellipse.\n
    Si ellipseMode('corners') x,y sont les coordonnées du coin du haut gauche du rectangle contenant l'ellipse.\n
    et dont la largeur et la hauteur prennent les valeurs fixées.\n
    L'ellipse est remplie par la couleur définie par fill(couleur).\n
    paramètres optionnels :\n
    fill = couleur de remplissage prend le dessus sur fill()\n
    stroke : couleur du contour prend le dessus sur stroke()\n
    stroke_weight : largeur du contour prend le dessus sur strokeWeight()\n
    fill_mouse_on : couleur du fond quand la souris est dessus\n
    command : nom de la fonction à appeler si l'ellipse est cliqué\n
    name : valeur passée à la fonction désignée par command
    """
    ellipse_mode = kwargs.get("ellipse_mode", processing.__ellipse_center_mode)
    ellipse_mode = kwargs.get("center_mode", ellipse_mode)
    fill = kwargs.get("fill", processing.get_fill_color())
    no_fill = kwargs.get("no_fill", processing.__no_fill)
    stroke = kwargs.get("stroke", processing.__border_color)
    stroke_weight = kwargs.get("stroke_weight", processing.__border_width)
    fill_mouse_on = kwargs.get("fill_mouse_on", processing.__fill_color_mouse_on)
    no_stoke = kwargs.get("no_stroke", False)
    command = kwargs.get("command", None)
    command_mouse_over = kwargs.get("command_mouse_over", None)
    name = kwargs.get("name", None)
    if processing.__scale != 1:
        largeur *= processing.__scale
        hauteur *= processing.__scale
    if no_stoke is True:
        stroke_weight = 0
    if isinstance(fill, str):
        fill = processing.rgb_color(fill)
    if isinstance(stroke, str):
        stroke = processing.rgb_color(stroke)
    if processing.get_rotation_rad() == 0 and processing.__flip_axe_h is None and processing.__flip_axe_v is None:
        if ellipse_mode:
            x -= largeur / 2
            y -= hauteur / 2
        if no_fill is False:
            if fill_mouse_on is not None and in_ellipse(*processing.mouseXY(), x + largeur / 2,
                                                        y + hauteur / 2, largeur, hauteur):
                if processing.mouse_click_down() and command is not None:
                    if name is not None:
                        command(name)
                    else:
                        command()
                if command_mouse_over is not None:
                    if name is not None:
                        command_mouse_over(name)
                    else:
                        command_mouse_over()
                pygame.draw.ellipse(processing.screen, fill_mouse_on,
                                    (x + processing.__dx, y + processing.__dy, largeur, hauteur),
                                    0)
            else:
                pygame.draw.ellipse(processing.screen, fill,
                                    (x + processing.__dx, y + processing.__dy, largeur, hauteur),
                                    0)

        if stroke_weight > 0:
            pygame.draw.ellipse(processing.screen, stroke,
                                (x + processing.__dx, y + processing.__dy, largeur, hauteur),
                                stroke_weight)
    else:
        arc(x, y, largeur, hauteur, pie=False, **kwargs)


def circle(x: int, y: int, diametre: int, **kwargs):
    """Trace un cercle.\n
        Si ellipseMode('center') x et y sont les coordonnées du centre de l'ellipse.\n
    Si ellipseMode('corners') x,y sont les coordonnées du coin du haut gauche du rectangle contenant l'ellipse.\n
    Idem ellipse((x, y, diametre, diametre)\n
    Le cercle est rempli par la couleur définie par fill(couleur).\n
    paramètres optionnels :\n
    fill = couleur de remplissage prend le dessus sur fill()\n
    stroke : couleur du contour prend le dessus sur stroke()\n
    stroke_weight : largeur du contour prend le dessus sur strokeWeight()\n
    fill_mouse_on : couleur du fond quand la souris est dessus\n
    command : nom de la fonction à appeler si le cercle est cliqué\n
    name : valeur passée à la fonction désignée par command
    """
    ellipse_mode = kwargs.get("ellipse_mode", processing.__ellipse_center_mode)
    ellipse_mode = kwargs.get("center_mode", ellipse_mode)
    fill = kwargs.get("fill", processing.get_fill_color())
    no_fill = kwargs.get("no_fill", processing.__no_fill)
    stroke = kwargs.get("stroke", processing.__border_color)
    stroke_weight = kwargs.get("stroke_weight", processing.__border_width)
    fill_mouse_on = kwargs.get("fill_mouse_on", processing.__fill_color_mouse_on)
    no_stoke = kwargs.get("no_stroke", False)
    command = kwargs.get("command", None)
    command_mouse_over = kwargs.get("command_mouse_over", None)
    name = kwargs.get("name", None)
    if processing.__scale != 1:
        diametre *= processing.__scale
    if no_stoke is True:
        stroke_weight = 0
    if isinstance(fill, str):
        fill = processing.rgb_color(fill)
    if isinstance(stroke, str):
        stroke = processing.rgb_color(stroke)
    points = [(x, y)]
    points = processing.transformation(points)
    x, y = points[0]
    if processing.__flip_axe_h is not None:
        y -= diametre
    if processing.__flip_axe_v is not None:
        x -= diametre
    if ellipse_mode:
        x -= diametre / 2
        y -= diametre / 2

    if no_fill is False:
        if fill_mouse_on is not None and in_circle(*processing.mouseXY(), x + diametre / 2,
                                                   y + diametre / 2, diametre):
            if processing.mouse_click_down() and command is not None:
                if name is not None:
                    command(name)
                else:
                    command()
            if command_mouse_over is not None:
                if name is not None:
                    command_mouse_over(name)
                else:
                    command_mouse_over()
            pygame.draw.ellipse(processing.screen, fill_mouse_on,
                                (x, y, diametre, diametre),
                                0)
        else:
            pygame.draw.ellipse(processing.screen, fill,
                                (x, y, diametre, diametre),
                                0)
    if stroke_weight > 0:
        pygame.draw.ellipse(processing.screen, stroke,
                            (x, y, diametre, diametre),
                            stroke_weight)


def triangle(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, **kwargs):
    """Trace un triangle dont les trois sommets ont pour coordonnées (x1, y1), (x2, y2), et (x3, y3).
    Le triangle est rempli par la couleur définie par fill(couleur).
    paramètres optionnels :
    fill = couleur de remplissage prend le dessus sur fill()
    stroke : couleur du contour prend le dessus sur stroke()
    stroke_weight : largeur du trait prend le dessus sur strokeWeight()
    fill_mouse_on : couleur du fond quand la souris est dessus
    command : nom de la fonction à appeler si le triangle est cliqué
    name : valeur passée à la fonction désignée par command"""
    points = [(x1, y1), (x2, y2), (x3, y3)]
    polygone(points, **kwargs)


def quad(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int, **kwargs):
    """Trace un quadrilatère dont les quatre sommets ont pour coordonnées (x1, y1), (x2, y2), (x3, y3) et (x4, y4)."""
    points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    polygone(points, **kwargs)


def polygone(points: list, **kwargs):
    """Trace un polygone à partie d'une liste de points\n
    Le polygone est rempli par la couleur définie par fill(couleur).\n
    paramètres optionnels :\n
    fill = couleur de remplissage prend le dessus sur fill()\n
    stroke : couleur du contour prend le dessus sur stroke()\n
    stroke_weight : largeur du trait prend le dessus sur strokeWeight()\n
    fill_mouse_on : couleur du fond quand la souris est dessus\n
    command : nom de la fonction à appeler si le polygone est cliqué\n
    name : valeur passée à la fonction désignée par command"""
    points = processing.transformation(points)
    fill = kwargs.get("fill", processing.get_fill_color())
    no_fill = kwargs.get("no_fill", processing.__no_fill)
    stroke = kwargs.get("stroke", processing.__border_color)
    stroke_weight = kwargs.get("stroke_weight", processing.__border_width)
    fill_mouse_on = kwargs.get("fill_mouse_on", processing.__fill_color_mouse_on)
    no_stroke = kwargs.get("no_stroke", False)
    command = kwargs.get("command", None)
    command_mouse_over = kwargs.get("command_mouse_over", None)
    name = kwargs.get("name", None)
    click_up = kwargs.get("click_up", False)
    if no_stroke is True:
        stroke_weight = 0
    if isinstance(fill, str):
        fill = processing.rgb_color(fill)
    if no_fill is True:
        if no_stroke is False:
            pygame.draw.polygon(processing.screen, stroke,
                                points, width=stroke_weight)
    else:
        if processing.in_polygone(*processing.mouseXY(), points):
            if ((not click_up and processing.mouse_click_down()) or (
                    click_up and processing.mouse_click_up())) and command is not None:
                if name is not None:
                    command(name)
                else:
                    command()
            if fill_mouse_on is None:
                pygame.draw.polygon(processing.screen, fill,
                                    points)
            else:
                pygame.draw.polygon(processing.screen, fill_mouse_on,
                                    points)
                if command_mouse_over is not None:
                    if name is not None:
                        command_mouse_over(name)
                    else:
                        command_mouse_over()
        else:
            pygame.draw.polygon(processing.screen, fill,
                                points)
        if stroke_weight != 0:
            pygame.draw.polygon(processing.screen, stroke,
                                points, width=stroke_weight)


def not_filled_polygone(points: list, **kwargs) -> None:
    """crée un polygone vide.\n
    paramètres optionnels :\n
    stroke : couleur du contour prend le dessus sur stroke()\n
    stroke_weight : largeur du trait prend le dessus sur strokeWeight()\n
    fill_mouse_on : couleur du trait quand la souris est dessus\n
    command : nom de la fonction à appeler si le polygone est cliqué\n
    name : valeur passée à la fonction désignée par command"""
    points.append(points[0])
    for i in range(len(points) - 1):
        line(points[i][0] + processing.__dx, points[i][1] + processing.__dy, points[i + 1][0] + processing.__dx,
             points[i + 1][1] + processing.__dy, **kwargs)


def k_line(points: list, **kwargs) -> None:
    """trace un ligne brisée à partir d'une liste de points\n
    [[1,2],[5,6],[8,3],.....]\n
    nb_point = nb_segments + 1\n
    paramètres optionnels :\n
    stroke : couleur du contour prend le dessus sur stroke()\n
    stroke_weight : largeur du trait prend le dessus sur strokeWeight()\n
    fill_mouse_on : couleur du trait quand la souris est dessus\n
    command : nom de la fonction à appeler si le polygone est cliqué\n
    name : valeur passée à la fonction désignée par command"""
    for i in range(len(points) - 1):
        line(points[i][0], points[i][1], points[i + 1][0],
             points[i + 1][1], **kwargs)


def arc(x: int, y: int, largeur: int, hauteur: int, angle_debut: float = None, angle_fin: float = None, **kwargs):
    """Créer une portion d'ellipse type part de tarte qui pourra être rempli entre les points repérés par
    les angles angleDébut et angle_fin. x et y sont les coordonnées du centre du cercle.
    L'arc est rempli par la couleur définie par fill(couleur).\n
    paramètres optionnels :\n
    fill = couleur de remplissage prend le dessus sur fill()\n
    stroke : couleur du contour prend le dessus sur stroke()\n
    stroke_weight : largeur du contour prend le dessus sur strokeWeight()\n
    fill_mouse_on : couleur du fond quand la souris est dessus\n
    command : nom de la fonction à appeler si l'arc est cliqué\n
    name : valeur passée à la fonction désignée par command
    """
    pie = kwargs.get("pie", True)
    ellipse_mode = kwargs.get("ellipse_mode", processing.__ellipse_center_mode)
    # recalcule de x et y si x,y centre de l'ellipse
    if not ellipse_mode:
        x += largeur / 2
        y += hauteur / 2

    # conversion des angle en radians
    if angle_debut is None:
        angle_debut = 0
        angle_fin = 2 * processing.PI
    else:
        angle_debut = processing.radians(angle_debut)
        angle_fin = processing.radians(angle_fin)
    points = []

    # calcul des points de l'arc
    if pie:
        points = [(x, y)]
    if angle_debut > angle_fin:
        angle_fin += 2 * math.pi
    angle = angle_debut
    while angle < angle_fin - 0.1:
        points.append((largeur * math.cos(angle) / 2 + x,
                       -hauteur * math.sin(angle) / 2 + y))
        angle += 0.1
    points.append((largeur * math.cos(angle_fin) / 2 + x,
                   -hauteur * math.sin(angle_fin) / 2 + y))
    polygone(points, **kwargs)


def circle_arc(x: int, y: int, diametre: int, angle_debut: float, angle_fin: float, **kwargs):
    """idem arc mais à partir d'un disque
    L'arc est rempli par la couleur définie par fill(couleur).\n
    paramètres optionnels :\n
    fill = couleur de remplissage prend le dessus sur fill()\n
    stroke : couleur du contour prend le dessus sur stroke()\n
    stroke_weight : largeur du contour prend le dessus sur strokeWeight()\n
    fill_mouse_on : couleur du fond quand la souris est dessus\n
    command : nom de la fonction à appeler si l'ellipse est cliqué\n
    name : valeur passée à la fonction désignée par command
    """
    arc(x, y, diametre, diametre, angle_debut, angle_fin, **kwargs)


def arc_points(x: int, y: int, largeur: int, hauteur: int, angle_debut: float, angle_fin: float, sens_trigo=True) -> list:
    """retourne une liste des points du contour de l'ellipse entre les points repérés par
    les angles angleDébut et angle_fin (en radians). x et y sont les coordonnées du centre du cercle.
    permet de créer des polygones de forme compliquée"""

    # conversion des angles en radians
    angle_debut = trigo.radians(angle_debut)
    angle_fin = trigo.radians(angle_fin)
    points = []

    # calcul des points de l'arc
    pas = 0.1
    if angle_debut > angle_fin and sens_trigo:
        angle_fin += 2 * processing.PI
    if not sens_trigo:
        pas = -pas
    angle = angle_debut
    if pas > 0:
        while angle < angle_fin - pas:
            points.append((largeur * math.cos(angle) / 2 + x,
                           -hauteur * math.sin(angle) / 2 + y))
            angle += pas
    else:
        while angle > angle_fin - pas:
            points.append((largeur * math.cos(angle) / 2 + x,
                           -hauteur * math.sin(angle) / 2 + y))
            angle += pas
    points.append((largeur * math.cos(angle_fin) / 2 + x,
                   -hauteur * math.sin(angle_fin) / 2 + y))
    return points


def dist(x1, y1, x2, y2):
    """retourne la distance entre deux points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def midPoint(x1, y1, x2, y2):
    """retourne le milieu d'un segment defini par deux points"""
    return (x2 + x1) / 2, (y2 + y1) / 2


if __name__ == '__main__':
    cc = ellipseMode("center")
    print(cc, ellipseMode(cc))
    cc = rectMode("center")
    print(cc, rectMode(cc))
    print(rectMode(), ellipseMode())
