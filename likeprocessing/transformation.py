import likeprocessing.processing as processing
from likeprocessing.trigo import *


def translate(x: [int, None] = None, y: [int, None] = None)->[tuple, None]:
    """initialise les valeurs relatives du déplacement et renvoie la valeur précédente de celui-ci (tuple)"""
    st = processing.get_dx(),processing.get_dy()
    if x is not None:
        processing.set_dx(processing.get_dx() + x)
    if y is not None:
        processing.set_dy(processing.get_dy() + y)
    return st

def scale(echelle=1):
    """initilise la valeur du zoom 1 par defaut renvoie la valeur précédente de cette valeur"""
    sc = processing.get_scale()
    processing.set_scale(echelle)
    return sc

def init_translate(dx=0,dy=0):
    """set absolute translation dx,dy = 0,0"""
    processing.set_dx(dx)
    processing.set_dy(dy)


def get_translate() -> tuple:
    """return translation like tuple (x,y)"""
    return (processing.get_dx(), processing.get_dy())


def rotate(angle: float, axis=(0, 0)):
    """execute an absolute rotation on next drawing fonctions return a tuple of the previous value (angle, axis)"""
    rot = processing.get_rotation(),processing.get_axis()
    processing.set_rotation(angle)
    processing.set_axis(axis)
    return rot


def get_rotation() -> [int, float]:
    """retourne la valeur de l'angle de rotation dans l'unité choisie (voir angleMode)"""
    return processing.__rotation / processing.get_angle_mode()


def get_rotation_rad() -> [int, float]:
    """retourne la valeur de l'angle de rotation en radian"""
    return processing.__rotation


def rotation(points: list) -> list:
    """rotation calculation """
    pr = []
    if processing.get_rotation_rad() == 0:
        return points
    else:
        if processing.__scale == 1:
            a = complex(*processing.get_axis()) + complex(processing.__dx, processing.__dy)
        else:
            ax, ay = processing.get_axis()
            a = complex(ax * processing.__scale, ay * processing.__scale) + complex(processing.__dx, processing.__dy)
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
        pts.append([pt[0] + processing.get_dx(), pt[1] + processing.get_dy()])
    return pts


def multiplication(points: list, facteur: [int, float]) -> list:
    if facteur == 1:
        return points
    pts = []
    for pt in points:
        pts.append([pt[0] * facteur, pt[1] * facteur])
    return pts


def transformation(points: list) -> list:
    """excecute rotation and symmetry transformation
    on next drawing functions"""
    pts = multiplication(points, processing.__scale)
    pts = processing.translation(pts)
    pts = processing.rotation(pts)
    pts = processing.symetrie_y(pts)
    pts = processing.symetrie_x(pts)
    return pts

if __name__ == '__main__':
    st = translate(10,10)
    print(st, translate(*st))