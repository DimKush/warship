import uuid
from abc import ABC, abstractmethod
from math import cos, sin, pi
from typing import List

from back.point import Point, Movement, AngleMovement
from back.config import AREA_WIDTH, AREA_HEIGHT
from back.ships import MainShip


class Entity(ABC):
    def __init__(self):
        self.axis = Point(100, 200)
        self.bounds = []
        self.z_index = 1
        self.tangible = True
        self.angle_motion = AngleMovement(curr_value=10, delta=1.3, max_value=40)
        self.vector_motion = Movement(curr_value=10, delta=20, max_value=40)

    @property
    def x(self):
        return self.axis.x

    @property
    def y(self):
        return self.axis.y

    @abstractmethod
    def next(self, time):
        pass

    @abstractmethod
    def collision(self, entities: List):
        pass

    def set_moving(self, angle_moving, speed_moving):
        self.angle_motion.moving = angle_moving
        self.vector_motion.moving = speed_moving


class Player(Entity):
    def __init__(self, ):
        super().__init__()

        self.id = str(uuid.uuid1())
        self.ship_model = MainShip()
        self.bounds = ((self.x + p.x, self.y + p.y) for p in self.ship_model.bounds)

    def next(self, t: float):
        self.angle_motion.set_next(t)
        self.vector_motion.set_next(t)

        x_delta = self.vector_motion.current * sin(self.angle_motion.angle_current) * t
        y_delta = self.vector_motion.current * cos(self.angle_motion.angle_current) * t

        new_bounds = []
        for point in self.bounds:
            x = self.axis.x + (point[0] - self.axis.x) * cos(self.angle_motion.current) \
                - (point[1] - self.axis.y) * sin(self.angle_motion.current) - x_delta
            y = self.axis.y + (point[1] - self.axis.y) * cos(self.angle_motion.current) \
                + (point[0] - self.axis.x) * sin(self.angle_motion.current) + y_delta

            new_bounds.append((x, y))
        self.bounds = new_bounds

        self.axis.x -= x_delta
        self.axis.y += y_delta

        self.axis.x = self.axis.x % AREA_WIDTH
        self.axis.y = self.axis.y % AREA_HEIGHT

    def collision(self, entity: Entity):
        return False

    def get_info(self):
        return {'id': self.id,
                'x': self.axis.x,
                'y': self.axis.y,
                'r': self.angle_motion.angle_current,
                'bounds': self.bounds
                }
