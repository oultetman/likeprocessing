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
        a = complex(*get_axis()) + complex(processing.__dx,processing.__dy)
        angle = get_rotation()
        for pt in points:
            p = complex(*pt)
            p -= a
            r = complex(math.cos(angle), -math.sin(angle))
            p *= r
            p += a
            pr.append([p.real, p.imag])
        return pr