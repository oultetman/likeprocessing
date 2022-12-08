import math
from typing import Annotated, Union
import likeprocessing.processing as processing
import pygame
from pygame.colordict import THECOLORS as COLORS
from likeprocessing.exceptions import RgbError
from likeprocessing.trigo import angleMode
import likeprocessing.processing

rgb_value = tuple[int, int, int]


def base_colors_name() -> list:
    return ["black", "blue", "purple", "cyan", "pink",
            "red", "orange", "yellow", "green", "olive",
            "brown", "grey", "white"]


def background(couleur_image: any):
    """applique une couleur ou une image sur le fond. l'image doit être charger avec loadImage """
    if isinstance(couleur_image, pygame.Surface):
        processing.__background_image = couleur_image
    else:
        c = rgb_color(couleur_image)
        if c is not None:
            processing.__background_color = c
    processing.draw_background()


def noFill() -> tuple:
    """supprime la couleur de fond d'une figure (rect, square, ellipse ...) """
    processing.__no_fill = True
    return processing.__fill_color


def stroke(couleur: any = None):
    """initialise la couleur du bord des figures"""
    processing.__border_width = processing.__last_border_width
    if couleur is None:
        return processing.__border_color
    last_color = processing.__border_color
    c = rgb_color(couleur)
    if c is not None:
        processing.__border_color = c
        return last_color


def strokeWeight(epaisseur: int = None):
    if epaisseur is not None:
        processing.__last_border_width = processing.__border_width
        processing.__border_width = epaisseur
    return processing.__last_border_width


def noStroke():
    """supprime le bord des figures"""
    processing.__last_border_width = processing.__border_width
    processing.__border_width = 0
    return processing.__last_border_width


def noCursor():
    pygame.mouse.set_visible(False)


def cursor(cursor=pygame.SYSTEM_CURSOR_ARROW):
    pygame.mouse.set_cursor(cursor)


def save_fill_stroke():
    """save fill and stroke parameters"""
    processing.__last_border_width = processing.__border_width
    processing.__last_border_color = processing.__border_color
    processing.__last_fill_color = processing.__fill_color
    processing.__last_no_fill = processing.__no_fill


def restore_fill_stroke():
    """restore fill and stroke parameters"""
    processing.__border_width = processing.__last_border_width
    processing.__border_color = processing.__last_border_color
    processing.__fill_color = processing.__last_fill_color
    processing.__no_fill = processing.__last_no_fill


def get_border_width():
    return processing.__border_width


def get_fill_color():
    """return current color fill"""
    return processing.__fill_color


def get_border_color():
    """return current border color"""
    return processing.__border_color


def get_stroke():
    """return current border color"""
    return processing.__border_color


def fill(couleur: Union[str, rgb_value, None] = None):
    """initialise la couleur de fond des figures"""
    if couleur is None:
        return processing.__last_fill_color
    try:
        rgb_valid(couleur)
    except Exception as err:
        print(f"{err} fill({couleur})")
        raise
    c = rgb_color(couleur)
    if c is not None:
        processing.__last_fill_color = processing.__fill_color
        processing.__fill_color = c
    processing.__no_fill = False
    return processing.__last_fill_color


def fill_mouse_on(couleur: any):
    """initialise la couleur de fond des figures quand la souris est dessus"""
    c = rgb_color(couleur)
    if c is not None:
        processing.__fill_color_mouse_on = c


def noFill_mouse_on():
    processing.__fill_color_mouse_on = None


def color(rouge: int, vert: int = None, bleu: int = None):
    if vert is None:
        return rouge, rouge, rouge
    return rouge, vert, bleu


def frameRate(valeur=None):
    """initialise le nombre de frame par secondes"""
    if valeur is None:
        return processing.__fps
    elif valeur > 0:
        fps = valeur


def setFrameRate(valeur):
    """initialise le nombre de frame par secondes"""
    frameRate(valeur)


def getFrameRate() -> float:
    """retourne le nombre de frame par secondes"""
    return frameRate()


def noLoop() -> None:
    """La fonction draw() ne sera executé qu'une seule fois """
    processing.__no_loop = True


def loop() -> None:
    """reprend l'execution de la fonction draw() en boucle"""
    processing.__no_loop = False


def stop() -> None:
    """ stop the loop like no_loop()"""
    noLoop()


def rgb_valid(valeur: tuple):
    if isinstance(valeur, tuple):
        for v in valeur:
            if v < 0 or v > 255:
                raise RgbError("In rgb tuple each number must be in [0;255]")


def rgb_color(valeur) -> [tuple, None]:
    """retourne un tuple de 4 éléments rgb + transparence à partir d"un tuple rgb, d'une chaine de caractères
    désignant la couleur ex black, d'une chaine #12FAE6 ou #12FAE6FF"""
    if isinstance(valeur, tuple):
        if len(valeur) == 3:
            return tuple([v for v in valeur] + [255])
        elif len(valeur) == 4:
            return valeur
    elif isinstance(valeur, int):
        return min(255, valeur), min(255, valeur), min(255, valeur), 255
    elif isinstance(valeur, str):
        if valeur[0] == '#' and len(valeur) == 7:
            return int(valeur[1:3], 16), int(valeur[3:5], 16), int(valeur[5:], 16), 255
        elif valeur[0] == '#' and len(valeur) == 9:
            return int(valeur[1:3], 16), int(valeur[3:5], 16), int(valeur[5:7], 16), int(valeur[7:], 16)
        elif valeur[0:2] == '0x' and len(valeur) == 8:
            return int(valeur[2:4], 16), int(valeur[4:6], 16), int(valeur[6:], 16), 255
        elif COLORS.get(valeur.lower()):
            return COLORS.get(valeur.lower())
    return None


def reset():
    processing.__dx = 0
    processing.__dy = 0
    processing.__rotation = 0
    processing.__axis = (0, 0)
    processing.__flip_axe_v = None
    processing.__flip_axe_h = None
    processing.__print_x = 5
    processing.__print_y = 5
    processing.__print_ligne = [25]


if __name__ == '__main__':
    f = fill("black")
    print(f)
    print(fill(f))

    f = noFill()
    print(f)

    s = noStroke()
    print(s)
    sw = strokeWeight(3)
    print(sw, strokeWeight(sw))
