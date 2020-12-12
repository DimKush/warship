import uuid
from os import listdir
from random import randint

from back.config import AREA_WIDTH, AREA_HEIGHT
import back.entities as be
from back.effects import EffectFactory
from back.physics_system import PhysicsSystem
from back.ships import main_ship, renegade_ship
from back.singleton import SingletonMeta


class EntityManager(metaclass=SingletonMeta):
    def __init__(self, physic_system: PhysicsSystem = None):
        self.__physics_system = hasattr(self, 'physics_system') or physic_system
        self.players = {}
        self.bots = {}
        self.player_count = 0
        self.bot_count = 0

    def create_ship(self, _type, uid, name):
        distance = 50
        while True:
            x, y = randint(0, AREA_WIDTH), randint(0, AREA_HEIGHT)
            bbox = x - distance, y - distance, x + distance, y + distance
            if not self.__physics_system.aabb_collision(bbox):
                if _type == 'player':
                    player = be.SpaceShip(x, y, 0, uid, main_ship, prepared_name=name)
                    self.player_count += 1
                    self.players[player.id] = player
                elif _type == 'bot':
                    player = be.SpaceShip(x, y, 0, uid, renegade_ship, prepared_name=name)
                    self.bot_count += 1
                    self.bots[player.id] = player
                else:
                    raise Exception('Not found ship type')

                self.__physics_system.add(player)
                return player

    def create_player(self, uid, name):
        self.create_ship('player', uid, name)

    def create_bot(self):
        self.create_ship('bot', f'bot-{str(uuid.uuid1())[:8]}', 'noname')

    def remove_ship(self, _id):
        removed_ship = None
        if _id in self.players:
            removed_ship = self.players.pop(_id)
            self.player_count -= 1
        if _id in self.bots:
            removed_ship = self.bots.pop(_id)
            self.bot_count -= 1
        if removed_ship:
            self.__physics_system.delete(removed_ship)

    def create_bullet(self, x, y, r, owner):
        bullet = be.Bullet(x, y, r, owner)
        self.__physics_system.add(bullet)

    def remove_bullet(self, obj):
        self.__physics_system.delete(obj)

    def create_static(self, file):
        stx = be.Statics(0, 0, 0, file)
        stx.load_body_configuration(file)
        self.__physics_system.add(stx)

    def load_statics(self, statics_path):
        for file in listdir(statics_path):
            self.create_static(file)

    def remove_all_dead(self):
        for entity in self.__physics_system.entities:
            if entity.hp <= 0:
                EffectFactory().add_to_pool('exp1', entity.x, entity.y)
                if isinstance(entity, be.SpaceShip):
                    self.remove_ship(entity.id)
                elif isinstance(entity, be.Bullet):
                    self.remove_bullet(entity)
                else:
                    raise Exception('Not expected object')

    def all(self):
        return self.__physics_system.entities
