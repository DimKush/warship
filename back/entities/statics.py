import json
from os.path import join

from back.config import STATICS_PATH
from back.entities.entity import Entity


class Statics(Entity):
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

    def get_info(self):
        data = super(Statics, self).get_info()
        del data['id']
        del data['c']
        return data

    def do_action(self, asd):
        pass
