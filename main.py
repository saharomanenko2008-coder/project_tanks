from tkinter import PhotoImage
import tkinter as tk
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


class GameObject(Object):
    def __init__(self, position, direction, size, color="gray"):
        self.color = color
        self.direction = direction
        self.collision = Collision(position, size)
        super().__init__(position, size)

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, canvas):
        pass



class Rectangle(GameObject):
    def __init__(self, position, size, color="gray"):
        super().__init__(position, 0, size, color)

    def update(self):
        self.collision.update()

    def draw(self, canvas):
        x0 = self.position.real - self.size.real
        y0 = HEIGHT - self.position.imag - self.size.imag
        x1 = self.position.real + self.size.real
        y1 = HEIGHT - self.position.imag + self.size.imag

        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color)

class Circle(GameObject):
    def __init__(self, position, size, color="gray"):
        super().__init__(position, 0, size, color)

    def update(self):
        self.collision.update()

    def draw(self, canvas):
        x0 = self.position.real - self.size.real
        y0 = HEIGHT - self.position.imag - self.size.imag
        x1 = self.position.real + self.size.real
        y1 = HEIGHT - self.position.imag + self.size.imag

        canvas.create_oval(x0, y0, x1, y1, fill=self.color)


class Projectile(GameObject):
    def __init__(self, position, direction, radius=5, color="gray"):
        self.time_elapsed = 0

        super().__init__(position, direction, complex(radius, radius), color)

    def update(self, **kwargs):
        dx = self.direction.real * self.time_elapsed
        dy = self.direction.imag * self.time_elapsed - (g * self.time_elapsed ** 2) / 2

        self.position += complex(dx, dy)
        self.time_elapsed += TIME_STEP
        self.collision.position = self.position

        for another in self.collision.objects_that_overlap:
            if isinstance(another, Rectangle) or isinstance(another, Projectile):
                self.is_active = False

        self.collision.update()

    def draw(self, canvas):
        x0 = self.position.real - self.size.real
        y0 = HEIGHT - self.position.imag - self.size.imag
        x1 = self.position.real + self.size.real
        y1 = HEIGHT - self.position.imag + self.size.imag

        canvas.create_oval(x0, y0, x1, y1, fill=self.color)
