import random

from back.entities import SpaceShip


class Scheduler:
    def __init__(self):
        self.__pool = []

    def add(self, obj, func, *args):
        command = obj, func, *args
        self.__pool.append(command)

    def exec_all(self):
        for command in self.__pool:
            entity, func, *args = command
            func(entity, *args)
        self.__pool = []

    def bot_ai(self, bot_obj):
        x = random.randint(0, 99)
        self.add(bot_obj, SpaceShip.shooting, .016)
        if x % 13 == 0:
            self.add(bot_obj, SpaceShip.set_moving, 'rotate', random.randint(-1, 1))
        self.add(bot_obj, SpaceShip.set_moving, 'direction', 1)
