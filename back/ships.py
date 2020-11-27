from dataclasses import dataclass
from typing import List


@dataclass
class Ship:
    name: str
    mobility: float
    speed: float
    acceleration: float
    hp: int
    hp_max: int
    shot_speed: float
    bullet_damage: int
    bullet_speed: int
    bounds: List


class MainShip(Ship):
    def __init__(self):
        self.name = 'predator'
        self.mobility = 1
        self.speed = 200
        self.acceleration = 150
        self.hp = 100
        self.hp_max = 100
        self.shot_speed = 6
        self.bounds = []
        self.bullet_damage = 10
        self.bullet_speed = 500


class RenegadeShip(Ship):
    def __init__(self):
        self.name = 'predator_renegate'
        self.mobility = 0.5
        self.speed = 120
        self.acceleration = 150
        self.hp = 100
        self.hp_max = 100
        self.shot_speed = 1.8
        self.bounds = []
        self.bullet_damage = 10
        self.bullet_speed = 400
