import uuid
from abc import ABC, abstractmethod
from math import sqrt
from typing import List
from math import cos, sin, pi
from back.config import AREA_WIDTH, AREA_HEIGHT


class Entity(ABC):
    def __init__(self):
        self.x = 200
        self.y = 200
        self.angle = 0
        self.rotation = 0
        self.ahead = 0
        self.speed = 70

    @abstractmethod
    def next(self, t: int):
        pass

    @abstractmethod
    def collision(self, entities: List):
        pass


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.id = str(uuid.uuid1())
        self.socket = None

    def next(self, t: float):
        self.angle += self.rotation
        self.x -= self.ahead * t * self.speed * sin(self.angle * pi / 180)
        self.y += self.ahead * t * self.speed * cos(self.angle * pi / 180)

        self.x = self.x % AREA_WIDTH
        self.y = self.y % AREA_HEIGHT

    def collision(self, entity: Entity):
        d = sqrt((entity.x - self.x) ** 2 + (entity.y - self.y) ** 2)
        return d < 20


    def get_info(self):
        return {'id': self.id, 'x': self.x, 'y': self.y, 'r': self.angle}
