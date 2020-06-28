from back.entities import Player, Entity, Bullet, Statics


class Game:
    def __init__(self):
        self.entities = []

    def init_scene(self):
        self.entities.append(Statics(0, 0))

    def add_player(self):
        player = Player(100, 200)
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
                self.entities.remove(entity)

    def get_state(self):
        return {
            'entities_count': len(self.entities),
            'entities': [pl.get_info() for pl in self.entities]
        }

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


