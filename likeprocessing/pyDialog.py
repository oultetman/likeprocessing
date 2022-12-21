import likeprocessing.processing as processing
import likeprocessing.affichage as affichage
import os.path
import pygame
from pygame.constants import *
import pygame_textinput
from likeprocessing.print_vars import *
from likeprocessing.texte import *
import tkinter as tk
from tkinter import filedialog
from likeprocessing.images import loadImage

pygame.font.init()
# from likeprocessing.couleur import *
import os


def filedialogbox():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


class Boite(pygame.Rect):
    ecran = None

    def __init__(self, parent, rect, **kwargs):
        if parent is None:
            self.Parent = pygame.Rect((0, 0, Boite.ecran.get_width(), Boite.ecran.get_height()))
        else:
            self.Parent = parent
        super().__init__(rect)
        self.stroke = kwargs.get("stroke", "black")
        self.fill = kwargs.get("fill", "white")
        self.stroke_weight = kwargs.get("stroke_weight", 1)
        self.infobulle = kwargs.get("tool_tips", "")
        self._expand = kwargs.get("expand", None)
        self.expend()
        self.affiche_tool_tips = False
        self.fillDisabled = kwargs.get('fillDisabled', affichage.rgb_color("grey"))
        self.strokeDisabled = kwargs.get("fill", affichage.rgb_color("grey90"))
        self.image_rect: pygame.surface = kwargs.get('image', None)
        self.destroy = False
        self.is_disabled = kwargs.get('disabled', False)
        self.x_bulle = self.x
        self.y_bulle = self.y
        self.tick = 0
        self.name = kwargs.get('name', None)
        if kwargs.get('no_fill', False):
            self.fill = None
        if kwargs.get('no_stroke', False):
            self.stroke_weight = 0
        self._visible = True
        # if isinstance(self.parent, Dialog) and self.parent.cadre:
        # if not isinstance(self.parent, pygame.Rect):
        try:
            self.top += self.parent.decy
            pass
        except:
            pass

    def init(screen: pygame.Surface):
        Boite.ecran = screen

    def expend(self):
        if self._expand is not None:
            if self._expand.upper() == "X":
                self.width = self.parent.width - 4
                self.x = 2
            elif self._expand.upper() == "Y":
                self.height = self.parent.height - 4
                self.y = 2
            elif self._expand.upper() == "XY":
                self.width = self.parent.width - 4
                self.x = 2
                self.height = self.parent.height - 4
                self.y = 2

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value

    @property
    def parent(self):
        return self.Parent

    @parent.setter
    def parent(self, monPere):
        self.Parent = monPere

    def setX(self, value: int):
        self.x = value  # + self.parent.x

    def setY(self, value: int):
        self.y = value  # + self.parent.y

    def move(self, x: int, y: int):
        self.setX(x)
        self.setY(y)

    def draw(self):
        if self.visible:
            if processing.get_resized():
                self.expend()
            if self.is_disabled is True:
                couleur_bord = self.strokeDisabled
                couleur_fond = self.fillDisabled
            else:
                couleur_bord = self.stroke
                couleur_fond = self.fill

            if self.image_rect is None:
                if self.fill is not None:
                    r = pygame.Surface((self.width, self.height))
                    r.fill(couleur_fond)
                else:
                    r = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
                    r = r.convert_alpha()
                Boite.ecran.blit(r, [self.parent.left + self.left, self.parent.top + self.top])
            else:
                Boite.ecran.blit(self.image_rect, (self.parent.left + self.left, self.parent.top + self.top),
                                 (0, 0, self.image_rect.get_width(), self.image_rect.get_height()))
            if self.stroke_weight > 0:
                r = pygame.Rect(self.parent.left + self.left, self.parent.top + self.top, self.width, self.height)
                pygame.draw.rect(Boite.ecran, couleur_bord, r, self.stroke_weight)

    def draw_infobulle(self):
        if self.affiche_tool_tips and self.tick < 100:
            processing.triangle(self.x_bulle, self.y_bulle, self.x_bulle + 5, self.y_bulle - 20,
                                self.x_bulle + 10, self.y_bulle - 10, fill="#EFF67B", no_stroke=True)
            tool_tips = MultiLineText(None, (self.x_bulle, self.y_bulle), self.infobulle,
                                      fill="#EFF67B", padx=5, no_stroke=True)
            tool_tips.bottom = tool_tips.y - 10
            tool_tips.left = tool_tips.x + 5
            tool_tips.draw()
        self.tick += 1

    def collidepoint(self, x, y):
        return super().collidepoint(x - self.parent.left, y - self.parent.top)

    def scan_mouse(self):
        """gestion des bulles d'info"""
        x, y = processing.mouseXY()
        if self.collidepoint(x, y):
            if self.infobulle != "":
                self.affiche_tool_tips = True
                self.x_bulle, self.y_bulle = x, y
        else:
            self.affiche_tool_tips = False
            self.tick = 0

    def scanKeyboard(self):
        pass


class MultiLineText(Boite):
    def __init__(self, parent, rect, texte, angle=0, **kwargs):
        if len(rect) == 2:
            rect = (rect[0], rect[1], 0, 0)
        elif len(rect) == 3:
            rect = (rect[0], rect[1], rect[2], 0)
        super().__init__(parent, rect, **kwargs)
        self._texte = texte.split("\n")
        self.stroke = kwargs.get("stroke", "black")
        self.stroke_weight = kwargs.get("stroke_weight", 1)
        if kwargs.get("no_stroke", False):
            self.stroke_weight = 0
        self.fill = kwargs.get("fill", None)
        self.police = kwargs.get("font", "arial")
        self.taille = kwargs.get("font_size", 12)
        self._couleurPolice = kwargs.get("font_color", "black")
        self.bold = kwargs.get('bold', None)
        self.italic = kwargs.get('italic', None)
        self.align_v = kwargs.get('align_v', "TOP").upper()
        self.align_h = kwargs.get('align_h', "LEFT").upper()
        self.padx = kwargs.get('padx', 0)
        self.pady = kwargs.get('pady', 0)
        self.angle = angle
        self.image = self.imageTexte()

    def text(self, texte: [str, None] = None):
        if texte is None:
            return self._texte
        self._texte = texte.split("\n")
        self.image = self.imageTexte()

    @property
    def couleurPolice(self):
        return self._couleurPolice

    @couleurPolice.setter
    def couleurPolice(self, couleur: tuple):
        self._couleurPolice = couleur
        self.image = self.imageTexte()

    def imageTexte(self):
        rec_font = pygame.font.SysFont(self.police, self.taille, bold=self.bold, italic=self.italic)
        text_bitmap = []
        width = 0
        height = 0
        for t in self._texte:
            text_bitmap.append(rec_font.render(t, True, self.couleurPolice))
            r = text_bitmap[-1].get_rect()
            width = max(width, r.width)
            height = height + r.height
        image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        y = 0
        x = 0
        for l in text_bitmap:
            if self.align_h == "LEFT":
                x = 0
            elif self.align_h == "CENTER":
                x = (width - l.get_width()) // 2
            elif self.align_h == "RIGHT":
                x = - 2 + (width - l.get_width())
            image.blit(l, (x, y))
            y += l.get_height()
        if self.angle != 0:
            image = pygame.transform.rotate(image, self.angle)
            width = image.get_width()
            height = image.get_height()
        self.width = max(width + 4, self.width) + 2 * self.padx
        self.height = max(height + 4, self.height) + 2 * self.pady
        return image

    def draw(self):
        if self.visible:
            # fonction qui permet l'affichage de texte à  l'ecran
            super().draw()
            if self.align_h == "LEFT":
                x = self.parent.left + self.left + 2 + self.padx
            elif self.align_h == "CENTER":
                x = self.parent.left + self.left + (self.width - self.image.get_width()) // 2
            elif self.align_h == "RIGHT":
                x = self.parent.left + self.left - 2 - self.padx + (self.width - self.image.get_width())
            if self.align_v == "TOP":
                y = self.parent.top + self.top + 2 + self.pady
            elif self.align_v == "CENTER":
                y = self.parent.top + self.top + (self.height - self.image.get_height()) // 2
            elif self.align_v == "BOTTOM":
                y = self.parent.top + self.top - 2 - self.pady + (self.height - self.image.get_height())
            Boite.ecran.blit(self.image, [x, y])
            self.draw_infobulle()

    def setWidth(self, value: int):
        self.width = value
        self.image = self.imageTexte()

    def __str__(self):
        return super().__str__() + " " + str(self.text)


