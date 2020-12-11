from back.physics import CasualPhysics
from back.storage import storage


class Entity:
    def __init__(self, x: float, y: float, r: float, context: str):
        self.id = 0
        self.hp = 1
        self.context_id = storage.get(context, {}).get('context_id')
        self.physics: CasualPhysics = CasualPhysics(x, y, r)

    @property
    def x(self):
        return self.physics.x

    @property
    def y(self):
        return self.physics.y

    @property
    def r(self):
        return self.physics.r

    def next(self, t: float):
        self.physics.update(t)

    def action_on_collision(self, entity):
        pass

    def set_moving(self, axis, direction):
        if axis == 'rotate':
            self.physics.angle_motion.set_moving(direction)
        elif axis == 'direction':
            self.physics.vector_motion.set_moving(direction)
        else:
            pass

    def get_info(self):
        return {'id': self.id,
                'type': type(self).__name__,
                'c': f'{int(self.x)} {int(self.y)} {round(self.r, 2)}',
                'aabb': self.physics.aabb_int,
                'context_id': self.context_id
                }
