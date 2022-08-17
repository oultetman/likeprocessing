import pygame
import likeprocessing.processing as processing
def loadImage(fichier: str) -> pygame.Surface:
    """retourne une surface de type image"""
    return pygame.image.load(fichier)

def image(image, x:int, y:int):
    processing.screen.blit(image, (0, 0))