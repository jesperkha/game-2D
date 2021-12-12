# Basic lighting

from pygame import Surface, SRCALPHA, transform
from math import sqrt

# Creates a circlular inverse shadow with specified radius
def create_circle(radius: int) -> Surface:
    width = radius * 2
    surf = Surface((width, width)).convert_alpha()
    for rx in range(width):
        for ry in range(width):
            dx = radius - rx
            dy = radius - ry
            dist = sqrt(dx*dx + dy*dy)
            opacity = 255 * dist / radius
            if opacity > 255: opacity = 255
            surf.set_at((rx, ry), (0, 0, 0, opacity))
    
    return surf


# Draws circle with center at pos
def draw_circle(dest: Surface, circle: Surface, pos: tuple) -> None:
    "Draws to dest. Does not work when directly drawn to window buffer."
    w = circle.get_width()
    h = circle.get_height()
    new_pos = (pos[0] - w/2, pos[1] - h/2)

    # Adjust for drawing Surface offscreen
    if new_pos[0] < 0: w += new_pos[0]
    if new_pos[1] < 0: h += new_pos[1]

    dest.fill((0, 0, 0))
    dest.fill((0, 0, 0, 0), (new_pos[0], new_pos[1], w, h))
    dest.blit(circle, new_pos)


# Class for methods with self referencing
class Circle:
    def __init__(self, window_size: tuple, radius: int) -> None:
        self.buffer = Surface((window_size[0], window_size[1]), SRCALPHA)
        self.radius = radius
        self.circle = create_circle(radius)

        # For pulsate
        self.psize = [self.circle.get_width(), self.circle.get_height()]
        self.dir   = 1
        self.svel  = 0
        self.speed = 0.1
        self.max_vel = 3

    
    # Draws to window through Circles buffer
    def draw(self, win: Surface, pos: tuple, circle: Surface = None) -> None:
        c = self.circle if not circle else circle
        draw_circle(self.buffer, c, pos)
        win.blit(self.buffer, (0, 0))

    
    # Draws circle as a pulsating ellipse with given speed
    def pulsate(self, win: Surface, pos: tuple) -> None:
        self.svel += self.speed * self.dir
        if abs(self.svel) > self.max_vel:
            self.svel = self.max_vel * self.dir

        self.psize[0] += self.svel
        self.psize[1] += self.svel

        if self.psize[0] / 2 > self.circle.get_width(): self.dir = -1
        if self.psize[0] / 2 < self.circle.get_width(): self.dir = 1
        size = (int(self.psize[0]), int(self.psize[1]))
        self.draw(win, pos, transform.smoothscale(self.circle, size))