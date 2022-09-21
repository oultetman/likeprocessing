import math
import likeprocessing.processing as processing

__angle_mode_str:str= "rad"

def angleMode(mode_angle: str = "") -> str:
    """
    :rtype: None\n
    :param mode_angle : type d'unité d'angle à utiliser\n
    :type mode_angle : str\n
    'rad' les angles des fonctions trigonométriques seront pris comme des radians (défaut)\n
    'deg' les angles des fonctions trigonométriques seront pris comme des degrés\n
    'grd' les angles des fonctions trigonométriques seront pris comme des grades\n
    Une exception est levée en cas d'erreur de paramètre

    si mode_angle == "" la valeur de mode est retournée (str)
     """
    global __angle_mode_str
    if mode_angle == "":
        return __angle_mode_str
    if mode_angle.lower() == "deg":
        processing.set_angle_mode(math.pi / 180)
        __angle_mode_str = "deg"
    elif mode_angle.lower() == "grd":
        processing.set_angle_mode(math.pi / 200)
        __angle_mode_str = "grd"
    elif mode_angle.lower() == "rad":
        processing.set_angle_mode(1)
        __angle_mode_str = "rad"
    else:
        raise ValueError


def cos(angle: float) -> float:
    """
    retourne le cosinus de angle en fonction du mode choisi (defaut : radian)
    :param angle:float
    :return: float
    """
    return math.cos(angle * processing.get_angle_mode())


def acos(value: float) -> float:
    """
    Return the arc cosine of value in mode chose.
    The result is between 0 and pi rd  if mode("rad").
    The result is between 0 and 180° if mode("deg").
    The result is between 0 and 200 grd if mode("grd").
    """
    return math.acos(value) / processing.get_angle_mode()


def sin(angle: float) -> float:
    """ Return the sine of angle.
    angle must be in radian rd  if mode("rad").
    angle must be in degree if mode("deg").
    angle must be in gradian if mode("grd").
    """
    return math.sin(angle * processing.get_angle_mode())


def asin(value: float) -> float:
    """
    Return the arc sine of x value.
    The result is between -pi/2 and pi/2. rd  if mode("rad").
    The result is between -90° and 90° if mode("deg").
    The result is between -100 and 100 grd if mode("grd").
    """
    return math.asin(value) / processing.get_angle_mode()


def tan(angle: float) -> float:
    """ Return the tangent of angle.
    angle must be in radian rd  if mode("rad").
    angle must be in degree if mode("deg").
    angle must be in gradian if mode("grd").
    """
    return math.tan(angle * processing.get_angle_mode())


def atan(value: float) -> float:
    """
    Return the arc tangent of value.
    The result is between -pi/2 and pi/2. rd  if mode("rad").
    The result is between -90° and 90° if mode("deg").
    The result is between -100 and 100 grd if mode("grd").
    """
    return math.atan(value) / processing.get_angle_mode()


def atan2(y: float, x: float) -> float:
    """
    Return the arc tangent (measured in radians) of y/x.
    The result is between -pi and pi. rd  if mode("rad").
    The result is between -180° and 180° if mode("deg").
    The result is between -200 and 200 grd if mode("grd").
    Unlike atan(y/x), the signs of both x and y are considered.
    """
    return math.atan2(y, x) / processing.get_angle_mode()

def radians(angle:float)->float:
    return angle * processing.get_angle_mode()

def degrees(angle:float)->float:
    return angle * processing.get_angle_mode() * 180 / math.pi

def grades(angle:float)->float:
    return angle * processing.get_angle_mode() * 200 / math.pi

if __name__ == '__main__':
    angleMode('deg')
    print(cos(180))
    print(asin(sin(180)))
    print(atan(-math.sqrt(3) / 2 / 0.5))
    print(atan2(-math.sqrt(3) / 2, -0.5))
    print(grades(180))
    print(radians(180))
    print(angleMode())