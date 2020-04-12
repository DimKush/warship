import uuid
from abc import ABC, abstractmethod
from math import sqrt
from typing import List
from math import cos, sin, pi
from back.config import AREA_WIDTH, AREA_HEIGHT


class Entity(ABC):
    def __init__(self):
        self.position = {'x': 0, 'y': 0}
        self.bounds = []

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
        self.bounds = [(-10, 0), (0, 40), (10, 0)]
        self.angle = {'current': 0, 'delta': 0}
        self.speed = {'current': 70, 'delta': 0}

    def set_delta(self, angle, speed):
        self.angle['delta'] = angle
        self.speed['delta'] = speed

    def next(self, t: float):
        self.angle['current'] += self.angle['delta']
        x_delta = self.speed['delta'] * t * self.speed['current'] * sin(self.angle['current'] * pi / 90)
        y_delta = self.speed['delta'] * t * self.speed['current'] * cos(self.angle['current'] * pi / 90)

        self.position['x'] -= x_delta
        self.position['y'] += y_delta

        self.new_bounds = []
        for point in self.bounds:
            x = self.position['x'] + \
                (point[0] - self.position['x']) * cos(self.angle['current'] * pi / 180) - \
                (point[1] - self.position['y']) * sin(self.angle['current'] * pi / 180)
            y = self.position['y'] + \
                (point[1] - self.position['y']) * cos(self.angle['current'] * pi / 180) + \
                (point[0] - self.position['x']) * sin(self.angle['current'] * pi / 180)
            self.new_bounds.append((x, y))

        self.position['x'] = self.position['x'] % AREA_WIDTH
        self.position['y'] = self.position['y'] % AREA_HEIGHT

    def collision(self, entity: Entity):
        return False

    def get_info(self):
        return {'id': self.id,
                'x': self.position['x'],
                'y': self.position['y'],
                'r': self.angle['current'],
                'bounds': self.new_bounds
                }
