import likeprocessing.processing as processing
import pygame
from pygame.colordict import THECOLORS as COLORS
from likeprocessing.pyDialog import Label


def textFont(police=None, taille=None):
    if police is not None:
        processing.set_font(police)
    if taille is not None:
        processing.set_font_size(taille)
    return processing.get_font(), processing.get_font_size()


def textSize(taille: int = None):
    if taille is not None:
        processing.set_font_size(taille)
    return processing.get_font_size()


def textCouleurCadre(couleur=None):
    if couleur is not None:
        processing.set_couleur_cadre_texte(couleur)
    return processing.get_couleur_bord_cadre_texte()


def text(texte: str, x, y, largeur=0, hauteur=0):
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
    h,v = align_h=textAlign()
    t = Label(None, (x, y, largeur, hauteur), texte, police, size,
              couleurBord=processing.get_couleur_bord_cadre_texte(), bold=b, italic=i,align_h=h,align_v=v)
    t.draw()


def textWidth(chaine: str) -> int:
    """retourne la largeur en pixels de l'affichage de chaine,
     dans la police et taille actuelles"""
    f = pygame.font.SysFont(*textFont())
    return f.size(chaine)[0]


def textStyle(style: str = None) -> str:
    if style is not None:
        processing.set_text_style(style.upper())
    return processing.get_text_style()


def textAlign(horizontal: str = None, vertical: str = None) -> tuple:
    if horizontal is not None:
        processing.set_text_align_h(horizontal)
    if vertical is not None:
        processing.set_text_align_v(vertical)
    return processing.get_text_align_h(), processing.get_text_align_v()
