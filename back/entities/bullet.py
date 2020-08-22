from back.effects import EffectFactory
from back.entities.entity import Entity
from back.geometry import GeometryLine
from back.point import Movement


class Bullet(Entity):
    def __init__(self, x: float, y: float, r: float, player_owner):
        super().__init__(x, y)
        self.id = 1
        self.owner = player_owner
        self.damage = player_owner.ship_model.bullet_damage
        self.effect_factory: EffectFactory = player_owner.effect_factory
        self.geometry = GeometryLine(x, y, r)
        self.load_body_configuration(f'bullet_{player_owner.ship_model.name}')
        self.geometry.rebuild()
        self.geometry.eval_true_bounding_box()
        self.geometry.vector_motion = Movement(curr_value=player_owner.ship_model.bullet_speed,
                                               max_value=player_owner.ship_model.bullet_speed)

    def action_on_collision(self, entity):
        from back.entities import Bullet, Statics, Player
        if isinstance(entity, Player):
            entity.hp -= self.damage
            if entity.hp > 0:
                self.owner.score += 10
            else:
                self.owner.score += 50
            self.hp = 0
        elif isinstance(entity, Statics):
            self.hp = 0
        elif isinstance(entity, Bullet):
            self.hp = 0
            entity.hp = 0
        else:
            print(f'Not described case for type {type(entity)}')

        self.effect_factory.add_to_pool('exp1', self.x, self.y)
