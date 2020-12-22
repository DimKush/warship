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


main_ship = Ship(
    name='predator',
    mobility=1,
    speed=200,
    acceleration=150,
    hp=100,
    hp_max=100,
    shot_speed=6,
    bounds=[],
    bullet_damage=10,
    bullet_speed=500
)

renegade_ship = Ship(
    name='predator_renegate',
    mobility=0.5,
    speed=120,
    acceleration=150,
    hp=100,
    hp_max=100,
    shot_speed=1.8,
    bounds=[],
    bullet_damage=10,
    bullet_speed=400
)
