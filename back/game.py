import time

import back.config as config
from back.effects import EffectFactory
from back.endpoint import Endpoint
from back.entities import SpaceShip
from back.entity_manager import EntityManager
from back.physics_system import PhysicsSystem
from back.scheduler import Scheduler


class Game:
    def __init__(self):
        self.endpoint = Endpoint()
        self.phs = PhysicsSystem()
        self.em = EntityManager(self.phs)
        self.scheduler = Scheduler()
        self.effects = EffectFactory()

    def init_scene(self):
        self.em.load_statics(config.STATICS_PATH)

    def exec_step(self, time_delta):
        self.scheduler.exec_all()
        self.phs.exec_next(time_delta)
        self.phs.collision_computer()
        self.em.remove_all_dead()

        if self.em.bot_count < config.BOTS_COUNT:
            self.em.create_ship('bot')

    def get_state(self):
        return {
            'entities': [pl.get_info() for pl in self.em.all()],
            'effects': self.effects.get_effects()
        }

    def run(self):
        last = time.time()
        curr_step_players = {}
        while True:
            curr = time.time()
            delta = float((curr - last))
            last = curr

            curr_step_players, new_players, expire_players = self.endpoint.scan_players(curr_step_players)

            for player in new_players:
                self.em.create_ship('player', player.get('player_id'), player.get('player_name'))

            for player in expire_players:
                self.em.remove_ship(player)

            for pl_id, pl_data in curr_step_players.items():
                player_obj: SpaceShip = self.em.players.get(pl_id)
                if player_obj:
                    self.scheduler.add(player_obj,
                                       SpaceShip.set_shooting,
                                       pl_data.get('shooting'))
                    self.scheduler.add(player_obj,
                                       SpaceShip.set_moving,
                                       pl_data.get('angle', 0),
                                       pl_data.get('direction', 0))
                else:
                    self.em.remove_ship(pl_id)

            self.exec_step(delta)
            self.endpoint.send_data_to_player(self.get_state())

            delay = config.RPS - (time.time() - curr)
            delay = 0 if delay < 0 else delay
            time.sleep(delay)


def main_game():
    print('Core game started.')
    game = Game()
    game.init_scene()
    game.run()
