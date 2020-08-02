import uuid

import back.entities as ee
from back.entities.entity import Entity
from back.point import Movement, AngleMovement
from back.ships import Ship, MainShip


class Player(Entity):
    def __init__(self, x: float, y: float, ship_model: Ship = MainShip):
        super().__init__(x, y)
        self.id = str(uuid.uuid1())
        self.name = ''
        self.ship_model = ship_model()
        self.load_body_configuration(self.ship_model.name)
        self.geometry.vector_motion = Movement(delta=self.ship_model.acceleration,
                                               max_value=self.ship_model.speed)
        self.geometry.angle_motion = AngleMovement(delta=self.ship_model.mobility * 2.5,
                                                   max_value=self.ship_model.mobility)
        self.geometry.eval_approximately_bounding_box()
        self.hp = self.ship_model.hp
        self.hp_max = self.ship_model.hp_max
        self.shot_counter = 0
        self.shoting = False

    def set_action(self, flag: int):
        self.shoting = flag != 0

    def do_action(self, time_delta):
        if self.shot_counter <= 0:
            if self.shoting:
                bullet = ee.Bullet(self.x, self.y, self.geometry.angle_motion.angle_current, self)
                self.shot_counter = 1 / self.ship_model.shot_speed
                return bullet
        elif self.shot_counter > 0:
            self.shot_counter -= time_delta
        return None

    def action_on_collision(self, entity):
        if isinstance(entity, Player) or isinstance(entity, ee.Statics):
            self.geometry = self.prev_geometry
            self.geometry.vector_motion.curr *= -1
            self.geometry.angle_motion.curr *= -1

    def get_info(self):
        data = super(Player, self).get_info()
        data.update({'hp': self.hp, 'hp_max': self.hp_max, 'name': self.name})
        return data
