import likeprocessing.processing as processing
import pygame
from pygame.colordict import THECOLORS as COLORS
from likeprocessing.pyDialog import Label


def textFont(police=None, taille=None) -> tuple:
    """change la police et la taille texte
    retourne la police et la taille du texte courante si aucun paramètre est passé"""
    if police is not None:
        processing.set_font(police)
    if taille is not None:
        processing.set_font_size(taille)
    return processing.get_font(), processing.get_font_size()


def textSize(taille: int = None):
    """change la taille texte
    retourne la taille du texte courante si aucun paramètre est passé"""
    if taille is not None:
        processing.set_font_size(taille)
    return processing.get_font_size()


def textCouleurCadre(couleur=None):
    """change la couleur du cadre du texte
    retourne la couleur du cadre du texte courante si aucun paramètre est passé"""
    if couleur is not None:
        processing.set_couleur_cadre_texte(couleur)
    return processing.get_couleur_bord_cadre_texte()


def text(texte: str, x, y, largeur=0, hauteur=0):
    """Ecrit le texte à la position x,y en fonction du style et de alignement courant"""
    if processing.__rect_center_mode:
        x -= largeur / 2
        y -= hauteur / 2
    police, size = textFont()
    if textStyle() == "BOLD":
        b = True
        i = False
    elif textStyle() == "ITALIC":
        b = False
        i = True
    elif textStyle() == "BOLDITALIC":
        b = True
        i = True
    else:
        b = False
        i = False
    h, v = align_h = textAlign()
    t = Label(None, (x + processing.__dx, y + processing.__dy, largeur, hauteur), texte, police, size,
              couleurFond=processing.get_fill_color(),
              couleurBord=processing.get_border_color(), largeurBord=processing.get_border_width(), bold=b, italic=i,
              align_h=h, align_v=v)
    t.draw()


__border_width = 1
__fill_color = (255, 255, 255)
__border_color = (0, 0, 0)


def textWidth(chaine: str) -> int:
    """retourne la largeur en pixels de l'affichage de chaine,
     dans la police et taille actuelles"""
    f = pygame.font.SysFont(*textFont())
    return f.size(chaine)[0]


def textStyle(style: str = None) -> str:
    """change le style du texte
    NORMAL BOLD ITALIC BOLDITALIC
    retourne le style courant si aucun paramètre est passé"""
    if style is not None:
        processing.set_text_style(style.upper())
    return processing.get_text_style()


def textAlign(horizontal: str = None, vertical: str = None) -> tuple:
    """change l'alignment du texte
    horizontal : LEFT CENTER RIGHT
    veritcal : TOP CENTER BOTTOM
    retourne l'alignement courant si aucun paramètre est passé"""
    if horizontal is not None:
        processing.set_text_align_h(horizontal)
    if vertical is not None:
        processing.set_text_align_v(vertical)
    return processing.get_text_align_h(), processing.get_text_align_v()
