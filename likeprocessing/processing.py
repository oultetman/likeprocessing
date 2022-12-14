import pygame

from likeprocessing.pyDialog import *
import math


HALF_PI = math.pi / 2
PI = math.pi
QUARTER_PI = math.pi / 4
TWO_PI = math.pi * 2
pmouseX, pmouseY = 0, 0
RADIANS = 1
DEGREES = 2 * math.pi / 180
debug = False
__text_style = "NORMAL"
__font = 'arial'
__font_size = 12
__font_color = "black"
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
__last_fill_color = (255, 255, 255)
__fill_color_mouse_on = None
__border_color = (0, 0, 0)
__last_border_color = (0, 0, 0)
__fps = 60
__no_loop = False
__no_fill = False
__last_no_fill = False
__dx = 0
__dy = 0
__score = 0
__key_pressed = False
__quitter = False
__title = "processing"
__rect_center_mode = False
__ellipse_center_mode = False
__events = []
var_globales = {}
__click = False
__click_up = False
__click_down = False
__mouse_wheel = 0
__frameCount = 0
objets = []
aliens = None
screen = pygame.display.set_mode((300, 200), pygame.RESIZABLE)
Boite.init(screen)
__rotation = 0
__axis = (0,0)
__flip_axe_v = None
__flip_axe_h = None
__print_x = 5
__print_y = 5
__print_ligne = [25]
__scale = 1
__resizable = 0
__resized = False
__print_console=[]
ihm = []
from random import randint
from likeprocessing.affichage import *
from likeprocessing.transformation import *
from pygame.locals import *
from likeprocessing.formes import *
from likeprocessing.tempos import Tempo
from likeprocessing.images import *
from likeprocessing.texte import *
from likeprocessing.print_vars import print_var

def set_debug(valeur):
    processing.debug = valeur

def debuger():
    if processing.debug:
        print("debug")

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
    """retourne la largeur de l'??cran"""
    return processing.__width


def height():
    """retourne la hauteur de l'??cran"""
    return processing.__height


def size(largeur: int, hauteur: int):
    """initialise les dimensions de l'??cran"""
    processing.__width, processing.__height = largeur, hauteur
    processing.screen = pygame.display.set_mode((largeur, hauteur),processing.__resizable)
    pygame.display.set_caption(__title)

def resizable_screen(resizable:bool=True):
    if resizable:
        processing.__resizable = pygame.RESIZABLE
    else:
        processing.__resizable = 0

def createCanvas(largeur: int, hauteur: int, resizable:bool = False):
    """creer une fen??tre de taille largeur*hauteur"""
    resizable_screen(resizable)
    size(largeur, hauteur)


def title(titre: str):
    """change le titre de la fen??tre"""
    global __title
    __title = titre
    pygame.display.set_caption(__title)


def save_background():
    """fait une copie du contenu de la fenetre"""
    global __background_image
    __background_image = screen.copy()


def draw_background():
    """dessine le background de la fen??tre"""
    if type(__background_image) is pygame.Surface:
        screen.blit(__background_image, (0, 0))
    else:
        screen.fill(__background_color)


def keys() -> [bool]:
    """l'etat des touches du clavier"""
    return pygame.key.get_pressed()


def keyIsPressed() -> bool:
    """retourne True si une touche du clavier est press??e """
    return __key_pressed


def isKeyPressed():
    """retourne True si une touche du clavier est press??e """
    return __key_pressed


def keyIsDown(code) -> bool:
    """retourne True si une touche(code) est press??e """
    return pygame.key.get_pressed()[code] == True


def frameCount():
    """retourne le nombre de boucle effectu??e depuis le lancement du programme"""
    return processing.__frameCount


def mouseIsPressed():
    """retourne True si une touche de la souris est appuy??e"""
    return __click


def mouse_button_pressed():
    """retourne le numero de la touche de la souris qui est appuy??e 0,1 ou 2
    -1 si aucune touche est enfonc??e"""
    boutons = pygame.mouse.get_pressed()
    for i in range(3):
        if boutons[i]:
            return i
    return -1


def mouse_click_up():
    """return True when the mouse button move down to up for one loop only """
    return processing.__click_up


def mouse_click_down():
    """return True when the mouse button move up to down for one loop only """
    return processing.__click_down


