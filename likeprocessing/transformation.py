import likeprocessing.processing as processing
from likeprocessing.trigo import *


def translate(x: int, y: int):
    processing.set_dx(processing.get_dx() + x)
    processing.set_dy(processing.get_dy() + y)


def init_translate():
    """set absolute translation dx,dy = 0,0"""
    processing.set_dx(0)
    processing.set_dy(0)


def get_translate() -> tuple:
    """return translation like tuple (x,y)"""
    return (processing.get_dx(), processing.get_dy())


def rotate(angle: float, axis=(0, 0)):
    """execute a rotation on next drawing fonctions"""
    processing.set_rotation(angle)
    processing.set_axis(axis)

def get_rotation() -> [int,float]:
    """retourne la valeur de l'angle de rotation dans l'unité choisie (voir angleMode)"""
    return processing.__rotation/processing.get_angle_mode()

def get_rotation_rad() -> [int,float]:
    """retourne la valeur de l'angle de rotation en radian"""
    return processing.__rotation

def rotation(points: list) -> list:
    """rotation calculation """
    pr = []
    if processing.get_rotation_rad() == 0:
        return points
    else:
        a = complex(*processing.get_axis()) + complex(processing.__dx, processing.__dy)
        angle = processing.get_rotation_rad()
        for pt in points:
            p = complex(*pt)
            p -= a
            r = complex(math.cos(angle), -math.sin(angle))
            p *= r
            p += a
            pr.append([p.real, p.imag])
        return pr


def flip_v(axe_v):
    """execute a vertical symmetry on next drawing functions with reference to axis x=axe_v"""
    processing.__flip_axe_v = axe_v


def flip_h(axe_h):
    """execute a horizontal symmetry on next drawing functions with reference to axis y=axe_h"""
    processing.__flip_axe_h = axe_h


def symetrie_y(points: list) -> list:
    """Calcul la symétrie verticale par rapport à l'axe processing.__flip_axe_y """
    if processing.__flip_axe_v is None:
        return points
    pts = []
    for pt in points:
        pts.append([2 * processing.__flip_axe_v - pt[0], pt[1]])
    return pts


def symetrie_x(points: list) -> list:
    """Calcul la symetrie horizontale par rapport à l'axe processing.__flip_axe_x """
    if processing.__flip_axe_h is None:
        return points
    pts = []
    for pt in points:
        pts.append([pt[0], 2 * processing.__flip_axe_h - pt[1]])
    return pts

def translation(points: list) -> list:
    """execute une translation sur une liste de points"""
    if processing.get_dx() == 0 and processing.get_dy() == 0:
        return points
    pts = []
    for pt in points:
        pts.append([pt[0]+processing.get_dx(),pt[1]+processing.get_dy()])
    return pts

def transformation(points: list) -> list:
    """excecute rotation and symmetry transformation
    on next drawing functions"""
    pts = processing.translation(points)
    pts = processing.rotation(pts)
    pts = processing.symetrie_y(pts)
    pts = processing.symetrie_x(pts)
    return pts
