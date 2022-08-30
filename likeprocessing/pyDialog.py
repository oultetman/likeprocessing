import likeprocessing as processing
import os.path
import pygame

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
        self.destroy = False

    def init(screen: pygame.Surface):
        Boite.ecran = screen

    @property
    def parent(self):
        return self.Parent

    @parent.setter
    def parent(self, monPere):
        self.Parent = monPere

    def setX(self, value: int):
        self.x = value

    def setY(self, value: int):
        self.y = value

    def draw(self):
        r = pygame.Surface((self.width, self.height))
        if self.couleurFond:
            r.fill(self.couleurFond)
            Boite.ecran.blit(r, [self.Parent.left + self.left, self.Parent.top + self.top])
        if self.largeurBord>0:
            r = pygame.Rect(self.Parent.left + self.left, self.Parent.top + self.top, self.width, self.height)
            pygame.draw.rect(Boite.ecran, self.couleurBord, r, self.largeurBord)

    def collidepoint(self, x, y):
        return super().collidepoint(x - self.parent.left, y - self.parent.top)

    def scan_mouse(self):
        pass

    def scanKeyboard(self):
        pass


class PygTexte(Boite):
    def __init__(self, parent, rect, texte, police='arial', taille=12, angle=0, **kwargs):
        if len(rect) == 2:
            rect = (rect[0], rect[1], 0, 0)
        super().__init__(parent, rect, **kwargs)
        self._texte = texte.split("\n")
        self.police = police
        self.taille = taille
        self.largeurBord = kwargs.get('largeurBord', 1)
        self.couleurBord = kwargs.get('couleurBord', 1)
        self.couleurPolice = kwargs.get('couleurPolice', BLACK)
        self.angle = angle
        self.image = self.imageTexte()

    @property
    def texte(self):
        return self._texte

    @texte.setter
    def texte(self, text: str):
        self._texte = text.split("\n")
        self.image = self.imageTexte()

    def imageTexte(self):
        rec_font = pygame.font.SysFont(self.police, self.taille)
        text_bitmap = []
        width = 0
        height = 0
        for t in self._texte:
            text_bitmap.append(rec_font.render(t, True, self.couleurPolice))
            r = text_bitmap[-1].get_rect()
            width = max(width, r.width)
            height = height + r.height
        if self.angle != 0:
            text_bitmap = pygame.transform.rotate(text_bitmap, self.angle)
        self.width = max(width, self.width)
        self.height = max(height, self.height)
        return text_bitmap

    def draw(self):
        # fonction qui permet l'affichage de texte à  l'ecran
        super().draw()
        y = self.Parent.top + self.top
        for i in self.image:
            Boite.ecran.blit(i, [self.Parent.left + self.left, y])
            y += i.get_rect().height

    def __str__(self):
        return super().__str__() + " " + str(self.texte)


class Label(Boite):
    def __init__(self, parent, rect, texte: str, police='arial', taille=12, couleurPolice=BLACK,
                 angle=0, **kwargs):
        if len(rect) == 2:
            rect = (rect[0], rect[1], 0, 0)
        couleurBord = kwargs.get('couleurBord', "black")
        largeurBord = kwargs.get('largeurBord', 0)
        couleurFond = kwargs.get('couleurFond', None)
        self.bold = kwargs.get('bold', None)
        self.italic = kwargs.get('italic', None)
        self.align_v = kwargs.get('align_v', "TOP").upper()
        self.align_h = kwargs.get('align_h', "LEFT").upper()
        super().__init__(parent, rect, couleurBord=couleurBord, largeurBord=largeurBord, couleurFond=couleurFond)
        self._texte = texte
        self.police = police
        self.taille = taille
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

    @property
    def texte(self):
        return self._texte

    @texte.setter
    def texte(self, text: str):
        self._texte = text
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
        # fonction qui permet l'affichage de texte à  l'ecran
        super().draw()
        if self.align_h == "LEFT":
            x = self.Parent.left + self.left + 2
        elif self.align_h == "CENTER":
            x = self.Parent.left + self.left + 2 + (self.width - self.image.get_width()) // 2
        elif self.align_h == "RIGHT":
            x = self.Parent.left + self.left - 2 + (self.width - self.image.get_width())
        if self.align_v == "TOP":
            y = self.Parent.top + self.top + 2
        elif self.align_v == "CENTER":
            y = self.Parent.top + self.top + 2 + (self.height - self.image.get_height()) // 2
        elif self.align_v == "BOTTOM":
            y = self.Parent.top + self.top - 2 + (self.height - self.image.get_height())
        Boite.ecran.blit(self.image, [x, y])

    def __str__(self):
        return super().__str__() + " " + str(self.texte)


