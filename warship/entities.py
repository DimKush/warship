import uuid
from abc import ABC, abstractmethod
from math import sqrt
from typing import List

from starlette.websockets import WebSocket

from warship.config import AREA_WIDTH, AREA_HEIGHT


class Entity(ABC):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0

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
        new_x = self.x + (self.vx * t * self.speed)
        if 0 <= new_x <= AREA_WIDTH:
            self.x = new_x

        new_y = self.y + (self.vy * t * self.speed)
        if 0 <= new_y <= AREA_HEIGHT:
            self.y = new_y

    def collision(self, entity: Entity):
        d = sqrt((entity.x - self.x) ** 2 + (entity.y - self.y) ** 2)
        return d < 20

    def set_socket(self, sock: WebSocket):
        self.socket = sock

    def set_movement(self, data):
        player = self
        if data['up']:
            player.vy = -1
        elif data['down'] and not data['up']:
            player.vy = +1
        else:
            player.vy = 0

        if data['left']:
            player.vx = -1
        elif data['right'] and not data['left']:
            player.vx = +1
        else:
            player.vx = 0

    def get_info(self):
        return {'id': self.id, 'x': self.x, 'y': self.y}
