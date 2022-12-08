import likeprocessing.processing as processing
import likeprocessing.affichage as affichage
import os.path
import pygame
from pygame.constants import *
import pygame_textinput

pygame.font.init()
from likeprocessing.couleur import *
import os


class Boite(pygame.Rect):
    ecran = None

    def __init__(self, parent, rect, **kwargs):
        if parent is None:
            self.Parent = pygame.Rect((0, 0, Boite.ecran.get_width(), Boite.ecran.get_height()))
        else:
            self.Parent = parent
        super().__init__(rect)
        self.couleurBord = kwargs.get('couleurBord', BLACK)
        self.couleurFond = kwargs.get('couleurFond', WHITE)
        self.largeurBord = kwargs.get('largeurBord', 1)
        self.couleurFondDisabled = kwargs.get('couleurFondDisabled', affichage.rgb_color("grey"))
        self.couleurBordDisabled = kwargs.get('couleurFond', affichage.rgb_color("grey90"))
        self.image_rect: pygame.surface = kwargs.get('image', None)
        self.destroy = False
        self.is_disabled = kwargs.get('disabled', False)
        self._visible = True
        if isinstance(self.parent, Dialog) and self.parent.cadre:
            self.top += 25

    def init(screen: pygame.Surface):
        Boite.ecran = screen

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
        self.x = value + self.parent.x

    def setY(self, value: int):
        self.y = value + self.parent.y

    def move(self, x: int, y: int):
        self.setX(x)
        self.setY(y)

    def draw(self):
        if self.visible:
            if self.is_disabled is True:
                couleur_bord = self.couleurBordDisabled
                couleur_fond = self.couleurFondDisabled
            else:
                couleur_bord = self.couleurBord
                couleur_fond = self.couleurFond

            if self.image_rect is None:
                if self.couleurFond is not None:
                    r = pygame.Surface((self.width, self.height))
                    r.fill(couleur_fond)
                else:
                    r = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
                    r = r.convert_alpha()
                Boite.ecran.blit(r, [self.Parent.left + self.left, self.Parent.top + self.top])
            else:
                Boite.ecran.blit(self.image_rect, (self.Parent.left + self.left, self.Parent.top + self.top),
                                 (0, 0, self.image_rect.get_width(), self.image_rect.get_height()))
            if self.largeurBord > 0:
                r = pygame.Rect(self.Parent.left + self.left, self.Parent.top + self.top, self.width, self.height)
                pygame.draw.rect(Boite.ecran, couleur_bord, r, self.largeurBord)

    def collidepoint(self, x, y):
        return super().collidepoint(x - self.parent.left, y - self.parent.top)

    def scan_mouse(self):
        pass

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
        self.couleurBord = kwargs.get('couleurBord', "black")
        self.largeurBord = kwargs.get('largeurBord', 1)
        self.couleurFond = kwargs.get('couleurFond', None)
        self.police = kwargs.get('police', "arial")
        self.taille = kwargs.get('size', 12)
        self._couleurPolice = kwargs.get('couleurPolice', "black")
        self.bold = kwargs.get('bold', None)
        self.italic = kwargs.get('italic', None)
        self.align_v = kwargs.get('align_v', "TOP").upper()
        self.align_h = kwargs.get('align_h', "LEFT").upper()
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
        self.width = max(width + 4, self.width)
        self.height = max(height + 4, self.height)
        return image

    def draw(self):
        if self.visible:
            # fonction qui permet l'affichage de texte à  l'ecran
            super().draw()
            if self.align_h == "LEFT":
                x = self.Parent.left + self.left + 2
            elif self.align_h == "CENTER":
                x = self.Parent.left + self.left + (self.width - self.image.get_width()) // 2
            elif self.align_h == "RIGHT":
                x = self.Parent.left + self.left - 2 + (self.width - self.image.get_width())
            if self.align_v == "TOP":
                y = self.Parent.top + self.top + 2
            elif self.align_v == "CENTER":
                y = self.Parent.top + self.top + (self.height - self.image.get_height()) // 2
            elif self.align_v == "BOTTOM":
                y = self.Parent.top + self.top - 2 + (self.height - self.image.get_height())
            Boite.ecran.blit(self.imageTexte(), [x, y])

    def __str__(self):
        return super().__str__() + " " + str(self.text)


