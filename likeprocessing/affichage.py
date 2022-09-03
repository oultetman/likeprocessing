import math

import likeprocessing.processing as processing
import pygame
from pygame.colordict import THECOLORS as COLORS
from likeprocessing.trigo import angleMode
import likeprocessing.processing


def background(couleur_image: any):
    """applique une couleur ou une image sur le fond. l'image doit être charger avec loadImage """
    if isinstance(couleur_image, pygame.Surface):
        processing.__background_image = couleur_image
    else:
        c = rgb_color(couleur_image)
        if c is not None:
            processing.__background_color = c
    processing.draw_background()


def noFill():
    """supprime la couleur de fond d'une figure (rect, square, ellipse ... """
    processing.__border_width = processing.__last_border_width
    processing.__no_fill = True


def stroke(couleur: any=None):
    """initialise la couleur du bord des figures"""
    if couleur is None:
        return processing.__border_color
    c = rgb_color(couleur)
    processing.__border_width = processing.__last_border_width
    if c is not None:
        processing.__border_color = c


def strokWeight(epaisseur:int):
    processing.__border_width = epaisseur
    processing.__last_border_width = processing.__border_width


def noStroke():
    """supprime le bord des figures"""
    processing.__last_border_width = processing.__border_width
    processing.__border_width = 0


def get_border_width():
    return processing.__border_width


def get_fill_color():
    return processing.__fill_color


def get_border_color():
    return processing.__border_color


def fill(couleur: any):
    """initialise la couleur de fond des figures"""
    c = rgb_color(couleur)
    if c is not None:
        processing.__fill_color = c
        processing.__no_fill = False


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


def rgb_color(valeur) -> [tuple, None]:
    """retourne un tuple de 4 éléments rgb + transparance à partir d"un tuple rgb, d'une chaine de caractères
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
    processing.__axis = None
    processing.__flip_axe_v = None
    processing.__flip_axe_h = None



