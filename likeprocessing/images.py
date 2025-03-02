import math

import pygame
import likeprocessing.processing as processing

Image = pygame.Surface


def loadImage(fichier: str) -> Image:
    """retourne une surface de type image"""
    try:
        return pygame.image.load(fichier)
    except:
        raise FileNotFoundError(fichier)


def loadImages(liste_images: list[str], sens=0) -> Image:
    """Retourne une surface qui est l'assemblage de toutes les images
    de la liste.Si sens = 1 les images sont assemblées verticalement
    et horizontalement si sens =0 """
    w, h = 0, 0
    list_screen_image = []
    if sens == 1:
        for i in range(len(liste_images)):
            list_screen_image.append(pygame.image.load(liste_images[i]))
            w = max(w, list_screen_image[i].get_width())
            h += list_screen_image[i].get_height()
        img = pygame.Surface((w, h))
        h = 0
        for i in range(len(list_screen_image)):
            img.blit(list_screen_image[i], (0, h))
            h += list_screen_image[i].get_height()
        return img
    elif sens == 0:
        for i in range(len(liste_images)):
            list_screen_image.append(pygame.image.load(liste_images[i]))
            h = max(h, list_screen_image[i].get_height())
            w += list_screen_image[i].get_width()
        img = pygame.Surface((w, h))
        w = 0
        for i in range(len(list_screen_image)):
            img.blit(list_screen_image[i], (w, 0))
            w += list_screen_image[i].get_width()
        return img


def image(picture, x, y,**kwargs):
    """Affiche une Image en plaçant le pixel en haut à gauche au point de coordonnées (x, y)
    dans la zone de dessin."""
    r = processing.get_rotation_rad() * 180 / math.pi
    flip_h = kwargs.get("flip_h", False)
    flip_v = kwargs.get("flip_v", False)
    if flip_h or flip_v:
        picture = pygame.transform.flip(picture, flip_h, flip_v)
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


def paste_image(picture: Image, paste_picture: Image, pos=(0, 0)) -> Image:
    """retourne une copie de picture dont une partie est remplacée par paste_picture à
    la position pos"""
    img = picture.copy()
    img.blit(paste_picture, pos)
    return img


def get_pixel_color(picture: Image, pos: tuple) -> tuple:
    """retourne la valeur de la couleur d'un pixel d'une image (picture)
     sous la forme d'un tuple"""
    return picture.get_at(pos)


ef resize_image(picture: Image, size: tuple[int, int]) -> Image:
    """ redimensionne une image en fonction de size"""
    return pygame.transform.smoothscale(picture, size)


def save_image(picture: Image, file_name: str):
    """"""
    pygame.image.save(picture, file_name)