class Label(Boite):
    """affiche un texte sur une ligne dans une boite"""

    def __init__(self, parent, rect, texte: str, angle=0, **kwargs):
        if len(rect) == 2:
            rect = (rect[0], rect[1], 0, 0)
        elif len(rect) == 3:
            rect = (rect[0], rect[1], rect[2], 0)
        couleurBord = kwargs.get('couleurBord', "black")
        largeurBord = kwargs.get('largeurBord', 0)
        couleurFond = kwargs.get('couleurFond', None)
        kwargs["police"] = kwargs.get('police', "arial")
        kwargs["size"] = kwargs.get('size', 12)
        kwargs["couleurPolice"] = kwargs.get('couleurPolice', "black")
        self.bold = kwargs.get('bold', None)
        self.italic = kwargs.get('italic', None)
        self.align_v = kwargs.get('align_v', "TOP").upper()
        self.align_h = kwargs.get('align_h', "LEFT").upper()
        super().__init__(parent, rect, couleurBord=couleurBord, largeurBord=largeurBord, couleurFond=couleurFond)
        self._texte = texte
        self.police = kwargs["police"]
        self.taille = kwargs["size"]
        self.couleurPolice = kwargs.get('couleurPolice', BLACK)
        self.couleurPoliceEnabled = kwargs.get('couleurPolice', BLACK)
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
        self.height = max(self.height, r.height + 4)
        if self.width == 0:
            self.width = r.width + 3
        elif r.width > self.width - 4:
            r.width = self.width - 4
            text_bitmap = text_bitmap.subsurface(r)

        return text_bitmap

    def draw(self):
        if self.visible:
            # fonction qui permet l'affichage de texte à  l'ecran
            if self.angle != 0:
                img = pygame.transform.rotate(self.image, self.angle)
                self.width = max(img.get_width(), self.width)
                self.height = max(img.get_height(), self.height)
            else:
                img = self.image
            super().draw()
            if self.align_h == "LEFT":
                x = self.Parent.left + self.left + 2
            elif self.align_h == "CENTER":
                x = self.Parent.left + self.left + (self.width - self.image.get_width()) // 2
            elif self.align_h == "RIGHT":
                x = self.Parent.left + self.left - 2 + (self.width - self.image.get_width())
            if self.align_v == "TOP":
                y = self.Parent.top + self.top + 2
            elif self.align_v == "CENTER":
                y = self.Parent.top + self.top + (self.height - self.image.get_height()) // 2
            elif self.align_v == "BOTTOM":
                y = self.Parent.top + self.top - 2 + (self.height - self.image.get_height())
            Boite.ecran.blit(img, [x, y])

    def __str__(self):
        return super().__str__() + " " + str(self.text)


