import pygame
import os
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
__width, __height = 1, 1
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
x0, y0 = 0, 0
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
screen = pygame.display.set_mode((1, 1), pygame.RESIZABLE)
Boite.init(screen)
__rotation = 0
__axis = (0, 0)
__flip_axe_v = None
__flip_axe_h = None
__print_x = 5
__print_y = 5
__print_ligne = [25]
__scale = 1
__resizable = 0
__resized = False
__print_console = []
__path = ""
__quit_cross_enabled = True
for p in sys.path:
    if "site-packages" in p and p[-13:] == "site-packages":
        __path = p + "\\likeprocessing\\"
    if not os.path.exists(__path):
        __path = ".\\likeprocessing\\"

ihm = []
from random import randint
from likeprocessing.affichage import *
from likeprocessing.transformation import *
from pygame.locals import *
from likeprocessing.formes import *
from likeprocessing.tempos import Tempo, Monostable, Pwm
from likeprocessing.images import *
from likeprocessing.texte import *
from likeprocessing.print_vars import print_var
from likeprocessing.tor import Tor

def save_global():
    variables = {}
    variables["text_style"] = processing.__text_style
    variables["font"] = processing.__font
    variables["font_size"] = processing.__font_size
    variables["font_color"] = processing.__font_color
    variables["couleur_bord_cadre_texte"] = processing.__couleur_bord_cadre_texte
    variables["text_align_h"] = processing.__text_align_h
    variables["text_align_v"] = processing.__text_align_v
    variables["angle_mode"] = processing.__angle_mode
    variables["background_color"] = processing.__background_color
    variables["background_image"] = processing.__background_image
    variables["border_width"] = processing.__border_width
    variables["last_border_width"] = processing.__last_border_width
    variables["fill_color"] = processing.__fill_color
    variables["last_fill_color"] = processing.__last_fill_color
    variables["fill_color_mouse_on"] = processing.__fill_color_mouse_on
    variables["border_color"] = processing.__border_color
    variables["last_border_color"] = processing.__last_border_color
    variables["rotation"] = processing.__rotation
    variables["axis"] = processing.__axis
    variables["flip_axe_v"] = processing.__flip_axe_v
    variables["flip_axe_h"] = processing.__flip_axe_h
    variables["rect_center_mode"] = processing.__rect_center_mode
    variables["ellipse_center_mode"] = processing.__ellipse_center_mode
    variables["x0"] = processing.x0
    variables["y0"] = processing.y0
    return variables

def init_globales(variables: dict = {}):
    if len(variables) == 0:
        processing.__text_style = "NORMAL"
        processing.__font = 'arial'
        processing.__font_size = 12
        processing.__font_color = "black"
        processing.__couleur_bord_cadre_texte = "black"
        processing.__text_align_h = "LEFT"
        processing.__text_align_v = "TOP"
        processing.__angle_mode = 1
        processing.__background_color = (0, 0, 0)
        processing.__background_image = None
        processing.__border_width = 1
        processing.__last_border_width = 1
        processing.__fill_color = (255, 255, 255)
        processing.__last_fill_color = (255, 255, 255)
        processing.__fill_color_mouse_on = None
        processing.__border_color = (0, 0, 0)
        processing.__last_border_color = (0, 0, 0)
        processing.__rotation = 0
        processing.__axis = (0, 0)
        processing.__flip_axe_v = None
        processing.__flip_axe_h = None
        processing.__rect_center_mode = False
        processing.__ellipse_center_mode = False
        processing.x0, processing.y0 = 0, 0
    else:
        processing.__text_style = variables["text_style"]
        processing.__font = variables["font"]
        processing.__font_size = variables["font_size"]
        processing.__font_color = variables["font_color"]
        processing.__couleur_bord_cadre_texte = variables["couleur_bord_cadre_texte"]
        processing.__text_align_h = variables["text_align_h"]
        processing.__text_align_v = variables["text_align_v"]
        processing.__angle_mode = variables["angle_mode"]
        processing.__background_color = variables["background_color"]
        processing.__background_image = variables["background_image"]
        processing.__border_width = variables["border_width"]
        processing.__last_border_width = variables["last_border_width"]
        processing.__fill_color = variables["fill_color"]
        processing.__last_fill_color = variables["last_fill_color"]
        processing.__fill_color_mouse_on = variables["fill_color_mouse_on"]
        processing.__border_color = variables["border_color"]
        processing.__last_border_color = variables["last_border_color"]
        processing.__rotation = variables["rotation"]
        processing.__axis = variables["axis"]
        processing.__flip_axe_v = variables["flip_axe_v"]
        processing.__flip_axe_h = variables["flip_axe_h"]
        processing.__rect_center_mode = variables["rect_center_mode"]
        processing.__ellipse_center_mode = variables["ellipse_center_mode"]
        processing.x0, processing.y0 = variables["x0"], variables["y0"]


