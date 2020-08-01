from abc import ABC, abstractmethod
from typing import List


class Ship(ABC):
    @abstractmethod
    def __init__(self):
        self.name: str
        self.mobility: float
        self.speed: float
        self.acceleration: float
        self.hp: int
        self.hp_max: int
        self.shot_speed: int
        self.bullet_damage: int
        self.bullet_speed: int
        self.bounds: List


class MainShip(Ship):
    def __init__(self):
        super().__init__()
        self.name = 'predator'
        self.mobility = 1.2
        self.speed = 200
        self.acceleration = 150
        self.hp = 100
        self.hp_max = 100
        self.shot_speed = 6
        self.bounds = ()
        self.bullet_damage = 10
        self.bullet_speed = 500


class RenegadeShip(Ship):
    def __init__(self):
        super().__init__()
        self.name = 'predator_renegate'
        self.mobility = 1
        self.speed = 220
        self.acceleration = 150
        self.hp = 100
        self.hp_max = 100
        self.shot_speed = 2
        self.bounds = ()
        self.bullet_damage = 10
        self.bullet_speed = 500