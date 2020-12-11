import json
from os import listdir
from os.path import join

from back.config import MODELS_PATH

storage = {}


def load_dynamics():
    for file_name in listdir(MODELS_PATH):
        name = file_name[:-5]
        with open(f'{join(MODELS_PATH, file_name)}', 'r') as f:
            obj = json.loads(f.read())
            storage[name] = obj


load_dynamics()