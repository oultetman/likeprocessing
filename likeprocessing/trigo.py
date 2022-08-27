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
    """
    Return the arc cosine of value in mode chose.
    The result is between 0 and pi rd  if mode("rad").
    The result is between 0 and 180° if mode("deg").
    The result is between 0 and 200 grd if mode("grd").
    """
    return math.acos(value) / get_mode()


def sin(angle: float) -> float:
    """ Return the sine of angle.
    angle must be in radian rd  if mode("rad").
    angle must be in degree if mode("deg").
    angle must be in gradian if mode("grd").
    """
    return math.sin(angle * get_mode())


def asin(value: float) -> float:
    """
    Return the arc sine of x value.
    The result is between -pi/2 and pi/2. rd  if mode("rad").
    The result is between -90° and 90° if mode("deg").
    The result is between -100 and 100 grd if mode("grd").
    """
    return math.asin(value) / get_mode()


def tan(angle: float) -> float:
    """ Return the tangent of angle.
    angle must be in radian rd  if mode("rad").
    angle must be in degree if mode("deg").
    angle must be in gradian if mode("grd").
    """
    return math.tan(angle * get_mode())


def atan(value: float) -> float:
    """
    Return the arc tangent of value.
    The result is between -pi/2 and pi/2. rd  if mode("rad").
    The result is between -90° and 90° if mode("deg").
    The result is between -100 and 100 grd if mode("grd").
    """
    return math.atan(value) / get_mode()


def atan2(y: float, x: float) -> float:
    """
    Return the arc tangent (measured in radians) of y/x.
    The result is between -pi and pi. rd  if mode("rad").
    The result is between -180° and 180° if mode("deg").
    The result is between -200 and 200 grd if mode("grd").
    Unlike atan(y/x), the signs of both x and y are considered.
    """
    return math.atan2(y, x) / get_mode()


if __name__ == '__main__':
    mode('deg')
    print(cos(180))
    print(asin(sin(180)))
    print(atan(-math.sqrt(3) / 2 / 0.5))
    print(atan2(-math.sqrt(3) / 2, -0.5))
