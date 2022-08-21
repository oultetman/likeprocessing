from likeprocessing.processing import *
t = Tempo(50)
t1 = Tempo(500)
o = 10
ferme = True
def setup():
    createCanvas(200, 400)
    background("grey")
    textFont("helvetica",12)
    textCouleurCadre("blue")
    print(textWidth("bonjour les amis"))
    textAlign("left","bottom")
    a = pygame.pixelarray.PixelArray(loadImage("fantome_jaune.png"))
    print(len(a))

    noStroke()

def draw():
    global o,ferme
    rect(10,10,100,50 ,allign_h="center",allign_v="top",image=loadImage("fantome_jaune.png"))
    fill("yellow")
    if t.fin():
        if t1.is_on() :
            o-=4
        else:
            o+=4
    arc1(100,200,100,o,-o)

    fill("white")
    circle(100,150,30)
    fill("black")
    circle(105,150,10)


run(globals())