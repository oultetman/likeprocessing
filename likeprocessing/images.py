import math

import pygame
import likeprocessing.processing as processing
def loadImage(fichier: str) -> pygame.Surface:
    """retourne une surface de type image"""
    return pygame.image.load(fichier)

def image(image,x,y):
    """Affiche une Image en plaçant le pixel en haut à gauche au point de coordonnées (x, y)
    dans la zone de dessin."""
    r = processing.get_rotation() * 180 / math.pi
    img = pygame.transform.rotate(image, r)
    x += image.get_width() / 2
    y += image.get_height() / 2
    x, y = processing.rotation([[x + processing.__dx, y + processing.__dy]])[0]
    processing.screen.blit(img,(x - img.get_width() / 2, y - img.get_height() / 2),
                           (0, 0, img.get_width(), img.get_height()))