class Label(Boite):
    """affiche un texte sur une ligne dans une boite"""

    def __init__(self, parent, rect, texte: str, angle=0, **kwargs):
        if len(rect) == 2:
            rect = (rect[0], rect[1], 0, 0)
        elif len(rect) == 3:
            rect = (rect[0], rect[1], rect[2], 0)
        # stroke_weight = kwargs.get("stroke_weight", 0)
        # stroke = kwargs.get("stroke", None)
        # if stroke is not None and stroke_weight == 0:
        #     stroke_weight = 1
        # fill = kwargs.get("fill", None)
        kwargs["stroke"] = kwargs.get("stroke", None)
        kwargs["stroke_weight"] = kwargs.get("stroke_weight", 0)
        if kwargs.get("stroke") is not None:
            kwargs["stroke_weight"] = 1
        kwargs["fill"] = kwargs.get("fill", None)
        kwargs["font"] = kwargs.get("font", "arial")
        kwargs["font_size"] = kwargs.get("font_size", 12)
        kwargs["font_color"] = kwargs.get("font_color", "black")
        self.bold = kwargs.get('bold', None)
        self.italic = kwargs.get('italic', None)
        self.align_v = kwargs.get('align_v', "TOP").upper()
        self.align_h = kwargs.get('align_h', "LEFT").upper()
        self.padx = kwargs.get('padx', 0)
        self.pady = kwargs.get('pady', 0)
        self.align_h = kwargs.get('align_h', "LEFT").upper()
        super().__init__(parent, rect, **kwargs)
        self._texte = texte
        self.police = kwargs["font"]
        self.taille = kwargs["font_size"]
        self.couleurPolice = kwargs.get("font_color", "black")
        self.couleurPoliceEnabled = kwargs.get("font_color", "black")
        self.couleurPoliceDisabled = (128, 128, 128)
        self.angle = angle
        self.image = self.imageTexte()
        self._enabled = True

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        if self._enabled:
            self.couleurPolice = self.couleurPoliceEnabled
        else:
            self.couleurPolice = self.couleurPoliceDisabled
        self.image = self.imageTexte()

    def setWidth(self, value: int):
        self.width = value
        self.image = self.imageTexte()

    def text(self, texte: [str, None] = None):
        if texte is None:
            return self._texte
        self._texte = texte
        self.image = self.imageTexte()

    def imageTexte(self):
        rec_font = pygame.font.SysFont(self.police, self.taille, bold=self.bold, italic=self.italic)
        text_bitmap = rec_font.render(self._texte, True, self.couleurPolice)
        r = text_bitmap.get_rect()
        self.height = max(self.height, r.height + 4) + 2 * self.pady
        if self.width == 0 or self.padx > 0:
            self.width = r.width + 4 + 2 * self.padx
        elif r.width > self.width - 4:
            r.width = self.width - 4
            text_bitmap = text_bitmap.subsurface(r)

        return text_bitmap

    def draw(self):
        if self.visible:
            # fonction qui permet l'affichage de texte à  l'ecran
            if self.angle != 0:
                img = pygame.transform.rotate(self.image, self.angle)
                self.width = max(img.get_width(), self.width) + 2 * self.padx
                self.height = max(img.get_height(), self.height) + 2 * self.pady
            else:
                img = self.image
            super().draw()
            if self.align_h == "LEFT":
                x = self.parent.left + self.left + 2 + self.padx
            elif self.align_h == "CENTER":
                x = self.parent.left + self.left + (self.width - self.image.get_width()) // 2
            elif self.align_h == "RIGHT":
                x = self.parent.left + self.left - 2 - self.padx + (self.width - self.image.get_width())
            if self.align_v == "TOP":
                y = self.parent.top + self.top + 2 + self.pady
            elif self.align_v == "CENTER":
                y = self.parent.top + self.top + (self.height - self.image.get_height()) // 2
            elif self.align_v == "BOTTOM":
                y = self.parent.top + self.top - 2 - self.pady + (self.height - self.image.get_height())
            Boite.ecran.blit(img, [x, y])
            self.draw_infobulle()

    def __str__(self):
        return super().__str__() + " " + str(self.text)


class TextEdit(Boite):
    """permet de créer un texte sur plusieurs ligne"""

    def __init__(self, parent, rect, texte: str, **kwargs):
        kwargs["stroke"] = kwargs.get("stroke", affichage.rgb_color("black"))
        kwargs["stroke_weight"] = kwargs.get("stroke_weight", 1)
        kwargs["fill"] = kwargs.get("fill", affichage.rgb_color("white"))
        kwargs["font"] = kwargs.get("font", "arial")
        kwargs["font_size"] = kwargs.get("font_size", 12)
        nb_ligne = kwargs.get('nb_ligne', 10)
        ps = pygame.font.SysFont(kwargs["font"], kwargs["font_size"])
        h = ps.size("bg")[0]
        rect = tuple(list(rect[:3]) + [(4 + h) * nb_ligne + 4])
        if parent is None:
            processing.ihm.append(self)
        super().__init__(parent, rect, **kwargs)
        self.police = kwargs["font"]
        self.texte = texte.split("\n")
        self.nb_ligne = nb_ligne
        self.ligne_actuelle = 0
        if self.nb_ligne > len(self.texte):
            self.texte += ["" for i in range(self.nb_ligne - len(self.texte))]
        self.lignes = [
            LineEdit(self, (2, 2 + (4 + h) * i, self.width - 4, (4 + h)), self.texte[i], **kwargs, name=i) for i in
            range(self.nb_ligne)]
        self.decalage = 0
        self._focus = False
        self.focus = False
        self.mouseOn = False

        self.key_tempo = processing.Tempo(100)

    def draw(self):
        if self.visible:
            super().draw()
            for l in self.lignes:
                l.draw()

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, val: bool):
        if val is False:
            self._focus = False
            self.lignes[self.ligne_actuelle].focus = False
            self.lignes[self.ligne_actuelle].texte.cursor_visible = False
        else:
            self._focus = True
            self.parent.objet_focus = True
        if self.focus:
            self.stroke = "blue"
        else:
            self.stroke = "black"

    def ajoute_ligne(self):
        self.lignes[self.ligne_actuelle].focus = False
        self.ligne_actuelle += 1
        self.lignes[self.ligne_actuelle].focus = True
        self.texte.insert(self.ligne_actuelle + self.decalage, "")
        self.texte_vers_ligne()

    def texte_vers_ligne(self):
        for i in range(self.nb_ligne):
            self.lignes[i].set_text(self.texte[i + self.decalage])
        self.nb_ligne = len(self.lignes)

    def ligne_vers_texte(self):
        for i in range(self.nb_ligne):
            self.texte[i + self.decalage] = self.lignes[i].text()

    def supprime_ligne(self):
        self.lignes[self.ligne_actuelle].focus = False
        self.texte.pop(self.ligne_actuelle + self.decalage)
        if self.ligne_actuelle > 0:
            self.ligne_actuelle -= 1
        self.lignes[self.ligne_actuelle].focus = True
        if self.nb_ligne > len(self.texte):
            self.texte.append("")
        self.texte_vers_ligne()
        pass

    def scan_mouse(self):
        x, y = processing.mouseXY()
        click = processing.mouse_click()
        if self.collidepoint(x, y):
            self.mouseOn = True
        else:
            self.mouseOn = False
        if self.mouseOn and click is True:
            self.parent.lostFocus()
            self.focus = True

    def scan_events(self):
        if self.is_disabled is False:
            self.scan_mouse()
            for l in self.lignes:
                l.scan_mouse()
            if self.focus:
                if processing.keyIsPressed() and self.key_tempo.fin():
                    if (processing.keyIsDown(K_UP) or processing.keyIsDown(K_LEFT) and self.lignes[
                        self.ligne_actuelle].texte.manager.cursor_pos == 0
                    ) and self.ligne_actuelle > 0:
                        if processing.keyIsDown(K_UP):
                            pos_cur = self.lignes[self.ligne_actuelle].texte.manager.cursor_pos
                        else:
                            pos_cur = len(self.texte)
                        self.lignes[self.ligne_actuelle].focus = False
                        self.ligne_actuelle -= 1
                        self.lignes[self.ligne_actuelle].focus = True
                        self.lignes[self.ligne_actuelle].texte.manager.cursor_pos = pos_cur

                    elif processing.keyIsDown(K_DOWN) and self.ligne_actuelle < len(self.lignes) - 1:
                        pos_cur = self.lignes[self.ligne_actuelle].texte.manager.cursor_pos
                        self.lignes[self.ligne_actuelle].focus = False
                        self.ligne_actuelle += 1
                        self.lignes[self.ligne_actuelle].focus = True
                        self.lignes[self.ligne_actuelle].texte.manager.cursor_pos = pos_cur
                    elif processing.keyIsDown(K_RETURN):
                        if self.lignes[self.ligne_actuelle].texte.manager.cursor_pos == 0:
                            self.ligne_actuelle -= 1
                        self.ajoute_ligne()
                    elif processing.keyIsDown(K_BACKSPACE) and len(self.lignes[self.ligne_actuelle]) == 0:
                        self.supprime_ligne()
                    else:
                        for l in self.lignes:
                            if l.focus:
                                l.texte.update(processing.events())

                self.ligne_vers_texte()

    def is_focused(self) -> int:
        for i in range(len(self.lignes)):
            if self.lignes[i].focus:
                return i

    def text(self) -> list:
        return self.texte

    def set_text(self, texte: str):
        texte = texte.split("\n")
        if self.nb_ligne > len(texte):
            texte += ["" for i in range(self.nb_ligne - len(texte))]
        for i, l in enumerate(self.lignes):
            l.set_text(texte[i])


