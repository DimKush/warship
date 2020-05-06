from abc import ABC, abstractmethod
from typing import List, Tuple

from back.point import Point


class Ship(ABC):
    @abstractmethod
    def __init__(self):
        self.name = ''
        self.mobility = 1
        self.speed = 1
        self.bounds: Tuple[Point]


class MainShip(Ship):
    def __init__(self):
        super().__init__()
        self.name = 'Main ship'
        self.mobility = 1
        self.speed = 1
        self.bounds = (
            Point(-15, -40),
            Point(-15, 40),
            Point(0, 60),
            Point(15, 40),
            Point(15, -40),
        )
