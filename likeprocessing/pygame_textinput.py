"""
Copyright 2021, Silas Gyger, silasgyger@gmail.com, All rights reserved.

Borrowed from https://github.com/Nearoo/pygame-text-input under the MIT license.
"""
from __future__ import annotations

import pygame
import pygame.locals as pl
import pyperclip

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyDialog import Boite, LineEdit

pygame.font.init()


class TextInputManager:
    '''
    Keeps track of text inputted, cursor position, etc.
    Pass a validator function returning if a string is valid,
    and the string will only be updated if the validator function
    returns true. 

    For example, limit input to 5 characters:
    ```
    limit_5 = lambda x: len(x) <= 5
    manager = TextInputManager(validator=limit_5)
    ```
    
    :param initial: The initial string
    :param validator: A function string -> bool defining valid input
    '''

    def __init__(self,
                 initial="",
                 validator=lambda x: True):
        self.left = initial  # string to the left of the cursor
        self.right = ""  # string to the right of the cursor
        self.validator = validator
        self.key_return = False
        self.selection_cursor_start = None
        self.selection_cursor_end = None

    def start_selection(self):
        self.selection_cursor_start = self.cursor_pos

    def end_selection(self):
        self.selection_cursor_end = self.cursor_pos

    def selection_value(self):
        if self.selection_cursor_start is None or self.selection_cursor_end is None:
            return ""
        start = min(self.selection_cursor_start, self.selection_cursor_end)
        end = max(self.selection_cursor_start, self.selection_cursor_end)
        return (self.left + self.right)[start:end]

    def erase_selection(self):
        if self.selection_cursor_start is None or self.selection_cursor_end is None:
            return
        start = min(self.selection_cursor_start, self.selection_cursor_end)
        end = max(self.selection_cursor_start, self.selection_cursor_end)
        complete = self.value
        self.value = complete[:start] + complete[end:]
        self.cursor_pos = start
        self.deselect()

    def deselect(self):
        self.selection_cursor_start = None
        self.selection_cursor_end = None

    def select_all(self):
        self.selection_cursor_start = 0
        self.selection_cursor_end = len(self.value)

    @property
    def value(self):
        """ Get / set the value currently inputted. Doesn't change cursor position if possible."""
        return self.left + self.right

    @value.setter
    def value(self, value):
        cursor_pos = self.cursor_pos
        self.left = value[:cursor_pos]
        self.right = value[cursor_pos:]

    @property
    def cursor_pos(self):
        """ Get / set the position of the cursor. Will clamp to [0, length of input]. """
        return len(self.left)

    @cursor_pos.setter
    def cursor_pos(self, value):
        """ Set the cursor position. Will clamp to [0, length of input]. """
        value = max(0, min(len(self.value), value))
        complete = self.value
        self.left = complete[:value]
        self.right = complete[value:]

    def update(self, events):
        """
        Update the interal state with fresh pygame events.
        Call this every frame with all events returned by `pygame.event.get()`.
        """
        self.key_return = False
        for event in events:
            if event.type == pl.KEYDOWN:
                v_before = self.value
                c_before = self.cursor_pos
                self._process_keydown(event)
                if not self.validator(self.value):
                    self.value = v_before
                    self.cursor_pos = c_before

    def _process_keydown(self, ev):
        if pygame.key.get_mods() == 4161:
            attrname = f"_process_shift_ctrl_{pygame.key.name(ev.key)}"
        elif pygame.key.get_mods() & pygame.KMOD_CTRL:
            attrname = f"_process_ctrl_{pygame.key.name(ev.key)}"
        elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
            attrname = f"_process_shift_{pygame.key.name(ev.key)}"
        else:
            attrname = f"_process_{pygame.key.name(ev.key)}"
        if hasattr(self, attrname):
            getattr(self, attrname)()
        else:
            self._process_other(ev)

    def _process_ctrl_backspace(self):
        self.left = self.left[:self.left.rfind(" ", 0, -1) + 1]

    def _process_ctrl_left(self):
        self.cursor_pos = self.left.rfind(" ", 0, -1) + 1

    def _process_ctrl_right(self):
        self.cursor_pos = self.find_end_of_word(self.cursor_pos)

    def _process_shift_right(self):
        if self.selection_cursor_start is None:
            self.selection_cursor_start = self.cursor_pos
            self.cursor_pos += 1
            self.selection_cursor_end = self.cursor_pos
        else:
            self.cursor_pos += 1
            self.selection_cursor_end = self.cursor_pos
        if self.selection_cursor_end == self.selection_cursor_start:
            self.selection_cursor_start = None
            self.selection_cursor_end = None

    def _process_shift_ctrl_right(self):
        if self.selection_cursor_start is None:
            self.selection_cursor_start = self.cursor_pos
            self.cursor_pos = self.find_end_of_word(self.cursor_pos)
            self.selection_cursor_end = self.cursor_pos
        else:
            self.cursor_pos = self.find_end_of_word(self.cursor_pos)
            self.selection_cursor_end = self.cursor_pos
        if self.selection_cursor_end == self.selection_cursor_start:
            self.selection_cursor_start = None
            self.selection_cursor_end = None

    def _process_shift_left(self):
        # Si aucune sélection n'est en cours
        if self.selection_cursor_start is None:
            self.selection_cursor_start = self.cursor_pos
            self.cursor_pos -= 1
            self.selection_cursor_end = self.cursor_pos
        else:
            self.cursor_pos -= 1
            self.selection_cursor_end = self.cursor_pos
        if self.selection_cursor_end == self.selection_cursor_start:
            self.selection_cursor_start = None
            self.selection_cursor_end = None

    def _process_shift_ctrl_left(self):
        if self.selection_cursor_start is None:
            self.selection_cursor_start = self.cursor_pos
            self.cursor_pos = self.find_start_of_word(self.cursor_pos)
            self.selection_cursor_end = self.cursor_pos
        else:
            self.cursor_pos = self.find_start_of_word(self.cursor_pos)
            self.selection_cursor_end = self.cursor_pos
        if self.selection_cursor_end == self.selection_cursor_start:
            self.selection_cursor_start = None
            self.selection_cursor_end = None

    def _process_shift_tab(self):
        if len(self.left)>=4 and self.left[-4:] == "    ": # 4 espaces
            self.left = self.left[:-4]

    def _process_delete(self):
        if self.selection_value() != "":
            self.erase_selection()
        else:
            self.right = self.right[1:]

    def _process_backspace(self):
        if self.selection_value() != "":
            self.erase_selection()
        else:
            self.left = self.left[:-1]

    def _process_right(self):
        self.cursor_pos += 1
        self.deselect()

    def _process_left(self):
        self.cursor_pos -= 1
        self.deselect()

    def _process_end(self):
        self.cursor_pos = len(self.value)
        self.deselect()

    def _process_ctrl_end(self):
        self.cursor_pos = len(self.value)
        self.deselect()

    def _process_ctrl_home(self):
        self.cursor_pos = 0
        self.deselect()

    def _process_home(self):
        self.cursor_pos = 0
        self.deselect()

    def _process_return(self):
        self.key_return = True

    def _process_enter(self):
        self.key_return = True

    def _process_tab(self):
        if self.right[:4] =="    ": # 4 espaces
            self.right = self.right[4:]
        self.left += "    "

    def _process_escape(self):
        self.deselect()

    def _process_other(self, event):
        if event.unicode != "" and self.selection_cursor_start is not None:
            self.erase_selection()
        self.left += event.unicode

    def _process_ctrl_v(self):
        coller = pyperclip.paste()
        print(coller)
        if self.selection_cursor_start is not None:
            self.erase_selection()
        self.left += coller

    def _process_ctrl_c(self):
        pyperclip.copy(self.selection_value())

    def _process_ctrl_x(self):
        pyperclip.copy(self.selection_value())
        self.erase_selection()

    def _process_ctrl_a(self):
        self.select_all()

    def find_end_of_word(self, cursor_pos):
        pos = cursor_pos + 1
        while pos < len(self.value) and self.value[pos] == " ":
            pos += 1
        while pos < len(self.value) and self.value[pos] != " ":
            pos += 1
        return pos

    def find_start_of_word(self, cursor_pos):
        pos = cursor_pos - 1
        while pos >= 0 and self.value[pos] == " ":
            pos -= 1
        while pos >= 0 and self.value[pos] != " ":
            pos -= 1
        return pos + 1


