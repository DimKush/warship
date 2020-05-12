from back.entities import Player, Entity, Bullet, Statics


class Game:
    def __init__(self):
        self.entities = []
        self.matrix_of_interaction = {
            Player: {Player: self.player_player, Bullet: self.player_bullet},
            Bullet: {Player: self.player_bullet}
        }

    def init_scene(self):
        self.entities.append(Statics(0, 0))

    def add_player(self):
        player = Player(100, 200)
        self.entities.append(player)
        return player

    def exec_step(self, time_delta):
        for entity in self.entities:
            entity.next(time_delta, self.entities)
            if bullet := entity.do_action(time_delta):
                self.entities.append(bullet)

    def get_state(self):
        return [pl.get_info() for pl in self.entities]

    def player_bullet(self, accessor: Entity, donor: Entity):
        if isinstance(accessor, Player) and isinstance(donor, Bullet):
            pass
        elif isinstance(accessor, Bullet) and isinstance(donor, Player):
            accessor, donor = donor, accessor

        if accessor.id != donor.owner_id:
            print('damage!!!')
            accessor.hp -= donor.damage
            if donor in self.entities:
                self.entities.remove(donor)

    def player_player(self, accessor: Player, donor: Player):
        accessor.hp -= 1
        donor.hp -= 1


