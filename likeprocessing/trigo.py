import math

__mode = 1


def get_mode()->float:
    """
    retourne un entier permettant la conversion d'un angle(degré, grade, et radian)  en radian\n
    :return: float\n
    """
    return __mode


def mode(mode_angle: str):
    """
    :rtype: None\n
    :param mode_angle : type d'unité d'angle à utiliser\n
    :type mode_angle : str\n
    'rad' les angles des fonctions trigo seront pris comme des radians (défaut)\n
    'deg' les angles des fonctions trigo seront pris comme des degrés\n
    'grd' les angles des fonctions trigo seront pris comme des gradians\n
    Une exception est levée en cas d'erreur de paramètre
     """
    global __mode

    if mode_angle == "deg":
        __mode = math.pi / 180
    elif mode_angle == "grd":
        __mode = math.pi / 200
    elif mode_angle == "rad":
        __mode = 1
    else:
        raise ValueError


def cos(angle: float) -> float:
    """
    retourne le cosinus de angle en fonction du mode choisi (defaut : radian)
    :param angle:float
    :return: float
    """
    return math.cos(angle * get_mode())


def acos(value: float) -> float:
    return math.acos(value) / get_mode()


def sin(angle: float) -> float:
    return math.sin(angle * get_mode())


def asin(value: float) -> float:
    return math.asin(value) / get_mode()


def tan(angle: float) -> float:
    return math.tan(angle * get_mode())


def atan(value: float) -> float:
    return math.atan(value) / get_mode()


def atan2(y: float, x: float) -> float:
    return math.atan2(y, x) / get_mode()


if __name__ == '__main__':
    mode('deg')
    print(cos(180))
    print(asin(sin(180)))
    print(atan(-math.sqrt(3) / 2 / 0.5))
    print(atan2(-math.sqrt(3) / 2, -0.5))
