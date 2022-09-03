from likeprocessing.pyDialog import *
import math

HALF_PI = math.pi / 2
PI = math.pi
QUARTER_PI = math.pi / 4
TWO_PI = math.pi * 2
pmouseX, pmouseY = 0, 0
RADIANS = 1
DEGREES = 2 * math.pi / 180
__text_style = "NORMAL"
__font = 'arial'
__font_size = 12
__couleur_bord_cadre_texte = "black"
__text_align_h = "LEFT"
__text_align_v = "TOP"
__angle_mode = 1
__width, __height = 300, 200
__background_color = (0, 0, 0)
__background_image = None
__border_width = 1
__last_border_width = 1
__fill_color = (255, 255, 255)
__border_color = (0, 0, 0)
__fps = 60
__no_loop = False
__no_fill = False
__dx = 0
__dy = 0
__score = 0
__key_pressed = False
__quitter = False
__title = "processing"
__rect_center_mode = False
__ellipse_center_mode = False
var_globales = {}
click = False
__frameCount = 0
objets = []
aliens = None
screen = pygame.display.set_mode((300, 200))
Boite.init(screen)
__rotation = 0
__axis = None
__flip_axe_v = None
__flip_axe_h = None
from random import randint
from likeprocessing.affichage import *
from likeprocessing.transformation import *
from pygame.locals import *
from likeprocessing.trigo import *
from likeprocessing.formes import *
from likeprocessing.tempos import Tempo
from likeprocessing.images import *
from likeprocessing.texte import *


def get_font():
    return __font


def set_font(font: str):
    global __font
    __font = font


def score(valeur: int = None):
    global __score
    if valeur is None:
        return __score
    elif valeur == 0:
        __score = 0
    else:
        __score += valeur


def random(mini, maxi=None):
    if maxi is None:
        maxi = mini
        mini = 0
    return randint(mini, maxi - 1)


def strokeWeight(epaiseur: int):
    """détermine la largeur du trait"""
    global __border_width
    __border_width = epaiseur


def mouseX():
    """retourne la position en X de la souris"""
    return pygame.mouse.get_pos()[0]


def mouseY():
    """retourne la position en Y de la souris"""
    return pygame.mouse.get_pos()[1]


def mouseXY() -> tuple[int, int]:
    """retourne la position x,y de la souris sous forme de tuple"""
    return pygame.mouse.get_pos()


def width():
    """retourne la largeur de l'écran"""
    return processing.__width


def height():
    """retourne la hauteur de l'écran"""
    return processing.__height


def size(largeur: int, hauteur: int):
    """initialise les dimensions de l'écran"""
    processing.__width, processing.__height = largeur, hauteur
    processing.screen = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption(__title)


def createCanvas(largeur: int, hauteur: int):
    """creer une fenêtre de taille largeur*hauteur"""
    size(largeur, hauteur)


def title(titre: str):
    """change le titre de la fenêtre"""
    global __title
    __title = titre
    pygame.display.set_caption(__title)


def save_background():
    """fait une copie du contenu de la fenetre"""
    global __background_image
    __background_image = screen.copy()


def draw_background():
    """dessine le background de la fenêtre"""
    if type(__background_image) is pygame.Surface:
        screen.blit(__background_image, (0, 0))
    else:
        screen.fill(__background_color)


def keys() -> list[bool]:
    """l'etat des touches du clavier"""
    return pygame.key.get_pressed()


def keyIsPressed() -> bool:
    """retourne True si une touche du clavier est pressée """
    return __key_pressed


def isKeyPressed():
    """retourne True si une touche du clavier est pressée """
    return __key_pressed


def keyIsDown(code) -> bool:
    """retourne True si une touche(code) est pressée """
    return pygame.key.get_pressed()[code] == True


def frameCount():
    """retourne le nombre de boucle effectuée depuis le lancement du programme"""
    return processing.__frameCount


def mouseIsPressed():
    """retourne True si une touche de la souris est appuyée"""
    return click is True


def mouse_button_pressed():
    """retourne le numero de la touche de la souris qui est appuyée 0,1 ou 2
    -1 si aucune touche est enfoncée"""
    boutons = pygame.mouse.get_pressed()
    for i in range(3):
        if boutons[i]:
            return i
    return -1


def redraw():
    """force le redessin de l'écran"""
    pygame.display.update()


def quitter(value=None):
    global __quitter
    if value is None:
        return __quitter
    elif value is False:
        __quitter = False


def run(globales):
    global __key_pressed, click, click_down, click_up, keys, __quitter, var_globales, __frameCount, clock, secondes
    global __tempo_seconde, __tempo_centieme, centiemes
    successes, failures = pygame.init()
    print("{0} successes and {1} failures".format(successes, failures))
    clock = pygame.time.Clock()
    if globales.get('setup'):
        globales['setup']()
    while True:
        clock.tick(__fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if globales.get('quit'):
                    __quitter = True
                else:
                    quit()
            elif event.type == pygame.KEYDOWN:
                __key_pressed = True
            elif event.type == pygame.KEYUP:
                if not 1 in pygame.key.get_pressed():
                    __key_pressed = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                click_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                click = False
                click_up = True

        if globales.get('scan_event'):
            globales['scan_event']()
        if globales.get('compute'):
            globales['compute']()
        if globales.get('draw_object'):
            globales['draw_object']()
        if globales.get('draw'):
            if __no_loop is False or (__no_loop is True and __frameCount == 0):
                draw_background()
                globales['draw']()
                reset()
        if __quitter:
            globales['quit']()
        pygame.display.update()  # Or pygame.display.flip()
        __frameCount += 1


def set_font_size(taille):
    """initialise la taille courante du texte"""
    global __font_size
    __font_size = taille


def get_font_size():
    """retourne la taille courante du texte"""
    return __font_size


def get_couleur_bord_cadre_texte():
    """retourne la couleur courante du cadre du texte"""
    return __couleur_bord_cadre_texte


def set_couleur_cadre_texte(couleur):
    """initialise la couleur courante du cadre du texte"""
    global __couleur_bord_cadre_texte
    __couleur_bord_cadre_texte = couleur


def set_text_style(style):
    """initialise le style courant du texte"""
    processing.__text_style = style


def get_text_style():
    """retourne le style courant du texte"""
    return processing.__text_style


def set_text_align_h(horizontal: str):
    """initialise l'alignement horizontal courant du texte"""
    processing.__text_align_h = horizontal


def get_text_align_h() -> str:
    """retourne l'alignement horizontal courant du texte"""
    return processing.__text_align_h


def set_text_align_v(vertical: str):
    """initialise l'alignement vertical courant du texte"""
    processing.__text_align_v = vertical


def get_text_align_v() -> str:
    """retoune l'alignement vertical courant du texte"""
    return processing.__text_align_v
