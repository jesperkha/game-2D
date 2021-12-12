# Version 1.1
# Standard 2D vector

from math import sqrt

# Simple vector class
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other: object) -> bool:
        return self.x != other.x or self.y != other.y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mult__(self, other):
        return Vector(self.x * other.x, self.y * other.y)

    def __div__(self, other):
        return Vector(self.x / other.x, self.y / other.y)
    
    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def add(self, other):
        self.x += other.x
        self.y += other.y

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y

    def mult(self, other):
        self.x *= other.x
        self.y *= other.y

    def div(self, other):
        self.x /= other.x
        self.y /= other.y

    def normalize(self):
        hyp = sqrt(self.x**2 + self.y**2)
        if hyp != 0:
            self.x /= hyp
            self.y /= hyp

    def zero(self):
        self.x = 0
        self.y = 0

    def get_mag(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    def tup(self):
        return (self.x, self.y)

    def set_as(self, x, y):
        self.x = x
        self.y = y

    def tset_as(self, tup):
        self.x = tup[0]
        self.y = tup[1]

    def copy(self):
        return Vector(self.x, self.y)

    @staticmethod
    def ZERO():
        return Vector(0, 0)
    
    @staticmethod
    def Normalize(vec) -> object:
        new_vec = vec.copy()
        hyp = sqrt(new_vec.x**2 + new_vec.y**2)
        if hyp != 0:
            new_vec.x /= hyp
            new_vec.y /= hyp
        
        return new_vec

    @staticmethod
    def dist(a, b) -> float:
        dx = a.x - b.x
        dy = a.y - b.y
        return sqrt(dx*dx + dy*dy)
