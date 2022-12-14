import math

import pygame
import likeprocessing.processing as processing

Image = pygame.Surface


def loadImage(fichier: str) -> Image:
    """retourne une surface de type image"""
    return pygame.image.load(fichier)


def image(picture, x, y):
    """Affiche une Image en plaçant le pixel en haut à gauche au point de coordonnées (x, y)
    dans la zone de dessin."""
    r = processing.get_rotation_rad() * 180 / math.pi
    img = pygame.transform.rotate(picture, r)
    x += picture.get_width() / 2
    y += picture.get_height() / 2
    x, y = processing.rotation([[x + processing.__dx, y + processing.__dy]])[0]
    processing.screen.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2),
                           (0, 0, img.get_width(), img.get_height()))


def copy_image(picture: Image, rect=None) -> Image:
    """retourne une copie de picture ou une partie de picture au dimensions de rect"""
    if rect is None:
        return picture.copy()
    elif isinstance(rect, tuple) and len(rect) == 4:
        return picture.subsurface(rect)


def get_pixel_color(picture: Image, pos: tuple) -> tuple:
    """retourne la valeur de la couleur d'un pixel d'une image (picture)
     sous la forme d'un tuple"""
    return picture.get_at(pos)

def resize_image(picture: Image, size: tuple[int,int]) -> Image:
    return pygame.transform.smoothscale(picture,size)