class TextInputVisualizer:
    """
    Utility class to quickly visualize textual input, like a message or username.
    Pass events every frame to the `.update` method, then get the surface
    of the rendered font using the `.surface` attribute.

    All arguments of constructor can also be set via attributes, so e.g.
    to change `font_color` do
    ```
    inputVisualizer.font_color = (255, 100, 0)
    ```
    The surface itself is lazily re-rendered only when the `.surface` field is 
    accessed, and if any parameters changed since the last `.surface` access, so
    values can freely be changed between renders without performance overhead.

    :param manager: The TextInputManager used to manage the user input
    :param font_object: a pygame.font.Font object used for rendering
    :param antialias: whether to render the font antialiased or not
    :param font_color: color of font rendered
    :param cursor_blink_interal: the interval of the cursor blinking, in ms
    :param cursor_width: The width of the cursor, in pixels
    :param cursor_color: The color of the cursor
    """

    def __init__(self,
                 manager=None,
                 font_object=None,
                 width_max: [int, None] = None,
                 antialias=True,
                 font_color=(0, 0, 0),
                 cursor_blink_interval=300,
                 cursor_width=3,
                 cursor_color=(0, 0, 0)
                 ):

        self._manager = TextInputManager() if manager is None else manager
        self._font_object = pygame.font.Font(pygame.font.get_default_font(), 25) if font_object is None else font_object
        self._width_max = width_max
        self._antialias = antialias
        self._font_color = font_color

        self._clock = pygame.time.Clock()
        self._cursor_blink_interval = cursor_blink_interval
        self._cursor_visible = False
        self._last_blink_toggle = 0

        self._cursor_width = cursor_width
        self._cursor_color = cursor_color

        self._surface = pygame.Surface((self._cursor_width, self._font_object.get_height()))
        self._rerender_required = True

    def set_cursor_pos(self, cursor_pos: int):
        """ Set the cursor position. """
        self.manager.cursor_pos = cursor_pos
        self._rerender()

    @property
    def value(self):
        """ Get / set the value of text alreay inputted. Doesn't change cursor position if possible."""
        return self.manager.value

    @value.setter
    def value(self, v):
        self.manager.value = v

    @property
    def manager(self):
        """ Get / set the underlying `TextInputManager` for this instance"""
        return self._manager

    @manager.setter
    def manager(self, v):
        self._manager = v

    @property
    def surface(self):
        """ Get the surface with the rendered user input """
        if self._rerender_required:
            self._rerender()
            self._rerender_required = False
        return self._surface

    @property
    def antialias(self):
        """ Get / set antialias of the render """
        return self._antialias

    @antialias.setter
    def antialias(self, v):
        self._antialias = v
        self._require_rerender()

    @property
    def font_color(self):
        """ Get / set color of rendered font """
        return self._font_color

    @font_color.setter
    def font_color(self, v):
        self._font_color = v
        self._require_rerender()

    @property
    def font_object(self):
        """ Get / set the font object used to render the text """
        return self._font_object

    @font_object.setter
    def font_object(self, v):
        self._font_object = v
        self._require_rerender()

    @property
    def cursor_visible(self):
        """ Get / set cursor visibility (flips again after `.cursor_interval` if continuously update)"""
        return self._cursor_visible

    @cursor_visible.setter
    def cursor_visible(self, v):
        self._cursor_visible = v
        self._require_rerender()

    @property
    def cursor_width(self):
        """ Get / set width in pixels of the cursor """
        return self._cursor_width

    @cursor_width.setter
    def cursor_width(self, v):
        self._cursor_width = v
        self._require_rerender()

    @property
    def cursor_color(self):
        """ Get / set the color of the cursor """
        return self._cursor_color

    @cursor_color.setter
    def cursor_color(self, v):
        self._cursor_color = v
        self._require_rerender()

    @property
    def cursor_blink_interval(self):
        """ Get / set the interval of time with which the cursor blinks (toggles), in ms"""
        return self._cursor_blink_interval

    @cursor_blink_interval.setter
    def cursor_blink_interval(self, v):
        self._cursor_blink_interval = v

    def update(self, events: pygame.event.Event):
        """
        Update internal state.
        
        Call this once every frame with all events returned by `pygame.event.get()`
        """

        # Update self.manager internal state, rerender if value changes
        value_before = self.manager.value
        self.manager.update(events)
        if self.manager.value != value_before:
            self._require_rerender()

        # Update cursor visibility after self._blink_interval milliseconds
        self._clock.tick()
        self._last_blink_toggle += self._clock.get_time()
        if self._last_blink_toggle > self._cursor_blink_interval:
            self._last_blink_toggle %= self._cursor_blink_interval
            self._cursor_visible = not self._cursor_visible
            self._require_rerender()

        # Make cursor visible when something is pressed
        if [event for event in events if event.type == pl.KEYDOWN]:
            self._last_blink_toggle = 0
            self._cursor_visible = True
            self._require_rerender()

    def _require_rerender(self):
        """
        Trigger a re-render of the surface the next time the surface is accessed.
        """
        self._rerender_required = True

    def _rerender(self):
        """ Rerender self._surface."""
        # Final surface is slightly larger than font_render itself, to accomodate for cursor
        rendered_surface = self.font_object.render(self.manager.value,
                                                   self.antialias,
                                                   self.font_color)
        rendered_left_surface = self.font_object.render(self.manager.left,
                                                        self.antialias,
                                                        self.font_color)
        w, h = rendered_surface.get_size()
        self._surface = pygame.Surface((w + self._cursor_width, h))
        self._surface = self._surface.convert_alpha(rendered_surface)
        self._surface.fill((0, 0, 0, 0))
        # Draw selection text rectangle if exists
        if self.manager.selection_value() != "":
            str_selection = self.manager.selection_value()
            selection_start = min(self.manager.selection_cursor_start, self.manager.selection_cursor_end)
            selection_x = self.font_object.size(self.value[:selection_start])[0]
            width_selection = min(self.font_object.size(str_selection)[0], self._width_max)
            selection_rect = pygame.Rect(selection_x, 0, width_selection, self.font_object.get_height())
            self._surface.fill((0, 0, 255, 100), selection_rect)
        # Draw the text
        area = pygame.Rect(max(0, rendered_left_surface.get_width() - self._width_max), 0,
                           self._width_max, h)
        self._surface.blit(rendered_surface, (0, 0), area)
        # Draw the cursor if visible
        if self._cursor_visible:
            str_left_of_cursor = self.manager.value[:self.manager.cursor_pos]
            cursor_x = min(self.font_object.size(str_left_of_cursor)[0], self._width_max)
            cursor_rect = pygame.Rect(cursor_x, 0, self._cursor_width, self.font_object.get_height())
            self._surface.fill(self._cursor_color, cursor_rect)

    def deselect(self):
        """ deselect the current selection """
        self.manager.deselect()
        self._require_rerender()


