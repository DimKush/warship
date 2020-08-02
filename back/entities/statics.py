import json
from os.path import join

from back.config import STATICS_PATH
from back.entities.entity import Entity


class Statics(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def load_body_configuration(self, file_name: str = None):
        file_name = file_name if file_name.endswith('.json') else f'{file_name}.json'
        f = open(f'{join(STATICS_PATH, file_name)}', 'r')
        obj = json.loads(f.read())

        self.context_id = obj['context_id']
        self.geometry.x, self.geometry.y = obj['x'], obj['y']
        self.geometry.bounds = [[p['x'] + obj['x'] + obj['offset_x'],
                                 p['y'] + obj['y'] + obj['offset_y']]
                                for p in obj['points']]
        self.geometry.eval_true_bounding_box()

    def next(self, t: float, others):
        pass