class LineEdit(Boite):
    """permet de créer un champs éditable sur une ligne"""
    LINE_EDIT_FOND = affichage.rgb_color("white")
    LINE_EDIT_FOND_DISABLED = affichage.rgb_color("grey")
    LINE_EDIT_BORD = affichage.rgb_color("black")
    LINE_EDIT_BORD_DISABLED = affichage.rgb_color("grey90")
    LINE_EDIT_TEXT_COLOR = affichage.rgb_color("black")
    LINE_EDIT_TEXT_COLOR_DISABLED = affichage.rgb_color("grey90")

    def __init__(self, parent, rect, texte: str, **kwargs):
        kwargs["stroke"] = kwargs.get("stroke", LineEdit.LINE_EDIT_BORD)
        kwargs["stroke_weight"] = kwargs.get("stroke_weight", 1)
        kwargs["fill"] = kwargs.get("fill", LineEdit.LINE_EDIT_FOND)
        kwargs["font"] = kwargs.get("font", "arial")
        kwargs["font_size"] = kwargs.get("font_size", 12)
        kwargs["font_color"] = kwargs.get("font_color", "black")
        name = kwargs.get('name', None)
        if parent is None:
            processing.ihm.append(self)
        elif isinstance(parent, TextEdit):
            kwargs["stroke_weight"] = 0
        ps = pygame.font.SysFont(kwargs["font"], kwargs["font_size"])
        h = ps.size("bg")[0]
        if len(rect) == 3:
            rect = tuple(list(rect[:3]) + [h + 8])
        elif len(rect) == 4:
            rect = tuple(list(rect[:3]) + [max(h + 4, rect[3])])
        super().__init__(parent, rect, **kwargs)
        ft = pygame.font.SysFont(kwargs["font"], kwargs["font_size"])
        manager = pygame_textinput.TextInputManager(initial=texte)
        self.texte: pygame_textinput.TextInputVisualizer = pygame_textinput.TextInputVisualizer(font_object=ft,
                                                                                                manager=manager,
                                                                                                font_color=kwargs[
                                                                                                    "font_color"])
        self.texte.input_string = texte
        self.texte.cursor_width = 2
        self._focus = False
        self.mouseOn = False
        self.name = name
        self.t = processing.Tempo(100)
        self.fonction = kwargs.get("command", None)

    def connecte(self, fonction):
        self.fonction = fonction

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, val: bool):
        if val is not self._focus:
            self._focus = not self._focus
            self.texte.focus = self._focus
        if self.focus:
            self.stroke = "blue"
            self.texte.cursor_visible = True
        else:
            self.stroke = "black"
            self.texte.cursor_visible = False

    def scan_events(self, events):
        if self.is_disabled is False:
            self.scan_mouse()
            if self.focus:
                text = self.texte.value
                self.texte.update(events)
                if self.fonction is not None and text != self.texte.value:
                    self.fonction(self)
            else:
                self.texte.cursor_visible = False
        else:
            self.focus = False
            self.texte.cursor_visible = False

    def draw(self):
        if self.visible:
            # if self.is_disabled is True:
            #     self.stroke = LineEdit.LINE_EDIT_BORD_DISABLED
            #     self.fill = LineEdit.LINE_EDIT_FOND_DISABLED
            # else:
            #     self.stroke = LineEdit.LINE_EDIT_BORD
            #     self.fill = LineEdit.LINE_EDIT_FOND
            super().draw()
            # Boite.ecran.blit(self.texte.get_surface(), (self.Parent.left + self.left + 3, self.Parent.top + self.top))
            dec = (self.height - self.texte.surface.get_height()) / 2
            Boite.ecran.blit(self.texte.surface, (self.parent.left + self.left + 3, self.parent.top + self.top + dec))
            self.draw_infobulle()

    def __str__(self):
        # return self.texte.input_string
        return self.texte.value

    def __len__(self):
        # return len(self.texte.input_string)
        return len(self.texte.value)

    def scan_mouse(self):
        if self.is_disabled is False:
            super().scan_mouse()
            x, y = processing.mouseXY()
            click = processing.mouse_click()
            if self.collidepoint(x, y):
                self.mouseOn = True
            else:
                self.mouseOn = False
                if processing.mouse_click_down():
                    self.focus = False
            if self.mouseOn and click is True and self.focus is False:
                if not isinstance(self.parent, TextEdit):
                    self.parent.lostFocus()
                self.focus = True
                self.parent.objet_focus = True
                # positionne le curseur au niveau de la souris
                c = 0
                while self.texte.font_object.size(self.texte.value[0:c])[0] < x - self.parent.x - self.x and c <= len(
                        self):
                    c += 1
                self.texte.manager.cursor_pos = c - 1
                # *************************
                if isinstance(self.parent, TextEdit):
                    self.parent.ligne_actuelle = self.name
            self.texte.cursor_visible = self.focus
        else:
            self.focus = False

    def text(self, texte: [str, None] = None):
        if texte is None:
            return self.texte.value
        self.set_text(texte)

    def set_text(self, texte: str):
        self.texte.value = str(texte)
        self.texte.update([])
        self.texte.cursor_visible = False


