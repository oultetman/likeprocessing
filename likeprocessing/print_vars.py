import sys

from likeprocessing.processing import *
from likeprocessing.texte import *
from likeprocessing.affichage import *
import traceback


def set_x(valeur: int):
    processing.__print_x = valeur


def set_y(valeur: int):
    processing.__print_y = valeur


def get_x():
    return processing.__print_x


def get_y():
    return processing.__print_y


def print_var(variable, **kwargs):
    selected = kwargs.get("selected", None)
    end = kwargs.get("end", None)
    if variable == "":
        set_y(get_y() + 5)
        set_x(5)
    elif variable == "\t":
        set_x(get_x() + 20)
    elif variable == "-":
        line(get_x(), get_y(), width() - 5, get_y())
        set_y(get_y() + 5)
    else:
        stack = traceback.extract_stack(limit=2)
        nom = stack[0][3].replace('print_var(', '').replace(')', '')
        pos = nom.find(',')
        if pos != -1:
            nom = nom[:pos]
        if isinstance(variable, list):
            textAlign("center", "center")
            text(nom, get_x(), get_y(), 40, 40)
            for i in range(len(variable)):
                if selected is not None and selected == i:
                    fill("grey")
                else:
                    fill("white")
                text(str(i), get_x() + 40 + i * 20, get_y(), 20, 20)
                text(str(variable[i]), get_x() + 40 + i * 20, get_y() + 20, 20, 20)
            if end is None or end == "-":
                set_x(5)
                set_y(get_y() + 45)
                processing.__print_ligne = [25]
                if end == "-":
                    line(get_x(), get_y(), width() - 5, get_y())
                    set_y(get_y() + 5)
            elif end == " " or end == "" or end == "-":
                set_x(get_x() + len(variable) * 20 + 42)
                processing.__print_ligne.append(45)
        else:
            textAlign("center", "center")
            fill("white")
            text(f"{nom} = {variable}", get_x(), get_y(), 0, 20)
            if end is None or end == "-":
                set_x(5)
                set_y(get_y() + max(processing.__print_ligne))
                processing.__print_ligne = [25]
                if end == "-":
                    line(get_x(), get_y(), width() - 5, get_y())
                    set_y(get_y() + 5)
            elif end == " " or end == "":
                set_x(get_x() + textWidth(f"{nom} = {variable}") + 4)
                processing.__print_ligne.append(25)


def printc(*args):
    processing.__print_console.append(args)


def draw_console():
    for ligne in processing.__print_console:
        texte = ""
        for m in ligne:
            texte += str(m) + " "
        text(texte, processing.__print_x, processing.__print_y, no_fill=True,no_stroke=True)
        processing.__print_y+=20
    processing.__print_y = 5
    processing.__print_x = 5
    processing.__print_console = []