class MultilineTextInputManager(TextInputManager):
    '''
    Keeps track of text inputted, cursor position, etc.
    Pass a validator function returning if a string is valid,
    and the string will only be updated if the validator function
    returns true.

    For example, limit input to 5 characters:
    ```
    limit_5 = lambda x: len(x) <= 5
    manager = TextInputManager(validator=limit_5)
    ```

    :param initial: The initial string
    :param validator: A function string -> bool defining valid input
    '''

    def __init__(self,
                 initial="", width_max=100, font_object=None,
                 validator=lambda x: True):
        super().__init__(initial, validator)
        self._width_max = width_max
        self.font_object = font_object

    def find_last_space(self, text):
        """ Find the last space in the text. """
        for i, char in enumerate(reversed(text)):
            if char.isspace():
                return len(text) - i
        return 0

    def slice_texte(self) -> (list[str], int, int):
        # Découper le texte en lignes selon la largeur maximale
        lines = []
        current_line = ""
        cursor_line = 0
        for i, char in enumerate(self.value):
            if char == "\n":
                current_line += "\n"
                lines.append(current_line)
                current_line = ""
            elif self.font_object.size(current_line + char)[0] < self._width_max:
                current_line += char
            else:
                p = self.find_last_space(current_line)
                lines.append(current_line[:p])
                current_line = current_line[p:] + char
        if len(self.value) > 0:
            lines.append(current_line)
        cursor_pos = self.cursor_pos  # -self.left.count("\n")
        # print(cursor_pos)
        # print(lines)
        # print([self.left])
        for i, line in enumerate(lines):
            ls = line
            if cursor_pos > len(ls):
                cursor_pos -= len(ls)
            elif len(ls) == 0 or (cursor_pos == len(ls) and i < len(lines) - 1):
                cursor_pos = 0
                cursor_line = i + 1
                break
            else:
                cursor_line = i
                break
        # print(cursor_pos,len(lines))
        # print()
        return lines, cursor_line, cursor_pos

    def _process_up(self):
        """ Move the cursor up. """
        lines, cursor_line, cursor_pos = self.slice_texte()
        if cursor_line > 0:
            s = sum([len(l) for l in lines[:cursor_line - 1]])
            m = min(cursor_pos, len(lines[cursor_line - 1].strip("\n")))
            self.cursor_pos = s + m
        self.deselect()

    def _process_shift_up(self):
        """ Move the cursor up while selecting. """
        lines, cursor_line, cursor_pos = self.slice_texte()
        if cursor_line > 0:
            s = sum([len(l) for l in lines[:cursor_line - 1]])
            m = min(cursor_pos, len(lines[cursor_line - 1].strip("\n")))
            cursor_pos = s + m
            if self.selection_cursor_start is None:
                self.selection_cursor_start = self.cursor_pos
                self.cursor_pos = cursor_pos
                self.selection_cursor_end = cursor_pos
            else:
                self.cursor_pos = cursor_pos
                self.selection_cursor_end = self.cursor_pos
            if self.selection_cursor_end == self.selection_cursor_start:
                self.selection_cursor_start = None
                self.selection_cursor_end = None

    def _process_down(self):
        """ Move the cursor down. """
        lines, cursor_line, cursor_pos = self.slice_texte()
        if cursor_line < len(lines) - 1:
            self.cursor_pos = sum([len(l) for l in lines[:cursor_line + 1]]) + min(cursor_pos,
                                                                                   len(lines[cursor_line + 1].strip(
                                                                                       "\n")))
        self.deselect()

    def _process_shift_down(self):
        """ Move the cursor down while selecting. """
        lines, cursor_line, cursor_pos = self.slice_texte()
        if cursor_line < len(lines) - 1:
            cursor_pos = sum([len(l) for l in lines[:cursor_line + 1]]) + min(cursor_pos,
                                                                               len(lines[cursor_line + 1].strip("\n"))
                                                                               )
            if self.selection_cursor_start is None:
                self.selection_cursor_start = self.cursor_pos
                self.cursor_pos = cursor_pos
                self.selection_cursor_end = cursor_pos
            else:
                self.cursor_pos = cursor_pos
                self.selection_cursor_end = self.cursor_pos
            if self.selection_cursor_end == self.selection_cursor_start:
                self.selection_cursor_start = None
                self.selection_cursor_end = None

    def _process_end(self):
        lines, cursor_line, cursor_pos = self.slice_texte()
        self.cursor_pos = sum([len(l) for l in lines[:cursor_line]]) + len(lines[cursor_line].strip("\n")) - 1
        self.deselect()

    def _process_home(self):
        lines, cursor_line, cursor_pos = self.slice_texte()
        self.cursor_pos = sum([len(l) for l in lines[:cursor_line]])
        self.deselect()

    def _process_return(self):
        """ Add a new line. """
        self.left += "\n"

    def _process_enter(self):
            """ Add a new line. """
            self.left += "\n"

    def move_up(self):
        """ Move the cursor up. """
        self._process_up()

    def move_down(self):
        """ Move the cursor down. """
        self._process_down()