class Bouton(Boite):
    BOUTON_FOND = affichage.rgb_color("white")
    BOUTON_FOND_MOUSE_ON = (229, 241, 251)
    BOUTON_BORD = affichage.rgb_color("gray68")
    BOUTON_BORD_MOUSE_ON = (0, 120, 215)
    BOUTON_FOND_DISABLED = affichage.rgb_color("grey")
    BOUTON_TEXT_COLOR = affichage.rgb_color("black")
    BOUTON_TEXT_COLOR_DISABLED = affichage.rgb_color("grey90")

    def __init__(self, parent, rect, texte, defaut=False, **kwargs):
        if defaut:
            b = 2
        else:
            b = 1
        if len(rect) == 2:
            rect = (rect[0], rect[1], 0, 0)
        elif len(rect) == 3:
            rect = (rect[0], rect[1], rect[2], 0)
        # if kwargs.get('no_fill', False):
        #     raise KeyError("no_fill is not Bouton property")
        # if kwargs.get('no_stroke', False):
        #     raise KeyError("no_stroke is not Bouton property")
        kwargs["align_v"] = kwargs.get("align_v", "center")
        kwargs["align_h"] = kwargs.get("align_h", "center")
        super().__init__(parent, rect, **kwargs)
        self.fonction = kwargs.get("command", None)
        self.mouseOn = False
        self.mouseClick = False
        self.texte = MultiLineText(self, (2, 2, self.width - 4, self.height - 4), texte, **kwargs)
        # self.width = max(self.width, self.texte.width + 4)
        self.height = max(self.height, self.texte.height + 4)
        # self.texte.left = self.left + (self.width - self.texte.width) // 2
        # self.texte.top = self.top + (self.height - self.texte.height) // 2
        self.forced = False
        self.texte.left = self.left + 2
        self.texte.top = self.top + 2
        self.focus = False

    def setX(self, value: int):
        self.x = value
        self.texte.left = self.left + (self.width - self.texte.width) // 2

    def setY(self, value: int):
        self.y = value  # + self.parent.y
        self.texte.top = self.top + (self.height - self.texte.height) // 2

    def setWidth(self, value: int):
        self.width = value  # + self.parent.y
        self.texte.setWidth(value - 4)

    def text(self, texte: [str, None] = None):
        if texte is None:
            return self.texte.text()
        self.texte.text(texte)
        self.width = max(self.width, self.texte.width + 4)
        self.height = max(self.height, self.texte.height + 4)

    @property
    def parent(self):
        return self.Parent

    @parent.setter
    def parent(self, monPere):
        self.Parent = monPere
        self.texte.parent = monPere

    def connecte(self, fonction):
        self.fonction = fonction

    def draw(self):
        if self.visible:
            if self.is_disabled:
                self.fill = Bouton.BOUTON_FOND_DISABLED
                self.texte.fill = Bouton.BOUTON_FOND_DISABLED
                self.texte.stroke = Bouton.BOUTON_FOND_DISABLED
                self.texte.couleurPolice = Bouton.BOUTON_TEXT_COLOR_DISABLED
                self.stroke = Bouton.BOUTON_TEXT_COLOR_DISABLED
            else:
                self.texte.couleurPolice = Bouton.BOUTON_TEXT_COLOR
                if self.forced:
                    self.fill = Bouton.BOUTON_BORD_MOUSE_ON
                    self.texte.fill = Bouton.BOUTON_BORD_MOUSE_ON
                    self.texte.stroke = Bouton.BOUTON_BORD_MOUSE_ON
                elif self.mouseOn:
                    self.stroke = Bouton.BOUTON_BORD_MOUSE_ON
                    if self.mouseClick:
                        self.fill = Bouton.BOUTON_BORD_MOUSE_ON
                        self.texte.fill = Bouton.BOUTON_BORD_MOUSE_ON
                        self.texte.stroke = Bouton.BOUTON_BORD_MOUSE_ON
                    else:
                        self.fill = Bouton.BOUTON_FOND_MOUSE_ON
                        self.texte.fill = Bouton.BOUTON_FOND_MOUSE_ON
                        self.texte.stroke = Bouton.BOUTON_FOND
                else:
                    self.stroke = Bouton.BOUTON_BORD
                    self.fill = Bouton.BOUTON_FOND
                    self.texte.fill = Bouton.BOUTON_FOND
                    self.texte.stroke = Bouton.BOUTON_FOND

            super().draw()
            self.texte.draw()
            self.draw_infobulle()

    def scan_mouse(self):
        if self.is_disabled is False and self.visible is True:
            super().scan_mouse()
            x, y = processing.mouseXY()
            click = processing.mouse_click()
            if self.collidepoint(x, y):
                self.parent.lostFocus()
                self.mouseOn = True
                self.focus = True
            else:
                self.mouseOn = False
                self.focus = False
            if click is False and self.mouseClick is True:
                self.mouseClick = False
                if self.mouseOn is True and self.fonction is not None:
                    if self.name is None:
                        self.fonction()
                    else:
                        self.fonction(self.name)
            elif click is True and self.mouseOn is True:
                self.mouseClick = True
        else:
            self.focus = False

    def __str__(self):
        return f"Bouton : {super().__str__()} {self.texte} {self.parent}"


