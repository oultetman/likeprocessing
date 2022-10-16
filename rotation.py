import cmath
import math

pc=(50,-50)
p=(100,-100)
r=(1,math.pi)
def complexe_ro_teta(ro,teta):
    return complex(ro*math.cos(teta),ro*math.sin(teta))

def rotate(point:tuple,angle:float,axis:tuple):
    p = complex(*point)
    a = complex(*axis)
    print(a)
    p -=a
    print(p)
    r = complex(math.cos(angle), math.sin(angle))
    p*=r
    p+=a
    return p.real, p.imag

print(rotate(p,math.pi,pc))