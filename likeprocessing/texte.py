import likeprocessing.processing as processing
import pygame


def textFont(police=None, taille=None) -> tuple:
    """change la police et la taille texte et retourne la valeur précédente de la police et de la taille du texte
    retourne la police et la taille du texte courante si aucun paramètre est passé"""
    ps = processing.get_font(), processing.get_font_size()
    if police is not None:
        processing.set_font(police)
    if taille is not None:
        processing.set_font_size(taille)
    return ps


def textSize(taille: int = None):
    """change la taille texte et retourne la valeur précédente de la taille
    retourne la taille du texte courante si aucun paramètre est passé"""
    t = processing.get_font_size()
    if taille is not None:
        processing.set_font_size(taille)
    return t


def textCouleurCadre(couleur=None):
    """change la couleur du cadre du texte et retourne la valeur précédente de la couleur
    retourne la couleur du cadre du texte courante si aucun paramètre est passé"""
    c = processing.get_couleur_bord_cadre_texte()
    if couleur is not None:
        processing.set_couleur_cadre_texte(couleur)
    return c


def text(texte: [str, int, float], x, y, largeur=0, hauteur=0, **kwargs):
    """Ecrit le texte à la position x,y en fonction du style et de alignement courant"""
    texte = str(texte)
    font = kwargs.get("font", processing.get_font())
    size = kwargs.get("font_size", processing.get_font_size())
    color = kwargs.get("font_color", processing.get_font_color())
    padx = kwargs.get("padx", 0)
    pady = kwargs.get("pady", 0)
    padxy = kwargs.get("padxy", 0)

    style = kwargs.get("style", textStyle())
    if padxy > 0:
        padx = pady = padxy
    no_stroke = kwargs.get("no_stroke", False)
    if no_stroke is True:
        stroke_weight = 0
    if style.upper() == "BOLD":
        b = True
        i = False
    elif style.upper() == "ITALIC":
        b = False
        i = True
    elif style.upper() == "BOLDITALIC":
        b = True
        i = True
    else:
        b = False
        i = False
    h, v = textAlign()
    kwargs["align_h"] = kwargs.get("align_h", h)
    kwargs["align_v"] = kwargs.get("align_v", v)
    ps = pygame.font.SysFont(font, size, bold=b, italic=i)
    text_bitmap = ps.render(texte, True, processing.rgb_color(color))
    text_bitmap = []
    width = largeur
    height = 0
    for t in texte.split("\n"):
        text_bitmap.append(ps.render(t, True, processing.rgb_color(color)))
        r = text_bitmap[-1].get_rect()
        width = max(width, r.width)
        height = height + r.height
    image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    yi = 0
    xi = 0
    for l in text_bitmap:
        if kwargs["align_h"].upper() == "CENTER":
            xi = (width - l.get_width()) // 2
        elif kwargs["align_h"].upper() == "RIGHT":
            xi = - 2 + (width - l.get_width())
        image.blit(l, (xi, yi))
        yi += l.get_height()
    largeur = max(largeur,width+2*padx)
    hauteur= max(hauteur,height+2*pady)
    processing.rect(x, y, largeur, hauteur, **kwargs)
    kwargs["no_stroke"] = True
    kwargs["no_fill"] = True
    processing.rect(x + padx, y + pady, largeur - 2 * padx, hauteur - 2 * pady, image=image, **kwargs)

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
    et retourne alignement precedent
    retourne l'alignement courant si aucun paramètre est passé"""
    align = processing.get_text_align_h(), processing.get_text_align_v()
    if horizontal is not None:
        processing.set_text_align_h(horizontal)
    if vertical is not None:
        processing.set_text_align_v(vertical)
    return align


if __name__ == '__main__':
    p = textFont("arial", 20)
    print(p, textFont(*p))
    print(textFont())
    al = textAlign("center", "center")
    print(al, textAlign(*al))
