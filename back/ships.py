import json
from abc import ABC, abstractmethod
from os import listdir
from os.path import join, isfile
from typing import List, Tuple

from back import config
from back.point import Point


class Ship(ABC):
    @abstractmethod
    def __init__(self):
        self.name: str
        self.mobility: float
        self.speed: float
        self.acceleration: float
        self.hp: int
        self.shot_speed: int
        self.bullet_damage: int
        self.bullet_speed: int
        self.bounds: Tuple[Point]


class MainShip(Ship):
    def __init__(self):
        super().__init__()
        self.name = 'predator'
        self.mobility = 2
        self.speed = 300
        self.acceleration = 300
        self.hp = 100
        self.shot_speed = 3
        self.bounds = ()
        self.bullet_damage = 5
        self.bullet_speed = 200
