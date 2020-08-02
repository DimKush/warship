class EffectFactory:
    def __init__(self):
        self.pool = []

    def add_to_pool(self, id_eff, x, y):
        self.pool.append({'id': id_eff, 'x': x, 'y': y})

    def get_effects(self):
        res = self.pool[::]
        self.pool.clear()
        return res


class ActionFactory:
    def __init__(self):
        self.pool = []

    def add_to_pool(self, count, func, *args):
        self.pool.append({'func': func, 'args': args, 'count': count})

    def do_tick(self):
        if self.pool:
            action = self.pool[0]
            action['func'](*action['args'])
            action['count'] -= 1
            if action['count'] <= 0:
                self.pool.pop(0)

    def clear_pool(self):
        self.pool.clear()
