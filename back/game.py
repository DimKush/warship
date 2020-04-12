from back.entities import Player


class Game:
    def __init__(self):
        self.entities = []

    def add_player(self):
        player = Player()
        self.entities.append(player)
        return player

    def exec_step(self, time_delta):
        for entity in self.entities:
            entity.next(time_delta)

    def get_state(self):
        return [pl.get_info() for pl in self.entities]
