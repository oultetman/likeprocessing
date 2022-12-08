from likeprocessing.processing import *

x = 0


def locomotive(x: int, y: int, couleur: str):
    fill(couleur)
    polygone([(x + 20, y + 10), (x + 30, y + 10), (x + 40, y + 20), (x + 40, y + 30), (x + 30, y + 40),
              (x + 30, y + 60), (x + 100, y + 60), (x + 100, y), (x + 160, y), (x + 160, y + 100),
              (x, y + 100), (x, y + 60), (x + 20, y + 60), (x + 20, y + 40), (x + 10, y + 30), (x + 10, y + 20), ])
    fill("white")
    rect(x + 110, y + 10, 40, 60)
    fill("brown")
    circle(x + 10, y + 100, 40)
    circle(x + 110, y + 100, 40)
    personnage(x + 100, y+10, 1)

def wagon(x: int, y: int, couleur: str, numero: str):
    fill(couleur)
    rect(x, y, 160, 100)
    fill("white")
    for i in range(x + 10, x + 150, 50):
        rect(i, y + 10, 40, 50)
    fill("brown")
    circle(x + 10, y + 100, 40)
    circle(x + 110, y + 100, 40)
    fill("white")
    text(numero, x + 75, y + 70)


def personnage(x_wagon: int, y_wagon: int, nombre: int):
    for i in range(nombre):
        fill("pink")
        circle(x_wagon + 15 + i * 50, y_wagon + 20, 30)
        fill("white")
        circle(x_wagon + 19 + i * 50, y_wagon + 25, 10)
        circle(x_wagon + 31 + i * 50, y_wagon + 25, 10)
        fill("red")
        ellipse(x_wagon + 20 + 50 * i, y_wagon + 37, 20, 10)


def setup():
    createCanvas(541, 400)
    background("grey")
    title("train")


def compute():
    global x
    x -= 1
    if x < -550:
        x = 550


def draw():
    translate(x, 0)
    locomotive(10, 30, "black")
    for i in range(3):
        if i % 2 == 0:
            wagon(190 + i * 180, 30, "blue", str(i))
        else:
            wagon(190 + i * 180, 30, "red", str(i))
        personnage(190 + i * 180, 30, i + 1)


run(globals())