class TextEdit(Boite):
    """permet de créer un texte sur plusieurs ligne"""

    def __init__(self, parent, rect, texte: str, **kwargs):
        kwargs["couleurBord"] = kwargs.get('couleurBord', affichage.rgb_color("black"))
        kwargs["largeurBord"] = kwargs.get('largeurBord', 1)
        kwargs["couleurFond"] = kwargs.get('couleurFond', affichage.rgb_color("white"))
        kwargs["police"] = kwargs.get('police', "arial")
        kwargs["size"] = kwargs.get('size', 12)
        nb_ligne = kwargs.get('nb_ligne', 10)
        ps = pygame.font.SysFont(kwargs["police"], kwargs["size"])
        h = ps.size("bg")[0]
        rect = tuple(list(rect[:3]) + [(4 + h) * nb_ligne + 4])
        if parent is None:
            processing.ihm.append(self)
        super().__init__(parent, rect, **kwargs)
        self.police = kwargs["police"]
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
            self.couleurBord = "blue"
        else:
            self.couleurBord = "black"

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
        kwargs['couleurBord'] = kwargs.get('couleurBord', LineEdit.LINE_EDIT_BORD)
        kwargs['largeurBord'] = kwargs.get('largeurBord', 1)
        kwargs['couleurFond'] = kwargs.get('couleurFond', LineEdit.LINE_EDIT_FOND)
        kwargs["police"] = kwargs.get('police', "arial")
        kwargs["size"] = kwargs.get('size', 12)
        kwargs["couleurPolice"] = kwargs.get('couleurPolice', "black")
        name = kwargs.get('name', None)
        if parent is None:
            processing.ihm.append(self)
        elif isinstance(parent, TextEdit):
            kwargs['largeurBord'] = 0
        ps = pygame.font.SysFont(kwargs["police"], kwargs["size"])
        h = ps.size("bg")[0]
        if len(rect) == 3:
            rect = tuple(list(rect[:3]) + [h + 8])
        elif len(rect) == 4:
            rect = tuple(list(rect[:3]) + [max(h + 4, rect[3])])
        super().__init__(parent, rect, **kwargs)
        ft = pygame.font.SysFont(kwargs["police"], kwargs["size"])
        manager = pygame_textinput.TextInputManager(initial=texte)
        self.texte: pygame_textinput.TextInputVisualizer = pygame_textinput.TextInputVisualizer(font_object=ft,
                                                                                                manager=manager,
                                                                                                font_color=kwargs[
                                                                                                    "couleurPolice"])
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
            self.couleurBord = "blue"
            self.texte.cursor_visible = True
        else:
            self.couleurBord = "black"
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
            #     self.couleurBord = LineEdit.LINE_EDIT_BORD_DISABLED
            #     self.couleurFond = LineEdit.LINE_EDIT_FOND_DISABLED
            # else:
            #     self.couleurBord = LineEdit.LINE_EDIT_BORD
            #     self.couleurFond = LineEdit.LINE_EDIT_FOND
            super().draw()
            # Boite.ecran.blit(self.texte.get_surface(), (self.Parent.left + self.left + 3, self.Parent.top + self.top))
            dec = (self.height - self.texte.surface.get_height()) / 2
            Boite.ecran.blit(self.texte.surface, (self.Parent.left + self.left + 3, self.Parent.top + self.top + dec))

    def __str__(self):
        # return self.texte.input_string
        return self.texte.value

    def __len__(self):
        # return len(self.texte.input_string)
        return len(self.texte.value)

    def scan_mouse(self):
        if self.is_disabled is False:
            x, y = processing.mouseXY()
            click = processing.mouse_click()
            if self.collidepoint(x, y):
                self.mouseOn = True
            else:
                self.mouseOn = False
                if processing.mouse_click_down():
                    self.focus = False
            if self.mouseOn and click is True and self.focus is False:
                self.focus = True
                self.parent.objet_focus = True
                # positionne le curseur au niveau de la souris
                c = 0
                while self.texte.font_object.size(self.texte.value[0:c])[0] < x - self.parent.x - self.x and c <= len(
                        self):
                    c += 1
                    # print(self.texte.font_object.size(self.texte.value[0:c])[0], x, c,self.x,self.parent)
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
        super().__init__(parent, rect, **kwargs)
        self.fonction = kwargs.get("command", None)
        self.mouseOn = False
        self.mouseClick = False
        self.texte = MultiLineText(parent, (2, 2), texte, **kwargs, align_v="center", align_h="center")
        self.width = max(self.width, self.texte.width + 4)
        self.height = max(self.height, self.texte.height + 4)
        self.texte.left = self.left + (self.width - self.texte.width) // 2
        self.texte.top = self.top + (self.height - self.texte.height) // 2
        self.focus = False

    def setX(self, value: int):
        self.x = value + self.parent.x
        self.texte.left = self.left + self.parent.x + (self.width - self.texte.width) // 2

    def setY(self, value: int):
        self.y = value + self.parent.y
        self.texte.top = self.top + self.parent.y + (self.height - self.texte.height) // 2

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
        self.texte.Parent = monPere

    def connecte(self, fonction):
        self.fonction = fonction

    def draw(self):
        if self.visible:
            if self.is_disabled:
                self.couleurFond = Bouton.BOUTON_FOND_DISABLED
                self.texte.couleurFond = Bouton.BOUTON_FOND_DISABLED
                self.texte.couleurBord = Bouton.BOUTON_FOND_DISABLED
                self.texte.couleurPolice = Bouton.BOUTON_TEXT_COLOR_DISABLED
                self.couleurBord = Bouton.BOUTON_TEXT_COLOR_DISABLED
            else:
                self.texte.couleurPolice = Bouton.BOUTON_TEXT_COLOR
                if self.mouseOn:
                    self.couleurBord = Bouton.BOUTON_BORD_MOUSE_ON
                    if self.mouseClick:
                        self.couleurFond = Bouton.BOUTON_BORD_MOUSE_ON
                        self.texte.couleurFond = Bouton.BOUTON_BORD_MOUSE_ON
                        self.texte.couleurBord = Bouton.BOUTON_BORD_MOUSE_ON
                    else:
                        self.couleurFond = Bouton.BOUTON_FOND_MOUSE_ON
                        self.texte.couleurFond = Bouton.BOUTON_FOND_MOUSE_ON
                        self.texte.couleurBord = Bouton.BOUTON_FOND
                else:
                    self.couleurBord = Bouton.BOUTON_BORD
                    self.couleurFond = Bouton.BOUTON_FOND
                    self.texte.couleurFond = Bouton.BOUTON_FOND
                    self.texte.couleurBord = Bouton.BOUTON_FOND

            super().draw()
            self.texte.draw()

    def scan_mouse(self):
        if self.is_disabled is False:
            x, y = processing.mouseXY()
            click = processing.mouse_click()
            if self.collidepoint(x, y):
                self.mouseOn = True
                self.focus = True
            else:
                self.mouseOn = False
                self.focus = False
            if click is False and self.mouseClick is True:
                self.mouseClick = False
                if self.mouseOn is True and self.fonction is not None:
                    self.fonction()
            elif click is True and self.mouseOn is True:
                self.mouseClick = True
        else:
            self.focus = False

    def __str__(self):
        return "Bouton " + super().__str__() + " " + str(self.texte)


