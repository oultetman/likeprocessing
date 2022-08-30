import math

__mode = 1


def angleMode(mode_angle: str = "") -> float:
    """
    :rtype: None\n
    :param mode_angle : type d'unité d'angle à utiliser\n
    :type mode_angle : str\n
    'rad' les angles des fonctions trigonométriques seront pris comme des radians (défaut)\n
    'deg' les angles des fonctions trigonométriques seront pris comme des degrés\n
    'grd' les angles des fonctions trigonométriques seront pris comme des grades\n
    Une exception est levée en cas d'erreur de paramètre

    si mode_angle == "" la valeur de mode est retourné
     """
    global __mode
    if mode_angle == "":
        return __mode
    if mode_angle.lower() == "deg":
        __mode = math.pi / 180
    elif mode_angle.lower() == "grd":
        __mode = math.pi / 200
    elif mode_angle.lower() == "rad":
        __mode = 1
    else:
        raise ValueError


def cos(angle: float) -> float:
    """
    retourne le cosinus de angle en fonction du mode choisi (defaut : radian)
    :param angle:float
    :return: float
    """
    return math.cos(angle * angleMode())


def acos(value: float) -> float:
    """
    Return the arc cosine of value in mode chose.
    The result is between 0 and pi rd  if mode("rad").
    The result is between 0 and 180° if mode("deg").
    The result is between 0 and 200 grd if mode("grd").
    """
    return math.acos(value) / angleMode()


def sin(angle: float) -> float:
    """ Return the sine of angle.
    angle must be in radian rd  if mode("rad").
    angle must be in degree if mode("deg").
    angle must be in gradian if mode("grd").
    """
    return math.sin(angle * angleMode())


def asin(value: float) -> float:
    """
    Return the arc sine of x value.
    The result is between -pi/2 and pi/2. rd  if mode("rad").
    The result is between -90° and 90° if mode("deg").
    The result is between -100 and 100 grd if mode("grd").
    """
    return math.asin(value) / angleMode()


def tan(angle: float) -> float:
    """ Return the tangent of angle.
    angle must be in radian rd  if mode("rad").
    angle must be in degree if mode("deg").
    angle must be in gradian if mode("grd").
    """
    return math.tan(angle * angleMode())


def atan(value: float) -> float:
    """
    Return the arc tangent of value.
    The result is between -pi/2 and pi/2. rd  if mode("rad").
    The result is between -90° and 90° if mode("deg").
    The result is between -100 and 100 grd if mode("grd").
    """
    return math.atan(value) / angleMode()


def atan2(y: float, x: float) -> float:
    """
    Return the arc tangent (measured in radians) of y/x.
    The result is between -pi and pi. rd  if mode("rad").
    The result is between -180° and 180° if mode("deg").
    The result is between -200 and 200 grd if mode("grd").
    Unlike atan(y/x), the signs of both x and y are considered.
    """
    return math.atan2(y, x) / angleMode()

def radians(angle:float)->float:
    return angle * angleMode()

def degrees(angle:float)->float:
    return angle * angleMode() * 180 / math.pi

def grades(angle:float)->float:
    return angle * angleMode() * 200 / math.pi

if __name__ == '__main__':
    angleMode('deg')
    print(cos(180))
    print(asin(sin(180)))
    print(atan(-math.sqrt(3) / 2 / 0.5))
    print(atan2(-math.sqrt(3) / 2, -0.5))
    print(gradians(180))
    print(radians(180))