from likeprocessing.processing import *

def setup():
    createCanvas(200, 400)
    background("grey")
    textFont("helvetica",12)
    textCouleurCadre("blue")
    print(textWidth("bonjour les amis"))
    textAlign("left","bottom")
def draw():
    rect(10,10,20,20)
    text("bonjour les amis",10,50,180,50)

run(globals())