def set_debug(valeur):
    processing.debug = valeur


def debuger():
    if processing.debug:
        print("debug")


def get_font():
    return processing.__font


def get_path():
    return processing.__path.replace("\\", "/")


def set_font(font: str):
    processing.__font = font



def score(valeur: int = None):
    if valeur is None:
        return processing.__score
    elif valeur == 0:
        processing.__score = 0
    else:
        processing.__score += valeur


def random(mini, maxi=None):
    """retourne un nombre aléatoire entre mini et maxi inclus
    si maxi n'est pas précisé, retourne un nombre aléatoire entre 0 et la valeur entrée en paramètre"""
    if maxi is None:
        maxi = mini
        mini = 0
    return randint(mini, maxi)


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
    processing.screen = pygame.display.set_mode((largeur, hauteur), processing.__resizable)
    pygame.display.set_caption(__title)
    processing.Boite.ecran = processing.screen


def resizable_screen(resizable: bool = True) -> None:
    """
    Configure la fenêtre pour qu'elle soit redimensionnable ou non.

    :param resizable: Un booléen indiquant si la fenêtre doit être redimensionnable (True) ou non (False).
    :type resizable: bool
    """
    if resizable:
        processing.__resizable = pygame.RESIZABLE
    else:
        processing.__resizable = 0


def createCanvas(largeur: int, hauteur: int, resizable: bool = False,**kwargs) -> None:
    """
    Crée une fenêtre de taille largeur x hauteur.

    :param largeur: La largeur de la fenêtre en pixels.
    :type largeur: int
    :param hauteur: La hauteur de la fenêtre en pixels.
    :type hauteur: int
    :param resizable: Un booléen indiquant si la fenêtre doit être redimensionnable (True) ou non (False). False par défaut.
    :type resizable: bool
    """
    icone  = kwargs.get("icone", None)
    if icone is not None:
        set_icone(icone)
    resizable_screen(resizable)
    size(largeur, hauteur)


def title(titre: str) -> None:
    """
    Change le titre de la fenêtre.

    :param titre: Le nouveau titre de la fenêtre.
    :type titre: str
    """
    global __title
    __title = str(titre)
    pygame.display.set_caption(__title)

def set_icone(icone:Union[Image,str]):
    """modifie l'icône de la fenêtre de l'application"""
    if isinstance(icone, str):
        icone = loadImage(icone)
    if isinstance(icone, Image):
        icone = resize_image(icone, (32, 32))
        pygame.display.set_icon(icone)

def save_background():
    """fait une copie du contenu de la fenetre"""
    global __background_image
    __background_image = screen.copy()


def reset_background() -> None:
    """
    supprime l'image de fond __background_image`.
    """
    global __background_image
    __background_image = None


def draw_background() -> None:
    """
    Dessine le fond de la fenêtre.

    Si une image de fond a été enregistrée avec `save_background`, cette image est dessinée sur la fenêtre.
    Sinon, la couleur de fond par défaut est utilisée pour remplir la fenêtre.
    """
    if type(__background_image) is pygame.Surface:
        screen.blit(__background_image, (0, 0))
    else:
        screen.fill(__background_color)


def keys() -> list[bool]:
    """
    Renvoie l'état de toutes les touches du clavier.

    Retourne une liste de booléens où chaque élément correspond à une touche du clavier.
    Si la touche est enfoncée, la valeur correspondante dans la liste est True, sinon False.
    """
    return list(pygame.key.get_pressed())


def keyIsPressed() -> bool:
    """
    Renvoie True si une touche du clavier est enfoncée.

    La fonction utilise une variable interne "__key_pressed" qui est mise à jour
    à chaque tour de boucle pour indiquer si une touche est actuellement enfoncée.
    """
    return __key_pressed


def isKeyPressed() -> bool:
    """
    Renvoie True si une touche du clavier est enfoncée.

    La fonction utilise une variable interne "__key_pressed" qui est mise à jour
    à chaque tour de boucle pour indiquer si une touche est actuellement enfoncée.
    """
    return __key_pressed


