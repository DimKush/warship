from back.entities import Player


class GameState:
    def __init__(self):
        self.players = {}

    def add_player(self):
        player = Player()
        self.players[player.id] = player
        return player.id

    def set_player_direction(self, player_id, ahead, delta_angle):
        self.players[player_id].ahead = ahead
        self.players[player_id].rotation = delta_angle

    def exec_step(self, time_delta):
        for _, player in self.players.items():
            player.next(time_delta)

    def get_state(self):
        return [pl.get_info() for _, pl in self.players.items()]