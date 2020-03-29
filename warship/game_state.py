fake_db = {
    'players': [],
    'ships': []
}


class GameState:
    def __init__(self):
        self.players = []
        self.ships = []
        self.bullets = []
        self.evaluator = None

    def save_state(self):
        fake_db['players'] = self.players
        fake_db['ships'] = self.ships

    def get_state(self):
        return fake_db

    def add_player(self, player):
        self.players.append(player)

    def send_state(self):
        pass

    def receive_signal(self):
        pass
