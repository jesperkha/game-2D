# Version 1.0

from math import sqrt
from lib.vector import Vector

class Entity:
    def __init__(self, size):
        self.pos = Vector.ZERO()
        self.spd = Vector.ZERO()

        # Euler integration
        self.vel = Vector.ZERO()
        self.acc = Vector.ZERO()

        # Verlet integration
        self.points = [] # { x, y, ox, oy, pinned }
        self.lines  = [] # { p1, p2, dist }
        self.rects  = [] # { p1, p2, p3, p4 }

        self.density = 0
        self.layer   = 1
        self.mass    = 0

        self.sprite = None
        self.size   = Vector(size[0], size[1])
        self.width  = size[0]
        self.height = size[1]
    
    def rect(self) -> tuple:
        return (self.pos.x, self.pos.y, self.width, self.height)


# Updates all points to their new poisition given their old one and external forces
def update_points(points: list[dict], xsum_force: int = 0, ysum_force: int = 0) -> None:
    for p in points:
        if p.pinned: continue
        velx = p["x"] - p["ox"]
        vely = p["y"] - p["oy"]
        p["ox"] = p["x"]
        p["oy"] = p["y"]
        p["x"] += velx + xsum_force
        p["y"] += vely + ysum_force


# Constrains both points in line to be within given distance
def update_lines(lines: list[dict]) -> None:
    for l in lines:
        dx = l["p1"]["x"] - l["p2"]["x"]
        dy = l["p1"]["y"] - l["p2"]["y"]
        dist = sqrt(dx*dx + dy*dy)
        diff = l["dist"] - dist
        perc = diff / dist / 2
        offsetx = dx * perc
        offsety = dy * perc
        if not l["p1"]["pinned"]:
            l["p1"]["x"] += offsetx
            l["p1"]["y"] += offsety
        if not l["p2"]["pinned"]:
            l["p2"]["x"] -= offsetx
            l["p2"]["y"] -= offsety
