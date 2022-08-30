from likeprocessing.processing import *
time = 0
s = 0
m = 0
h=0

t=Tempo(10)
def setup():
    createCanvas(400, 400)
    background("grey")
    angleMode("deg")



def draw():
    global time,s,m,h
    axe = (100,100)
    text(f"{int(h):02}:{int(m):02}:{s:02}",10,20,100,20)
    rotate(-s*6,axe)
    stroke("red")
    line(100,100,100,50)
    if t.fin():
        time+=1
        h=time/3600
        m=(time/60)%60
        s=time%60
    rotate(-m*6,axe)
    stroke("black")
    line(100,100,100,60)
    rotate(-h*30,axe)
    stroke("blue")
    line(100,100,100,80)


run(globals())
