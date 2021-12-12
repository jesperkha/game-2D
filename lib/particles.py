# Particle effects

from pygame import Surface, draw
from math import sqrt
from random import randrange, random

from lib.vector import Vector
from lib.font import Font

pool = []

def update(win, dt) -> None:
    for p in pool: p.update(win)


def randvel(px: bool = False, py: bool = False) -> tuple:
    x = random() - 0.5
    y = random() - 0.5
    if px: x = -random() * 0.5
    if py: y = -random() * 0.5
    mag = sqrt(x*x + y*y)
    x /= mag
    y /= mag
    return [x, y]


class Explosion:
    def __init__(self, x, y, grv: int = 0, lifetime: int = 100, amount: int = 20, speed: int = 1, col: tuple = (255, 255, 255)) -> None:
        self.grv = grv
        self.spd = speed
        self.col = col

        self.particles = []
        for _ in range(amount):
            p = [x, y, randvel(), randrange(lifetime//2, lifetime)]
            self.particles.append(p)
        
        pool.append(self)
    
    def update(self, win) -> None:
        for p in self.particles:
            p[2][1] += self.grv
            p[0] += p[2][0] * self.spd
            p[1] += p[2][1] * self.spd
            p[3] -= 1
            if p[3] <= 0:
                self.particles.remove(p)

            draw.rect(win, self.col, (p[0], p[1], 1, 1))
        
        if len(self.particles) == 0:
            pool.remove(self)


class WordBounce:
    font = Font("./assets/font_sheet.png")
    buffer = Surface((100, 100))

    def __init__(self, pos: tuple, word: str, grv: int = 0, lifetime: int = 60) -> None:
        if not WordBounce.font.loaded:
            print("Forgot WordBounce.font.load()")
            quit()

        self.pos = Vector(pos[0], pos[1])
        self.vel = randvel(py=True)
        self.grv = grv
        self.word = word
        self.word_length = self.font.render(self.buffer, (0, 0), self.word)[2]
        self.lifetime = lifetime
        pool.append(self)
    
    def update(self, win) -> None:
        self.vel[1] += self.grv
        self.pos.x  += self.vel[0]
        self.pos.y  += self.vel[1]
        self.lifetime -= 1
        if self.lifetime <= 0:
            pool.remove(self)

        x = self.pos.x - self.word_length/2
        self.font.render(win, (x, self.pos.y), self.word)