import json
import uuid
from os.path import join

from back.config import STATICS_PATH
from back.entities.entity import Entity


class Statics(Entity):
    def __init__(self, x, y, r, ctx):
        super(Statics, self).__init__(x, y, r, ctx)
        self.id = f'static-{str(uuid.uuid1())[:8]}'

    def load_body_configuration(self, file_name: str = None):
        file_name = file_name if file_name.endswith('.json') else f'{file_name}.json'
        f = open(f'{join(STATICS_PATH, file_name)}', 'r')
        obj = json.loads(f.read())

        self.context_id = obj['context_id']
        self.physics.x, self.physics.y = obj['x'], obj['y']
        self.physics.bounds = [[p['x'] + obj['x'] + obj['offset_x'],
                                p['y'] + obj['y'] + obj['offset_y']]
                               for p in obj['points']]
        self.physics.eval_natural_aabb()

    def next(self, t: float):
        pass

    def do_action(self, asd):
        pass
