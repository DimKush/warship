import back.entities as ee
from back.entities.bonus import Bonus
from back.entity_manager import EntityManager
from back.ships import Ship


class SpaceShip(ee.Entity):
    def __init__(self,
                 x: float,
                 y: float,
                 r: float,
                 uid: str,
                 ship_model: Ship,
                 prepared_name):
        super().__init__(x, y, r, ship_model.name)
        self.id = uid
        self.name = prepared_name
        self.ship_model = ship_model
        self.physics.load_points(self.ship_model.name)
        self.physics.vector_motion.set_delta(self.ship_model.acceleration)
        self.physics.vector_motion.set_max_current(self.ship_model.speed)
        self.physics.angle_motion.set_delta(self.ship_model.mobility)

        self.physics.eval_approximately_aabb()
        self.hp = self.ship_model.hp
        self.hp_max = self.ship_model.hp_max
        self.shot_counter = 0
        self.is_shooting = False
        self.score = 0
        self.bonuses = []

    def set_shooting(self, flag):
        if flag:
            self.is_shooting = True
        else:
            self.is_shooting = False

    def shooting(self, time_delta):
        if self.is_shooting:
            if self.shot_counter <= 0:
                self.shot_counter = 1 / self.ship_model.shot_speed
                EntityManager().create_bullet(self.x, self.y, self.r, self)
            else:
                self.shot_counter -= time_delta

    def action_on_collision(self, entity):
        if isinstance(entity, SpaceShip) or isinstance(entity, ee.Statics):
            self.physics.rollback()
        if isinstance(entity, Bonus):
            self.apply_bonus(entity)

    def next(self, t: float):
        super(SpaceShip, self).next(t)
        self.shooting(t)

    def get_info(self):
        data = super(SpaceShip, self).get_info()
        additional_info = {'hp': self.hp,
                           'hp_max': self.hp_max,
                           'name': self.name,
                           'score': self.score
                           }
        data.update(additional_info)
        return data

    def on_dead(self):
        EntityManager().create_bonus(self.x, self.y)

    def apply_bonus(self, bonus_obj: Bonus):
        bonus = {
            'duration': bonus_obj.duration,
            'characteristic': bonus_obj.characteristic
        }
        if bonus_obj.characteristic == 'bonus_shoot':
            self.ship_model.shot_speed = self.ship_model.shot_speed * (1 + bonus_obj.value / 100)
        elif bonus_obj.characteristic == 'bonus_speed':
            self.physics.vector_motion.set_delta(self.ship_model.acceleration * 2)
            self.physics.vector_motion.set_max_current(self.ship_model.speed * (1 + bonus_obj.value / 100))
            self.physics.angle_motion.set_delta(self.ship_model.mobility * 3)
        else:
            pass

        self.bonuses.append(bonus)
