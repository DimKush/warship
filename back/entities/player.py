import uuid

import back.entities as ee
from back.entities.entity import Entity
from back.movement import Movement
from back.ships import Ship, MainShip


class Player(Entity):
    def __init__(self, x: float, y: float, r: float, ship_model: Ship = MainShip, prepared_id=None, prepared_name=''):
        super().__init__(x, y, r)
        self.id = str(uuid.uuid1())[:8] if prepared_id is None else prepared_id
        self.name = prepared_name
        self.ship_model = ship_model()
        self.physics.load_points(self.ship_model.name)
        self.load_body_configuration(self.ship_model.name)
        self.physics.vector_motion = Movement(delta=self.ship_model.acceleration, max_value=self.ship_model.speed)
        self.physics.angle_motion = Movement(delta=self.ship_model.mobility * 2.5, max_value=self.ship_model.mobility)
        self.physics.eval_approximately_aabb()
        self.hp = self.ship_model.hp
        self.hp_max = self.ship_model.hp_max
        self.shot_counter = 0
        self.shoting = False
        self.score = 0

    def set_action(self, flag: int):
        self.shoting = flag != 0

    def do_action(self, time_delta):
        if self.shot_counter <= 0:
            if self.shoting:
                bullet = ee.Bullet(self.x, self.y, self.r, self)
                self.shot_counter = 1 / self.ship_model.shot_speed
                return bullet
        else:
            self.shot_counter -= time_delta
        return None

    def action_on_collision(self, entity):
        if isinstance(entity, Player) or isinstance(entity, ee.Statics):
            self.physics.rollback()

    def get_info(self):
        data = super(Player, self).get_info()
        additional_info = {'hp': self.hp,
                           'hp_max': self.hp_max,
                           'name': self.name,
                           'score': self.score
                           }
        data.update(additional_info)
        return data