class LineEdit(Boite):
    def __init__(self, parent, rect, texte: str, police='arial', taille=12, couleurPolice=BLACK, couleurFond=()):
        super().__init__(parent, rect)
        self.texte = TextInput(police)
        self.texte.input_string = texte
        self._focus = False

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, val: bool):
        if val is not self._focus:
            self._focus = not self._focus
            self.texte.focus = self._focus

    def update(self, events):
        self.texte.update(events)

    def draw(self):
        super().draw()
        Boite.ecran.blit(self.texte.get_surface(), (self.Parent.left + self.left + 3, self.Parent.top + self.top))

    def __str__(self):
        return self.texte.input_string

    def __len__(self):
        return len(self.texte.input_string)


class Bouton(Boite):
    BOUTON_FOND = (225, 255, 255)
    BOUTON_FOND_MOUSE_ON = (229, 241, 251)
    BOUTON_BORD = (173, 173, 173)
    BOUTON_BORD_MOUSE_ON = (0, 120, 215)

    def __init__(self, parent, rect, texte, defaut=False, **kwargs):
        if defaut:
            b = 2
        else:
            b = 1
        super().__init__(parent, rect, couleurBord=Bouton.BOUTON_BORD, largeurBord=b, couleurFond=Bouton.BOUTON_FOND)
        self.fonction = kwargs.get("command", None)
        self.mouseOn = False
        self.mouseClick = False
        self.texte = PygTexte(parent, (2, 2), texte, couleurFond=self.couleurFond, couleurBord=self.couleurFond)
        self.texte.left = self.left + (self.width - self.texte.width) // 2
        self.texte.top = self.top + (self.height - self.texte.height) // 2

    def setX(self, value: int):
        self.x = value
        self.texte.left = self.left + (self.width - self.texte.width) // 2

    def setY(self, value: int):
        self.y = value
        self.texte.top = self.top + (self.height - self.texte.height) // 2

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
        if self.mouseOn:
            self.couleurBord = Bouton.BOUTON_BORD_MOUSE_ON
            if self.mouseClick:
                self.couleurFond = Bouton.BOUTON_BORD_MOUSE_ON
                self.texte.couleurFond = Bouton.BOUTON_BORD_MOUSE_ON
                self.texte.couleurBord = Bouton.BOUTON_BORD_MOUSE_ON
            else:
                self.couleurFond = Bouton.BOUTON_FOND_MOUSE_ON
                self.texte.couleurFond = Bouton.BOUTON_FOND_MOUSE_ON
                self.texte.couleurBord = Bouton.BOUTON_FOND_MOUSE_ON
        else:
            self.couleurBord = Bouton.BOUTON_BORD
            self.couleurFond = Bouton.BOUTON_FOND
        super().draw()
        self.texte.draw()

    def scan_mouse(self):
        x, y = processing.mouseXY()
        click = processing.click
        if self.collidepoint(x, y):
            self.mouseOn = True
        else:
            self.mouseOn = False
        if click is False and self.mouseClick is True:
            self.mouseClick = False
            if self.mouseOn is True and self.fonction is not None:
                self.fonction()
        elif click is True and self.mouseOn is True:
            self.mouseClick = True


