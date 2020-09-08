import json
import time
from os import listdir
from random import randint
import redis

import back.entities as ee
from back.config import AREA_WIDTH, AREA_HEIGHT, STATICS_PATH, ENEMY_COUNT, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, RPS
from back.effects import EffectFactory


class Game:
    def __init__(self):
        self.entities = []
        self.enemies = 0
        self.players = {}
        self.effect_factory = EffectFactory()
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
        self.pubsub = self.redis.pubsub()
        self.player_pubsub = self.redis.pubsub()
        self.player_pubsub.psubscribe('players-state')

    def init_scene(self):
        for file in listdir(STATICS_PATH):
            stx = ee.Statics(0, 0)
            stx.load_body_configuration(file)
            self.entities.append(stx)

    def add_player(self, player_type=ee.Player, uid='', name=''):
        distance = 150
        while True:
            x, y = randint(0, AREA_WIDTH), randint(0, AREA_HEIGHT)
            bbox = x - distance, y - distance, x + distance, y + distance
            for entity in self.entities:
                if entity.geometry.box_collision(bbox):
                    break
            else:
                player = player_type(x, y, prepared_id=uid, prepared_name=name)
                player.set_effect_factory(self.effect_factory)
                self.entities.append(player)
                self.players[player.id] = player
                return player

    def del_player(self, player_id):
        if player_id in self.players:
            removed_player = self.players.pop(player_id)
            self.entities.remove(removed_player)

    def exec_step(self, time_delta):
        for entity in self.entities:
            entity.next(time_delta, self.entities)
            if bullet := entity.do_action(time_delta):
                self.entities.append(bullet)
            if entity.hp <= 0:
                if isinstance(entity, ee.Enemy):
                    self.enemies -= 1
                self.entities.remove(entity)

        if self.enemies < ENEMY_COUNT:
            self.add_player(ee.Enemy)
            self.enemies += 1

    def get_state(self):
        return {
            'entities_count': len(self.entities),
            'entities': [pl.get_info() for pl in self.entities],
            'effects': self.effect_factory.get_effects()
        }

    def scan_players(self, previous_players):
        players_state = self.player_pubsub.get_message()
        if players_state and players_state.get('data') != 1:
            data = json.loads(players_state.get('data').decode())

            for pl in data:
                if data[pl].get('shooting') == 1:
                    print(time.time())

            current_keys = set(data.keys())
            previous_keys = set(previous_players.keys())

            new_players = [data[pl] for pl in (current_keys - previous_keys)]
            dead_players = [pl for pl in (previous_keys - current_keys)]
            current_players = {pl: data[pl] for pl in current_keys}

            return current_players, new_players, dead_players
        else:
            return previous_players, [], []


if __name__ == '__main__':
    game = Game()
    game.init_scene()

    last = time.time()
    prev_pls = {}
    print('Core game started.')
    while True:
        curr = time.time()
        delta = float((curr - last))
        last = curr

        start_processing = time.time()
        prev_pls, new_pl, expire_pl = game.scan_players(previous_players=prev_pls)
        for pl in new_pl:
            game.add_player(uid=pl.get('player_id'), name=pl.get('player_name'))
        for pl in expire_pl:
            game.del_player(pl)
        for pl_id, pl_data in prev_pls.items():
            game.players[pl_id].set_action(pl_data.get('shooting', 0))
            game.players[pl_id].set_moving(pl_data.get('angle', 0), pl_data.get('direction', 0))

        game.exec_step(delta)
        game.pubsub.execute_command("PUBLISH", "game-state", json.dumps(game.get_state()))

        delay = RPS - (time.time() - start_processing)
        delay = 0 if delay < 0 else delay
        time.sleep(delay)
