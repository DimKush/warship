from os import listdir
from random import randint

from back.config import AREA_WIDTH, AREA_HEIGHT, STATICS_PATH, ENEMY_COUNT
from back.effects import EffectFactory
from back.entities import Player, Statics, Enemy


class Game:
    def __init__(self):
        self.entities = []
        self.enemies = 0
        self.effect_factory = EffectFactory()

    def init_scene(self):
        self.load_objects()

    def add_player(self, player_type=Player):
        distance = 150
        while True:
            x, y = randint(0, AREA_WIDTH), randint(0, AREA_HEIGHT)
            bbox = x - distance, y - distance, x + distance, y + distance
            for entity in self.entities:
                if entity.geometry.box_collision(bbox):
                    break
            else:
                player = player_type(x, y)
                player.set_effect_factory(self.effect_factory)
                self.entities.append(player)
                return player

    def del_player(self, player):
        if player in self.entities:
            self.entities.remove(player)

    def exec_step(self, time_delta):
        for entity in self.entities:
            entity.next(time_delta, self.entities)
            if bullet := entity.do_action(time_delta):
                self.entities.append(bullet)
            if entity.hp <= 0:
                if isinstance(entity, Enemy):
                    self.enemies -= 1
                self.entities.remove(entity)

        if self.enemies < ENEMY_COUNT:
            self.add_player(Enemy)
            self.enemies += 1

    def get_state(self):
        return {
            'entities_count': len(self.entities),
            'entities': [pl.get_info() for pl in self.entities],
            'effects': self.effect_factory.get_effects()
        }

    def load_objects(self):
        for file in listdir(STATICS_PATH):
            stx = Statics(0, 0)
            stx.load_body_configuration(file)
            self.entities.append(stx)
