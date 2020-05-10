from typing import List

from back.entities import Player, Entity, Bullet
from back.point import Point


class Game:

    def __init__(self):
        self.entities = []
        self.matrix_of_interaction = {
            Player: {Player: self.stop, Bullet: self.damage},
            Bullet: {Player: self.destroy, Bullet: self.destroy}
        }

    def add_player(self):
        player = Player(100, 200)
        self.entities.append(player)
        return player

    def exec_step(self, time_delta):
        for entity in self.entities:
            entity.next(time_delta)
            for other_entity in self.entities:
                if entity != other_entity \
                        and self.box_collision(entity, other_entity) \
                        and self.detail_collision(entity, other_entity):
                    func = self.matrix_of_interaction.get(type(entity)).get(type(other_entity))
                    func()
            if bullet := entity.shot(time_delta):
                self.entities.append(bullet)

    def get_state(self):
        return [pl.get_info() for pl in self.entities]

    @staticmethod
    def box_collision(entity_1: Entity, entity_2: Entity):
        x1, y1, x2, y2 = entity_1.bounding_box
        x3, y3, x4, y4 = entity_2.bounding_box
        if (x2 >= x3) and (x4 >= x1) and (y2 >= y3) and (y4 >= y1):
            return True
        return False

    @staticmethod
    def vector_multiple(p0: Point, p1: Point, p2: Point):
        return (p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y)

    def detail_collision(self, entity_1: Entity, entity_2: Entity):
        for p1, p2 in self.get_segments(entity_1.bounds):
            for p3, p4 in self.get_segments(entity_2.bounds):
                if self.vector_multiple(p1, p3, p2) * self.vector_multiple(p1, p4, p2) <= 0 and \
                        self.vector_multiple(p3, p1, p4) * self.vector_multiple(p3, p2, p4) <= 0:
                    return True
        return False

    @staticmethod
    def get_segments(bounds: List[Point]):
        return [(bounds[i], bounds[(i + 1) % len(bounds)]) for i in range(0, len(bounds))]

    def stop(self):
        print('STOP!')
    def damage(self):
        print('DAMAGE!!')
    def destroy(self):
        print('DESTROY!!!')