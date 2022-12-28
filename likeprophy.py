from likeprocessing.processing import *
import pymunk
import pymunk.pygame_util
class SpacePro(pymunk.Space):
    def __init__(self):
        super().__init__()
        self.objets=[]

    def add_obj(self,obj):
        super().add(obj.body,obj.shape)
        self.objets.append(obj)
        return len(self.objets)-1

    def draw(self):
        i = 0
        while i < len(self.objets):
            if self.objets[i].body.position.y < height():
                self.objets[i].draw()
                i += 1
            else:
                del self.objets[i]

    def step(self, pas):
        super().step(pas)

class Circle:
    def __init__(self, space, x, y, r,type=None,**kwargs):
        mass = kwargs.get("mass",1)
        density = kwargs.get("density", 1)
        self.fill = kwargs.get("fill", "white")
        if type is None:
            self.body = pymunk.Body(pymunk.moment_for_circle(mass, 0, r, (0, 0)))
        else:
            self.body = pymunk.Body(body_type=type)
          # 1
        self.body.position = x, y  # 2
        self.shape = pymunk.Circle(self.body, r)  # 3
        self.shape.mass = mass  # 4
        self.shape.friction = kwargs.get("friction",0.2)
        self.shape.elasticity = kwargs.get("elasticity",0.6)
        self.shape.collision_type = 6
        self.shape.density = density

    def draw(self):
        if get_ellipse_center_mode():
            circle(*self.body.position, self.shape.radius * 2,fill=self.fill)
        else:
            circle(self.body.position.x-self.shape.radius,self.body.position.y-self.shape.radius, self.shape.radius * 2, fill=self.fill)

class Ball(Circle):
    def __init__(self, space, x, y, r,**kwargs):
        super().__init__(space, x, y, r,**kwargs)

class StaticCircle(Circle):
    def __init__(self, space, x, y, r,**kwargs):
        super().__init__(space, x, y, r,pymunk.Body.STATIC,**kwargs)

class KinematicCircle(Circle):
    def __init__(self, space, x, y, r,**kwargs):
        super().__init__(space, x, y, r,pymunk.Body.KINEMATIC,**kwargs)

class Rect:
    def __init__(self, space, x, y, largeur, hauteur,type=None,**kwargs):
        mass = kwargs.get("mass",1)
        density = kwargs.get("density", 1)
        self.fill=kwargs.get("fill","white")
        angle=kwargs.get("angle",processing.get_rotation_rad())
        self.rectMode = kwargs.get("rectMode", processing.get_rect_center_mode())
        self.width = largeur
        self.height = hauteur
        self.points = [(-self.width/2,-self.height/2),(self.width/2,-self.height/2),(self.width/2,self.height/2),(-self.width/2,self.height/2)]
        self.points = processing.rotation(self.points,angle=angle,axis=self.points[0])
        moment = pymunk.moment_for_poly(mass, self.points, (0, 0))
        if type is None:
            self.body = pymunk.Body(mass, moment)
        else:
            self.body = pymunk.Body(body_type=type)  # 1
        if self.rectMode:
            self.body.position = x,y
        else:
            self.body.position = x+self.width/2, y+self.height/2  # 2
        self.shape = pymunk.Poly(self.body, self.points)
        translate(*self.body.position)
        self.points=translation(self.points)
        init_translate()
        self.shape.friction = kwargs.get("friction",1)
        self.shape.elasticity = kwargs.get("elasticity",0.95)
        self.shape.density = density

    @property
    def position(self):
        if not self.rectMode:
            return self.body.position[0]-self.width/2, self.body.position[1]-self.height/2
        return  self.body.position

    @position.setter
    def position(self,pos:tuple,center=False):
        if not self.rectMode:
            self.body.position = pos[0]+self.width/2, pos[1]+self.height/2
        else:
            self.body.position = pos[0], pos[1]
        self.points = [(-self.width / 2, -self.height / 2), (self.width / 2, -self.height / 2),
                       (self.width / 2, self.height / 2), (-self.width / 2, self.height / 2)]
        translate(*self.body.position)
        self.points=translation(self.points)
        init_translate()

    def draw(self):
        if isinstance(self,DynamicRect):
            self.points = [v.rotated(self.body.angle) + self.body.position for v in self.shape.get_vertices()]
        polygone(self.points,fill=self.fill)

class StaticRect(Rect):
    def __init__(self, space, x, y, largeur, hauteur,**kwargs):
        super().__init__(space, x, y, largeur, hauteur,pymunk.Body.STATIC,**kwargs)

class KinematicRect(Rect):
    def __init__(self, space, x, y, largeur, hauteur,**kwargs):
        super().__init__(space, x, y, largeur, hauteur, pymunk.Body.KINEMATIC,**kwargs)

class DynamicRect(Rect):
    def __init__(self, space, x, y, largeur, hauteur,**kwargs):
        super().__init__(space, x, y, largeur, hauteur,**kwargs)
