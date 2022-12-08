from likeprocessing.processing import *
set_debug(True)
time = 0
s = 0
m = 0
h = 0
t = Tempo(10)


def essai(name):
    print(f"ok {name}")


def essai1():
    print("ok")


def trian(name):
    print(f"salut {name}")


def setup():
    createCanvas(400, 400,)
    background("grey")
    angleMode("deg")
    ellipseMode("center")
    strokeWeight(2)


def compute():
    pass


def draw():
    global time, s, m, h
    stroke("black")
    circle(100, 100, 100, fill_mouse_on="grey", command=essai1)
    axe = (100, 100)
    if t.fin():
        s += 1
    text(f"{int(h):02}:{int(m):02}:{s:02}", 10, 20, 100, 20, allign_h="center")
    rotate(-s * 6, axe)
    stroke("red")
    line(100, 100, 100, 50)
    rotate(-s / 10, axe)
    stroke("black")
    line(100, 100, 100, 60)
    rotate(-s / 120, axe)
    stroke("blue")
    line(100, 100, 100, 80)
    rotate(-30, (0, 0))
    fill("white")
    circle_arc(200, 200, 50, 0, 270, pie=False, command=essai)
    line(250, 250, 400, 250, fill_mouse_on="red", command=essai, name="ligne")
    rotate(0)
    triangle(250, 250, 300, 350, 250, 350, fill_mouse_on="red", command=trian, name="essai triangle")
    text("salut les amis", 20, 30, 350,20, allign_h="center", font="arial", font_size=48, font_color="green",pady=30)
    if mouse_click():
        print("true")
        dist()

run(globals())