def keyIsDown(code: int) -> bool:
    """
    Renvoie True si la touche correspondante au code donné est enfoncée.

    La fonction utilise la méthode "get_pressed" de la classe "pygame.key" pour
    récupérer l'état actuel de toutes les touches du clavier. Elle compare ensuite
    la valeur correspondante à la touche spécifiée par son code pour déterminer si elle est enfoncée.
    """
    return pygame.key.get_pressed()[code] == True


def frameCount() -> int:
    """
    Renvoie le nombre de tours de boucle effectués depuis le début du programme.

    La variable "__frameCount" est mise à jour automatiquement à chaque tour de boucle.
    """
    return processing.__frameCount



def mouseIsPressed() -> bool:
    """retourne True si une touche de la souris est appuyée"""
    return __click


def mouse_button_pressed() -> int:
    """retourne le numero de la touche de la souris qui est appuyée 0,1 ou 2
    -1 si aucune touche est enfoncée"""
    boutons = pygame.mouse.get_pressed()
    for i in range(3):
        if boutons[i]:
            return i
    return -1


def mouse_click_up()->bool:
    """return True when the mouse button move down to up for one loop only """
    return processing.__click_up


def mouse_click_down()->bool:
    """return True when the mouse button move up to down for one loop only """
    return processing.__click_down


def mouse_click()->bool:
    """return True if mouse button is down"""
    return processing.__click


def mouse_wheel_state() -> int:
    """Return 1 if the mouse wheel is turned up, -1 if the mouse wheel is turned down, and 0 if it is not turned."""
    return processing.__mouse_wheel


def redraw() -> None:
    """Force the screen to be redrawn."""
    pygame.display.update()


def events() -> list:
    return processing.__events


def run(globales):
    global __key_pressed, __click, __click_down, __click_up, keys, __quitter, var_globales, __frameCount, clock, secondes
    global __tempo_seconde, __tempo_centieme, centiemes, __events, __mouse_wheel, __resized, __quit_cross_enabled
    successes, failures = pygame.init()
    print("{0} successes and {1} failures".format(successes, failures))
    clock = pygame.time.Clock()
    if globales.get('setup'):
        globales['setup']()
    while True:
        clock.tick(__fps)
        __events = pygame.event.get()
        for event in __events:
            if event.type == pygame.QUIT and __quit_cross_enabled is True:
                __quitter = True
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
                Tor.reset_front()
                draw_background()
                globales['draw']()
                reset()
        if __quitter:
            if globales.get('exit'):
                globales['exit']()
            if __quitter:
                quit()

        pygame.display.update()  # Or pygame.display.flip()
        __frameCount += 1
        __click_down = False
        __click_up = False
        __mouse_wheel = 0
        __resized = False

def get_mouse_wheel()->int:
    """
    :rtype: int
    """
    return processing.__mouse_wheel

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
    """initialise l'axe de symétrie verticale"""
    processing.__flip_axe_v = axe_v


def get_flip_axe_v() -> [int, float]:
    """retourne l'axe de symétrie verticale"""
    return processing.__flip_axe_v


def set_flip_axe_h(axe_h: [int, float]):
    """initialise l'axe de symétrie horizontale"""
    processing.__flip_axe_h = axe_h


def get_flip_axe_h() -> [int, float]:
    """retourne l'axe de symétrie horizontale"""
    return processing.__flip_axe_h


def set_dx(translation_absolue_x: [int, float]):
    """initialise la valeur courant de la translation"""
    processing.__dx = translation_absolue_x


def get_dx() -> [int, float]:
    """retourne la valeur courant de la translation"""
    return processing.__dx


def set_dy(tanslation_absolue_y: [int, float]):
    """initialise la translation absolue en y"""
    processing.__dy = tanslation_absolue_y


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
    """ set scale parameter"""
    processing.__scale = echelle


def get_scale():
    """return scale parameter"""
    return processing.__scale


def get_background_color():
    """return background color"""
    return processing.__background_color


def get_background_image():
    """return background image"""
    return processing.__background_image


def set_background_image(image: Image):
    """set background image"""
    processing.__background_image = image

def get_quit():
    """get __quitter"""
    return processing.__quitter

def set_quit(value:bool):
    """set __quitter (True or False)"""
    processing.__quitter = value

def disabled_quit_cross():
    """disabled quit cross of windows"""
    processing.__quit_cross_enabled = False

def enabled_quit_cross():
    """enabled quit cross of windows"""
    processing.__quit_cross_enabled = True

def borner(valeur : [int,float],borne_mini: [int,float],borne_maxi: [int,float] )->[int,float]:
    return max(borne_mini, min(valeur, borne_maxi))