class Dialog(Boite):
    """Classe qui permet de créer une boite de dialogue vide
    munie d'une barre de titre et d'une casse de fermeture"""
    dialogue = 1
    FOND = (255, 255, 255)
    BORD = (150, 150, 150)
    LARGEUR_BORD = 1

    def __init__(self, parent, rect, **kwargs):
        kwargs["stroke"] = kwargs.get("stroke", Dialog.BORD)
        kwargs["stroke_weight"] = kwargs.get("stroke_weight", Dialog.LARGEUR_BORD)
        kwargs["fill"] = kwargs.get("fill", Dialog.FOND)
        kwargs["title"] = kwargs.get("title", "Dialog" + str(Dialog.dialogue))
        super().__init__(parent, rect, **kwargs)
        Dialog.dialogue += 1
        self.num_object = 1
        self.pos = kwargs.get('pos', None)
        self.objet = {}
        self.destroyed = []
        self.cadre = kwargs.get('cadre', True)
        self.frame = kwargs.get('frame', False)
        self.decy = 0
        if self.frame:
            self.cadre = False
            # dialogue type frame
            self.fill = self.parent.fill
            self.stroke_weight = 0
            self.addObjet(Boite(self, (0, 9, self.width, self.height - 9), fill=self.fill), "frame_cadre")
            self.addObjet(
                Label(self, (7, 1, 0, 0), kwargs["title"], fill=self.fill), "frame_title")
            self.decy = self.objet_by_name("frame_title").height + 1

        elif self.cadre:
            self.addObjet(
                Boite(self, (2, 2, self.width - 19, 22), stroke=Dialog.BORD, stroke_weight=1,
                      fill="lightblue"),
                "title_box")
            self.addObjet(
                Label(self, (2, 2, self.width - 19, 22), kwargs["title"], align_v="center"),
                "title")
            self.addObjet(Bouton(self, (self.width - 17, 2, 16), "X"), "close")
            self.objet['close'].connecte(self.quitter)
            self.decy = 25

        self._visible = True
        self.start_drop = None
        self.destroy = False
        self._focus = False
        self.modale = False
        self.positionne()
        self.objet_focus = False

    def __str__(self):
        return f"Dialog : {super()}"

    def positionne(self):
        if self.pos == "center":
            self.center_me()

    def center_me(self):
        """center la boite sur l'écran"""
        self.x = (self.parent.width - self.width) // 2
        self.y = (self.parent.height - self.height) // 2

    def quitter(self):
        self._visible = False
        self.focus = False
        self.destroy = True

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, value: bool):
        self._focus = value
        if self.cadre is True:
            self.objet['title'].enabled = self._focus
        if self._focus:
            self._visible = True

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        if value:
            self.focus = True
        else:
            self._visible = False
            self.focus = False

    def setWidth(self, value: int):
        self.width = value
        if self.cadre:
            self.objet['close'].setX(self.width - 17)
            self.objet['title_box'].width = self.width - 19
            self.objet['title'].setWidth(self.width - 19)
        if self.frame:
            self.objet['frame_cadre'].width = self.width

    def setHeight(self, value: int):
        self.height = value
        if self.frame:
            self.objet['frame_cadre'].height = self.height - 9

    @property
    def title(self):
        return self.objet['title'].text

    @title.setter
    def title(self, texte: str):
        self.objet["title"].text(str(texte))

    def addObjet(self, objet, nom: [str, int] = ""):
        if type(objet) == list:
            for o in objet:
                if type(o) == tuple or type(o) == list:
                    self.objet[o[1]] = o[0]
                else:
                    o.parent = self
                    self.objet[f"obj_{self.num_object}"] = o
                    self.num_object += 1
        else:
            if nom == "":
                nom = f"obj_{self.num_object}"
            nom = str(nom)
            objet.parent = self
            self.objet[nom] = objet
            if nom[:4] == "obj_":
                self.num_object += 1

    def delObjet(self, nom_objet: str):
        if self.objet.get(nom_objet) is not None:
            self.destroyed.append(nom_objet)

    def center(self, objet_name: [str, list[str]], groupe=False):
        """centre horizontalement les objets sur le dialog"""
        if isinstance(objet_name, str):
            objet_name = [objet_name]
        if groupe:
            mini = self.width
            maxi = 0
            for o in objet_name:
                if self.objet[o].x < mini:
                    mini = self.objet[o].x
                if self.objet[o].x + self.objet[o].width > maxi:
                    maxi = self.objet[o].x + self.objet[o].width
            w = maxi - mini
            decalage = (self.width - w) // 2 - mini
            for o in objet_name:
                self.objet[o].setX(decalage + self.objet[o].x)
        else:
            for o in objet_name:
                self.objet[o].setX((self.width - self.objet[o].width) // 2)

    def alligne_h(self, objets_name: list[str], **kwargs):
        margin_left = kwargs.get("margin_left", None)
        margin_right = kwargs.get("margin_right", None)
        egalise = kwargs.get("egalise", False)
        padx = kwargs.get("padx", 2)
        height_maxi = 0
        width_maxi = 0
        for o in objets_name:
            if self.objet[o].height > height_maxi:
                height_maxi = self.objet[o].height
            if self.objet[o].x + self.objet[o].width + 2 > width_maxi:
                width_maxi = self.objet[o].x + self.objet[o].width + 2
        if width_maxi > self.width:
            self.width = width_maxi
        for o in objets_name:
            self.objet[o].height = height_maxi
            self.objet[o].setY(self.objet[objets_name[0]].y)
            if egalise:
                self.objet[o].width = self.objet[objets_name[0]].width
        if kwargs.get("expand", None) is not None:
            if kwargs["expand"].upper() == "X":
                width = (self.width - padx * (len(objets_name) + 1)) / len(objets_name)
                for o in objets_name:
                    self.objet[o].width = width
        if margin_left is not None:
            x = margin_left
        elif margin_right is not None:
            x = self.width - 2 - margin_right - (padx * len(objets_name) - 1)
            for o in objets_name:
                x -= self.objet[o].width
        else:
            x = self.width - (padx * (len(objets_name) - 1))
            for o in objets_name:
                x -= self.objet[o].width
            x /= 2
            x += 10
        for o in objets_name:
            self.objet[o].setX(x)
            x += self.objet[o].width + padx

    def pack(self, objet_name: [str, list[str]], **kwargs):
        if isinstance(objet_name, str):
            objet_name = [objet_name]
        pady = kwargs.get("pady", None)
        margin_left = kwargs.get("margin_left", None)
        margin_right = kwargs.get("margin_right", None)
        decy = 0
        if isinstance(self, Dialog):
            if self.cadre:
                decy = 24
        if pady is None:
            hauteur_totale_objet = 0
            for o in objet_name:
                hauteur_totale_objet += self.objet[o].height
            pady = round((self.height - decy - hauteur_totale_objet) / (len(objet_name) + 1))

        y = decy
        for o in objet_name:
            self.objet[o].setY(y + pady)
            y = self.objet[o].bottom
        if margin_left is None and margin_right is None:
            self.center(objet_name)
        elif margin_left is not None:
            for o in objet_name:
                self.objet[o].setX(margin_left)
        elif margin_right is not None:
            for o in objet_name:
                self.objet[o].setX(self.right - margin_right - self.objet[o].width)

    def draw(self):
        """dessine la boite de dialogue"""
        while len(self.destroyed) > 0:
            self.objet.pop(self.destroyed.pop())
        if self._visible:
            if self.focus:
                self.stroke_weight = 1
            else:
                self.stroke_weight = 0
            super().draw()
            if not isinstance(self, ListBox):
                for o in self.objet.values():
                    o.draw()

    def scan_mouse(self):
        x, y = processing.mouseXY()
        click = processing.mouse_click()
        is_ihm: bool = isinstance(self, IhmScreen)
        if is_ihm or (self.visible and self.focus):
            if not is_ihm:
                if click:
                    self.lostFocus()
                    self.objet_focus = False
                else:
                    self.start_drop = None

            for o in self.objet.values():
                if o.visible:
                    # gestion de boite de dialogue enfant de ihm
                    if isinstance(self, IhmScreen) and isinstance(o, Dialog):
                        if o.collidepoint(x, y) or o.start_drop is not None:
                            if click or o.frame or not o.cadre:
                                o.focus = True
                            affichage.cursor(SYSTEM_CURSOR_ARROW)
                            o.scan_mouse()
                            o.scanKeyboard()
                        if (o.frame or not o.cadre) and not o.collidepoint(x, y):
                            o.focus = False
                        if o.modale:
                            modale = True
                            break
            if not self.modale:
                # try:
                objets = list(self.objet.values())
                for o in objets:
                    if o.visible:
                        if o == self.objet.get('title_box') and (
                                o.collidepoint(x, y) or self.start_drop is not None) and click:

                            if self.start_drop is None:
                                self.start_drop = (self.x - x, self.y - y)
                            else:
                                self.x = x + self.start_drop[0]
                                self.y = y + self.start_drop[1]

                        elif isinstance(o, TextEdit):
                            o.scan_events()
                        elif isinstance(o, ListBox):
                            if o.collidepoint(*processing.mouseXY()):
                                o.scan_mouse()
                        elif isinstance(o, ComboBox):
                            o.scan_mouse()
                        else:
                            o.scan_mouse()

    def scanKeyboard(self):
        for o in self.objet.values():
            if isinstance(o, LineEdit) and o.focus:
                o.scan_events(processing.events())
            elif isinstance(o, TextEdit) and o.focus:
                o.scan_events()

    def lostFocus(self):
        for o in self.objet.values():
            if isinstance(o, LineEdit):
                o.focus = False
                o.texte.cursor_visible = False
            elif isinstance(o, Bouton):
                o.mouseOn = False
                o.focus = False
            elif isinstance(o, TextEdit):
                o.focus = False
            else:
                o.focus = False

    def ajuste(self, margin=10):
        """ajuste la boite de dialogue à son contenant avec une marge (margin)"""
        widthmax, heightmax = 0, 0
        for o in self.objet.values():
            if o.x + o.width > widthmax:
                widthmax = o.x + o.width
            if o.y + o.height > heightmax:
                heightmax = o.y + o.height
        self.setWidth(widthmax + margin)
        self.setHeight(heightmax + margin)
        self.positionne()

    def objet_by_name(self, name: [str, int]) -> ["Dialog", Bouton, LineEdit, Label, MultiLineText, TextEdit]:
        return self.objet.get(str(name))

    def disabled(self, name: str):
        if name == "all":
            for o in self.objet.values():
                o.is_disabled = True
        else:
            self.objet_by_name(name).is_disabled = True

    def enabled(self, name: str):
        if name == "all":
            for o in self.objet.values():
                o.is_disabled = False
        else:
            self.objet_by_name(name).is_disabled = False

    def mouse_on_object(self) -> bool:
        for o in self.objet.values():
            if o._visible and o.collidepoint(*processing.mouseXY()):
                return True
        return False


class IhmScreen(Dialog):
    FOND = None
    BORD = affichage.rgb_color("black")
    LARGEUR_BORD = 0

    def __init__(self, **kwargs):
        kwargs["stroke"] = kwargs.get("stroke", IhmScreen.BORD)
        kwargs["stroke_weight"] = kwargs.get("stroke_weight", IhmScreen.LARGEUR_BORD)
        kwargs["fill"] = kwargs.get("fill", IhmScreen.FOND)
        kwargs['cadre'] = kwargs.get('cadre', None)
        super().__init__(None, (0, 0, processing.width(), processing.height()), **kwargs)
        self.decy = 0

    def init(self):
        self.setWidth(processing.width())
        self.setHeight(processing.height())
        self.focus = False
        self.fill = processing.get_background_color()

    def scan_events(self):
        if processing.get_resized():
            self.init()
        self.scan_mouse()
        self.scanKeyboard()

    def obj_focused(self) -> [None, "Dialog", Bouton, Label, LineEdit, TextEdit]:
        for o in self.objet.values():
            if o.focus:
                return o
        return None

    def show_modale(self, object_name):
        self.modale = True
        self.lostFocus()
        self.objet_by_name(object_name).focus = True

    def close_modale(self, object_name):
        self.modale = False
        self.objet_by_name(object_name).visible = False


class ListRadio(Dialog):
    def __init__(self, parent, rect, list_item: list, **kwargs):
        kwargs['cadre'] = False
        kwargs['frame'] = True
        selected = kwargs.get('selected', 0)
        l, c = kwargs.get('ligxcol', f"{len(list_item)}x1").split("x")
        l, c = int(l), int(c)
        self.multiple = kwargs.get('multiple', False)
        super().__init__(parent, rect, **kwargs)
        self.liste_item = list_item
        h = 21
        b = Radio(self, (1, 1, self.width - 15, h), self.liste_item[0], (selected == 0), **kwargs)
        h = b.height
        self.addObjet(b)
        for i in range(l):
            for j in range(c):
                n = i * c + j
                if 0 < n < len(list_item):
                    self.addObjet(
                        Radio(self, (1 + j * self.width, i * h, self.width - 15, h), self.liste_item[n], (selected == n),
                              **kwargs))
        self.setHeight((1 + i) * h + self.decy + 1)
        self.setWidth(self.width * c)

    def values(self) -> list:
        v = []
        index = 0
        for o in self.objet.values():
            if isinstance(o, Radio) :
                if o.value:
                    v.append(index)
                index += 1
        return v


class ListBox(Dialog):
    def __init__(self, parent, rect, list_item: list, **kwargs):
        kwargs['cadre'] = False
        super().__init__(parent, rect, **kwargs)
        kwargs["extend"] = kwargs.get("extend", False)
        kwargs["no_stroke"] = kwargs.get("no_stroke", True)
        kwargs["command"] = kwargs.get("command", self.click)
        self.selected = 0
        self.liste_item = [[i, False] for i in list_item]
        kwargs["max_selected"] = kwargs.get("max_selected", len(self.liste_item))
        self.max_selected = kwargs.pop("max_selected")
        h = 21
        kwargs["name"] = 0
        b = Bouton(self, (1, 1, self.width - 2, h), self.liste_item[0][0], **kwargs)
        h = b.height
        self.nb_affiche = len(self.liste_item)
        self.addObjet(b, 0)
        self.scroll_bar = None
        self.debut = 0
        self.decy = 0
        for i in range(1, len(list_item)):
            kwargs["name"] = i
            self.addObjet(Bouton(self, (1, 1 + i * h, self.width - 2, h), self.liste_item[i][0], **kwargs), i)
        if kwargs["extend"]:
            self.height = len(self.liste_item) * h + 2
        else:
            if self.height < len(self.liste_item) * h + 2:
                self.nb_affiche = self.height // h
                self.scroll_bar = ScrollBar(self, self.nb_affiche, len(self.liste_item))
                for o in self.objet.values():
                    o.setWidth(o.width - self.scroll_bar.width)
                self.addObjet(self.scroll_bar, "scoll_bar")

    def click(self, name):
        if self.liste_item[name][1] is False and self.selected < self.max_selected:
            self.liste_item[name][1] = True
            self.selected += 1
        elif self.liste_item[name][1]:
            self.liste_item[name][1] = False
            self.selected -= 1

    def select_item(self, list_index_item: list[int]):
        for index in list_index_item:
            self.liste_item[index][1] = True

    def select_all(self):
        for item in self.liste_item:
            item[1] = True

    def unseselect_all(self):
        for item in self.liste_item:
            item[1] = False

    def draw(self):
        while len(self.destroyed) > 0:
            self.objet.pop(self.destroyed.pop())
        if self._visible:
            super().draw()
            boutons = list(self.objet.values())
            if self.scroll_bar is not None:
                self.debut = self.scroll_bar.value()
            else:
                self.debut = 0
            fin = self.debut + self.nb_affiche
            c = 0
            for i in range(0, len(self.liste_item)):
                o = boutons[i]
                if self.debut <= i < fin:
                    o.visible = True
                    o.setY(1 + c * o.height)
                    c += 1
                    if self.liste_item[i][1]:
                        self.objet_by_name(i).forced = True
                    else:
                        self.objet_by_name(i).forced = False
                    o.draw()
                else:
                    o.visible = False
                o.mouseOn = False

            if self.scroll_bar is not None:
                self.scroll_bar.draw()

    def scan_mouse(self):
        x, y = processing.mouseXY()
        if self.collidepoint(x, y):
            self.focus = True
        super().scan_mouse()


class Radio(Bouton):
    def __init__(self, parent, rect, texte, defaut=False, **kwargs):
        kwargs["command"] = self.click
        super().__init__(parent, rect, texte, defaut, **kwargs)
        self.texte.x = self.x + 17
        self.width = self.texte.width + 17
        self.value = defaut

    def click(self):
        if not self.parent.multiple:
            if self.value is False:
                for o in self.parent.objet.values():
                    if isinstance(o, Radio):
                        o.value = False
            self.value = True
        else:
            self.value = not self.value

    def draw(self):
        if self.visible:
            if self.is_disabled:
                self.fill = Bouton.BOUTON_FOND_DISABLED
                self.texte.fill = Bouton.BOUTON_FOND_DISABLED
                self.texte.stroke = Bouton.BOUTON_FOND_DISABLED
                self.texte.couleurPolice = Bouton.BOUTON_TEXT_COLOR_DISABLED
                self.stroke = Bouton.BOUTON_TEXT_COLOR_DISABLED
            else:
                self.texte.couleurPolice = Bouton.BOUTON_TEXT_COLOR
                if self.forced:
                    self.fill = Bouton.BOUTON_BORD_MOUSE_ON
                    self.texte.fill = Bouton.BOUTON_BORD_MOUSE_ON
                    self.texte.stroke = Bouton.BOUTON_BORD_MOUSE_ON
                elif self.mouseOn:
                    self.stroke = Bouton.BOUTON_BORD_MOUSE_ON
                    self.fill = None
                    self.texte.fill = None
                    self.stroke = processing.rgb_color("darkgrey")
                    self.stroke_weight = 1
                else:
                    self.stroke_weight = 0
                    self.fill = None
                    self.texte.fill = self.fill
                    self.texte.stroke_weight = 0

            Boite.draw(self)
            self.texte.draw()
            pygame.draw.circle(Boite.ecran, processing.rgb_color("black"),
                               (self.x + self.parent.x + 9, self.y + self.parent.y + self.height / 2), 7, width=1)
            self.mouseOn = False
            if self.value:
                pygame.draw.circle(Boite.ecran, processing.rgb_color("black"),
                                   (self.x + self.parent.x + 9, self.y + self.parent.y + self.height / 2), 4)
            self.draw_infobulle()


class ComboBox(Dialog):
    def __init__(self, parent, rect, list_item: list, **kwargs):
        kwargs['cadre'] = None
        super().__init__(parent, rect, **kwargs)
        kwargs["extend"] = kwargs.get("extend", False)
        kwargs["no_stroke"] = kwargs.get("no_stroke", True)
        kwargs["command"] = kwargs.get("command", self.click_item)
        self.liste_item = [[i, False] for i in list_item]
        self.hauteur_ligne = 21
        self.decy = 22
        kwargs["name"] = 0
        line_edit = Label(self, (0, 0, self.width - 8, 22), self.liste_item[0][0], stroke="black", align_v="center")
        bouton = Bouton(self, (self.width - 18, 0, 28, 22), "V", command=self.open_close)
        self.addObjet(line_edit, "label")
        self.addObjet(bouton, "bouton")
        b = Bouton(self, (1, 22, self.width - 2, self.hauteur_ligne), self.liste_item[0][0], **kwargs)
        self.hauteur_ligne = b.height
        self.nb_affiche = len(self.liste_item)
        self.addObjet(b, 0)
        self.scroll_bar = None
        self.debut = 0
        self.close = True
        self._value = 0
        for i in range(1, len(list_item)):
            kwargs["name"] = i
            self.addObjet(Bouton(self, (1, (1 + i) * self.hauteur_ligne, self.width - 2, self.hauteur_ligne),
                                 self.liste_item[i][0], **kwargs), i)
        if kwargs["extend"]:
            self.height = len(self.liste_item) * self.hauteur_ligne + 2
        else:
            if self.height < len(self.liste_item) * self.hauteur_ligne + 2:
                self.nb_affiche = (self.height - self.decy) // self.hauteur_ligne
                self.scroll_bar = ScrollBar(self, self.nb_affiche, len(self.liste_item))
                for o in self.objet.values():
                    o.setWidth(o.width - self.scroll_bar.width)
                self.addObjet(self.scroll_bar, "scoll_bar")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        if value < len(self.liste_item):
            self._value = value
            self.objet_by_name("label").text(self.liste_item[value][0])
        else:
            raise IndexError(f"value must be lower than len(self.liste_item)\n{value} >= {len(self.liste_item)} ")

    def open_close(self):
        self.close = not self.close

    def click_item(self, name):
        self.objet_by_name("label").text(self.liste_item[int(name)][0])
        self.value = int(name)
        self.close = True

    def draw(self):
        while len(self.destroyed) > 0:
            self.objet.pop(self.destroyed.pop())
        if self._visible:
            super().draw()
            boutons = list(self.objet.values())

            c = 0
            if self.close:
                fin = 0
                if self.scroll_bar is not None:
                    self.scroll_bar.visible = False
                self.height = 22
            else:
                self.height = self.nb_affiche * self.hauteur_ligne + self.decy
                if self.scroll_bar is not None:
                    self.scroll_bar.visible = True
                    self.debut = self.scroll_bar.value() + 2
                else:
                    self.debut = 2
                fin = self.debut + self.nb_affiche
            boutons[0].draw()
            boutons[1].draw()
            for i in range(2, len(self.liste_item) + 2):
                o = boutons[i]
                if self.debut <= i < fin:
                    o.visible = True
                    o.setY(1 + c * o.height + self.decy)
                    c += 1
                    if self.liste_item[i - 2][1]:
                        self.objet_by_name(i - 2).forced = True
                    else:
                        self.objet_by_name(i - 2).forced = False
                else:
                    o.visible = False
                o.draw()
                o.mouseOn = False

            if self.scroll_bar is not None:
                self.scroll_bar.draw()

    def scan_mouse(self):
        x, y = processing.mouseXY()
        if self.collidepoint(x, y):
            self.focus = True
            super().scan_mouse()
        else:
            self.focus = False
            self.close = True

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, value: bool):
        self._focus = value
        if value is None:
            self.close = True


