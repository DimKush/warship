from back.effects import EffectFactory
from back.entities.entity import Entity
from back.geometry import GeometryLine
from back.point import Movement


class Bullet(Entity):
    def __init__(self, x: float, y: float, r: float, player_owner):
        super().__init__(x, y)
        self.id = 1
        self.owner_id = player_owner.id
        self.damage = player_owner.ship_model.bullet_damage
        self.effect_factory: EffectFactory = player_owner.effect_factory
        self.geometry = GeometryLine(x, y, r)
        self.load_body_configuration(f'bullet_{player_owner.ship_model.name}')
        self.geometry.rebuild()
        self.geometry.eval_true_bounding_box()
        self.geometry.vector_motion = Movement(curr_value=player_owner.ship_model.bullet_speed,
                                               max_value=player_owner.ship_model.bullet_speed)

    def action_on_collision(self, entity):
        import back.entities as ee
        if isinstance(entity, ee.Player):
            entity.hp -= self.damage
            self.hp = 0
        elif isinstance(entity, ee.Statics):
            self.hp = 0
        elif isinstance(entity, ee.Bullet):
            self.hp = 0
            entity.hp = 0
        self.effect_factory.add_to_pool('exp1', self.x, self.y)