class Dialog(Boite):
    """Classe qui permet de créer une boite de dialogue vide
    munie d'une barre de titre et d'une casse de fermeture"""
    dialogue = 1
    FOND = (255, 255, 255)
    BORD = (150, 150, 150)

    def __init__(self, parent, rect, **kwargs):
        super().__init__(parent, rect, couleurBord=Dialog.BORD, largeurBord=1, couleurFond=Dialog.FOND)
        self.pos = kwargs.get('pos', None)
        self.objet = {}
        self.addObjet(
            Boite(self, (2, 2, self.width - 19, 16), couleurBord=Dialog.BORD, largeurBord=1, couleurFond=Dialog.FOND),
            "title_box")
        self.addObjet(Label(self, (4, 2, self.width - 19, 16), "Dialog" + str(Dialog.dialogue)), "title")
        self.addObjet(Bouton(self, (self.width - 17, 2, 16, 16), "X"), "close")
        self.visible = True
        self.start_drop = None
        Dialog.dialogue += 1
        self.num_object = 1
        self.destroy = False
        self.objet['close'].connecte(self.quitter)
        self._focus = False
        self.focus = False
        self.modale = False
        self.positionne()

    def positionne(self):
        if self.pos == "center":
            self.center_me()

    def center_me(self):
        """center la boite sue l'écran"""
        self.x = (self.parent.width - self.width) // 2
        self.y = (self.parent.height - self.height) // 2

    def quitter(self):
        self.visible = False
        self.destroy = True

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, value: bool):
        self._focus = value
        self.objet['title'].enabled = self._focus

    def setWidth(self, value: int):
        self.width = value
        self.objet['close'].setX(self.width - 17)
        self.objet['title_box'].width = self.width - 19
        self.objet['title'].setWidth(self.width - 19)

    def setHeight(self, value: int):
        self.height = value

    @property
    def title(self):
        return self.objet['title'].texte

    @title.setter
    def title(self, texte: str):
        self.objet["title"].texte = str(texte)

    def addObjet(self, objet, nom: str = None):
        if type(objet) == list:
            for o in objet:
                if type(o) == tuple or type(o) == list:
                    self.objet[o[1]] = o[0]
                else:
                    self.objet[f"obj_{self.num_object}"] = o
                    self.num_object += 1
        else:
            if nom is None:
                nom = f"obj_{self.num_object}"
            self.objet[nom] = objet
            if nom[:4] == 'obj_':
                self.num_object += 1

    def center(self, objet_name: [str, list[str]]):
        if isinstance(objet_name, list):
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
            self.objet[objet_name].setX((self.width - self.objet[objet_name].width) // 2)

    def draw(self):
        if self.visible:
            super().draw()
            for o in self.objet.values():
                o.draw()

    def scan_mouse(self):
        x, y = processing.mouseXY()
        click = processing.click
        if self.visible and self.focus:
            if click:
                self.lostFocus()
            else:
                self.start_drop = None
            for o in self.objet.values():
                if type(o) == Bouton:
                    if o.collidepoint(x, y):
                        o.mouseOn = True
                    else:
                        o.mouseOn = False
                    if click is False and o.mouseClick is True:
                        o.mouseClick = False
                        if o.mouseOn is True and o.fonction is not None:
                            o.fonction()
                    elif click is True and o.mouseOn is True:
                        o.mouseClick = True
                elif type(o) == LineEdit:
                    if o.collidepoint(x, y) and click is True:
                        o.focus = True
                elif o == self.objet['title_box'] and (
                        o.collidepoint(x, y) or self.start_drop is not None) and click == True:
                    if self.start_drop is None:
                        self.start_drop = (x, y)
                    elif self.start_drop != (x, y):
                        self.x += x - self.start_drop[0]
                        self.y += y - self.start_drop[1]
                        self.start_drop = x, y

    def scanKeyboard(self):
        for o in self.objet.values():
            if type(o) == LineEdit and o.focus:
                o.update(processing.events)

    def lostFocus(self):
        for o in self.objet.values():
            if type(o) == LineEdit:
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
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if not event.key in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:  # FIXME: Delete at beginning of line?
                    self._input_string = self._input_string[:max(self.cursor_position - 1, 0)] + \
                                         self._input_string[self.cursor_position:]

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pl.K_DELETE:
                    self._input_string = self._input_string[:self.cursor_position] + \
                                         self._input_string[self.cursor_position + 1:]

                elif event.key == pl.K_RETURN:
                    return True

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self._input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self._input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                else:
                    # If no special key is pressed, add unicode of key to input_string
                    self._input_string = self._input_string[:self.cursor_position] + \
                                         event.unicode + \
                                         self._input_string[self.cursor_position:]
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pl.KEYUP:
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
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

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
        print(obj)

    def scanEvent(self):
        x, y = processing.mouseXY()
        if self.obj_focus is not None and self.obj_focus.modale is True:
            self.obj_focus.scan_mouse()
            self.obj_focus.scanKeyboard()
        else:
            for o in self:
                if isinstance(o, Dialog):
                    if o.collidepoint(x, y):
                        if processing.click:
                            if self.obj_focus is None or not self.obj_focus.collidepoint(x, y):
                                self.take_focus(o)
                        o.scan_mouse()
                        o.scanKeyboard()
                else:
                    o.scan_mouse()


if __name__ == '__main__':
    t = PygTexte(0, 1, "bonjour")
    b = Boite((100, 150, 50, 20))
    b.draw()