class ScrollBar:

    def __init__(self, parent, affiche, maxi: float, **kwargs):
        self.visible = True
        self.is_disabled = False
        self.parent = parent
        self.curseur = Boite(parent, (0, 0, 10, 20))
        self.fond = Boite(parent, (
            self.parent.width - self.curseur.width, 0, self.curseur.width, parent.height - parent.decy))
        self._width = self.curseur.width
        self._height = parent.height - parent.decy
        self.curseur.mouse_click_down = False
        kwargs["orientation"] = kwargs.get("orientation", "e")
        self.orientation = kwargs.pop("orientation")
        self.pos = 0
        self.mouse_click_down = False
        self.pas = maxi - affiche
        if self.orientation == "e":
            self.height = self.parent.height - self.parent.decy
            self.curseur.x = self.parent.right - self.parent.x - self.curseur.width
            self.curseur.y = self.parent.decy + (
                    self.parent.height - self.parent.decy - self.curseur.height) * self.pos / 100
            self.curseur.height = self.height * affiche // maxi
            self.fond = Boite(self.parent, (
                self.curseur.x, self.parent.decy, self.curseur.width, self.parent.height - self.parent.decy),
                              fill="grey32")
        elif self.orientation == "s":
            self.width, self.curseur.height = self.curseur.height, self.curseur.width
            self.width = self.parent.width * affiche // maxi
            self.curseur.x = self.parent.width * self.pos / 100
            self.curseur.y = self.parent.height - self.parent.decy - self.curseur.height
            self.fond = Boite(self.parent, (self.curseur.x, self.curseur.y, self.parent.width, self.curseur.height),
                              fill="grey32")

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.fond.width = self._width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.fond.height = self._height

    def value(self):
        if self.orientation == "e":
            return round(self.pas * (self.curseur.y - self.parent.decy) / (self.height - self.curseur.height))
        if self.orientation == "s":
            return round(self.pas * (self.curseur.x) / (self.width - self.curseur.width))

    def draw(self):
        if self.visible:
            self.fond.draw()
            self.curseur.draw()

    def scan_mouse(self):
        if self.is_disabled is False:
            x, y = processing.mouseXY()
            click = processing.mouse_click()
            if self.curseur.collidepoint(x, y) and click:
                self.curseur.mouse_click_down = True
            elif not click:
                self.curseur.mouse_click_down = False
            if self.fond.collidepoint(x, y):
                if click:
                    x -= self.parent.x
                    y -= self.parent.y
                    # déplacement avec le curseur
                    if self.orientation == "s":
                        self.curseur.centerx = min(max(x, self.curseur.width // 2),
                                                   self.parent.width - self.curseur.width / 2)
                    elif self.orientation == "e":
                        self.curseur.centery = min(max(y, self.parent.decy + self.curseur.height // 2),
                                                   self.parent.decy + self.fond.height - self.curseur.height // 2)
                else:
                    # déplacement avec la roulette sur scroller
                    if processing.mouse_wheel_state() == 1:
                        self.curseur.y = max(self.parent.decy, self.curseur.y - self.curseur.height // 8)
                    elif processing.mouse_wheel_state() == -1:
                        self.curseur.y = min(self.height + self.parent.decy - self.curseur.height,
                                             self.curseur.y + self.curseur.height // 8)
            elif self.parent.collidepoint(x, y):
                # déplacement avec la roulette
                if processing.mouse_wheel_state() == 1:
                    self.curseur.y = max(self.parent.decy, self.curseur.y - self.curseur.height // 8)
                elif processing.mouse_wheel_state() == -1:
                    self.curseur.y = min(self.height + self.parent.decy - self.curseur.height,
                                         self.curseur.y + self.curseur.height // 8)


class TextInput:
    """
    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """

    def __init__(self, font_family="arial",
                 font_size=12,
                 antialias=True,
                 text_color=(0, 0, 0),
                 cursor_color=(0, 0, 1),
                 repeat_keys_initial_ms=400,
                 repeat_keys_interval_ms=35):
        """
        Args:
            font_family: Name or path of the font that should be used. Default is pygame-font
            font_size: Size of the font in pixels
            antialias: (bool) Determines if antialias is used on fonts or not
            text_color: Color of the text
            repeat_keys_initial_ms: ms until the keydowns get repeated when a key is not released
            repeat_keys_interval_ms: ms between to keydown-repeats if key is not released
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self._input_string = ""  # Inputted text
        if not os.path.isfile(font_family): font_family = pygame.font.match_font(font_family)
        self.font_object = pygame.font.Font(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = 0  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0
        self.focus = False

        self.clock = pygame.time.Clock()

    @property
    def input_string(self):
        return self._input_string

    @input_string.setter
    def input_string(self, texte):
        self._input_string = texte
        self.cursor_position = len(texte)
        self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

    def update(self, events):
        touche = None
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if not event.key in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == K_BACKSPACE:
                    self._input_string = self._input_string[:max(self.cursor_position - 1, 0)] + \
                                         self._input_string[self.cursor_position:]

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == K_DELETE:
                    self._input_string = self._input_string[:self.cursor_position] + \
                                         self._input_string[self.cursor_position + 1:]

                elif event.key == K_RETURN or event.key == K_DOWN or event.key == K_UP:
                    return True

                elif event.key == K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self._input_string))

                elif event.key == K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == K_END:
                    self.cursor_position = len(self._input_string)

                elif event.key == K_HOME:
                    self.cursor_position = 0

                else:
                    # If no special key is pressed, add unicode of key to input_string
                    self._input_string = self._input_string[:self.cursor_position] + \
                                         event.unicode + \
                                         self._input_string[self.cursor_position:]
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock
            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = self.keyrepeat_intial_interval_ms - \
                                                  self.keyrepeat_interval_ms

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(KEYDOWN, key=event_key, unicode=event_unicode))

        # Rerender text surface:
        self.surface = self.font_object.render(self._input_string, self.antialias, self.text_color)
        if self.focus:
            # Update self.cursor_visible
            self.cursor_ms_counter += self.clock.get_time()
            if self.cursor_ms_counter >= self.cursor_switch_ms:
                self.cursor_ms_counter %= self.cursor_switch_ms
                self.cursor_visible = not self.cursor_visible

            if self.cursor_visible:
                cursor_y_pos = self.font_object.size(self._input_string[:self.cursor_position])[0]
                # Without this, the cursor is invisible when self.cursor_position > 0:
                if self.cursor_position > 0:
                    cursor_y_pos -= self.cursor_surface.get_width()
                self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

            self.clock.tick()

        return False

    def get_surface(self):
        self.update([])
        return self.surface

    def get_text(self):
        return self._input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self._input_string = ""


class GroupeBoite(list):
    def __init__(self, l: list):
        super().__init__(l)
        self.obj_focus = None

    def draw(self):
        for o in self:
            if type(o) == Dialog:
                if o.focus:
                    self.obj_focus = o
                else:
                    o.draw()
            else:
                o.draw()
        if self.obj_focus is not None:
            self.obj_focus.draw()
        i = 0
        while i < len(self):
            if self[i].destroy is True:
                if self[i] == self.obj_focus:
                    self.obj_focus = None
                self.pop(i)
            else:
                i += 1

    def append(self, dialogue: Dialog) -> None:
        if self.obj_focus is None or self.obj_focus.modale is False:
            super().append(dialogue)
            self.take_focus(self[-1])

    def take_focus(self, obj):
        for dia in self:
            dia.focus = False
        obj.focus = True
        self.obj_focus = obj

    def scan_event(self):
        x, y = processing.mouseXY()
        if self.obj_focus is not None and self.obj_focus.modale is True:
            self.obj_focus.scan_mouse()
            self.obj_focus.scanKeyboard()
        else:
            for o in self:
                if isinstance(o, Dialog):
                    if o.collidepoint(x, y):
                        if processing.mouse_click():
                            if self.obj_focus is None or not self.obj_focus.collidepoint(x, y):
                                self.take_focus(o)
                        o.scan_mouse()
                        o.scanKeyboard()
                else:
                    o.scan_mouse()


class MessageBox(Dialog):
    parent: IhmScreen
    state_bouton = -1
    nb_instances = 0

    def bp(self, name):
        MessageBox.nb_instances = 0
        self.value = name

    def quitter(self):
        MessageBox.nb_instances = 0
        self.value = 4

    def __init__(self, parent: Dialog, title, texte, boutons, icone):
        if MessageBox.nb_instances != 0:
            raise "Only one instance of MessageBox is autorized"
        MessageBox.nb_instances = 1
        MessageBox.parent = parent
        MessageBox.parent.answer_info = -1
        super().__init__(self.parent, (10, 10, 200, 100), title=title)
        self.addObjet(Label(self, (2, 2, 50, 50), "", image=icone), "image")
        self.addObjet(MultiLineText(self, (62, 2, 148, 50), texte, align_v="center", no_stroke=True), "texte")
        y = self.objet_by_name("texte").bottom - 25 + 10
        for n, nom in enumerate(boutons):
            self.addObjet(Bouton(self, (2 + 40 * n, y, 80, 30), boutons[n], command=self.bp, name=n), boutons[n])
        self.alligne_h(boutons, egalise=True)
        self.ajuste()
        self.center_me()
        self.value = -1

    def response(self) -> int:
        x, y = 0, 0
        self.focus = True
        while self.value == -1:
            self.draw()
            processing.redraw()
            __events = pygame.event.get()
            for event in __events:
                if event.type == 1024:
                    x, y = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if processing.get_click() is False:
                        processing.set_click(True)
                        processing.set_click_down(True)
                elif event.type == pygame.MOUSEBUTTONUP:
                    processing.set_click(False)
                    processing.set_click_up(True)
            if x != 0 and y != 0:
                self.scan_mouse()
        return self.value


class ShowInfo(MessageBox):
    def __init__(self, parent, message="", title="Information"):
        super().__init__(parent, title, message, ["Ok"], loadImage(".\likeprocessing\info.png"))


class ShowWarning(MessageBox):
    def __init__(self, parent, message="", title="Attention", ):
        super().__init__(parent, title, message, ["Ok"], loadImage(".\likeprocessing\warning.png"))


class ShowError(MessageBox):
    def __init__(self, parent, message="", title="Erreur"):
        super().__init__(parent, title, message, ["Ok"], loadImage(".\likeprocessing\error.png"))


class AskYesNo(MessageBox):
    def __init__(self, parent, message="", title="Question"):
        super().__init__(parent, title, message, ["Oui", "Non"], loadImage(".\likeprocessing\question.png"))


class AskOkCancel(MessageBox):
    def __init__(self, parent, message="", title="Question"):
        super().__init__(parent, title, message, ["Ok", "Cancel"], loadImage(".\likeprocessing\question.png"))


class AskRetriyCancel(MessageBox):
    def __init__(self, parent, message="", title="Question"):
        super().__init__(parent, title, message, ["Réessayer", "Annulé"], loadImage(".\likeprocessing\question.png"))


if __name__ == '__main__':
    t = MultiLineText(0, 1, "bonjour")
    b = Boite((100, 150, 50, 20))
    b.draw()
