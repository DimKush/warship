import json

import redis

from back.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


class Endpoint:
    def __init__(self):
        _redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
        self.__general_pubsub = _redis.pubsub()
        self.__player_pubsub = _redis.pubsub()
        self.__player_pubsub.psubscribe('players-state')

    def scan_players(self, previous_players: dict):
        players_state = self.__player_pubsub.get_message()
        if players_state and players_state.get('data') != 1:
            data = json.loads(players_state.get('data').decode())

            current_keys = set(data.keys())
            previous_keys = set(previous_players.keys())

            new_players = [{**data[pl], 'player_id': pl} for pl in (current_keys - previous_keys)]
            dead_players = [pl for pl in (previous_keys - current_keys)]
            current_players = {pl: data[pl] for pl in current_keys}

            return current_players, new_players, dead_players
        else:
            return previous_players, [], []

    def send_data_to_player(self, state: dict):
        self.__general_pubsub.execute_command("PUBLISH", "game-state", json.dumps(state))
