from math import cos, sin, atan2, degrees
from abc import ABC, abstractmethod

WIDTH = 800
HEIGHT = 600
g = 9.81
TIME_STEP = 0.0075
SPEED = 0.75
ROTATION_SPEED = 0.0075
ADD_POWER_SPEED = 1.0075
MAX_POWER = 15
TIME_BETWEEN_SHOTS = 0.8

def angle_from_vector(vector: complex):
    x, y = vector.real, vector.imag
    angle_rad = atan2(-y, x)
    angle_deg = degrees(angle_rad)
    return angle_deg

def sign(x):
    return (x > 0) - (x < 0)

def dot(v1: complex, v2: complex) -> float:
    return v1.real * v2.real + v1.imag * v2.imag

def normalize(v: complex) -> complex:
    if abs(v) == 0:
        return complex(0, 0)
    return v / abs(v)

class Object(ABC):
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.is_active = True

    @abstractmethod
    def update(self):
        pass

class Collision(Object):
    def __init__(self, position, half_size):
        self.overlap = False
        self.objects_that_overlap = []
        super().__init__(position, half_size)

    def update(self):
        self.objects_that_overlap.clear()

        self.overlap = False

    def check_hit(self, another):
        delta_pos = self.position - another.collision.position

        if (abs(delta_pos.real) <= self.size.real + another.collision.size.real and
                abs(delta_pos.imag) <= self.size.imag + another.collision.size.imag):
            self.overlap = True
            self.objects_that_overlap.append(another)