class MultilineTextInputVisualizer(TextInputVisualizer):
    """
    Utility class to quickly visualize textual multiline input, like a long message or text.
    Pass events every frame to the `.update` method, then get the surface
    of the rendered font using the `.surface` attribute.

    All arguments of constructor can also be set via attributes, so e.g.
    to change `font_color` do
    ```
    inputVisualizer.font_color = (255, 100, 0)
    ```
    The surface itself is lazily re-rendered only when the `.surface` field is
    accessed, and if any parameters changed since the last `.surface` access, so
    values can freely be changed between renders without performance overhead.

    :param manager: The TextInputManager used to manage the user input
    :param width_max: The maximum width of the rendered text, in pixels
    :param height_max: The maximum height of the rendered text, in pixels
    :param font_object: a pygame.font.Font object used for rendering
    :param antialias: whether to render the font antialiased or not
    :param font_color: color of font rendered
    :param cursor_blink_interal: the interval of the cursor blinking, in ms
    :param cursor_width: The width of the cursor, in pixels
    :param cursor_color: The color of the cursor
    """

    def __init__(self, manager: MultilineTextInputManager,
                 width_max: int,
                 height_max: int,
                 font_object: pygame.font.Font,
                 antialias: bool = True,
                 font_color: tuple[int, int, int] = (0, 0, 0),
                 cursor_blink_interval: int = 300,
                 cursor_width: int = 2,
                 cursor_color: tuple[int, int, int] = (0, 0, 0)):
        self.manager = manager
        super().__init__(self.manager, font_object, width_max, antialias, font_color, cursor_blink_interval,
                         cursor_width, cursor_color)
        self._height_max = height_max
        self._scroll_offset = 0
        self._line_height = self.font_object.get_height()
        self._current_line_index = 0
        self._lines = []

    def posxy_to_cursor_pos(self, x: int, y: int) -> int:
        """ Convert a position (x, y) to a cursor position. """
        # Trouver la ligne correspondante à la position y
        if len(self._lines) == 0:
            return 0
        line_index = max(min((y + self._scroll_offset) // self._line_height, len(self._lines) - 1), 0)
        # Trouver la position du curseur dans cette ligne
        cursor_pos = sum([len(l) for l in self._lines[:line_index]])
        nb_car = len(self._lines[line_index])
        i = 0
        for i in range(nb_car):
            w_car = self.font_object.size(self._lines[line_index][:i + 1])[0]
            if w_car >= x:
                break
        if i == nb_car - 1:
            if self._lines[line_index][i] not in ["\n", " "]:
                cursor_pos += i + 1
            else:
                cursor_pos += nb_car - 1
        else:
            cursor_pos += i
        return cursor_pos

    def set_cursor_pos(self, cursor_pos: int):
        """ Set the cursor position. """
        self.manager.cursor_pos = cursor_pos
        self._rerender()

    def _rerender(self):
        """ Rerender self._surface with multi-line text support. """

        # Découper le texte en lignes, trouver la ligne contenant le curseur et la position du curseur dans cette ligne
        self._lines, self._current_line_index, cursor_pos = self.manager.slice_texte()
        # Calculer la hauteur totale nécessaire pour toutes les lignes
        total_height = self._line_height * len(self._lines)

        # Ajuster le scroll pour rendre le curseur visible
        top_visible_line = self._scroll_offset // self._line_height
        bottom_visible_line = top_visible_line + self._height_max // self._line_height

        if self._current_line_index <= top_visible_line:
            # Curseur au-dessus de la zone visible, scroll vers le haut
            self._scroll_offset = max(0, self._current_line_index * self._line_height)
        elif self._current_line_index >= bottom_visible_line:
            # Curseur en dessous de la zone visible, scroll vers le bas
            self._scroll_offset = min(total_height - self._height_max, self._current_line_index * self._line_height)

        # Créer la surface en fonction de la hauteur visible
        self._surface = pygame.Surface((self._width_max, self._height_max), pygame.SRCALPHA)
        self._surface.fill((0, 0, 0, 0))

        # Calcul des indices de la sélection
        if self.manager.selection_cursor_start is not None and self.manager.selection_cursor_end is not None:
            start = min(self.manager.selection_cursor_start, self.manager.selection_cursor_end)
            end = max(self.manager.selection_cursor_start, self.manager.selection_cursor_end)
        else:
            start, end = None, None

        # Dessiner chaque ligne visible
        selected_lines = 0
        for i, line in enumerate(self._lines):
            y_position = i * self._line_height - self._scroll_offset
            if 0 <= y_position < self._height_max:  # Si la ligne est visible
                if line == "":
                    # Si la ligne est vide, on dessine un espace pour que la hauteur de la ligne soit correcte
                    line = " "
                if line[-1] == "\n":
                    # Enlever le retour à la ligne à la fin de la ligne
                    line = line[:-1]
                rendered_line = self.font_object.render(line, self.antialias, self.font_color)
                text_width, text_height = rendered_line.get_size()

                # Gérer la sélection ligne par ligne
                if start is not None and end is not None:

                    line_start_index = sum(
                        len(self._lines[i]) for i in range(i))  # Index de début de cette ligne
                    line_end_index = line_start_index + len(line) - 1

                    # Vérifie si la sélection croise cette ligne
                    if line_end_index > start and line_start_index < end:
                        # Calcule les indices locaux de la sélection pour cette ligne
                        selection_start = max(0, start - line_start_index)
                        if self._current_line_index == i and self.manager.cursor_pos == end:
                            selection_end = cursor_pos
                        else:
                            selection_end = min(len(line), end - line_start_index)
                        # print("ss, se :",selection_start, selection_end)
                        # Découpe la ligne en trois parties : avant, sélectionnée, après
                        before_selection = line[:selection_start]
                        selected_text = line[selection_start:selection_end]
                        after_selection = line[selection_end:]
                        # print(f"before: '{before_selection}', selected '{selected_text}', after :'{after_selection}'")

                        # Dessiner le fond bleu pour la sélection
                        selected_surface = self.font_object.render(selected_text, True, self.font_color)
                        selected_width, _ = selected_surface.get_size()
                        selection_rect = pygame.Rect(self.font_object.size(before_selection)[0], y_position,
                                                     selected_width,
                                                     text_height,
                                                     )
                        self._surface.fill((0, 0, 255, 100), selection_rect)

                        # Affiche le texte avant la sélection
                        self._surface.blit(self.font_object.render(before_selection, True, self.font_color),
                                           (0, y_position))

                        # Affiche le texte sélectionné
                        self._surface.blit(selected_surface,
                                           (selection_rect.x, selection_rect.y))

                        # Affiche le texte après la sélection
                        self._surface.blit(self.font_object.render(after_selection, True, self.font_color),
                                           (selection_rect.x + selected_width, selection_rect.y))

                    else:
                        self._surface.blit(rendered_line, (0, y_position))
                else:
                    self._surface.blit(rendered_line, (0, y_position))

        # Gérer le curseur
        if self._cursor_visible:
            try:
                cursor_x = self.font_object.size(self._lines[self._current_line_index][:cursor_pos])[0]
            except:
                cursor_x = 0
            cursor_y = self._current_line_index * self._line_height - self._scroll_offset

            if 0 <= cursor_y < self._height_max:
                cursor_rect = pygame.Rect(cursor_x, cursor_y, self._cursor_width, self._line_height)
                self._surface.fill(self._cursor_color, cursor_rect)

        # Debugging pour traquer le scroll
        DEBUG = False
        if DEBUG:
            print(f"Cursor line: {self._current_line_index}, Cursor position: {cursor_pos}")
            if self.manager.cursor_pos < len(self.manager.value):
                print(
                    f"cursor: {self.manager.cursor_pos}, char_pos_cursor: '{self.manager.value[self.manager.cursor_pos]}'")
            # if len(self.manager.left) > 0 and len(self.manager.right) > 0:
            #     print(f", left[-1]: {ord(self.manager.left[-1])} , right[0]: {self.manager.right[0]} ")
            print(
                f"startm: {self.manager.selection_cursor_start}, endm: {self.manager.selection_cursor_end} start: {start}, end: {end}")


class TextLineInput(TextInputVisualizer):
    """encapsulates a single line of text input"""

    def __init__(self, parent: [Boite, LineEdit],
                 initial: str = "",
                 validator=lambda x: True,
                 antialias=True,
                 font_color=(0, 0, 0),
                 cursor_blink_interval=300,
                 cursor_width=3,
                 cursor_color=(0, 0, 0)
                 ):
        self.parent = parent
        self.manager = TextInputManager(initial, validator)
        super().__init__(self.manager, self.parent.font_object, self.parent.width - 6, antialias, font_color,
                         cursor_blink_interval,
                         cursor_width, cursor_color)


class MultilineTextLineInput(MultilineTextInputVisualizer):
    """encapsulates a single line of text input"""

    def __init__(self, parent: [Boite, LineEdit],
                 initial: str = "",
                 validator=lambda x: True,
                 antialias=True,
                 font_color=(0, 0, 0),
                 cursor_blink_interval=300,
                 cursor_width=3,
                 cursor_color=(0, 0, 0)
                 ):
        self.parent = parent
        self.manager = MultilineTextInputManager(initial, self.parent.width - 6, self.parent.font_object, validator)
        super().__init__(self.manager, self.parent.width - 6, self.parent.height - 6, self.parent.font_object,
                         antialias, font_color,
                         cursor_blink_interval, cursor_width, cursor_color)


######################################
#  The example from the repo README: #
######################################

if __name__ == "__main__":
    pygame.init()

    # No arguments needed to get started

    # But more customization possible: Pass your own font object
    font = pygame.font.SysFont("Consolas", 12)
    # Create own manager with custom input validator
    manager = MultilineTextInputManager(
        initial="bonjour les amis. Comment allez vous ? Moi je vais bien pour l'instant mais demain il va pleuvoir.",
        width_max=200, font_object=font)
    # Pass these to constructor
    textinput_custom = MultilineTextInputVisualizer(manager=manager, width_max=200, height_max=40, font_object=font)
    # Customize much more
    textinput_custom.cursor_width = 4
    textinput_custom.cursor_blink_interval = 400  # blinking interval in ms
    textinput_custom.antialias = False
    textinput_custom.font_color = (0, 85, 170)

    managerl = TextInputManager(initial="bonjour les amis. ")
    # Pass these to constructor
    textinput_customl = TextInputVisualizer(manager=managerl, width_max=200, font_object=font)
    # Customize much more
    textinput_customl.cursor_width = 4
    textinput_customl.cursor_blink_interval = 400  # blinking interval in ms
    textinput_customl.antialias = False
    textinput_customl.font_color = (0, 85, 170)

    screen = pygame.display.set_mode((1000, 500))
    clock = pygame.time.Clock()

    # Pygame now allows natively to enable key repeat:
    pygame.key.set_repeat(200, 25)

    while True:
        screen.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()



        # Feed it with events every frame
        if pygame.mouse.get_pos()[1] < 90:
            textinput_custom.update(events)
        else:
            textinput_customl.update(events)

        # Get its surface to blit onto the screen
        pygame.draw.rect(screen, (255, 255, 255), (10, 50, 200, 40))
        screen.blit(textinput_custom.surface, (10, 50))

        pygame.draw.rect(screen, (255, 255, 255), (10, 150, 200, 40))
        screen.blit(textinput_customl.surface, (10, 150))
        # Modify attributes on the fly - the surface is only rerendered when .surface is accessed & if values changed
        # textinput_custom.font_color = [(c + 10) % 255 for c in textinput_custom.font_color]

        # Check if user pressed return
        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            print(f"User pressed enter! Input so far: {textinput_custom.value}")

        pygame.display.update()
        clock.tick(30)
