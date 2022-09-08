import math

import pygame
import likeprocessing.processing as processing

Image = pygame.Surface


def loadImage(fichier: str) -> pygame.Surface:
    """retourne une surface de type image"""
    return pygame.image.load(fichier)


def image(picture, x, y):
    """Affiche une Image en plaçant le pixel en haut à gauche au point de coordonnées (x, y)
    dans la zone de dessin."""
    r = processing.get_rotation() * 180 / math.pi
    img = pygame.transform.rotate(picture, r)
    x += picture.get_width() / 2
    y += picture.get_height() / 2
    x, y = processing.rotation([[x + processing.__dx, y + processing.__dy]])[0]
    processing.screen.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2),
                           (0, 0, img.get_width(), img.get_height()))


def copy_image(picture: Image, rect=None) -> Image:
    if rect is None:
        return picture.copy()
    elif isinstance(rect, tuple) and len(rect) == 4:
        return picture.subsurface(rect)


def get_pixel_color(picture: Image, pos: tuple | list) -> tuple:
    return picture.get_at(pos)