def mouse_click():
    """return True if mouse button is down"""
    return processing.__click


def mouse_wheel_state():
    """return 1 if wheel turn up -1 if wheel turn down and 0 if not turn"""
    return processing.__mouse_wheel


def redraw():
    """force le redessin de l'??cran"""
    pygame.display.update()


def events() -> list:
    return processing.__events


def quitter(value=None):
    global __quitter
    if value is None:
        return __quitter
    elif value is False:
        __quitter = False


def run(globales):
    global __key_pressed, __click, __click_down, __click_up, keys, __quitter, var_globales, __frameCount, clock, secondes
    global __tempo_seconde, __tempo_centieme, centiemes, __events,__mouse_wheel,__resized
    successes, failures = pygame.init()
    print("{0} successes and {1} failures".format(successes, failures))
    clock = pygame.time.Clock()
    if globales.get('setup'):
        globales['setup']()
    while True:
        clock.tick(__fps)
        __events = pygame.event.get()
        for event in __events:
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
                if __click is False:
                    __click = True
                    __click_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                __click = False
                __click_up = True
            elif event.type == MOUSEWHEEL:
                __mouse_wheel = event.y
            elif event.type == pygame.VIDEORESIZE:
                processing.__width, processing.__height = event.w, event.h
                __resized = True
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
        __click_down = False
        __click_up = False
        __mouse_wheel = 0
        __resized = False
def set_click(value):
    global __click
    __click = value

def get_click():
    return processing.__click

def set_click_down(value):
    global __click_down
    __click_down = value

def set_click_up(value):
    global __click_up
    __click_up = value

def get_resized():
    return processing.__resized

def set_axis(axe: tuple):
    """initialise la valeur de l''axe de rotation"""
    if len(axe) == 2:
        processing.__axis = axe
    else:
        raise TypeError("axe is tuple and his length must be equal 2")


def get_axis() -> tuple:
    """retourne la valeur de l''axe de rotation"""
    return processing.__axis


def set_font_size(taille):
    """initialise la taille courante du texte"""
    global __font_size
    __font_size = taille


def set_font_color(color):
    """initialise la taille courante du texte"""
    global __font_size
    __font_size = color


def get_font_size():
    """retourne la taille courante du texte"""
    return __font_size


def get_font_color():
    """retourne la couleur courante du texte"""
    return __font_color


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


def set_flip_axe_v(axe_v: [int, float]):
    """initialise l'axe de sym??trie verticale"""
    processing.__flip_axe_v = axe_v


def get_flip_axe_v() -> [int, float]:
    """retourne l'axe de sym??trie verticale"""
    return processing.__flip_axe_v


def set_flip_axe_h(axe_h: [int, float]):
    """initialise l'axe de sym??trie horizontale"""
    processing.__flip_axe_h = axe_h


def get_flip_axe_h() -> [int, float]:
    """retourne l'axe de sym??trie horizontale"""
    return processing.__flip_axe_h


def set_dx(translation_absolue_x: [int, float]):
    """initialise la valeur courant de la translation"""
    processing.__dx = translation_absolue_x


def get_dx() -> [int, float]:
    """retourne la valeur courant de la translation"""
    return processing.__dx


def set_dy(tanslation_absole_y: [int, float]):
    """initialise la translation absolue en y"""
    processing.__dy = tanslation_absole_y


def get_dy() -> [int, float]:
    """retourne la translation absolue en y"""
    return processing.__dy


def set_rotation(angle: [int, float]):
    """initialise la valeur de l'angle de rotation"""
    processing.__rotation = radians(angle)


def get_rotation() -> float:
    return processing.__rotation


def get_angle_mode() -> float:
    """retourne la valeur de angle mode"""
    return processing.__angle_mode


def set_angle_mode(valeur: float):
    processing.__angle_mode = valeur


def set_rect_center_mode(center: bool):
    """initialise la valeur de rect_center_mode"""
    processing.__rect_center_mode = center


def get_rect_center_mode() -> bool:
    """retourne la valeur de rect_center_mode"""
    return processing.__rect_center_mode


def set_scale(echelle: [int, float]):
    processing.__scale = echelle


def get_scale():
    return processing.__scale

def get_background_color():
    return processing.__background_color