class Dialog(Boite):
    """Classe qui permet de créer une boite de dialogue vide
    munie d'une barre de titre et d'une casse de fermeture"""
    dialogue = 1
    FOND = (255, 255, 255)
    BORD = (150, 150, 150)
    LARGEUR_BORD = 1

    def __init__(self, parent, rect, **kwargs):
        cb = kwargs.get('couleurBord', Dialog.BORD)
        lb = kwargs.get('largeurBord', Dialog.LARGEUR_BORD)
        cf = kwargs.get('couleurFond', Dialog.FOND)
        super().__init__(parent, rect, couleurBord=cb, largeurBord=lb, couleurFond=cf)
        self.pos = kwargs.get('pos', None)
        self.objet = {}
        cadre = kwargs.get('cadre', True)
        self.destroyed = []
        self.cadre = cadre
        if self.cadre:
            decy = 25
            self.addObjet(
                Boite(self, (2, 2 - decy, self.width - 19, 22), couleurBord=Dialog.BORD, largeurBord=1,
                      couleurFond="lightblue"),
                "title_box")
            self.addObjet(
                Label(self, (2, 2 - decy, self.width - 19, 22), "Dialog" + str(Dialog.dialogue), align_v="center"),
                "title")
            self.addObjet(Bouton(self, (self.width - 17, 2 - decy, 16), "X"), "close")
            self.objet['close'].connecte(self.quitter)
        self._visible = True
        self.start_drop = None
        Dialog.dialogue += 1
        self.num_object = 1
        self.destroy = False
        self._focus = False
        self.modale = False
        self.positionne()
        self.objet_focus = False

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

    def setHeight(self, value: int):
        self.height = value

    @property
    def title(self):
        return self.objet['title'].text

    @title.setter
    def title(self, texte: str):
        self.objet["title"].text(str(texte))

    def addObjet(self, objet, nom: str = None):
        if type(objet) == list:
            for o in objet:
                if type(o) == tuple or type(o) == list:
                    self.objet[o[1]] = o[0]
                else:
                    o.parent = self
                    self.objet[f"obj_{self.num_object}"] = o
                    self.num_object += 1
        else:
            if nom is None:
                nom = f"obj_{self.num_object}"
            objet.parent = self
            self.objet[nom] = objet
            if nom[:4] == 'obj_':
                self.num_object += 1

    def delObjet(self, nom_objet: str) -> object | None:
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

    def pack(self, objet_name: [str, list[str]], **kwargs):
        if isinstance(objet_name, str):
            objet_name = [objet_name]
        pady = kwargs.get("pady", None)
        margin_left = kwargs.get("margin_left", None)
        margin_right = kwargs.get("margin_right", None)
        if pady is None:
            hauteur_totale_objet = 0
            for o in objet_name:
                hauteur_totale_objet += self.objet[o].height
            pady = round((self.height - hauteur_totale_objet) / (len(objet_name) + 1))
        y = 0
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
        while len(self.destroyed) > 0:
            self.objet.pop(self.destroyed.pop())
        if self._visible:
            super().draw()
            for o in self.objet.values():
                o.draw()

    def scan_mouse(self):
        x, y = processing.mouseXY()
        click = processing.mouse_click()
        is_ihm: bool = isinstance(self, IhmScreen)
        modale = False
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
                            if click:
                                o.focus = True
                            affichage.cursor(SYSTEM_CURSOR_ARROW)
                            o.scan_mouse()
                            o.scanKeyboard()
                        if o.modale:
                            modale = True
                            break
            if not modale:
                for o in self.objet.values():
                    if o.visible:
                        if type(o) == Bouton:
                            o.scan_mouse()
                        elif isinstance(o, LineEdit):
                            o.scan_mouse()
                        elif isinstance(o, TextEdit):
                            o.scan_events()
                        elif o == self.objet.get('title_box') and (
                                o.collidepoint(x, y) or self.start_drop is not None) and click:

                            if self.start_drop is None:
                                self.start_drop = (self.x - x, self.y - y)
                            else:
                                self.x = x + self.start_drop[0]
                                self.y = y + self.start_drop[1]

                        elif isinstance(o, TextEdit):
                            o.scan_events()

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
            if isinstance(o, TextEdit):
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

    def objet_by_name(self, name: str) -> ["Dialog", Bouton, LineEdit, Label, MultiLineText, TextEdit]:
        return self.objet.get(name)

    def disabled(self, name: str):
        if name == "all":
            for o in self.objet.values():
                o.is_disabled = True
                print(type(o), o.is_disabled)
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
        kwargs['couleurBord'] = kwargs.get('couleurBord', IhmScreen.BORD)
        kwargs['largeurBord'] = kwargs.get('largeurBord', IhmScreen.LARGEUR_BORD)
        kwargs['couleurFond'] = kwargs.get('couleurFond', IhmScreen.FOND)
        kwargs['cadre'] = kwargs.get('cadre', None)
        super().__init__(None, (0, 0, processing.width(), processing.height()), **kwargs)

    def init(self):
        self.setWidth(processing.width())
        self.setHeight(processing.height())
        self.focus = False

    def scan_events(self):
        self.scan_mouse()
        self.scanKeyboard()

    def obj_focused(self) -> [None, "Dialog", Bouton, Label, LineEdit, TextEdit]:
        for o in self.objet.values():
            if o.focus:
                return o
        return None


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

    def scanEvent(self):
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


if __name__ == '__main__':
    t = MultiLineText(0, 1, "bonjour")
    b = Boite((100, 150, 50, 20))
    b.draw()
