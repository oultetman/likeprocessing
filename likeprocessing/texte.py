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
    width = 0
    height = 0
    margin_left = kwargs.get("margin_left", 0)
    margin_top = kwargs.get("margin_top", 0)
    margin_right = kwargs.get("margin_right", 2)
    margin_bottom = kwargs.get("margin_bottom", 2)
    extend = kwargs.get("extend", True)

    for t in texte.split("\n"):
        text_bitmap.append(ps.render(t, True, processing.rgb_color(color)))
        r = text_bitmap[-1].get_rect()
        width = max(width, r.width)
        height = height + r.height
    # if not extend:
    image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    # else:
    #     image = pygame.Surface((largeur, hauteur), pygame.SRCALPHA, 32)
    yi = 0
    xi = 0
    for l in text_bitmap:
        if kwargs["align_h"].upper() == "CENTER":
            xi = (width - l.get_width()) // 2
        elif kwargs["align_h"].upper() == "RIGHT":
            xi = (width - l.get_width())
        image.blit(l, (xi, yi))
        yi += l.get_height()
    if extend or largeur <= 0:
        largeur = max(largeur, width + 2 * padx)
    if extend or hauteur <= 0:
        hauteur = max(hauteur, height + 2 * pady)
    image2 = pygame.Surface((largeur, hauteur), pygame.SRCALPHA, 32)
    yi = margin_top + pady
    xi = margin_left + padx
    if kwargs["align_h"].upper() == "CENTER":
        xi = (largeur - image.get_width()) // 2
    elif kwargs["align_h"].upper() == "RIGHT":
        xi = -margin_right + (largeur - image.get_width())
    if kwargs["align_v"].upper() == "CENTER":
        yi = (hauteur - image.get_height()) // 2
    elif kwargs["align_v"].upper() == "BOTTOM":
        yi = -margin_bottom + (hauteur - image.get_height())
    image2.blit(image, (xi, yi))
    processing.rect(x, y, largeur, hauteur, **kwargs)
    kwargs["no_stroke"] = True
    kwargs["no_fill"] = True
    processing.rect(x, y, largeur, hauteur, image=image2, **kwargs)


__border_width = 1
__fill_color = (255, 255, 255)
__border_color = (0, 0, 0)


def text_button(texte: [str, int, float], x, y, largeur=0, hauteur=0, **kwargs):
    """Crée un bouton avec le texte passé en paramètre"""
    if largeur == 0 or hauteur == 0:
        kwargs["padx"] = kwargs.get("padx", 5)
        kwargs["pady"] = kwargs.get("pady", 5)
    kwargs["align_h"] = "center"
    kwargs["align_v"] = "center"
    kwargs["command"] = kwargs.get("command", None)
    kwargs["name"] = kwargs.get("name", None)
    kwargs["fill_mouse_on"] = kwargs.get("fill_mouse_on", "grey")
    text(texte, x, y, largeur, hauteur, **kwargs)


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
