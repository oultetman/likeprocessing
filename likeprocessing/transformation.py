import likeprocessing.processing as processing
from likeprocessing.trigo import *


def translate(x: int, y: int):
    processing.__dx += x
    processing.__dy += y


def get_axis():
    return processing.__axis


def get_rotation():
    return processing.__rotation


def rotate(angle: float, axis=(0, 0)):
    processing.__rotation = angle * angleMode()
    processing.__axis = axis


def rotation(points: list) -> list:
    pr = []
    if get_rotation() == 0:
        return points
    else:
        a = complex(*get_axis()) + complex(processing.__dx, processing.__dy)
        angle = get_rotation()
        for pt in points:
            p = complex(*pt)
            p -= a
            r = complex(math.cos(angle), -math.sin(angle))
            p *= r
            p += a
            pr.append([p.real, p.imag])
        return pr


def flip_v(axe_v):
    """entraîne une symétrie verticale par rapport à l'axe axe_y"""
    processing.__flip_axe_v = axe_v


def flip_h(axe_h):
    """entraîne une symétrie horizontale par rapport à l'axe axe_x"""
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


def transformation(points: list) -> list:
    pts = processing.rotation(points)
    pts = processing.symetrie_y(pts)
    pts = processing.symetrie_x(pts)
    return pts
