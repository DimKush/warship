import uuid
from abc import ABC, abstractmethod
from math import sqrt
from typing import List
from math import cos, sin, pi
from back.config import AREA_WIDTH, AREA_HEIGHT


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Entity(ABC):
    def __init__(self):
        self.pos = Point(100, 200)
        self.bounds = []

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @abstractmethod
    def next(self, time):
        pass

    @abstractmethod
    def collision(self, entities: List):
        pass


class Player(Entity):
    def __init__(self, ):
        super().__init__()

        self.id = str(uuid.uuid1())
        self.bounds = [(-15 + self.x, 0 + self.y),
                       (-15 + self.x, 80 + self.y),
                       (0 + self.x, 100 + self.y),
                       (15 + self.x, 80 + self.y),
                       (15 + self.x, 0 + self.y)]
        self.angle = {'current': 0, 'delta': 0}
        self.speed = {'current': 90, 'delta': 0}

    def set_delta(self, angle, speed):
        self.angle['delta'] = angle
        self.speed['delta'] = speed

    def next(self, t: float):
        self.angle['current'] += self.angle['delta']
        x_delta = self.speed['delta'] * t * self.speed['current'] * sin(self.angle['current'] * pi / 180)
        y_delta = self.speed['delta'] * t * self.speed['current'] * cos(self.angle['current'] * pi / 180)

        new_bounds = []
        for point in self.bounds:
            x = self.pos.x + (point[0] - self.pos.x) * cos(self.angle['delta'] * pi / 180) - (point[1] - self.pos.y) * sin(self.angle['delta'] * pi / 180) - x_delta
            y = self.pos.y + (point[1] - self.pos.y) * cos(self.angle['delta'] * pi / 180) + (point[0] - self.pos.x) * sin(self.angle['delta'] * pi / 180) + y_delta

            new_bounds.append((x, y))
        self.bounds = new_bounds

        self.pos.x -= x_delta
        self.pos.y += y_delta

        self.pos.x = self.pos.x % AREA_WIDTH
        self.pos.y = self.pos.y % AREA_HEIGHT

    def collision(self, entity: Entity):
        return False

    def get_info(self):
        return {'id': self.id,
                'x': self.pos.x,
                'y': self.pos.y,
                'r': self.angle['current'],
                'bounds': self.bounds
                }
